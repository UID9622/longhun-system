# S3 · AutoDL 7B SFT 部署包（Qwen2.5-7B-Instruct · 词表增量 + LoRA）

**DNA**: `#龍芯⚡️丙午·丁酉·癸未·未时·䷚颐-S3-AUTODL-SETUP-V0.1-UID9622`
**归属名:** 诸葛鑫 | UID9622 · 龍芯北辰
**License:** MulanPSL v2 (https://license.coscl.org.cn/MulanPSL2)
**父任务:** D-01 Step3（AutoDL 7B 正式批次·S2 前置已过：本地管线🟢 S2-A/S2-C）

> 本包在老大 AutoDL 开户**之前**写好，实例开通后照 README 跑，不临时写。
> 诚实口径：所有时长/显存为**推演级**（防空壳·未在 AutoDL 实测），实例开通冒烟后以实测更新。

---

## 一、角色与卡型（防空壳：3060 ≠ 正式训练卡）

| 卡型 | 显存 | 单价 | ¥50 可跑 | 本包定位 |
|:---|:---:|:---:|:---:|:---|
| RTX4090 | 24G | ~¥2.38/h | ~21h | 🟢 **正式含词表增量训练**（推荐） |
| RTX3060 | 12G | ~¥0.86/h | ~58h | 🟡 冒烟+小步验证（7B+emb 增量在 12G 很挤·如实标） |

> 依据 D-01 路由文档：3060=推理够用·4090=训练主推。老大收条里"3060 跑 4-6h"未实测，不采信为承诺。

## 二、前置（老大做三步·完成后报 IP 与卡型）

1. AutoDL 注册+实名 https://www.autodl.com
2. 充值 ¥50
3. 控制台→SSH 管理→添加公钥：本地 `cat ~/.ssh/id_ed25519_uid9622.pub`
4. **回报 AI**：实例 IP、SSH 端口（非 22）、卡型（4090/3060）

## 三、本地上传物（开跑前一次性 scp 三批）

```bash
# ① S1 词表迁移产物(README 后端 sft 脚本用·vocab 151832)
scp -P <port> \
  models/base_models_v4.0/Qwen2.5-7B-Instruct/tokenizer_longhun.json \
  models/base_models_v4.0/Qwen2.5-7B-Instruct/tokenizer_longhun_report.json \
  root@<ip>:/root/autodl-tmp/s3_upload/

# ② 本部署包(setup/run/sft_7b.py/README·即 deploy/autodl_s3/)
scp -P <port> -r deploy/autodl_s3/. root@<ip>:/root/autodl-tmp/s3_upload/

# ③ 训练数据 train.jsonl+valid.jsonl(与本地 corpus 同格式·现役 881+98 可先冒烟)
scp -P <port> -r models/longhun-v1.0/lora_output/data root@<ip>:/root/autodl-tmp/s3_upload/data
```
产物出处：S1 词表迁移 v1.1（Qwen2.5 vocab 151643 → **151832**·181 词注入·SHA256 49d499d4·报告 articles/2026-09-06-D01-S1-词表迁移报告-v1.0.md）
> 正式批次数据=S4 语料扩源后 corpus 生成(先本地跑 S2-C 同款校验再上传)，881+98 仅为冒烟用。

## 四、步骤（先 setup → 再 run）

```bash
# 1) 环境初始化（镜像/依赖/权重拉取/tokenizer 覆盖）
bash setup_autodl.sh <IP或空>

# 2) 训练（卡型自动/手动模板）
bash run_sft_7b.sh 4090    # 或 3060（冒烟级·见脚本注释）
```

## 五、显存/超参模板（诚实口径·推演级）

| 项 | 4090 24G | 3060 12G |
|:---|:---|:---|
| 精度 | 4bit qlora + bf16 | 4bit qlora（仅冒烟 5min） |
| LoRA rank/alpha | 32/64 | 16/32 |
| emb 增量训练 | ✅ modules_to_save=embed_tokens,lm_head | ❌ 冻结（12G 装不下全 emb 梯度） |
| batch/grad_accum | 2 / 8 | 1 / 4 |
| 优化器 | paged_adamw_8bit | paged_adamw_8bit |
| 预计时长(1epoch) | 推演 2-5h（语料扩源后看量） | 仅验证用 |

> **emb 增量是 S1 词表迁移的价值所在（新 181 词 embedding 须真训），故正式批次必须 4090。**
> 3060 的价值=¥0 级别先证"远端 Linux 栈可复现本地结果"，不冒充正式训练。

## 六、训练数据（何时扩源）

- 当前 corpus 32K（偏小）→ 语料扩源（S4）完成后先跑 S2-C 同款本地全量校验，再传 AutoDL
- 数据文件：`train.jsonl/valid.jsonl`（行支持 `messages`/`prompt+response`/`instruction`/`text`(扩源文本块·全序列续训)·sft_7b.py 逐行分型可混）
- AutoDL 端路径 `/root/autodl-tmp/s3_upload/data/`

## 七、验收口径（与本地 S2-C 同秤不可直比·如实）

- 🟢 验收1：远端训练 loss 曲线下降（train 与 val 双通道后段<前段）
- 🟡 验收2：7B Val 与本地 1.5B(0.979) 不同秤，**不可直比**；正式等效判定=Val<0.2/召回≥90%/漂移≥80%（D-01 判定标准·待 S3 实跑）
- 🟢 验收3：tokenizer 注入词可解码（`tokenizer_longhun_report.json` 抽查）

## 八、防错清单

- [ ] AutoDL 镜像选带 CUDA 的 PyTorch 镜像（`setup_autodl.sh` 已处理）
- [ ] 权重拉取走 hf-mirror（国内网络直连 HF 会断）→ 脚本已 export HF_ENDPOINT
- [ ] tokenizer 覆盖前备份原 tokenizer.json
- [ ] 关闭实例前 `autosave`/结果回传本地（scp 回来）
- [ ] 计费确认：关机才停计费·¥50 预算提醒

---
**三色**: 🟢 脚本包+上传物清单就绪（本地实机未跑·AutoDL 待实例）· 🟡 时长/显存推演级 · 🔴 0
