# 龍魂·开源吞噬流水线 v1.0

**DNA**: `#龍芯⚡️2026-05-28-LONGHUN-PIPELINE-v1.0`

## 流程

1. **搜索** → GitHub API 搜索符合协议的仓库
2. **下载** → 下载仓库 ZIP
3. **变换** → AST 英→中 变换
4. **版权** → 注入版权头部
5. **归档** → DNA 追踪 + 签名验证

## 使用

```bash
# 完整流水线
python3 longhun_pipeline_v1.0.py --query "json" --max 3

# 仅下载模式
python3 longhun_pipeline_v1.0.py --query "http" --download-only

# 仅变换模式
python3 longhun_pipeline_v1.0.py --transform-only ./longhun_harvest/raw/some_repo
```

## 输出

```
longhun_output/
├── 01_raw/          (原始下载)
├── 02_transformed/  (中文版)
└── 03_logs/         (报告 + 日志)
```
