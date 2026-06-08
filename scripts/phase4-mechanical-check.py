#!/usr/bin/env python3
"""
clsh-project Phase 4 机械自检脚本
===================================
纯机械检查，零 LLM 依赖。
用于 E2E 测试和实际项目的 Phase 4 自检门禁。

用法：python3 phase4-mechanical-check.py <项目目录>

检查项：
  1. 文件存在性
  2. 模板关键词覆盖
  3. 文档字数上限
  4. 实现细节规范（constitution 必须包含）
"""

import os
import sys
import json
import glob

# ============================================================
# Config: 模板要求
# ============================================================
TEMPLATE_RULES = {
    "overview.md": {
        "keywords": ["状态", "进度表"],
        "max_lines": 60,
    },
    "changes/*/conversation.md": {
        "keywords": ["需求", "决策"],
        "max_lines": 60,
    },
    "changes/*/proposal.md": {
        "keywords": ["技术方案", "不在范围内"],
        "max_lines": 70,
    },
    "source-of-truth/constitution.md": {
        "keywords": ["约束", "禁止", "验收标准"],
        "max_lines": 60,
    },
    "changes/*/tasks.md": {
        "keywords": ["验收标准", "不在范围内"],
        "max_lines": 80,
    },
}

# 实现细节规范（constitution 必须包含）
# 结构化检查：只检查是否有"实现细节规范"节，不检查具体内容（适配 CLI/Web/API 等项目类型）
IMPL_SECTION_PATTERNS = [
    r'##\s*实现细节规范',
    r'##\s*实现细节',
    r'###\s*实现细节',
]

# 通用实现细节内容（不区分项目类型）
IMPL_CONTENT_KEYWORDS = {
    "has_encoding": {
        "keywords": ["编码", "encoding", "utf-8", "UTF-8"],
        "desc": "编码规范",
    },
    "has_error_handling": {
        "keywords": ["错误处理", "错误输出", "error handling", "stderr", "异常", "错误码", "错误响应"],
        "desc": "错误处理规范",
    },
}

# 宽松关键词（如果没有明确的节标题，检查是否有足够多的实现细节内容）
IMPL_FALLBACK_KEYWORDS = ["规范", "格式", "存储", "路径", "标记", "响应", "哈希", "编码", "状态码", "认证"]


def find_file(base, pattern):
    """Find file matching glob pattern"""
    full = os.path.join(base, pattern)
    matches = glob.glob(full)
    return matches[0] if matches else None


def check_file(path, keywords, max_lines):
    """Check a single file for keyword coverage and line count"""
    if not os.path.exists(path):
        return {"exists": False, "keywords_found": [], "keywords_missing": keywords,
                "lines": 0, "over_limit": False}
    
    with open(path) as f:
        content = f.read()
    
    lines = content.count('\n') + 1
    found = [kw for kw in keywords if kw in content]
    missing = [kw for kw in keywords if kw not in content]
    over_limit = lines > max_lines
    
    return {
        "exists": True,
        "keywords_found": found,
        "keywords_missing": missing,
        "lines": lines,
        "max_lines": max_lines,
        "over_limit": over_limit,
    }


