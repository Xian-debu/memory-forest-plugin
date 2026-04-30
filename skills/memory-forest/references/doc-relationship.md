---
name: 文档关系树
description: 记忆森林下的文档体系关系 — 森林层 + 系统树层 + 项目树层 + 经验树层
type: project
id: SYS-LEAF-docrel
tree: system
layer: L4
parent: SYS-BRANCH-meta
originSessionId: 439d65d5-aade-426e-807f-de0013c8a345
---
# 文档关系树（记忆森林版）

## 完整层级结构

```
                    ┌─────────────────────────────┐
                    │     forest-root.md           │
                    │     (森林根源, L4, ABSOLUTE)  │
                    │     绝对第一入口              │
                    └─────────────┬───────────────┘
                                  │
            ┌─────────────────────┼─────────────────────┐
            │                     │                     │
            ▼                     ▼                     ▼
┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐
│   MF-SPEC.md      │ │  MF-RUNTIME.md    │ │   MEMORY.md       │
│   (森林宪法)       │ │  (运行时行为)      │ │   (快速索引)       │
│   节点/分层/心跳   │ │  会话/加载/GC     │ │   各树入口         │
└───────────────────┘ └───────────────────┘ └───────────────────┘

═══════════════════════════════════════════════════════════════
                        记忆树层
═══════════════════════════════════════════════════════════════

system-tree/ROOT          experiences-tree/ROOT       projects-tree/ROOT
(系统配置)                 (核心经验)                  (项目任务)
    │                          │                           │
    ├─ branch-config           ├─ patterns/ (L3)           └─ <project>/
    │   ├─ role-definition     └─ core/ (L4)                   ├─ ROOT
    │   └─ dev-overview                                        ├─ branch-*
    │                                                          └─ leaf-*
    ├─ branch-methodology
    │   ├─ tech-methodology
    │   ├─ debug-methodology
    │   └─ design-standards
    │
    ├─ branch-quality
    │   ├─ dev-standards
    │   ├─ doc-standards
    │   ├─ module-standards
    │   ├─ tool-standards
    │   ├─ selfcheck-standards
    │   └─ baseline-verification
    │
    ├─ branch-safety
    │   └─ system-ops-safety
    │
    └─ branch-meta
        ├─ doc-usage-guide
        ├─ doc-relationship (本文档)
        ├─ doc-revision
        └─ project-init
```

## 层级优先级（冲突裁决顺序）

```
L4 — forest-root + MF-SPEC + MF-RUNTIME     (森林宪法: 不可被任何下层推翻)
L4 — system-tree 核心配置                    (角色 + 环境: 定义我是谁)
L4 — system-tree 安全分支                    (安全红线: 不可违反)
L3 — system-tree 方法论分支                   (分析视角: 指导思维)
L2 — system-tree 质量标准分支                 (代码/模块规范: 指导编写)
L2 — system-tree 元规范分支                   (文档演进来: 指导维护)
L2 — projects-tree                           (项目记忆: 任务上下文)
L1 — projects-tree LEAF nodes                (任务记忆: 当前执行状态)
L0 — 会话上下文                               (瞬时记忆: 不持久化)
```

## 循环依赖
- 无循环依赖。引用方向: 森林 → 树根 → 分支 → 叶节点

## 规范完整性检查清单（隶属 system-tree）
- [x] config — role-definition, dev-overview
- [x] methodology — tech-methodology, debug-methodology, design-standards
- [x] quality — dev-standards, doc-standards, module-standards, tool-standards, selfcheck-standards, baseline-verification
- [x] safety — system-ops-safety
- [x] meta — doc-usage-guide, doc-relationship, doc-revision, project-init
- [x] forest — forest-root, MF-SPEC, MF-RUNTIME, MEMORY
- [x] trees — system-tree/ROOT, experiences-tree/ROOT, projects-tree/ROOT
- [x] branches — branch-config, branch-methodology, branch-quality, branch-safety, branch-meta
