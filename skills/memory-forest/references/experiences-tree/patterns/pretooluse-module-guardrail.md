---
id: EXP-PAT-0041
type: EXPERIENCE
tree: experiences
layer: L3
status: ACTIVE
created: 2026-05-14
heartbeat: '2026-05-14'
priority: HIGH
source: PROJ-EVOL-0007
tags:
- pretooluse
- guardrail
- edit-protection
- validation-gate
originSessionId: CURRENT
---
# PreToolUse 模块护栏 — 编辑前自动验证模式

## 触发条件
当需要防止 LLM 在没有验证的情况下修改已验证模块时。

## 核心模式
在 PreToolUse hook 中拦截 Edit/Write 操作：
1. 检查目标文件是否属于受保护模块（PROTECTED_MODULES 字典）
2. 如果模块有 validate 脚本 → 自动运行 `--quick`（15s timeout）
3. 如果 validate PASSES → 输出 stderr 警告 + 记录到 guardrail_violations.json
4. 下次 SessionStart 读取 violations 并注入上次违规记录

## Why
LLM 可能在单次会话内做出多个错误修改，且不会在中间停下来检查。护栏不阻止操作（PreToolUse 不能 blocking），但通过警告 + 跨会话审计形成威慑。

## How to apply
- PROTECTED_MODULES 字典: module_path_prefix → validate_script
- 只对 Edit/Write 操作触发，不对 Read/Bash
- Validate 超时 15s，不阻塞工具调用
- Violations 保留最近 20 条
- SessionStart 注入最近 5 条 violations

## 反例
- PreToolUse 试图阻止工具调用 → 做不到，强行阻止会卡住
- 对 Read 操作也触发 → 噪音过多，忽略警告
- 不设 timeout → validate 脚本卡住会阻塞整个工具调用

## 来源
Evolution 3 (PROJ-EVOL-0007)
