# DNA: #龍芯⚡️丙午·丙申·庚戌·䷙大畜-SCRIPT-MANAGER-v1.2-UID9622
# CONFIRM: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
# SEAL: #ZHUGEXIN⚡️2025-🇨🇳🐉⚖️♠️🧚🏼‍♀️❤️♾️-DEVICE-BIND-SOUL
# 龍魂本地训练引擎 v1.1

**DNA**: `#龍芯⚡️2026-06-28-LONGHUN-TRAIN-v1.1`

不依赖 Ollama，不依赖任何第三方推理框架，纯 PyTorch + 本地语料，代码全部自己掌控。

## 目录结构

```
train/
├── data/raw/              # 手动 override 语料（可选）
├── data/processed/        # 自动收集的语料落在这里
├── src/
│   ├── config.py          # 所有超参数 + 自动收集目录配置
│   ├── collect_corpus.py  # 自动语料收集器
│   ├── tokenizer.py       # 字符级分词器（可替换）
│   ├── dataset.py         # 数据集
│   ├── model.py           # 龍魂 LM 模型结构
│   └── trainer.py         # 训练主程序
├── output/models/         # 训练好的模型 + 词表
├── scripts/train.sh       # 一键训练脚本
└── requirements.txt       # 最小依赖
```

## 使用方法

### 1. 安装依赖

```bash
cd ~/longhun-system/train
pip install -r requirements.txt
```

### 2. 一键训练（自动收集语料）

```bash
./scripts/train.sh
# 或
python3 src/trainer.py
```

训练前会自动扫描 `config.py` 里配置的目录，把 `.md`/`.txt` 收集到 `data/processed/auto_corpus/`，同时过滤密钥、`.env`、私密文件。

### 3. 手动追加语料（可选）

如果你想额外塞一些文件，直接丢进 `data/raw/`：

```bash
cp 你的额外语料.txt data/raw/
```

`data/raw/` 里的内容和自动收集的语料会一起训练。

### 4. 产出物

- `output/models/龍魂-0.1B.pt`：模型权重
- `output/models/龍魂-0.1B_tokenizer.json`：词表
- `output/龍魂-0.1B_train_report.json`：训练报告（含 DNA、参数量、loss 曲线）

## 自动收集目录（在 config.py 里改）

默认扫描：

- `~/longhun-system/01_protocols`
- `~/longhun-system/papers`
- `~/longhun-system/docs`
- `~/longhun-system/memory-universe`
- `~/longhun-system/skills`
- `~/longhun-system/06_技術文檔`

想加目录，直接改 `src/config.py` 里的 `auto_corpus_sources`。

## 可焊点

| 文件 | 可改内容 |
|---|---|
| `src/config.py` | 模型大小、学习率、轮数、序列长度、自动收集目录 |
| `src/tokenizer.py` | 换成 BPE / SentencePiece / CNSH 专用分词 |
| `src/model.py` | 把 LSTM 换成 Transformer、加 RoPE、RMSNorm、LoRA |
| `src/dataset.py` | 加数据清洗、去重、采样策略 |
| `src/trainer.py` | 加学习率调度、验证集、早停、分布式训练 |

## 君子协议

本训练引擎受龍魂 DNA 追溯保护。训练数据主权归 UID9622 所有，模型权重不出本地，未经授權不得对外发布。

---

> 人民数据主权 · 平台服务降级 · 龍魂自主可控
