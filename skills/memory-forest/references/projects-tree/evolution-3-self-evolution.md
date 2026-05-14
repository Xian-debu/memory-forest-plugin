---
id: PROJ-EVOL-0007
type: LEAF
tree: projects
layer: L2
status: COMPLETED
parent: PROJ-ROOT-0000
created: 2026-05-14
completed: 2026-05-14
heartbeat: '2026-05-14'
priority: HIGH
owner: claude-code
tags:
- self-evolution
- guardrail
- anti-hallucination
- validation
- resonance
- session-start
- anti-pattern
experience_refs:
- EXP-PAT-0039
- EXP-PAT-0040
- EXP-PAT-0041
originSessionId: CURRENT
---
# 第三次自我进化 — 防呆机械体系 (2026-05-14)

## 触发
用户第三次显式要求自我进化，核心主题：**防呆**。用户将 LLM 描述为"短记忆强能力个体，容易胡搞臆想，脑子不好的超人"。要求进化的一切有利于 LLM 自身运作。

## 核心矛盾分析

**已有**: PHILOSOPHY Ch9 (LLM 认知约束) + PREFLIGHT.md + 16 条 feedback + 8 条 L4 行为准则——规则极其完整。

**缺失**: 规则是"纸面上的"，依赖 LLM 自觉执行。NPU 误诊事件（2026-05-14）证明：即使规则就在记忆里，LLM 也会跳过直接行动。validate 模式只在 NPU 一个项目落地。共振仅 5 条 error 规则。

**进化方向**: 将纸面规则转化为**机械执行的前置注入**——不需要 LLM "记得"去检查，而是一开始就注入上下文。

## Round 1: 互补配对 — validate 矩阵 + SessionStart 强化

### 1A: validate 脚本矩阵 (5 个新脚本)
基于 validate_npu.py 模板（嵌入基线知识 + 区分正常/退化），创建了覆盖全部高风险模块的验收脚本：

| 脚本 | 覆盖面 |
|------|--------|
| `validate_mf.py` | Memory Forest 结构健康 + 心跳新鲜度 + 循环引用检测 |
| `validate_resonance.py` | signals.json 规则有效性 + 引擎功能 + 覆盖率基线 |
| `validate_hooks.py` | settings.json 完整性 + hook 脚本存在性 + timeout 检查 |
| `validate_services.py` | Ollama + Docker + NPU + Guardian + n8n + Disk/Mem |
| `validate_all.py` | 主运行器：并行执行全部 5 模块，JSON/Text 双输出 |

设计原则: 每个检查项标注预期范围、原理、真回归阈值。LLM 下次看到数字时，跑 validate 脚本即可自动判断是否为 bug。

### 1B: SessionStart 机械 PREFLIGHT 注入
增强 `system_drive.py generate_context_injection()` 新增 5 个注入段：

1. **Validation Status** — 自动运行 `validate_all.py --quick --json`，结果注入上下文
2. **PREFLIGHT Checklist** — 机械步骤清单（grep memory → run validate → read docs）
3. **STOP Signals** — 5 种反模式的即时停止规则
4. **Known LLM Failure Patterns** — 从 feedback 提炼的 4 个历史错误模式，带真相说明
5. **Available Validate Scripts** — 列出所有 validate_*.py，让 LLM 知道它们的存在

每段不超过 5 行，总注入 ~2500 chars。

## Round 2: 高价值独立 — 共振规则扩展 + 防呆护栏

### 2C: 共振规则大规模扩展
`signals.json` 全面重写为 v3.0.0：
- **error→memory**: 5 → 32 条规则（覆盖 OOM/GPU/网络/序列化/编译/下载/Docker/swap/401/captcha 等）
- **tool→memory**: 8 → 27 条规则（覆盖 ollama/latex/validate/npu/cdp/docker/systemctl/openvino 等）
- **context_signals**: 7 → 11 个场景（新增 npu/ppt/browser/aegis）
- **guardrail_anti_patterns**: 全新 10 条反模式规则（designing_own_test/judging_by_number/modify_without_context 等）

所有规则通过正则匹配验证，10/10 测试用例全部正确映射。

### 2D: PreToolUse 防呆护栏
增强 `system_drive.py cmd_pre_tool()`：
- 当检测到 Edit/Write 操作目标为受保护模块时
- 自动运行该模块的 validate 脚本（quick mode, 15s timeout）
- 若 validate PASSES → 输出 stderr 警告 + 记录到 `guardrail_violations.json`
- 下次 SessionStart 会读取 violations 并注入上下文

## Round 3: 质量维护 + 文档

### 3E: 记忆森林质量
- 130 nodes, 68 ACTIVE, 12 COMPLETED, 0 DORMANT
- 全部心跳新鲜，无循环引用
- GC: 无候选节点
- 16 feedback memories, 44 experience patterns

## 进化后环境状态

| 指标 | 进化前 | 进化后 |
|------|--------|--------|
| validate 脚本 | 1 (NPU only) | 6 (all modules) |
| SessionStart 注入段 | 4 | 9 |
| error→memory 规则 | 5 | 32 |
| tool→memory 规则 | 8 | 27 |
| context_signals | 7 | 11 |
| anti_pattern 规则 | 0 | 10 |
| PreToolUse 护栏 | 无 | Edit/Write 自动拦截 |
| validate_all 基线 | 无 | 5 modules, 70 checks |

## 核心设计原则 (Evolution 3 提炼)

1. **机械优于自觉**: 规则再完整，依赖 LLM "记得"就是失败。前置注入 > 文档 > 记忆。
2. **基线嵌入代码**: 每个 validate 脚本自带"什么是正常"的知识，不需要查记忆。
3. **验证优于推理**: 所有诊断的第一步是跑 validate，不是自己设计测试。
4. **已知错误 = 不可重复**: feedback 反模式直接注入 SessionStart，每会话可见。
5. **护栏不阻塞**: PreToolUse 护栏只警告不阻止——LLM 有最终决策权，但警告会记录为 violations 供下会话审计。

## 经验提炼

- [EXP-PAT-0039] validate 脚本防呆矩阵 — 基线嵌入代码模式推广
- [EXP-PAT-0040] SessionStart 机械 PREFLIGHT — 前置注入方法论
- [EXP-PAT-0041] PreToolUse 模块护栏 — 编辑前自动验证模式
