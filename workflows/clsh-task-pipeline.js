export const meta = {
  name: "clsh-task-pipeline",
  description: "Phase 4 single-task pipeline: coder → artist? → tester ⇄ fix → reviewer ⇄ fix",
  whenToUse:
    "After tasks.md approved and one task brief is ready; coordinator runs this per task",
  phases: [
    { title: "Coder" },
    { title: "Artist" },
    { title: "Tester" },
    { title: "Reviewer" },
  ],
  model: "standard",
  permissions: [
    { permission: "bash", patterns: ["git *"], reason: "read commit range for review package" },
  ],
}

/**
 * args:
 *   taskN: number
 *   briefPath: string
 *   reportDir: string          // e.g. .clsh/reports
 *   needUI: boolean
 *   maxFix: number             // default 2
 *   coderTimeoutMs: number     // default 900000
 *   otherTimeoutMs: number     // default 600000
 *   fromStage: "coder"|"artist"|"tester"|"reviewer"  // resume after partial
 *   modelBase: string          // default "standard"; omit-friendly
 *   modelUpgrade: string|null  // used on fix rounds; null/"" = inherit engine default (no model field)
 *   agentPrefix: string        // default "clsh-"; set "general" path via agentType override below
 *   useRoleAgents: boolean     // default true; false → agentType "general" + contract in prompt
 */

const CODED_SCHEMA = {
  type: "object",
  required: ["status", "files", "tdd", "interfaces", "ui_touchpoints", "fixed_finding_ids"],
  properties: {
    status: { enum: ["DONE", "DONE_WITH_CONCERNS", "NEEDS_CONTEXT", "BLOCKED"] },
    files: {
      type: "object",
      required: ["created", "modified", "tests"],
      properties: {
        created: { type: "array", items: { type: "string" } },
        modified: { type: "array", items: { type: "string" } },
        tests: { type: "array", items: { type: "string" } },
      },
    },
    tdd: {
      type: "object",
      required: ["red_cmd", "green_cmd", "green_output_excerpt"],
      properties: {
        red_cmd: { type: "string" },
        red_output_excerpt: { type: "string" },
        green_cmd: { type: "string" },
        green_output_excerpt: { type: "string" },
      },
    },
    interfaces: { type: "array", items: { type: "string" } },
    ui_touchpoints: { type: "array", items: { type: "string" } },
    known_gaps: { type: "array", items: { type: "string" } },
    fixed_finding_ids: { type: "array", items: { type: "string" } },
    base_commit: { type: "string" },
    head_commit: { type: "string" },
  },
}

const TESTER_SCHEMA = {
  type: "object",
  required: ["status", "verdict", "covering_tests", "findings", "evidence"],
  properties: {
    status: { enum: ["DONE", "DONE_WITH_CONCERNS", "NEEDS_CONTEXT", "BLOCKED"] },
    verdict: { enum: ["PASS", "FAIL"] },
    covering_tests: {
      type: "object",
      required: ["cmd", "output_excerpt", "pass_fail_counts"],
      properties: {
        cmd: { type: "string" },
        output_excerpt: { type: "string" },
        pass_fail_counts: { type: "string" },
      },
    },
    findings: {
      type: "array",
      items: {
        type: "object",
        required: ["id", "severity", "description"],
        properties: {
          id: { type: "string" },
          severity: { enum: ["Critical", "Important", "Minor"] },
          description: { type: "string" },
        },
      },
    },
    evidence: { type: "string" },
  },
}

const REVIEWER_SCHEMA = {
  type: "object",
  required: ["status", "spec", "quality", "findings"],
  properties: {
    status: { enum: ["DONE", "DONE_WITH_CONCERNS", "NEEDS_CONTEXT", "BLOCKED"] },
    spec: { enum: ["PASS", "FAIL"] },
    quality: { enum: ["APPROVED", "ISSUES"] },
    findings: {
      type: "array",
      items: {
        type: "object",
        required: ["id", "severity", "description"],
        properties: {
          id: { type: "string" },
          severity: { enum: ["Critical", "Important", "Minor"] },
          description: { type: "string" },
          file: { type: "string" },
        },
      },
    },
  },
}

