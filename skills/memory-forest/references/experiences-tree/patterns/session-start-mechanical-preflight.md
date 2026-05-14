---
id: EXP-PAT-0040
type: EXPERIENCE
tree: experiences
layer: L3
status: ACTIVE
created: 2026-05-14
heartbeat: '2026-05-14'
priority: HIGH
source: PROJ-EVOL-0007
tags:
- session-start
- preflight
- injection
- guardrail
- mechanical-enforcement
originSessionId: CURRENT
---
# SessionStart 机械 PREFLIGHT — 前置注入方法论

## 触发条件
当 LLM 环境有完备的规则/文档/checklist 但 LLM 仍然会"忘记"执行时。

## 核心模式
利用 SessionStart hook 的 stdout→context 注入机制，在每次会话开始时**机械地**注入：
1. **Validation Status** — 自动跑 validate_all.py --quick，结果直接进上下文
2. **PREFLIGHT Checklist** — 不是"建议"，是格式化的机械步骤（带具体命令）
3. **STOP Signals** — 5 种反模式的即时停止规则
4. **Known Failure Patterns** — 从 feedback 历史提炼，带真相说明防止重蹈
5. **Available Scripts** — 列出所有 validate 脚本，让 LLM 知道它们存在

## Why
LLM 没有跨会话记忆。PHILOSOPHY Ch9 + PREFLIGHT 写得很完整，但在 150K+ token 的上下文里会被稀释。前置注入确保反模式警告在会话开始时高优先级出现。

## How to apply
- 注入段控制在 2500 chars 以内（过长会被截断）
- 每段 ≤ 5 行，点到为止，不展开
- STOP Signals 用粗体关键词触发 LLM 注意力
- 具体命令用反引号包裹（`grep -i ...`）
- Validation 结果如果 ALL PASS，加一句"your hypothesis is probably wrong"

## 反例
- 注入长篇哲学讨论 → LLM 不会细读
- 只注入"建议"不注入"STOP" → LLM 会忽略
- 注入后不更新 → 反模式列表过时

## 来源
Evolution 3 (PROJ-EVOL-0007)
