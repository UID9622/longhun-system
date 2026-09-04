# 🐉 CNSH 多模态感知示例库 v1.0

> DNA: #龍芯⚡️丙午·丁酉·SENSE-CNSH-EXAMPLES-V1.0-UID9622
> 创建者: 诸葛鑫（UID9622）· 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 配套文档: docs/CNSH-多模态感知语法-v1.0.md（17条目·★9桥接/☆8草案）
> 生态: Motto · AV-Flamingo · PE-AV · SenseNova-MARS · Alpamayo-R1 · fusion-embedding

## 示例一览（4个·全部 cnsh run 可执行）

| # | 文件 | 借鉴开源 | 演示能力 | 草案语法 |
|---:|:---|:---|:---|:---|
| 1 | 1_视觉定位_借鉴Motto.cnsh | Motto（多模态定位） | 细粒度视觉定位判定 | 感知.定位(图片, 目标) -> 区域 |
| 2 | 2_音视频联合_借鉴AVFlamingo.cnsh | Audio-Visual Flamingo | 画面+音轨联合判定 | 感知.音视频(文件) -> 联合描述 |
| 3 | 3_多模态检索_借鉴PEAV.cnsh | PE-AV（统一嵌入） | 跨模态最近邻检索内核 | 多模态.检索(音频, 库) -> 匹配 |
| 4 | 4_感知决策执行_借鉴MARS.cnsh | SenseNova-MARS / Alpamayo-R1 | 三色决策→动作序列 | 决策.推理(结果) -> 动作 |

## 运行方式

```bash
# 纯 CNSH 运行（演示决策/检索/联合内核）
python3 08_BIN/cnsh.py run examples/cnsh_multimodal/1_视觉定位_借鉴Motto.cnsh

# 真实多模态识别 + CNSH 语法输出（桥接引擎）
lh sense <图片> --cnsh        # 视觉行/文字行/分层行
lh sense <视频> --frames 4 --cnsh
lh sense <文件> --auto         # 三色闭环（决策执行落地）
```

## 设计说明

- 双形态：每个示例 = 纯 CNSH 可运行内核（数据模拟·展示语法与决策逻辑）+ 头部注释给出真实桥接命令（lh sense --cnsh/--auto 产出真实数据）
- 诚实分层：★已桥接 与 ☆草案 在 docs/CNSH-多模态感知语法-v1.0.md §5 明确标注
- CNSH 能力边界（实测）：函数/返回/如果/打印/长度/数字list循环/文本== 可用；字符串list元素、函数体内注释行（编译器 bug·已绕开——注释全部置函数外）、保留字参数名 不可用
- 吸收原则：开源给设计理念，龍魂只取「语法层思想 + 桥接层落地」——不复制代码、不引未验证能力、数据不出机
