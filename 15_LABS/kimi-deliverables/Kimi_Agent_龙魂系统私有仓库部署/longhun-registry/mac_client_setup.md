<!--
#龍芯⚡️{年干支}·{月干支}·{日干支}·{卦名}-REGISTRY-DEPLOY-v1.0
# 注：干支以本地生成器 bin/lh_dna_generator.py 输出为准，禁止手写
# 署名：龍芯北辰 UID9622
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

## 五、踩坑速查（来自参考文章 4 大坑）

| 症状 | 原因 | 解法 |
|---|---|---|
| push 报 401 | 没登录 / 密码错 | 重做第二节 docker login |
| connection refused | IP 或端口错 / 防火墙未放行 | 服务器执行 `firewall-cmd --add-port=5000/tcp --permanent && firewall-cmd --reload` |
| `http: server gave HTTP response to HTTPS client` | daemon.json 未配 insecure-registries | 重做第一节并重启 Docker Desktop |
| 重启服务器后仓库没了 | 部署脚本已用 --restart=always + systemd，正常不会发生 | 服务器上 `docker start longhun-registry` |

> 出处标注：[快速链接: 参考文章] https://blog.csdn.net/Margrop/article/details/163312205 （401/WWW-Authenticate 与 insecure-registries 章节）
