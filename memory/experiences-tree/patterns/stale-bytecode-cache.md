---
id: EXP-PAT-0019
name: stale-bytecode-cache
description: Python .pyc 缓存导致修复后仍报同样错误 — Jupyter kernel 不重启 + __pycache__ 未清理
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
- debugging
- python
- jupyter
- caching
- self-correction
---
# 代码修复后错误不变 → 先清 .pyc 缓存

## 症状

修改了 `.py` 文件后重新运行，报错的行号、错误信息、traceback 和修改前一模一样。

## 根因

Python 双重缓存机制：
1. **`__pycache__/*.pyc`** — 编译后的字节码，Python 在 `.py` 文件 mtime 早于 `.pyc` 时才重新编译。如果文件编辑后 mtime 未更新（如 docker cp 保留了原始时间戳），`.pyc` 永远是旧的
2. **`sys.modules`** — Jupyter notebook 的 kernel 进程存活期间，已导入的模块不会重新加载。即使 `.py` 和 `.pyc` 都已更新，`import` 语句仍返回内存中的旧对象

## 排查流程

当用户报告"修了但没生效"时，自检顺序：
1. **确认文件确实被修改了** — `grep` 检查目标行
2. **检查 `.pyc` 时间戳** — `find -name "*.pyc" -ls`，对比 `.py` 的 mtime
3. **检查是否是 Jupyter** — notebook 输出中的 `execution_count` 如果和上次相同，说明 kernel 未重启

## 修复

```bash
# 清除所有 __pycache__
find . -name "__pycache__" -type d -exec rm -rf {} +
# Jupyter: Kernel → Restart Kernel
```

## 教训

**用户说"还是报错"时，不要直接怀疑自己改错了代码。** 先检查文件是否真的被加载了新版本。本案例中，`.py` 文件已正确修复（`grep` 验证），但 13 个 `__pycache__` 目录 + Jupyter kernel 缓存导致旧代码仍在运行。

这符合 EXP-CORE-0002（三次重复即自省）——用户第二次说同一个错误时，不应重复改代码，而应追问"为什么修复没生效"。

## 适用场景

- Jupyter notebook 中 `import` 外部 `.py` 文件后修改该文件
- Docker 容器内编辑 Python 文件（`docker cp` 可能保留 mtime）
- 任何 Python 进程长运行期间修改源码的场景
