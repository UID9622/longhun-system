# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 🐉 龍魂内网 · 设备加入指南
# DNA: #龍芯⚡️丙午·辛未·乙酉·申时·䷾既济-JOIN-GUIDE-v1.0

> 网关地址: http://192.168.1.10:9622
> 前提: 设备和Mac在同一局域网

## Mac加入
```bash
curl -s http://192.168.1.10:9622/health  # 验证连通
python3 ~/longhun-system/deploy/scripts/longhun-internal-net/longhun-peer-client.py "设备名" mac 192.168.1.10
```

## Windows加入
```powershell
# 1. 安装Python3 https://python.org
# 2. 下载peer-client.py到本地
curl -o peer-client.py http://192.168.1.10:9622/peers/client
# 3. 运行
python peer-client.py "Win办公机" win 192.168.1.10
```

## Linux/树莓派加入
```bash
curl -s http://192.168.1.10:9622/health
python3 peer-client.py "Linux开发机" linux 192.168.1.10
```

## 手机加入
浏览器访问: http://192.168.1.10:8445
(Web门户自适应移动端)

## 验证
```bash
curl http://192.168.1.10:9622/peers  # 查看所有在线设备
```
