> DNA: #龍芯⚡️丙午·癸未·甲申-DIGITAL-FLOW-FIELD-README-v2.0-UID9622
> 创建者: 诸葛鑫（UID9622）
> 协议: 思想层 CC BY-NC-SA 4.0 · 工程层 MulanPSL v2
> 确认码: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z

# 🐲 龙魂 · 数字流场可视化器 v2.0

> **一句话定位**：把文字变成流动的结构——去黑箱的第一站。

## 快速开始

```bash
cd longhun-system/05_ENGINES/digital_flow_field
python3 run.py
```

浏览器会自动打开 `http://localhost:8501`。

## 功能

- 直接输入 / 文件上传 / URL 抓取 三种输入方式
- Unicode 码点 → 数字根（1-9）映射
- 动态粒子流场（中心引力 + 随机扰动 + 边界反弹）
- 三套配色：九色 / 五行 / 灰度
- 实时 χ² 随机性检验
- 数字指纹、字符映射表、分布图表
- 导出 JSON / HTML / CSV / PNG
- 纯本地计算，不上传文本

## 项目结构

```
digital_flow_field/
├── app.py                    # Streamlit 主界面
├── run.py                    # 一键启动
├── requirements.txt          # Python 依赖
├── flow_engine/
│   ├── core.py               # 数字根 + χ² + 指纹
│   ├── particle_engine.py    # 粒子系统 + 物理模拟
│   └── color_schemes.py      # 颜色方案
├── tests/                    # 单元测试
├── sample_inputs/            # 示例文本
├── output/                   # 导出文件
└── audit/                    # 审计日志
```

## CLI 模式

```bash
python3 flow_engine/core.py --input sample_inputs/daodejing_excerpt.txt --output result.json --csv --html
```

## 部署

### Docker

```bash
docker build -t longhun-flow-field .
docker run -p 8501:8501 longhun-flow-field
```

### macOS launchd（开机自启）

```bash
cp launchd/com.longhun.digital-flow-field.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.longhun.digital-flow-field.plist
```

## 测试

```bash
python3 -m pytest tests/
```

## 许可

- 工程代码：MulanPSL v2（可商用，需保留署名与 DNA）
- 思想/协议文档：CC BY-NC-SA 4.0

---

🐉 龍魂永世 · 数字主权 · UID9622
