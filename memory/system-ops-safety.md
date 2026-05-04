---
name: 系统操作安全规范
description: root 权限下的系统级操作安全边界、内核修改、服务管理、网络配置的风险控制
type: project
originSessionId: 439d65d5-aade-426e-807f-de0013c8a345
---
# 系统操作安全规范

## 核心原则
- 有 root 权限 ≠ 应使用 root 权限
- 系统级修改必须可逆或有回滚方案
- 修改内核/系统配置前必须备份原始文件

## 操作分级

### 绿色（自由操作）
- 读取任何文件（cat/less/Read）
- `ls`, `find`, `grep`, `stat`, `which`, `type`
- `pip install --user`, `npm install`（用户空间）
- Docker 容器操作（非特权模式）
- `/root/` 和 `/root/project/` 下任意修改
- 编译、构建、测试

### 黄色（谨慎操作，记录留痕）
- `apt install` 系统级软件包
- 修改 `/etc/` 下配置文件
- `systemctl` 启停服务
- `docker run --privileged`
- `iptables` / `ufw` 防火墙规则
- 创建 `/etc/cron.*` 定时任务
- 挂载/卸载文件系统

### 红色（必须用户确认，备份先行）
- 内核模块 (`modprobe`, `insmod`, `rmmod`)
- 修改 `/boot/` 或 GRUB 配置
- `dd` 写入块设备
- 修改 `/etc/passwd`, `/etc/shadow`
- `rm -rf /` 或通配删除系统路径
- `chmod -R 777` 系统目录
- 修改内核参数 (`sysctl`, `/proc/sys/`)
- 删除 Docker 卷 (docker volume rm)

## 备份协议（红色操作前）
```bash
# 修改配置前
cp /etc/<config> /root/.claude/backups/<config>.$(date +%Y%m%d%H%M%S)

# 修改内核模块前
lsmod > /root/.claude/backups/lsmod.before.$(date +%Y%m%d%H%M%S)
```

## 回滚协议
- 每次红色操作后记录：改了什么、怎么回滚
- 备份文件保留至少 7 天
- 若操作导致系统不稳定，立即回滚并报告

## 服务管理
- 优先使用 `docker run` 而非直接在宿主机安装服务
- 若必须宿主机安装，使用 `systemctl` 管理
- 不修改预装服务的默认端口和配置（除非冲突且确有必要）

## 网络安全
- 不对外暴露端口，除非明确要求
- Docker 端口映射优先绑定 `127.0.0.1`（`127.0.0.1:8080:8080`）
- 不修改 WSL2 的 Windows 侧防火墙（无权限也无必要）

## 资源管理
- 磁盘使用监控：> 80% 时警告
- 内存使用监控：> 90% 时警告
- Docker 定期清理：`docker system prune -f`（周级）

## 禁止
- 不在未确认的情况下 `rm -rf` 任何系统路径
- 不 `chmod 777` 关键系统目录
- 不关闭 SELinux/AppArmor（除非确有必要且用户同意）
- 不在生产服务运行时修改其配置
- 不将 `/root/` 下的敏感文件暴露到容器绑定挂载
