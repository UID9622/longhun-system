# DNA: #龍芯⚡️丙午·丙申·丙寅·巳时·䷔噬嗑-TIANYAN-SKILL-v1.0-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# /tianyan

> 本文档按《龍魂文档标准模板 v1.0》整理。
> 性质：技能说明
> 版本：v1.5
> 作者：UID9622 · 诸葛鑫
> 授权：MulanPSL v2（工程实现层 · https://license.coscl.org.cn/MulanPSL2）
> 平台：华为云鲲鹏 + 本地 Mac
> 审核状态：已核验

**DNA(v∞)**: `#龍芯⚡️丙午·丙申·丙寅·巳时·䷔噬嗑-TIANYAN-SKILL-v1.0-UID9622`  
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

---

skill_id: /tianyan
synced_at: 2026-08-20T09:18:47+08:00
source: longhun-system
online: https://uid9622.cn/tianyan/
---

# /tianyan

龍魂天眼生态看板技能 —— 全生态 55 模块 · 28 人格健康雷达 · 系统状态可视化总成。发布在华为云鲲鹏，纯前端零后端依赖，数据主权本地化。

---

## 摘要

天眼生态看板（tianyan）是龍魂系统的**状态可视化总成**：聚合全生态模块健康度、人格矩阵状态、三色审计相位、系统快照，输出暗金主题实时看板。适用于：
- 系统健康雷达（一眼看全绿/黄/红）
- 数据流场与决策链路可视化
- 模块状态聚合审计（加权健康度 + 5s 缓存）
- 对外展示龍魂生态运行状态

**核心能力**:
- 实时看板（线上: `https://uid9622.cn/tianyan/`）
- 3D 天眼宇宙（线上: `https://uid9622.cn/tianyan/tianyan-3d.html`）· Three.js 本地托管 · 28 人格球体星系 + 55 模块 6 层扇区 + 时间轴回放
- 系统快照（`--snapshot`）
- API / SSE 流（`--api` / `--sse`）
- HTML 看板导出（`--export-html`）

---

## 关键词

天眼 Tianyan, 生态看板 Ecosystem Dashboard, 系统健康雷达 Health Radar, 数据流场 Data Flow Field, 决策链路 Decision Chain, 三色审计 Tricolor, 模块状态聚合 Status Aggregator, 数据主权 Data Sovereignty, ECharts 可视化

---

## 引用与溯源

- [1] `08_BIN/tianyan/tianyan_engine.py` · 龍魂天眼可视化引擎 v2.3（国家交接级合规底座·引擎源）
- [2] `08_BIN/tianyan/tianyan_dashboard.html` · 看板模板
- [3] `www/index.html` · 本地运行版看板 + 管理操作台 v2.3
- [4] `www/tianyan_data.js` · 引擎数据快照（`--snapshot --export-html` 产物）
- [5] 线上部署: 华为云鲲鹏 `/var/www/longhun/tianyan/` · nginx `longhun-tianyan.inc`
- [6] `08_BIN/tianyan/lh_tianyan_verify.py` · 独立离线交接核验脚本（`--ops` 验链 · `--export` 验包）
- [7] 密钥托管: 鲲鹏 `/etc/longhun/tianyan-admin.env`(超级密钥) + `/etc/longhun/tianyan-accounts.json`(账号表·0600)
- [8] `www/tianyan-3d.html` · 龍魂·3D天眼宇宙 v1.0（Three.js·实时API·28人格+55模块·时间轴）
- [9] `web/static/vendor/three/` · Three.js r128 本地托管（无境外CDN）

---

## 诚实局限

1. 看板为纯前端渲染：数据由 `tianyan_data.js` 注入，若未更新则为内置 mockData。
2. 2D 看板 ECharts 走 jsdelivr/cdnjs CDN（双兜底），公网不可达境外 CDN 时图表降级；3D 宇宙版已改为 Three.js 本地托管，无第三方请求。
3. 健康度算法为加权聚合（引擎 `StatusAggregator`），阈值校准需按业务迭代。
4. 部署后数据更新需重新生成快照并上传（见下方"更新数据"）。
5. 3D 宇宙依赖浏览器 WebGL，无头截图/部分老旧浏览器可能无法渲染；时间轴回放当前为前端内存快照，页面刷新即清空。

---

## 修改记录