def run_checks(project_dir):
    """Run all mechanical checks"""
    results = {}
    all_pass = True
    
    for pattern, rules in TEMPLATE_RULES.items():
        path = find_file(project_dir, pattern)
        if not path:
            path = os.path.join(project_dir, pattern.replace("*/", ""))
        
        check = check_file(path, rules["keywords"], rules["max_lines"])
        results[pattern] = check
        
        passed = (check["exists"] and 
                  not check["keywords_missing"] and 
                  not check["over_limit"])
        if not passed:
            all_pass = False
    
    # Check implementation specs in constitution
    # 结构化检查：检查是否有"实现细节规范"节（适配 CLI/Web/API 等项目类型）
    const_path = find_file(project_dir, "source-of-truth/constitution.md")
    if not const_path:
        const_path = os.path.join(project_dir, "source-of-truth/constitution.md")
    
    impl_results = {}
    if os.path.exists(const_path):
        with open(const_path) as f:
            content = f.read()
        
        import re
        
        # 1. 检查是否有实现细节节标题
        impl_section_found = False
        for pattern in IMPL_SECTION_PATTERNS:
            if re.search(pattern, content, re.IGNORECASE):
                impl_section_found = True
                break
        
        # 2. 如果没有明确的节标题，检查是否有足够多的实现细节内容（至少 3 个关键词）
        if not impl_section_found:
            keyword_count = sum(1 for kw in IMPL_FALLBACK_KEYWORDS if kw in content)
            if keyword_count >= 3:
                impl_section_found = True
        
        # 3. 检查通用实现细节内容
        impl_content_found = 0
        for name, spec in IMPL_CONTENT_KEYWORDS.items():
            found = any(kw in content for kw in spec["keywords"])
            impl_results[name] = {"found": found, "desc": spec["desc"]}
            if found:
                impl_content_found += 1
        
        # 4. 评分：有实现细节节(主要) + 有通用内容(次要)
        impl_results["_section_found"] = impl_section_found
        impl_results["_content_count"] = impl_content_found
        
        if not impl_section_found:
            all_pass = False
    else:
        impl_results["_section_found"] = False
        impl_results["_content_count"] = 0
        for name, spec in IMPL_CONTENT_KEYWORDS.items():
            impl_results[name] = {"found": False, "desc": spec["desc"]}
        all_pass = False
    
    return results, impl_results, all_pass


def print_report(results, impl_results, all_pass):
    """Print formatted report"""
    print("=" * 50)
    print("📋 Phase 4 机械自检报告")
    print("=" * 50)
    
    for pattern, check in results.items():
        name = os.path.basename(pattern)
        if check["exists"]:
            kw_ok = "✅" if not check["keywords_missing"] else "❌"
            ln_ok = "✅" if not check["over_limit"] else "❌"
            print(f"  {name:<25} 存在=✅ 关键词={kw_ok} 行数={ln_ok} ({check['lines']}/{check['max_lines']})")
            if check["keywords_missing"]:
                print(f"    缺失关键词: {check['keywords_missing']}")
            if check["over_limit"]:
                print(f"    超出行数限制: {check['lines']} > {check['max_lines']}")
        else:
            print(f"  {name:<25} 存在=❌")
    
    print(f"\n{'─'*50}")
    print("📋 实现细节规范检查")
    section_found = impl_results.get("_section_found", False)
    content_count = impl_results.get("_content_count", 0)
    section_status = "✅" if section_found else "❌"
    print(f"  {section_status} 实现细节节: {'有明确节标题或足够内容' if section_found else '缺少实现细节规范节'}")
    for name, spec in impl_results.items():
        if name.startswith("_"):
            continue
        status = "✅" if spec["found"] else "❌"
        print(f"  {status} {spec['desc']}")
    
    print(f"\n{'─'*50}")
    status = "✅ PASS" if all_pass else "❌ FAIL"
    print(f"  总结: {status}")
    
    return all_pass


def main():
    if len(sys.argv) < 2:
        print("用法: python3 phase4-mechanical-check.py <项目目录>")
        sys.exit(1)
    
    project_dir = sys.argv[1]
    
    if not os.path.exists(project_dir):
        print(f"❌ 项目目录不存在: {project_dir}")
        sys.exit(1)
    
    results, impl_results, all_pass = run_checks(project_dir)
    print_report(results, impl_results, all_pass)
    
    # Output JSON for machine parsing
    report = {
        "project_dir": project_dir,
        "template_checks": results,
        "impl_specs": impl_results,
        "all_pass": all_pass,
    }
    print(f"\n{json.dumps(report, indent=2, ensure_ascii=False)}")


if __name__ == "__main__":
    main()
