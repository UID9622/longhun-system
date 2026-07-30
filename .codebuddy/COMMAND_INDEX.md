# 龍魂·命令总目 · Command Index

> 🔴 **真实入口在鲲鹏！** `https://uid9622.cn/api/cmd/` → 所有国产AI统一查询
> 📋 **本地副本**（方便离线使用）· 新增/修改脚本 → AI同步更新鲲鹏 + 此处
> 🔗 API端点: `/api/cmd`(JSON) · `/api/cmd/quick`(速查) · `/api/cmd/search?q=`(搜索) · `/api/cmd/ports`(端口) · `/api/cmd/index.md`(Markdown)
> 📌 原则：鲲鹏是唯一真相来源，Notion是镜像，本地是备份
> 📌 更新: 2026-07-29 v1.2 | DNA: #龍芯⚡️丙午·癸未·丁未-COMMAND-INDEX-v1.2-VISUAL

---

## ⚡ 三秒速查

| 干什么 | 命令 | 备注 |
|:---|:---|:---|
| 进菜单 | `lh` | 交互控制台，8大类 |
| 搜 | `lh search "关键词"` | Bing→缓存→审计 |
| 做视频 | `lh video --script 稿.txt` | v3.0·AI配图 |
| 做3D | `lh 3d --input 图.png` | 图生三维 |
| 验主权 | `python3 bin/lh_verify 视频.mp4` | DNA盲水印提取·公开可用 |
| 看状态 | `lh status` | 模型Val·引擎·告警 |
| 审计 | `lh audit` | 全系统安全 |
| 签名 | `python3 bin/lh_gpg_sign.py sign .` | GPG分离签名 |
| 推远端 | `python3 bin/lh_auto_cannon.py` | GitHub+Gitee+GitCode |
| 同步鲲鹏 | `bash deploy/sync-to-kunpeng.sh` | → 119.13.90.27 |
| SSH鲲鹏 | `ssh -i ~/.ssh/longhun_kunpeng_ed25519 root@119.13.90.27` | 密钥优先 |

---

## 📂 分类索引

### 🎛️ 日常交互
```
lh                          # 交互控制台（8大类菜单）
lh --dashboard              # 人格仪表盘
lh --audit                  # 一键审计
lh --push                   # 推远端
lh --health                 # 引擎健康
lh --console                # Web操作台
```

### 🔍 搜索 & 知识
```
lh search "关键词"           # → bin/lh_search_engine.py
```

### 🎬 多媒体
```
lh video --script 稿.txt     # → bin/lh_video_studio.py
lh video --list              # → bin/lh_video_index.py
lh 3d --input 图.png         # → bin/lh_3d_pipeline.py

# 主权验证（公开可用·任何人可验）
python3 bin/lh_verify 视频.mp4            # 提取DNA盲水印
python3 bin/lh_verify *.mp4 --json        # JSON格式·批量验证
python3 bin/lh_verify 视频.mp4 --quiet    # 静默模式（返回退出码）

# 高级视频（真声+增强）
lh video --script 稿.txt --voice uid9622 --enhance nano --name "标题"

# 蚁群可视化视频
python3 engines/lh_ant_colony_visual.py full -d ants/
# → 然后 lh video --script ants/ant_narration.txt --voice uid9622

# 人格协作视频
python3 engines/lh_persona_orchestra_visual.py full -d personas/
# → 然后 lh video --script personas/persona_narration.txt --voice uid9622
```

### 🎨 视觉引擎群（新增·v4.1.5）
```
# 纳米视觉超分辨率增强
python3 engines/lh_nano_vision_engine.py enhance -i lowres.png -s 4 -o highres.png
python3 engines/lh_nano_vision_engine.py info     # 引擎信息

# 蚁群分布可视化（4图）
python3 engines/lh_ant_colony_visual.py topo      # 蚁后-工蚁拓扑
python3 engines/lh_ant_colony_visual.py heatmap   # 信息素热力
python3 engines/lh_ant_colony_visual.py dashboard # 涌现仪表盘
python3 engines/lh_ant_colony_visual.py narrate   # 解说词

# 人格协作可视化（5图）
python3 engines/lh_persona_orchestra_visual.py heatmap  # 20x20权重热力
python3 engines/lh_persona_orchestra_visual.py graph    # 协作力导向图
python3 engines/lh_persona_orchestra_visual.py audit    # 审计链路
python3 engines/lh_persona_orchestra_visual.py pie      # 四层饼图
python3 engines/lh_persona_orchestra_visual.py narrate  # 解说词

# 系统健康全景图
python3 engines/lh_system_health_panorama.py panorama  # 九宫格全景图
python3 engines/lh_system_health_panorama.py report    # 文本报告
python3 engines/lh_system_health_panorama.py narrate   # 解说词
```

### 🛡️ 审计 & 安全
```
lh audit                     # → bin/lh_full_system_audit.py
python3 bin/lh_deben_audit.py scan    # 德本五问
python3 bin/lh_memory_load.py         # 焊死记忆加载
python3 bin/lh_system_eval.py         # 健康评分
python3 bin/lh_self-heal.py           # 自助修复
python3 bin/longhun_self_check_v1.0.py # 系统自检
python3 bin/lh_align_checker.py       # 🔥对齐复盘·重复函数·缺失DNA·缺失GPG
```

