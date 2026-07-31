# plan_safeai.md — 龍魂最安全AI · 上下文安全引擎落地

## 目标
把"最安全的AI"从宣言变成可执行系统：
- 不用拦截词库（关键词拦截=黑箱+误伤），用**上下文意图判定 + 七因子行为密码学 + P0–P4分层治理**
- 该松的松：善意学习→概念解释+风险提示+合规边界
- 该紧的紧：恶意请求→拒绝可执行细节，转向防护/法律后果/求助渠道
- 全程DNA追溯、不删除只冻结、零黑箱（每个判定给出可审计理由）

## Stage 1 — 设计+编码（vibecoding-general-swarm，1个coder子代理）
输出 /mnt/agents/output/longhun-safe-ai/ ：
1. `longhun_safe_engine_v1.0.py` — 核心引擎：
   - IntentClassifier：上下文意图分类（善意学习/灰色/恶意），不依赖关键词表
   - SevenFactorAudit：F1–F7行为密码学审计（复用KFPP七因子框架）
   - P0P4Governor：P0–P4分层裁决（该松的松/该紧的紧）
   - DNATrace：干支时间戳DNA链，只追加不删除
   - 判定结果必须输出：级别+触发因子+可审计理由+申诉入口（零黑箱）
2. `config/p0_p4_rules.yaml` — P0–P4规则配置（可审计、可调，P0不可改）
3. `tests/` — 测试用例（善意请求放行/恶意请求熔断/灰色转向 各≥5例）
4. `README.md` — 部署说明（本地部署、数据不出户）
5. `SAFETY_PROTOCOL_v1.0.md` — 安全协议文档（新格式DNA，可发布版）

## Stage 2 — 验证
运行测试全部通过，实测三类请求各跑一遍出结果

## Stage 3 — 交付
打包 + 发布说明（Gitee/GitHub开源发布步骤）
