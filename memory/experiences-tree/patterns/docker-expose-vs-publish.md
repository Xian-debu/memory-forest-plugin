---
id: EXP-PAT-0016
name: docker-expose-vs-publish-vscode-tunnel
description: Docker EXPOSE vs -p publish 的幻觉 + VS Code 自动端口隧道
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
- docker
- port-forwarding
- vscode
- debugging
- 排查
---
# Docker EXPOSE vs -p 端口映射 + VS Code 自动隧道幻觉

## 根因

Docker 有两种端口机制：
- **EXPOSE** (Dockerfile 指令): 纯元数据声明，不创建任何端口映射
- **-p host:container** (docker run 参数): 实际发布端口到宿主机

如果只 EXPOSE 不 -p，端口只在容器内可达。但 **VS Code Server 连接进容器后会自动扫描容器内监听的端口并创建 tunnel 转发**，让用户能在浏览器直接访问。

这会制造一种完美的幻觉：**用户体感和直接端口映射完全没区别**，以为自己用了 -p 8888:8888。

## 排查方法

```bash
# 1. 检查实际端口映射 (HostConfig.PortBindings 才是真相)
docker ps -a --format '{{.Names}} {{.Ports}}'
# 0.0.0.0:8000->8000/tcp  → 已发布
# 8888/tcp                   → 仅 EXPOSE，未发布

# 2. 精确检查
docker inspect dev | jq '.[0].HostConfig.PortBindings'    # 实际映射
docker inspect dev | jq '.[0].Config.ExposedPorts'         # 仅元数据

# 3. 查 bash 历史确认原始命令
grep "docker run" ~/.bash_history
```

**关键区分:** `docker ps` 输出中，`8888/tcp` (无 `->`) = EXPOSE 未发布；`0.0.0.0:8888->8888/tcp` = 已发布。

## 为什么 VS Code 隧道让人产生幻觉

1. 用户连接 VS Code → 容器
2. VS Code Server 扫描容器内端口 → 发现 8888 在监听
3. VS Code 自动创建 tunnel → 浏览器 `localhost:8888` 能访问
4. 用户以为这是 `-p 8888:8888` 的效果
5. 某天用户不连 VS Code 直接访问 → 端口不通 → 才发现真相

## 教训

- 排查 Docker 端口问题时，**不要信任记忆**。人的记忆会被"体感正常"覆盖
- 首选证据链: `docker inspect` → `docker ps` → bash history
- 如果容器 PortBindings 为空或没有目标端口 → 从没发布过，问题不在"为什么失效"

## 适用场景

- Docker Desktop / WSL2 环境端口转发排查
- "以前可以直接访问，现在突然不行了"类问题
- VS Code Remote / Dev Container 开发环境
