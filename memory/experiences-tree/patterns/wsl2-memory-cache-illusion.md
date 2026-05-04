---
id: EXP-PAT-0022
name: wsl2-memory-cache-illusion
description: WSL2 VM 不向 Windows 归还缓存内存，导致宿主机内存显示虚高
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
- memory
- debugging
- linux-cache
- docker
---
# WSL2 内存使用虚高 — 文件缓存幻觉

## 场景

宿主 Windows 任务管理器显示内存 40-41GB 已用，但 WSL2 内部 `free -h` 显示只用了 10GB。用户担心内存泄漏。

## 问题

WSL2 VM 的 `MemTotal` 就是它向 Windows 申请的全部物理内存。Linux 内部文件缓存 (page cache) 会膨胀到填满可用空间，即使 `free` 显示为 "available"，**Windows 侧仍把整个 VM 的内存分配算作 "in use"**。

三层账本不一致：
```
Windows 任务管理器:     40GB used  ← 用户看到这个，以为要爆了
  └─ WSL2 VM (MemTotal):  32GB    ← Windows 全算成 used
       ├─ Linux 进程 RSS:   8GB   ← 真正的活跃使用
       ├─ Linux 文件缓存:  20GB   ← .mat 文件读后缓存，可回收但 WSL2 不归还
       └─ Linux free:        2GB
```

**Why:** WSL2 的 `/proc/meminfo` 中 `Cached` 和 `Inactive(file)` 在 Linux 看来是可回收的，但 WSL2 不会主动 `drop_caches` 归还给 Hyper-V，Windows 侧只能看到 VM 持有的总量。

## 诊断

```bash
# WSL2 内部：看真正活跃使用
cat /proc/meminfo | grep -E "^AnonPages|^Cached|^Inactive"

# 如果 Inactive(file) + Cached 占大头，就是文件缓存幻觉
# 找谁填满了缓存
find / -type f -size +10M -atime -1 2>/dev/null | xargs ls -lh
# 通常是大数据集文件 (.mat, .h5, .npy) 被反复读写
```

## 修复

**不需要修复** — 文件缓存在内存压力下会自动回收。除非：

```bash
# 一次性释放 (临时)
echo 3 | sudo tee /proc/sys/vm/drop_caches

# 永久限制 WSL2 内存上限 (%UserProfile%\.wslconfig)
[wsl2]
memory=24GB
```

## 适用场景

- 任何在 WSL2 内反复读写大文件的场景 (数据集加载、checkpoint 读写)
- Docker 容器内跑数据 pipeline，容器停了但宿主机内存没降
- 看到 WSL2 `free` 正常但 Windows 内存告警时

## 反例

- 盲目 `drop_caches` 解决 "看起来高但实际无所谓" 的问题
- 把文件缓存高当作进程内存泄漏去查