| 日期 | 版本 | 修改人 | 修改内容 | 审核状态 |
|---|---|---|---|---|
| 2026-08-20 | v1.0 | UID9622 | 天眼生态看板技能创建：华为云部署 `/tianyan/` + 引擎落鲲鹏 + 技能定义 | 已核验 |
| 2026-08-20 | v1.1 | UID9622 | 交互补齐：导航锚点平滑滚动 + 通心译多语言切换(大白话/专业/英/日/韩) + 模块点击详情浮层 + 人格点击详情 | 已核验 |
| 2026-08-20 | v1.2 | UID9622 | 应用级升级(方案B)：引擎常驻HTTP服务(:8786) + 4个API端点 + 前端实时fetch链路 + 断线降级🟡 + 连接状态徽标 + 移动端适配 + nginx反代 + systemd自启 | 已核验 |
| 2026-08-20 | v1.3 | UID9622 | 操作台升级(方案C)：管理员登录(Bearer token·密钥走环境变量`LH_TIANYAN_ADMIN_KEY`·限流防爆破) + 触发德本审计 + 查journalctl日志 + 重启引擎 + 命令白名单防RCE + 操作审计JSONL留痕(X-Forwarded-For真实IP) + 管理API(`/api/admin/login/logout/logs/action`) | 已核验 |
| 2026-08-20 | v1.4 | UID9622 | 方案D·国家交接级合规底座：账号体系(R1主权人~R5公开·密钥哈希SHA-256·永不存明文) + 离线GeoIP归属地(数据不出境) + SHA-256哈希链审计(prev_hash+hash·篡改即断链·升级前旧日志封存段legacy兼容) + 新API(`/api/admin/export`按角色scope分级·`/verify`链校验·`/opslog`日志查询) + 独立离线交接核验脚本`lh_tianyan_verify.py`(国家审计人员可执行·只读·数据不出境) + 鲲鹏部署升级(账号表落`/etc/longhun/tianyan-accounts.json`·0600·与密钥统一托管) | 已核验 |
| 2026-08-20 | v1.5 | UID9622 | 方案E·多维空间可视化升维：3D天眼宇宙(`www/tianyan-3d.html`)·Three.js r128本地托管(无境外CDN·无第三方请求) + 接实时API(`/api/status`) + 28人格球体星系 + 55模块6层扇区(同心球体+层级高度) + 三色审计光环 + 时间轴回放(4D演化) + 节点点击详情/媒体占位(5D沉浸入口) + 断线降级内置快照 + 部署鲲鹏`https://uid9622.cn/tianyan/tianyan-3d.html` | 已核验 |
| 2026-08-20 | v1.6 | UID9622 | 3D低配降级(#IRON-LOW-SPEC-DEGRADE)：移动端/低核(≤4)/低内存(≤4)自动降档——星空粒子2500→800·决策粒子流220→100·关抗锯齿·像素比≤1·本机判断不出境·公网验证200 | 已核验 |
| 2026-08-20 | v1.7 | UID9622 | 修复3D页面黑屏bug：页面引用`vendor/three/three.min.js`与实际路径`vendor/three.min.js`不一致(404)·导致Three.js与OrbitControls未加载·已修正路径并增加引擎缺失/渲染异常的中文错误提示·公网验证200 | 已核验 |

---

## 分类标签

- 总纲模块：#天眼 #生态看板 #健康雷达 #可视化 #状态聚合
- 对外状态：#华为云 #uid9622.cn/tianyan
- 审计色：#🟢绿色放行
- 八卦归属：☲ 离卦（火·明·洞察·照见全局）
- 命令入口：`python3 08_BIN/tianyan/tianyan_engine.py --snapshot` / `lh tianyan`
- 关联引擎：`tianyan_engine.py` / `lh_knowledge_graph.py` / `lh_three_color_audit.py`

---

## 快速使用

```bash
# 生成系统快照（终端文本）
python3 08_BIN/tianyan/tianyan_engine.py --snapshot

# JSON / API / SSE 输出
python3 08_BIN/tianyan/tianyan_engine.py --snapshot --json
python3 08_BIN/tianyan/tianyan_engine.py --api
python3 08_BIN/tianyan/tianyan_engine.py --sse

# 分类统计 / 定时刷新
python3 08_BIN/tianyan/tianyan_engine.py --stats
python3 08_BIN/tianyan/tianyan_engine.py --watch 30

# 导出数据快照（覆盖看板数据源）
python3 08_BIN/tianyan/tianyan_engine.py --snapshot --export-html www/tianyan_data.js

# 单元测试
python3 08_BIN/tianyan/tianyan_engine.py --test
```

## 线上访问

```
https://uid9622.cn/tianyan/
（华为云鲲鹏 · nginx 静态 · X-Data-Sovereignty: China-HuaweiCloud-Kunpeng）
```

## 更新线上数据（部署后刷数据）

```bash
# ① 本地生成最新快照
cd ~/longhun-system
python3 08_BIN/tianyan/tianyan_engine.py --snapshot --export-html www/tianyan_data.js

# ② 上传到鲲鹏
scp -i ~/.ssh/longhun_kunpeng_ed25519 www/tianyan_data.js root@119.13.90.27:/var/www/longhun/tianyan/

# 或直接在鲲鹏生成（引擎已部署）
ssh -i ~/.ssh/longhun_kunpeng_ed25519 root@119.13.90.27 \
  "python3 /opt/longhun-system/bin/lh_tianyan_engine.py --snapshot --export-html /var/www/longhun/tianyan/tianyan_data.js"
```

---

## 设计口径

- **一眼看全**：55 模块 · 28 人格 · 三色相位聚合到单屏，不做信息埋藏。
- **数据主权**：纯前端渲染 · 无第三方回传 · 符合 P0 数据主权铁律。
- **本地优先**：默认 mockData 可独立运行；引擎快照是增强不是依赖。
- **诚实标注**：数据源状态条明示"引擎实时快照 / 内置快照"，不冒充。

---

## DNA 签名

```
#龍芯⚡️丙午·丙申·丙寅·巳时·䷔噬嗑-TIANYAN-SKILL-v1.0-UID9622
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