function findingsBlock(findings) {
  if (!findings || !findings.length) return "(none)"
  return findings
    .map((f) => `- [${f.id}] (${f.severity}) ${f.description}`)
    .join("\n")
}

function openIds(findings) {
  return (findings || [])
    .filter((f) => f.severity === "Critical" || f.severity === "Important")
    .map((f) => f.id)
}

function covered(open, fixed) {
  if (!open.length) return true
  const set = new Set(fixed || [])
  return open.every((id) => set.has(id))
}

export default async function () {
  const taskN = args.taskN ?? 0
  const briefPath = args.briefPath
  const reportDir = args.reportDir ?? ".clsh/reports"
  const needUI = !!args.needUI
  const maxFix = args.maxFix ?? 2
  const coderTimeoutMs = args.coderTimeoutMs ?? 900000
  const otherTimeoutMs = args.otherTimeoutMs ?? 600000
  const modelBase = args.modelBase ?? "standard"
  // null/"" → omit model on upgrade (inherit); never hardcode a missing group name
  const modelUpgradeRaw = args.modelUpgrade
  const modelUpgrade =
    modelUpgradeRaw === undefined ? modelBase : modelUpgradeRaw === "" ? null : modelUpgradeRaw
  const useRoleAgents = args.useRoleAgents !== false
  const agentType = (role) => (useRoleAgents ? `clsh-${role}` : "general")
  const roleContract = (role) =>
    useRoleAgents
      ? ""
      : `ROLE CONTRACT (${role}): follow clsh-${role} rules — TDD if coder, no nested subagents, structured schema only, no self-approve.\n`
  let stage = args.fromStage ?? "coder"

  if (!briefPath) return { status: "NEEDS_HUMAN", reason: "briefPath required" }
  if (!(await exists(briefPath))) {
    return { status: "NEEDS_HUMAN", reason: `brief not found: ${briefPath}` }
  }

  const coderReport = `${reportDir}/task-${taskN}-coder-report.json`
  const artistReport = `${reportDir}/task-${taskN}-artist-report.json`
  const testerReport = `${reportDir}/task-${taskN}-tester-report.json`
  const reviewerReport = `${reportDir}/task-${taskN}-reviewer-report.json`
  const findingsPath = `${reportDir}/task-${taskN}-open-findings.json`
  const resultPath = `${reportDir}/task-${taskN}-pipeline-result.json`

  let lastFindings = []
  try {
    const raw = await readFile(findingsPath)
    if (raw) lastFindings = JSON.parse(raw)
  } catch (_) {
    lastFindings = []
  }

  async function runCoder(round, model) {
    phase(`Coder r${round}`)
    const prompt = [
      roleContract("coder"),
      "You are clsh-coder. Read the brief file path below as the ONLY requirements source.",
      `Brief: ${briefPath}`,
      "Implement with TDD (RED→GREEN). Do not spawn other agents.",
      "Return a structured object matching the schema. status DONE only if red+green evidence exists.",
      "green_output_excerpt must include the real command output summary, not a claim.",
      round > 0
        ? `You MUST address these open finding ids and list them in fixed_finding_ids:\n${findingsBlock(lastFindings)}`
        : "",
      "ui_touchpoints: list UI surfaces for artist (empty if none).",
    ].join("\n")
    const opts = {
      agentType: agentType("coder"),
      schema: CODED_SCHEMA,
      timeoutMs: coderTimeoutMs,
      label: `coder-r${round}`,
    }
    if (model) opts.model = model
    return agent(prompt, opts)
  }

  async function runArtist(round) {
    phase(`Artist r${round}`)
    const coderJson = (await readFile(coderReport)) || "{}"
    const prompt = [
      roleContract("artist"),
      "You are clsh-artist. Polish UI only; do not change public APIs.",
      `Brief: ${briefPath}`,
      `Coder report JSON: ${coderReport}`,
      `Coder JSON content:\n${coderJson}`,
      "Touch only files listed under coder.files and ui_touchpoints.",
      "Return structured object with status, files, contracts_kept, fixed_finding_ids.",
      lastFindings.length
        ? `Address if UI-related:\n${findingsBlock(lastFindings)}`
        : "",
    ].join("\n")
    return agent(prompt, {
      agentType: agentType("artist"),
      schema: {
        type: "object",
        required: ["status", "files", "fixed_finding_ids"],
        properties: {
          status: { enum: ["DONE", "DONE_WITH_CONCERNS", "NEEDS_CONTEXT", "BLOCKED"] },
          files: {
            type: "object",
            required: ["created", "modified"],
            properties: {
              created: { type: "array", items: { type: "string" } },
              modified: { type: "array", items: { type: "string" } },
            },
          },
          contracts_kept: { type: "array", items: { type: "string" } },
          fixed_finding_ids: { type: "array", items: { type: "string" } },
        },
      },
      timeoutMs: otherTimeoutMs,
      label: `artist-r${round}`,
    })
  }

  async function runTester(round) {
    phase(`Tester r${round}`)
    const prompt = [
      roleContract("tester"),
      "You are clsh-tester. Independently verify the implementation. Do not fix code.",
      `Brief: ${briefPath}`,
      `Coder report: ${coderReport}`,
      needUI ? `Artist report: ${artistReport}` : "No artist stage.",
      "Run covering tests yourself. PASS requires real command output evidence.",
      "Return structured object with verdict PASS|FAIL and findings[].",
      lastFindings.length
        ? `Prior open findings must be re-checked:\n${findingsBlock(lastFindings)}`
        : "",
    ].join("\n")
    return agent(prompt, {
      agentType: agentType("tester"),
      schema: TESTER_SCHEMA,
      timeoutMs: otherTimeoutMs,
      label: `tester-r${round}`,
    })
  }

  async function runReviewer(round) {
    phase(`Reviewer r${round}`)
    const prompt = [
      roleContract("reviewer"),
      "You are clsh-reviewer. Two-axis review: spec compliance AND code quality.",
      `Brief: ${briefPath}`,
      `Coder report: ${coderReport}`,
      `Tester report: ${testerReport}`,
      needUI ? `Artist report: ${artistReport}` : "",
      "Diff package may be generated by coordinator at .clsh/reviews/task-N-diff.txt if present.",
      "Return structured object with spec PASS|FAIL and quality APPROVED|ISSUES and findings[].",
      lastFindings.length
        ? `Re-check prior findings:\n${findingsBlock(lastFindings)}`
        : "",
    ]
      .filter(Boolean)
      .join("\n")
    return agent(prompt, {
      agentType: agentType("reviewer"),
      schema: REVIEWER_SCHEMA,
      timeoutMs: otherTimeoutMs,
      label: `reviewer-r${round}`,
    })
  }

  async function persist(path, obj) {
    await writeFile(path, JSON.stringify(obj, null, 2))
  }

  async function stall(stageName, round, extra) {
    const out = {
      status: "NEEDS_HUMAN",
      stage: stageName,
      round,
      reason: extra,
      findings_path: findingsPath,
    }
    await persist(resultPath, out)
    return out
  }

  // ---- coder (+ optional artist) loop against tester ----
  let fixRound = 0
  let coderOut = null
  let artistOut = null
  let testerOut = null

  const startImpl = stage === "coder" || stage === "artist" || stage === "tester"
  if (startImpl) {
    while (fixRound <= maxFix) {
      const model = fixRound === 0 ? modelBase : modelUpgrade
      coderOut = await runCoder(fixRound, model)
      if (!coderOut) {
        if (fixRound >= maxFix) return stall("coder", fixRound, "agent() null after max attempts")
        fixRound++
        continue
      }
      await persist(coderReport, coderOut)
      if (coderOut.status === "BLOCKED" || coderOut.status === "NEEDS_CONTEXT") {
        return stall("coder", fixRound, coderOut.status)
      }

      if (needUI && stage !== "tester") {
        artistOut = await runArtist(fixRound)
        if (!artistOut) {
          if (fixRound >= maxFix) return stall("artist", fixRound, "agent() null")
          fixRound++
          continue
        }
        await persist(artistReport, artistOut)
        if (artistOut.status === "BLOCKED") {
          return stall("artist", fixRound, "BLOCKED")
        }
      }

      testerOut = await runTester(fixRound)
      if (!testerOut) {
        if (fixRound >= maxFix) return stall("tester", fixRound, "agent() null")
        fixRound++
        continue
      }
      await persist(testerReport, testerOut)

      if (testerOut.verdict === "PASS") break

      lastFindings = testerOut.findings || []
      await persist(findingsPath, lastFindings)
      const open = openIds(lastFindings)
      const fixed = (coderOut.fixed_finding_ids || []).concat(
        (artistOut && artistOut.fixed_finding_ids) || []
      )
      // next iteration must address open ids — pass via lastFindings in prompts
      if (fixRound >= maxFix) {
        return stall("tester", fixRound, `FAIL with open findings after maxFix: ${open.join(",")}`)
      }
      // Prefer artist for UI-only Critical findings
      const uiOnly =
        lastFindings.length > 0 &&
        lastFindings.every((f) => /ui|css|layout|style|visual/i.test(f.description || ""))
      stage = uiOnly && needUI ? "artist" : "coder"
      fixRound++
    }
  }

  if (!testerOut || testerOut.verdict !== "PASS") {
    return stall("tester", fixRound, "tester did not PASS")
  }

  // ---- reviewer loop ----
  let revRound = 0
  let revOut = null
  while (revRound <= maxFix) {
    revOut = await runReviewer(revRound)
    if (!revOut) {
      if (revRound >= maxFix) return stall("reviewer", revRound, "agent() null")
      revRound++
      continue
    }
    await persist(reviewerReport, revOut)
    const critical = (revOut.findings || []).filter((f) => f.severity === "Critical")
    if (revOut.spec === "PASS" && revOut.quality === "APPROVED" && critical.length === 0) {
      break
    }
    lastFindings = (revOut.findings || []).filter(
      (f) => f.severity === "Critical" || f.severity === "Important"
    )
    await persist(findingsPath, lastFindings)
    if (revRound >= maxFix) {
      return stall(
        "reviewer",
        revRound,
        `open findings after maxFix: ${openIds(lastFindings).join(",")}`
      )
    }
    // one more coder fix round against reviewer findings
    stage = "coder"
    fixRound = 0
    while (fixRound <= maxFix) {
      const model = fixRound === 0 ? modelBase : modelUpgrade
      coderOut = await runCoder(fixRound, model)
      if (!coderOut) {
        if (fixRound >= maxFix) return stall("coder", fixRound, "null in reviewer-fix")
        fixRound++
        continue
      }
      await persist(coderReport, coderOut)
      if (!covered(openIds(lastFindings), coderOut.fixed_finding_ids)) {
        if (fixRound >= maxFix)
          return stall("coder", fixRound, "fixed_finding_ids did not cover open findings")
        fixRound++
        continue
      }
      testerOut = await runTester(fixRound)
      if (testerOut && testerOut.verdict === "PASS") {
        await persist(testerReport, testerOut)
        break
      }
      if (testerOut) await persist(testerReport, testerOut)
      lastFindings = (testerOut && testerOut.findings) || lastFindings
      await persist(findingsPath, lastFindings)
      if (fixRound >= maxFix) return stall("tester", fixRound, "still FAIL after reviewer-fix")
      fixRound++
    }
    revRound++
  }

  if (!revOut || revOut.spec !== "PASS" || revOut.quality !== "APPROVED") {
    return stall("reviewer", revRound, "reviewer not APPROVED")
  }

  const result = {
    status: "GREEN",
    taskN,
    coderReport,
    artistReport: needUI ? artistReport : null,
    testerReport,
    reviewerReport,
    fixRounds: fixRound,
    reviewRounds: revRound,
  }
  await persist(resultPath, result)
  log(`task ${taskN} GREEN after ${fixRound} impl / ${revRound} review rounds`)
  return result
}
