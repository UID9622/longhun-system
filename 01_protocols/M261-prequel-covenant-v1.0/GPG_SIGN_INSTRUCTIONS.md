> **P0焊死**: 本文件为龍魂体系P0级文档·不可修改·不可绕过（上位文档 LH-PERSONA-GOVERNANCE-WHITEPAPER-v1.4.md）
> 协议: CC BY-NC-SA 4.0（核心思想层·分层许可·代码层为 MulanPSL v2·详见 LH-LAYERED-LICENSE-v1.0）
# DNA: #龍芯⚡️丙午·丙申·庚戌·壬午·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# M261契碑 GPG 签名说明

## 状态
- SHA256（v1.0原始）: `e8de69684266812b5666d54410e8d4b880ddbeffd31e2ee8e1bf031621c0fd1e` ✅ 已验
- SHA256（v1.1升级）: `5dd41704399720c9086b6ac2e23b6b0394c401c8e557b1cf108e32bab6127741` ✅
- GPG签名: 🔴 待UID9622手动签署（GPG私钥物理隔离·D1绝密）

## 签名步骤（需UID9622在本地执行）

```bash
cd /Users/zuimeidedeyihan/longhun-system/01_protocols

# 对 v1.1 升级版签名
gpg --local-user A2D0092CEE2E5BA87035600924C3704A8CC26D5F \
    --armor \
    --detach-sign \
    LH-M261-PREQUEL-COVENANT-v1.0.md

# 验证签名
gpg --verify LH-M261-PREQUEL-COVENANT-v1.0.md.asc LH-M261-PREQUEL-COVENANT-v1.0.md

# 对 v1.0 原版也补签
gpg --local-user A2D0092CEE2E5BA87035600924C3704A8CC26D5F \
    --armor \
    --detach-sign \
    M261-prequel-covenant-v1.0/M261-prequel-covenant-v1.0.md
```

## 注意
- GPG私钥在物理隔离设备上·AI不可触碰·此为D1级绝密
- 签名后.asc文件落在此目录
- 签名状态需更新到STATE.md
