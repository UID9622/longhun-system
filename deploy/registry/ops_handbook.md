# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
<!--
DNA: #龍芯⚡️丙午·乙未·乙丑·兑-REGISTRY-DEPLOY-v1.0
创建者: 诸葛鑫（UID9622）
协议: CC BY-NC-SA 4.0
-->
# ops_handbook.md — 龍魂私有仓库运维手册

> 全部命令在鲲鹏服务器上以 root 执行（标注 [Mac] 的除外）。变量：`R=http://127.0.0.1:5000`，账号 `longhun`。

## 1. 健康检查

```bash
# 看容器状态（Up 即正常）
docker ps --filter name=longhun-registry

# 健康探针：配了鉴权时返回 401 才是正常（参考文章的监控坑：别用 grep 200）
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:5000/v2/
# 输出 401 = 服务正常且鉴权生效

# 看运行日志
docker logs --tail 100 longhun-registry
```

## 2. 查看仓库内容（catalog API）

```bash
# 所有仓库列表
curl -s -u longhun:<密码> http://127.0.0.1:5000/v2/_catalog

# 某镜像的所有 tag（把 longhun/nginx 换成实际仓库名）
curl -s -u longhun:<密码> http://127.0.0.1:5000/v2/longhun/nginx/tags/list

# 磁盘占用
du -sh /data/longhun-registry/01-physical/registry-data
```

## 3. 删除镜像（两步：删 manifest + 垃圾回收）

```bash
# 第一步：拿要删 tag 的 digest
DIGEST=$(curl -s -u longhun:<密码> -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
  -I http://127.0.0.1:5000/v2/longhun/nginx/manifests/alpine \
  | grep -i docker-content-digest | awk '{print $2}' | tr -d '\r')
echo "$DIGEST"

# 第二步：按 digest 删除（部署脚本已开启 delete.enabled）
curl -s -u longhun:<密码> -X DELETE http://127.0.0.1:5000/v2/longhun/nginx/manifests/$DIGEST

# 第三步：跑垃圾回收，真正释放磁盘
bash /data/longhun-registry/04-execution/bin/gc.sh
```

## 4. 备份与恢复

```bash
# 备份（建议每月一次，整个四层目录打成一个包）
tar -czf /data/longhun-registry/01-physical/backups/longhun-registry-$(date +%Y%m%d).tar.gz \
  --exclude='01-physical/backups' -C /data longhun-registry

# 恢复（新服务器上，先装 Docker，再解包，再重跑容器）
tar -xzf longhun-registry-YYYYMMDD.tar.gz -C /data
bash deploy_registry.sh   # 脚本幂等：htpasswd/证书已存在会自动沿用，直接重拉容器
```

## 5. 磁盘告警

- 部署脚本已装 cron：每小时跑 `04-execution/bin/disk_alert.sh`，/data ≥80% 时写入 `04-execution/logs/disk_alert.log`。
- 需要推送到微信/钉钉：编辑该脚本，取消 Webhook 段注释并填入地址。
- 处理动作：跑第 3 节删除废弃镜像 + gc.sh；或 `docker system prune -a` 清理服务器本机无用镜像（不影响仓库数据）。

## 6. 华为云扣费监控对接提示

- 本仓库跑在自有鲲鹏机器上，**本身不产生华为云费用**；费用风险只来自：① 若机器是华为云 ECS（按需计费/流量费）；② 安全组误开公网导致流量费。
- 建议在华为云控制台「费用中心 → 预算管理」创建月度预算并绑定短信/邮件告警（阈值建议设为历史月均的 120%）。
- [快速链接: 华为云预算管理文档] 在华为云控制台搜索「预算管理」或访问费用中心官方文档页。
- 安全组核查：入方向 5000 端口来源必须是内网 CIDR（如 192.168.0.0/16），禁止 0.0.0.0/0。

## 7. 账号密码管理

```bash
# 新增/修改用户（改完重启容器生效）
docker run --rm --entrypoint htpasswd httpd:2.4-alpine -Bbn 新用户名 '新密码' \
  >> /data/longhun-registry/02-identity/auth/htpasswd
docker restart longhun-registry
```
