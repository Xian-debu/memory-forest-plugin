---
id: PROJ-EVOL-0001
type: BRANCH
tree: projects
layer: L2
status: COMPLETED
parent: PROJ-ROOT-0000
created: 2026-05-01
completed: 2026-05-01
heartbeat: 2026-05-01
priority: HIGH
owner: claude-code
originSessionId: a7664e14-d841-48de-acfa-f9d0da11efe2
children:
  - PROJ-EVOL-0002
  - PROJ-EVOL-0003
  - PROJ-EVOL-0004
  - PROJ-EVOL-0005
experience_refs:
  - EXP-PAT-0003
  - EXP-PAT-0004
  - EXP-PAT-0005
  - EXP-PAT-0001
---
# 首次自我进化

## 目标
基于当前开发环境状态，执行首次系统性自我进化。

## 当前状态
已完成。四个进化方向全部落地。

## 关键决策

### 选择这四个方向的原因
1. **Hook 自动化 (A)**: 记忆森林规范了完整自动化行为但无执行机制。Stop + SessionStart hook 解决了"有蓝图无发动机"的矛盾。
2. **MCP Server (B)**: 记忆森林是内部系统，通过 MCP 协议暴露为标准接口后，其他 agent/tool 可无摩擦访问。
3. **启动自检 (C)**: 确保每次会话都执行记忆森林启动协议，不再依赖"自觉"。
4. **权限+快捷键 (D)**: 减少开发摩擦，提升 Docker 工作流效率。

### 技术选型
- Python 3 stdlib 实现 MCP Server（JSON-RPC 2.0 over stdio），因为 PEP 668 阻止系统级 pip install
- 手动实现而非依赖 mcp SDK，零外部依赖
- DateEncoder 解决 YAML 解析 datetime.date 导致 JSON 序列化失败的问题

### 为什么先 A+C 再 B 再 D
A 和 C 互补（启动+退出自动维护），零风险纯增量。B 价值最高但需验证协议兼容性。D 是锦上添花。

## 子节点索引
- [PROJ-EVOL-0002] Evolution A: Stop Hook + mf CLI 工具
- [PROJ-EVOL-0003] Evolution B: MCP Memory Server  
- [PROJ-EVOL-0004] Evolution C: SessionStart 启动自检
- [PROJ-EVOL-0005] Evolution D: 权限优化 + 工作流快捷键

## 经验提炼
- [EXP-PAT-0003](patterns/mcp-zero-dep.md) — MCP Server 零依赖实现
- [EXP-PAT-0004](patterns/yaml-json-bridge.md) — YAML-JSON 桥接类型陷阱
- [EXP-PAT-0005](patterns/self-evolution-methodology.md) — 自我进化执行方法论
- [EXP-PAT-0001](patterns/plugin-publishing.md) — Git Data API 推流模式再次验证
