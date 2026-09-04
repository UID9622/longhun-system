# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
<!--
DNA: #龍芯⚡️丙午·乙未·乙丑·壬午·䷹兑-REGISTRY-DEPLOY-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
-->
# mac_client_setup.md — Mac (Apple M4 Max) 终端操作手册

> 前提：鲲鹏服务器已跑完 deploy_registry.sh。下文把 `<服务器IP>` 全部替换成服务器内网 IP（部署脚本结尾已打印），示例用 `192.168.1.10`。所有命令在 Mac 的「终端」App 里逐条复制粘贴。

## 一、让 Docker Desktop 信任内网仓库（HTTP 模式，默认）

Docker 默认只允许 HTTPS 或 localhost 拉镜像，内网 HTTP 仓库需加白名单（参考文章同款做法）。

```bash
# 1. 先真备份已有配置（带时间戳，不会互相覆盖；没有旧配置也不报错）
mkdir -p ~/.docker
cp ~/.docker/daemon.json ~/.docker/daemon.json.bak.$(date +%Y%m%d%H%M%S) 2>/dev/null || true
```

**先判断：你以前改过 Docker 配置吗？** 如果 `ls ~/.docker/daemon.json` 显示文件已存在且里面不止本仓库这一行（比如配过镜像加速器、代理等），**不要直接覆盖**，按下面「手动合并」操作；如果文件不存在或只有默认内容，直接执行下面的写入即可。

```bash
# 2a. 无已有配置时：直接写入（不存在则新建）
cat > ~/.docker/daemon.json <<'EOF'
{
  "insecure-registries": ["192.168.1.10:5000"]
}
EOF
```

```bash
# 2b. 已有配置时：手动合并 insecure-registries 字段（复制粘贴级）
# 先打开现有配置看看里面有什么：
cat ~/.docker/daemon.json
# 然后用文本编辑器打开编辑：
open -a TextEdit ~/.docker/daemon.json
# 在最外层大括号里加一行（注意：如果它前面已有其他键值对，上一行末尾要补一个英文逗号）：
#   "insecure-registries": ["192.168.1.10:5000"]
# 合并后示例（假设原来有 registry-mirrors）：
# {
#   "registry-mirrors": ["https://xxx.mirror.aliyuncs.com"],
#   "insecure-registries": ["192.168.1.10:5000"]
# }
# 存盘后校验 JSON 没写坏（输出 ok 即合法）：
python3 -c "import json; json.load(open('$HOME/.docker/daemon.json')); print('ok')"
# 若校验报错，用第 1 步的时间戳备份恢复：cp ~/.docker/daemon.json.bak.* ~/.docker/daemon.json
```

```bash
# 2. 重启 Docker Desktop 让配置生效
osascript -e 'quit app "Docker"' ; open -a Docker
# 等顶部菜单栏小鲸鱼图标不再动（约 20 秒）即重启完成
```

> 若部署时启用了 TLS（ENABLE_TLS=1），跳过本节，改用证书信任：
> 把服务器上 `/data/longhun-registry/02-identity/certs/domain.crt` 拷到 Mac，双击导入钥匙串并设为「始终信任」，同时把 `longhun-registry.local` 写进 Mac 的 /etc/hosts 指向服务器 IP。

## 二、登录仓库

```bash
# 3. 登录（账号密码是部署脚本第 4 步打印的那一组）
docker login 192.168.1.10:5000
# Username: longhun
# Password: <粘贴部署时打印的密码>
# 看到 Login Succeeded 即成功
```

## 三、推拉镜像（以 nginx 为例，全程复制粘贴）

```bash
# 4. 从公网拉一个 arm64 测试镜像（M4 Max 本身就是 arm64，天然匹配鲲鹏）
docker pull --platform linux/arm64 nginx:alpine
```

```bash
# 5. 打 tag：把镜像改名成"指向私有仓库"的名字
docker tag nginx:alpine 192.168.1.10:5000/longhun/nginx:alpine
```

