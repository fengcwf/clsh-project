# Full-Stack Monorepo Scaffolding Template

> Vue 3 + Fastify + Prisma + PostgreSQL + Docker Compose 项目的标准文件结构和依赖顺序。

## 目录结构

```
<project>/
├── docker-compose.yml          # PostgreSQL + Redis + MinIO + API + Web
├── package.json                # workspace: ["packages/*"]
├── tsconfig.base.json          # 共享 TS 配置
├── README.md
├── .gitignore
└── packages/
    ├── api/                    # Fastify 后端
    │   ├── package.json
    │   ├── tsconfig.json
    │   ├── Dockerfile
    │   ├── .env.example
    │   ├── prisma/
    │   │   ├── schema.prisma   # 所有数据模型
    │   │   └── seed.ts         # 种子数据
    │   ├── src/
    │   │   ├── index.ts        # Fastify 入口 + 路由注册
    │   │   ├── routes/         # API 路由（按模块拆分）
    │   │   └── lib/            # 工具库（minio, upload, grader 等）
    │   └── test/               # Vitest 集成测试
    ├── web/                    # Vue 3 前端
    │   ├── package.json
    │   ├── tsconfig.json
    │   ├── vite.config.ts
    │   ├── index.html
    │   ├── Dockerfile
    │   ├── nginx.conf
    │   ├── env.d.ts
    │   └── src/
    │       ├── main.ts         # Vue 入口
    │       ├── App.vue
    │       ├── router/index.ts
    │       ├── layouts/        # 布局组件
    │       ├── views/          # 页面组件
    │       ├── stores/         # Pinia Store
    │       └── api/client.ts   # Axios 封装
    └── worker/                 # 后台 Worker（可选）
        ├── package.json
        ├── tsconfig.json
        └── src/
            ├── index.ts
            └── transcoder.ts
```

## Task 执行顺序（典型全栈项目）

```
T1  项目脚手架     → docker-compose + package.json + tsconfig
T2  数据模型       → Prisma schema（必须先于所有路由）
T3  认证模块       → auth.ts + middleware（被其他路由依赖）
T4  核心 CRUD      → 业务路由（courses, lessons, materials）
T5  文件上传       → upload routes + minio lib
T6  异步处理       → worker（独立进程）
T7  扩展业务       → assignments, questions, submissions
T8  业务逻辑       → grader, analytics（纯逻辑或路由）
T9  前端脚手架     → router + stores + api client + layouts
T10 前端页面       → views（按用户流程：登录→列表→详情→操作）
T11 测试           → 集成测试 + E2E
```

## Prisma Schema 模板（教育平台）

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

// 核心模型：User, Course, Lesson, Material, Assignment, Submission, Question, StudentProgress, Enrollment
// 关系：Course → Teacher(User), Lesson → Course, Material → Lesson
//       Assignment → Course + Creator(User), Submission → Student(User) + Assignment
//       Question → Assignment, StudentProgress → Student(User) + Lesson
//       Enrollment → Student(User) + Course
```

## Fastify 路由注册模式

```typescript
// src/index.ts
import { authRoutes } from './routes/auth.js';
import { courseRoutes } from './routes/courses.js';
// ... 其他路由

await app.register(authRoutes);
await app.register(courseRoutes);
// ... 顺序不重要，Fastify 支持并行注册
```

## Vue 3 页面组件模式

```vue
<template>
  <div class="page-name">
    <!-- Element Plus 组件 -->
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import apiClient from '../api/client';
import { ElMessage } from 'element-plus';

// Composition API only, no Options API
</script>

<style scoped>
/* BEM 命名 */
</style>
```

## 常见 Pitfall

1. **Schema 遗漏模型** — 路由引用了 Enrollment 但 schema 中未定义 → 运行时报错
2. **路由未注册** — 创建了 progress.ts 但忘记在 index.ts 中 `await app.register(progressRoutes)`
3. **变量名截断** — 批量生成时 `MINIO_SECRET_KEY` 被截断为 `MINIO_SECRET_KEY=proces..._KEY`
4. **测试无法导入** — 集成测试导入 `app` 但 index.ts 有 side effect（调用 `start()`）→ 需要 `if (NODE_ENV !== 'test')` 守卫
5. **Enrollment 关系** — Enrollment 模型需要与 StudentProgress 和 Submission 建立关系（如果 analytics 路由需要）
