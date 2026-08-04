# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 鲲鹏部署·一键就绪卡片
# DNA: #龍芯⚡️丙午·辛未·乙酉·申时·䷾既济-KUNPENG-READY-v1.0

## 前置条件
- [ ] 物理开机 + 插网线
- [ ] SSH 可用 (root@119.13.90.27)
- [ ] Mac已配好SSH密钥

## 执行（SSH连上鲲鹏后）
```bash
# 1. 上传部署包
scp -r /Users/zuimeidedeyihan/longhun-system/deploy root@119.13.90.27:/data/

# 2. SSH进入
ssh root@119.13.90.27

# 3. 一键部署
bash /data/deploy/scripts/deploy_kunpeng_perfect.sh

# 4. 部署监控
bash /data/deploy/scripts/monitor_setup.sh

# 5. 验证
curl http://localhost:9622/health
```

## 部署后Mac端操作
```bash
# 注册鲲鹏到内网
curl -X POST http://119.13.90.27:9622/register \
  -H 'Content-Type: application/json' \
  -d '{"id":"kunpeng-center","name":"鲲鹏中心","type":"kunpeng","ip":"119.13.90.27"}'
```

## 预期结果
| 端口 | 服务 |
|:---|:---|
| 9622 | 内网网关(主) |
| 9623 | 注册中心 |
| 8766 | AutoFlow引擎 |
| 8445 | Web门户 |
