---
id: EXP-PAT-0011
name: verify-merge-order
description: 配置/参数合并顺序必须从代码验证，不可信任注释/文档
type: LEAF
tree: experiences
layer: L3
status: ACTIVE
parent: EXP-ROOT-0000
heartbeat: '2026-05-05'
originSessionId: dc7b6208-9d01-4be5-a94f-1e85b570f468
---
# 配置合并顺序：读代码不读注释

**规则**: 参数合并顺序（dict update / `{**a, **b}`）直接决定哪个源胜出。永远从代码推导合并顺序，不要信任注释或变量名。

**Why**: `net_define_examples.py` 注释写 "param_space 返回的值会覆盖 fixed_config"，但 `assemble_config` 的实现是 `{**study_best_params, **fixed_config}`，fixed_config 后合并所以覆盖前值。这个错误注释导致 run.py 中 `fixed_config` 包含了 4 个架构超参（freq_dim, n_bands, band_width, kernel_mode），它们覆盖了 Optuna 搜索的结果，使贝叶斯架构搜索完全无效。

**How to apply**: 审计任何 config/param/dict merge 逻辑时：1) 找到合并操作的实际代码 2) 确定谁后合并谁胜出 3) 对照所有调用方验证意图匹配 4) 如发现注释与代码不一致，以代码为准更新注释。
