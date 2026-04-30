---
id: PROJ-ROOT-0000
type: ROOT
tree: projects
layer: L2
status: ACTIVE
created: 2026-04-30
heartbeat: 2026-04-30
priority: HIGH
owner: claude-code
children: []
originSessionId: 439d65d5-aade-426e-807f-de0013c8a345
---
# 项目记忆树 — 根源节点

## 目标
管理所有项目相关的任务记忆。每个项目一个子目录，每个子目录一棵子树。

## 当前项目
尚无活跃项目。项目将在用户发起时创建。

## 项目创建模板
```
projects/<project-name>/
├── ROOT.md          # 项目根源节点
├── branch-<name>.md # 功能/里程碑分支
└── leaf-<name>.md   # 具体任务叶节点
```

## 项目归档规则
- 项目完成后 30 天 → 压缩全文为摘要
- 90 天后 → 仅保留 ROOT 摘要 + 提炼的经验
- 180 天后 → 物理删除（经验已提取到 experiences-tree）

## 活跃项目索引
无。
