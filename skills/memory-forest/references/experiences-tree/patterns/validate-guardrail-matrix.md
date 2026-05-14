---
id: EXP-PAT-0039
type: EXPERIENCE
tree: experiences
layer: L3
status: ACTIVE
created: 2026-05-14
heartbeat: '2026-05-14'
priority: HIGH
source: PROJ-EVOL-0007
tags:
- validate
- guardrail
- baseline
- anti-hallucination
- fool-proof
originSessionId: CURRENT
---
# validate 脚本防呆矩阵 — 基线嵌入代码模式

## 触发条件
当需要在 LLM 环境中防止"看到正常数据当 bug 修"时。

## 核心模式
为每个高风险模块创建 `validate_*.py`，脚本本身嵌入：
1. **基线常量** — 正常数值范围 + 为什么是这个范围
2. **回归标记** — 什么数字才是真正的 bug
3. **自然语言解释** — 输出不自带解释=下次 LLM 还会误判

## 关键要素
- 每个 check() 返回 (ok bool, detail str)，detail 自带解释
- 区分 "NORMAL: bge-m3 dense embedding baseline" 和 "CHECK: outside expected range"
- 脚本顶部注明参考的记忆文件路径
- `--quick` 模式跳过语义质量检查（供自动调用）
- `validate_all.py` 主运行器并行执行所有模块

## 反例
- 测试只有 assert 没有解释 → LLM 看到数字不知道是不是 baseline
- 只有 pass/fail 没有 warn → 把已知限制当 bug
- validate 脚本存在但 LLM 不知道 → SessionStart 必须列出

## 适用场景
任何 LLM 曾经误诊过的系统，任何有"已知奇怪值但不是 bug"的系统。

## 来源
Evolution 3 (PROJ-EVOL-0007)，基于 NPU 误诊事件 (diagnose-before-modify)
