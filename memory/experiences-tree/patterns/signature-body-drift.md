---
id: EXP-PAT-0021
name: signature-body-drift
description: 跨文件命名重构后函数签名与函数体不一致 — grep 替换改body忘改签名
type: PATTERN
tree: experiences
layer: L3
status: ACTIVE
created: 2026-05-03
heartbeat: '2026-05-05'
priority: HIGH
owner: claude-code
parent: EXP-ROOT-0000
originSessionId: CURRENT
tags:
- refactoring
- naming-convention
- audit
- bug-pattern
- parameter-mismatch
---
# 命名重构后签名/函数体不一致

## 场景

跨多文件统一命名规范时（如 `save_dir` → `save_root` + `model_name`），用 grep/正则批量替换函数体中的旧名字，但函数签名在文件顶部，容易被漏掉。

## 问题

大规模命名重构时，替换操作天然倾向于"函数体内局部变量"而漏掉三处：

1. **函数签名** — `def foo(save_dir='figures')` 中的 `save_dir` 不在函数体内，grep 替换可能不覆盖
2. **被调用者新参数** — 调用者已经 `func(save_root=..., model_name=...)` 但被调用者签名未加这些参数 → NameError
3. **闭包/跨作用域变量** — 内部函数引用了外部函数的局部变量（如 `mname`），该变量在签名中不可见

**Why:** 在本次框架重构中，7 个文件同时改造 `save_dir` → `save_root` + `model_name`，用 grep 替换了函数体中的 `save_dir` 引用，但：
- `diagnose_domain_shift()` 签名保留了旧 `save_dir='figures'`，函数体却用了未定义的 `save_root` 和 `model_name`
- `_plot_shift_figure()` 引用了调用者局部变量 `mname`，但该变量不在其作用域中
- `kfold.py:79` 中 `model_name = config.get('model_name', 'Unknown')` 覆盖了函数参数 `model_name`

## 修复

**审计方法 — 每个被改函数检查三点：**
```
1. 函数签名 ←→ 函数体一致性：签名中每个参数都在 body 中使用了吗？body 中每个未定义的变量都在签名中了吗？
2. 调用者 ←→ 被调用者签名一致性：调用者传递的每个 kwarg 都在被调用者签名中存在吗？
3. 内部函数 ¬ 使用外部局部变量：检查是否有 def _helper() 引用外部 var
```

**具体命令：**
```bash
# 对每个改造文件，列出所有函数签名和所有未定义引用
grep -n "^def \|save_root\|save_dir\|model_name\|mname" file.py
# 手动验证: body 中引用的每个变量要么在签名中，要么在函数内定义
```

## 适用场景

- 任何跨 3+ 文件的命名规范化/重构
- 参数语义变更（如单一路径 → 根目录+模型名组合）
- 函数提取/合并后参数透传链路变更
- grep/sed 批量替换后的代码审计

## 反例

- 只 grep 替换函数体，不逐函数检查签名
- 信任"函数体跑通了 = 签名没问题" — NameError 在单元测试中可能走到那个分支才触发
- 内部 helper 函数不检查作用域依赖
