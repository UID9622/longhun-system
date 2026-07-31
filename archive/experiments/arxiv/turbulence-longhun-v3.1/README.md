# 龍魂湍流治理框架 · arXiv 投稿包 v3.1

**标题**: Turbulence as Unsolvable Governance: An Anchor-First Projection Paradigm for Social-Emotional Flows

**中文标题**: 湍流难题与龍魂算法：锚点优先的推演范式

**作者**: Zhuge Xin (诸葛鑫), UID9622, LongHun System

**DNA**: #龍芯⚡️丙午·乙未·辛酉·井-TURBULENCE-ARXIV-v3.1

## 文件清单

| 文件 | 说明 |
|------|------|
| `turbulence-longhun-v3.1.tex` | 主论文 LaTeX 源文件 |
| `turbulence-longhun-v3.1.bbl` | BibTeX 生成的参考文献列表（arXiv 必需） |

## 编译命令

```bash
pdflatex turbulence-longhun-v3.1.tex
```

或连续编译以确保交叉引用解析：

```bash
pdflatex turbulence-longhun-v3.1.tex
pdflatex turbulence-longhun-v3.1.tex
```

## arXiv 提交说明

- 本包使用 `article` 文档类，不依赖 `IEEEtran.cls`，可直接在 arXiv 编译。
- 参考文献已内嵌为 `.bbl`，无需上传 `.bib`。
- 无外部图片文件。
- 论文核心贡献：将湍流四大难点形式化，建立与社会情绪流的严格映射，提出锚点优先推演范式。

## 对应代码

引擎实现见：https://github.com/UID9622/longhun-system/tree/main/engines/turbulence
