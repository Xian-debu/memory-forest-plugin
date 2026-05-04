---
id: PROJ-ROOT-0000
type: ROOT
tree: projects
layer: L2
status: ACTIVE
subordinate_to: PHIL-ROOT-0000
created: 2026-04-30
heartbeat: '2026-05-05'
priority: HIGH
owner: claude-code
children:
- PROJ-FWREF-0000
- PROJ-EVOL-0001
- PROJECTS-BRANCH-0001
- PROJ-OLLAM-0001
originSessionId: 439d65d5-aade-426e-807f-de0013c8a345
---
# 项目记忆树 — 根源节点

**本树受 PHILOSOPHY.md（L5 绝对底层）约束。项目执行策略以六条哲学原则为指导。**

## 目标
管理所有项目相关的任务记忆。每个项目一个子目录，每个子目录一棵子树。

## 活跃项目
- [框架重构](framework-refactor/ROOT.md) — 轴承故障诊断实验框架模块化 (Phase 1-4 完成, 2026-05-01)
- [首次自我进化](evolution-1-self-evolution.md) — Stop Hook + mf CLI + MCP Server + SessionStart (2026-05-01 完成)
- [n8n工作流系统搭建](PROJECTS-BRANCH-0001.md) — n8n Docker + DeepSeek API 自动化工作流 (2026-05-01 完成)
- [本地 AI 模型系统](PROJ-OLLAM-0001.md) — Ollama + RTX 5070 + 嵌入索引 + 代码审查 (2026-05-01 进行中)

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