**黑箱审计协议**（P1·v2.0·AI输出五层校验）：
- 协议: `01_protocols/LH-PROMPT-BLACKBOX-AUDIT-v2.0.md`
- 坑位: `01_protocols/LH-BLACKBOX-PITFALLS-v1.0.md`（10坑·3致命/4高危）
- Manifest: `01_protocols/LH-BLACKBOX-AUDIT-MANIFEST-v2.0.json`

### ✍️ GPG 签名 (🔥焊死)
```
python3 bin/lh_gpg_sign.py sign <路径>      # 签名
python3 bin/lh_gpg_sign.py sign --force .   # 强制全签
python3 bin/lh_gpg_sign.py verify <文件>    # 验证
python3 bin/lh_gpg_sign.py scan <目录>      # 扫描未签名
```
密钥: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`

### 🛡️ 反詐·彎彎繞繞檢測（新增·v3.0）
```
# 綜合分析（默認·推薦）
python3 bin/lh_anti_fraud_detector.py analyze -t "要分析的文字"

# 彎繞指數
python3 bin/lh_anti_fraud_detector.py wind -t "文字"

# 綜合風險評分
python3 bin/lh_anti_fraud_detector.py score -t "文字"

# 生成反制話術
python3 bin/lh_anti_fraud_detector.py counter -t "對方的話術"

# 批量檢測（每行一條）
python3 bin/lh_anti_fraud_detector.py batch -f comments.txt

# 場景模式
python3 bin/lh_anti_fraud_detector.py analyze -t "..." -c douyin_live
python3 bin/lh_anti_fraud_detector.py analyze -t "..." -c wechat
```
模式庫: `data/anti_fraud_patterns_v3.0.json` (14維度·彎彎繞繞原理)
協議: `01_protocols/LH-BEHAVIOR-CRYPTOGRAPHY-ANTI-FRAUD-v1.0.md`
民間手冊: `01_protocols/LH-ANTI-FRAUD-QUICK-GUIDE-v1.0.md`

### 🚀 部署 & 同步
```
bash deploy/sync-to-kunpeng.sh              # 代码同步鲲鹏
bash deploy/deploy-now.sh                   # 一键部署
bash deploy/scripts/health_check.sh         # 鲲鹏健康检查(Bark)
bash deploy/scripts/monitor_setup.sh        # systemd+监控
python3 bin/lh_auto_cannon.py               # Git全量推送
```

### 🌐 网络限流应对（`bin/lh_network/`）
```
bash bin/lh_network/05_network_fix_all.sh      # 一键检测+修复限流
bash bin/lh_network/01_hk_proxy_setup.sh       # 华为云香港代理部署（首次配置）
bash bin/lh_network/02_auto_proxy.sh           # 终端自动检测限流+切换代理
bash bin/lh_network/03_model_download_mirror.sh # 模型下载国内镜像配置
bash bin/lh_network/04_kunpeng_offline.sh      # 鲲鹏离线节点配置
```
三层防御: 本地v4.0(离线推理) → 香港代理(SOCKS5) → 国内镜像(hf-mirror.com) → 鲲鹏离线(终极兜底)

### 🧠 模型训练
```
python3 bin/lh_lora_trainer_v4.py           # MLX LoRA训练
python3 bin/lh_download_v40_bases.py        # 数据拉取
ollama run longhun-v3.7                     # 主力模型(Qwen2.5-1.5B)
ollama run longhun-v4.0                     # 新底座(Llama-3.1-8B)
```

### 📊 记忆 & 日志
```
lh memory --today                           # 今日执行日志
lh memory --summary                         # 记忆层统计
lh logs --tail 20                           # 聚合日志
```

### 🔧 运维
```
bash bin/start_all.sh                       # 一键启动所有服务
bash bin/refresh-longhun.sh                 # 刷新龍魂环境
lh schedule list                            # 定时任务
lh web                                      # 仪表盘 → :9630
```

---

## 🔌 服务端口

| 端口 | 服务 | 位置 |
|:---:|:---|:---:|
| 9625 | 纳米视觉API | 鲲鹏 |
| 9630 | Web仪表盘 | Mac |
| 9631 | 搜索引擎 | Mac |
| 9636 | 健康全景API | 鲲鹏 |
| 8766 | 知识中枢 | Mac |
| 8771 | 统一记忆 | Mac |
| 8773 | 统一记忆 | 鲲鹏 |
| 8781 | 军团指挥 | Mac |
| 8788 | 视频画廊 | Mac |
| 8899 | 价格审计 | Mac |

---

## 📝 更新日志（增量追加·不覆盖）

| 2026-07-30 | v1.4 | 网络限流应对方案v1.0入库·6文件·部署区新增🌐网络限流应对 | AI |
| 2026-07-30 | v1.3 | 黑箱审计协议v2.0入库·3文件·审计安全区新增黑箱审计协议+坑位分析 | AI |

| 日期 | 变更 | 影响命令 |
|:---|:---|:---|
| 2026-07-29 | 视觉引擎群 v4.1.5上线 | 纳米视觉·蚁群可视化·人格可视化·健康全景 |
| 2026-07-29 | 鲲鹏部署2个新API服务 | :9625(纳米视觉) :9636(健康全景) |
| 2026-07-28 | 命令总目 v1.1 迁至鲲鹏统一入口 | 全部 |
| 2026-07-28 | 鲲鹏API上线: /api/cmd/* | cmd_routes.py |
| 2026-07-28 | GPG签名引擎上线 | `lh_gpg_sign.py` |
| 2026-07-28 | 创建命令总目 v1.0 | 全部 |
