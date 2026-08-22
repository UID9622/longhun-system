# 龍魂·真实性标识协议模块 · 云码接入说明

DNA: #龍芯⚡️丙午·乙未·丁未·丙午·䷫姤-云码接入-V1.0
归属: 龍魂系统 UID9622 · 免费开源 · 零黑箱

## 模块清单
| 文件 | 功能 | 状态 |
|---|---|---|
| index.html | 协议规范 + 知识图谱原型 + 脚本标注器 | 完整可用 |
| tagger.html | M1 批量打标器（规则引擎+AI复核接口） | 可用，AI 复核为 STUB |
| pipeline.html | M2 视频流水线接口层（分镜 JSON 已焊死格式） | 可用，视频引擎为 STUB |
| embed.html | M3 官网嵌入卡片（iframe 进 longhun888.com / uid9622.cn） | 完整可用 |
| js/lh_interface.js | **唯一接口适配层** | STUB/LOCAL 双模式 |
| deploy/deploy_kunpeng.sh | 鲲鹏部署脚本 | 待本地执行 |

## 云码接管步骤（总共改 1 行 + 起 3 个端点）
1. `bash deploy/deploy_kunpeng.sh` 部署到鲲鹏
2. 在龍魂 FastAPI 操作台（127.0.0.1:9527）实现 4 个端点：
   - `POST /api/v1/truth/judge` — 入参 `{text}`，出参 `{tag, score, by}`（AI 复核打标）
   - `POST /api/v1/truth/video` — 入参分镜 JSON（见 pipeline.html 导出格式），出参 `{job_id, status}`（接数字人/龍音ASR/视频生成）
   - `POST /api/v1/truth/graph` — 入参图谱 JSON，接龍魂知识图谱模块入库
   - `POST /api/v1/dna/sign` — 调 `bin/lh_dna_generator.py`，返回正式 DNA 追溯码
3. 改 `js/lh_interface.js` 第 20 行：`MODE: 'STUB'` → `MODE: 'LOCAL'`

## 焊死约束（云码不可改）
- 角标常驻每镜，禁止仅片头声明（P3-1）
- 声称「实」无来源 → 自动降级「疑」（P3-3）
- 无标签 → 默认「疑」（P0）
- 不删除只冻结：改标/纠错一律追加记录，不改写历史
- DNA 干支四柱+卦名一律以本地生成器输出为准，禁止手写
