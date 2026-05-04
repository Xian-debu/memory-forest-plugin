---
id: EXP-PAT-0017
name: wsl2-swap-vhdx-orphan
description: WSL2 每次启动创建 GUID 目录存放 swap.vhdx，关闭后不清理，累积到 ~16GB
type: PATTERN
tree: experiences
layer: L3
status: ACTIVE
created: 2026-05-03
heartbeat: '2026-05-05'
priority: MEDIUM
owner: claude-code
parent: EXP-ROOT-0000
originSessionId: CURRENT
tags:
- wsl2
- swap
- disk-space
- memory
- cleanup
---
# WSL2 swap.vhdx 孤儿文件累积

## 根因

WSL2 每次启动时在 `%USERPROFILE%\AppData\Local\Temp\<GUID>\swap.vhdx` 创建交换文件，大小默认是物理内存的 25%（32GB → 8GB swap，对应 `.wslconfig` 中的 `swap=` 参数或默认值）。

**WSL2 关闭时不清理旧的 swap 文件。** 每次重启生成新的 GUID 目录，旧的留在原地成为孤儿。

多次重启后可能有 2-4 个孤儿 swap 文件，每个 8GB，累积占用 16-32GB。

## 辨别方法

```bash
# 找到所有 swap.vhdx
find /mnt/c/Users/ZYX/AppData/Local/Temp/ -name "swap.vhdx" -exec ls -lah {} \;

# 判断哪个是当前活跃的
uptime                              # WSL 启动时间
free -h                             # 当前 swap 大小
# 修改时间 ≈ WSL 启动时间的 = 当前活跃
# 修改时间 < WSL 启动时间的 = 孤儿，可安全删除
```

## 为什么训练后会被发现

训练（GPU + 大数据集 + DataLoader）产生内存压力，WSL 往 swap 写入数据，swap.vhdx 文件时间戳被更新。用户查看 C 盘时看到"新修改的大文件"，误以为是训练直接生成的，但 swap 文件自 WSL 启动起就一直存在。

## 清理

- **孤儿 swap（当前 WSL 会话之前的时间戳）**: 直接 `rm -rf` 整个 GUID 目录
- **当前活跃 swap**: WSL 运行时不可删，关闭 WSL 后它会变成孤儿，但下次启动又会生成新的
- **限制大小**: 在 `.wslconfig` 中设置 `swap=4GB`（默认 25% RAM），但会增加 OOM 风险

## 易混场景

- WSL crash dump (`wsl-crashes/`): 进程崩溃时产生，每次 ~10GB
- 两者都在 `%TEMP%` 下，都是训练内存爆炸的"受害者"但 swap 是基础设施，crash dump 是直接产物
- 训练直接产物看：crash dump、模型 checkpoint、日志文件
- WSL 基础设施看：swap.vhdx、ext4.vhdx

## 适用场景

- WSL2 + Docker + GPU 训练环境
- C 盘空间突然减少的排查
- WSL 频繁重启后的磁盘清理