```bash
# 6. 推送到私有仓库
docker push 192.168.1.10:5000/longhun/nginx:alpine
# 看到 "Pushed" 多行即成功
```

```bash
# 7. 验证能拉回来：先删本地再从仓库拉
docker rmi 192.168.1.10:5000/longhun/nginx:alpine
docker pull 192.168.1.10:5000/longhun/nginx:alpine
```

## 四、常用速查

```bash
# 查看仓库里有哪些镜像（需登录后拿到的密码）
curl -s -u longhun:<密码> http://192.168.1.10:5000/v2/_catalog

# 查看某个镜像的所有 tag
curl -s -u longhun:<密码> http://192.168.1.10:5000/v2/longhun/nginx/tags/list

# 退出登录
docker logout 192.168.1.10:5000
```

## 五、踩坑速查（registry:2 四大经典坑 + 补充）

> 这 4 个坑来自参考文章实测总结：[快速链接: 参考文章] https://blog.csdn.net/Margrop/article/details/163312205
> 以下按"鉴权→端口→持久化→反向代理/信任"顺序排列，覆盖 95% 的 push/pull 报错。

| # | 症状 | 根因 | 解法 |
|:---:|------|------|------|
| 1 | `push 报 401 Unauthorized` | 鉴权坑：没登录 / 密码错 / htpasswd 文件路径不对 | `docker logout` 后重做第二节 `docker login`；服务器上确认 `/data/longhun-registry/02-identity/auth/htpasswd` 存在且权限 600 |
| 2 | `connection refused` | 端口坑：IP 或端口错 / 防火墙未放行 / 容器没绑 0.0.0.0 | 服务器执行 `firewall-cmd --add-port=5000/tcp --permanent && firewall-cmd --reload`（或 iptables）；确认 `docker port longhun-registry` 显示 `0.0.0.0:5000` |
| 3 | `http: server gave HTTP response to HTTPS client` | 信任坑：客户端 daemon.json 没配 `insecure-registries`，Docker 默认只信任 HTTPS | (a) 重做第一节配置 `insecure-registries` 并重启 Docker Desktop；(b) 或部署时加 `ENABLE_TLS=1` 走 HTTPS |
| 4 | 重启服务器后仓库没了 / 镜像丢了 | 持久化坑：没挂 volume 或挂了但路径错了 | 部署脚本已做双重防护：`-v ...:/var/lib/registry` + `--restart=always` + systemd unit。验证：`docker inspect longhun-registry | grep -A5 Mounts` |
| 5 | `x509: certificate signed by unknown authority` | TLS 坑：用了自签证书但 Mac 没信任 | 把服务器 `02-identity/certs/domain.crt` 拷到 Mac，双击导入「钥匙串访问」→ 找到该证书 → 右键「显示简介」→「信任」→「始终信任」 |
| 6 | `manifest for registry:2 not found` 或架构不匹配 | 镜像坑：拉到了错误架构的 registry 镜像 | 部署脚本已自动检测 `uname -m` 并用 `--platform` 拉对应架构。手动修复：`docker pull --platform linux/amd64 registry:2`（x86）或 `linux/arm64`（ARM） |
| 7 | push 很慢 / 卡住 | 网络坑：走了公网或代理 | 确认 Mac 和服务器在同一内网；`ping <服务器IP>` 延迟应 <5ms；检查是否配了 HTTP_PROXY 代理绕路 |
| 8 | 磁盘满了 push 报 500 | 容量坑：镜像 blob 撑满磁盘 | 服务器跑 `bash /data/longhun-registry/04-execution/bin/gc.sh` 回收已删除镜像空间；`docker system prune -a` 清本机无用镜像（不影响仓库数据） |

> 如果以上 8 条都排除了还不行：服务器 `docker logs --tail 50 longhun-registry` 看详细日志。
