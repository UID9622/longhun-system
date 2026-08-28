# DNA追溯码:#龍芯⚡️2026-06-22-LONGHUN-FONT-EMBED-WATERMARK-v1.0
"""
龍魂字元库 · 龍纹水印嵌入脚本
将 U+E200（龙纹）图标以 0.15 倍缩放后，嵌入到除源图标外所有字形的右下角 (520,520)。
"""
import json
import os
import sys
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# 路径配置
# ---------------------------------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_PATH = os.path.join(
    PROJECT_ROOT, "glyphs", "龍魂字元库_v0013_稳定版.json"
)
OUTPUT_PATH = os.path.join(
    PROJECT_ROOT, "glyphs", "龍魂字元库_v0014_龍纹版.json"
)

if len(sys.argv) > 1:
    SOURCE_PATH = sys.argv[1]
if len(sys.argv) > 2:
    OUTPUT_PATH = sys.argv[2]

SOURCE_UNICODE = "U+E200"
VIEWBOX_SIZE = 600
WATERMARK_TARGET = (520, 520)  # 水印中心目标位置
WATERMARK_SCALE = 0.15         # 缩放比例，约 45x45
WATERMARK_STROKES = 20         # 源龙纹图标的笔画数


def collect_points(path):
    """从笔画路径中提取所有坐标点，用于计算包围盒。"""
    xs, ys = [], []
    for cmd in path:
        t = cmd.get("类型")
        if t == "移动到":
            x, y = cmd["坐标"]
            xs.append(x)
            ys.append(y)
        elif t == "直线段":
            x, y = cmd["终点"]
            xs.append(x)
            ys.append(y)
    return xs, ys


def compute_bbox_center(path):
    """计算路径包围盒中心 (cx, cy)。"""
    xs, ys = collect_points(path)
    if not xs:
        return 0.0, 0.0
    return (min(xs) + max(xs)) / 2.0, (min(ys) + max(ys)) / 2.0


def transform_command(cmd, cx, cy, tx, ty, scale):
    """对单条路径命令做缩放+平移变换。"""
    t = cmd["类型"]
    if t == "移动到":
        x, y = cmd["坐标"]
        return {
            "类型": "移动到",
            "坐标": [
                round((x - cx) * scale + tx, 6),
                round((y - cy) * scale + ty, 6),
            ],
        }
    elif t == "直线段":
        x, y = cmd["终点"]
        return {
            "类型": "直线段",
            "终点": [
                round((x - cx) * scale + tx, 6),
                round((y - cy) * scale + ty, 6),
            ],
        }
    # 若未来出现其他命令类型，原样返回（保持稳健）
    return cmd


def main():
    print(f"[1/6] 加载字元库: {SOURCE_PATH}")
    with open(SOURCE_PATH, "r", encoding="utf-8") as f:
        library = json.load(f)

    glyphs = library["字符集_cnsh9622"]
    total = len(glyphs)
    print(f"[2/6] 共读取 {total} 个字形")

    # -----------------------------------------------------------------------
    # 定位并预处理龙纹源图标
    # -----------------------------------------------------------------------
    source_glyph = None
    source_name = None
    for name, glyph in glyphs.items():
        if glyph.get("unicode") == SOURCE_UNICODE:
            source_glyph = glyph
            source_name = name
            break

    if source_glyph is None:
        raise RuntimeError(f"未在字元库中找到源水印字形 {SOURCE_UNICODE}")

    source_path = source_glyph["笔画路径_cnsh9622"]
    cx, cy = compute_bbox_center(source_path)
    tx, ty = WATERMARK_TARGET

    watermark_strokes = [
        transform_command(cmd, cx, cy, tx, ty, WATERMARK_SCALE)
        for cmd in source_path
    ]

    print(
        f"[3/6] 源水印 {SOURCE_UNICODE}（{source_name}）中心: ({cx:.2f}, {cy:.2f}), "
        f"笔画数: {WATERMARK_STROKES}, 命令数: {len(watermark_strokes)}"
    )

    # -----------------------------------------------------------------------
    # 嵌入水印到所有非源字形
    # -----------------------------------------------------------------------
    embedded_count = 0
    skipped_count = 0

    for name, glyph in glyphs.items():
        if glyph.get("unicode") == SOURCE_UNICODE:
            skipped_count += 1
            continue

        if "笔画路径_cnsh9622" not in glyph:
            # 跳过无路径的字形，通常不应出现
            skipped_count += 1
            continue

        glyph["笔画路径_cnsh9622"].extend(watermark_strokes)
        glyph["笔画数"] = glyph.get("笔画数", 0) + WATERMARK_STROKES
        embedded_count += 1

    print(f"[4/6] 已嵌入 {embedded_count} 个字形，跳过 {skipped_count} 个（含源水印）")

    # -----------------------------------------------------------------------
    # 更新元数据
    # -----------------------------------------------------------------------
    meta = library.setdefault("元数据", {})
    prev_version = meta.get("版本", "unknown")
    meta["版本"] = f"{prev_version.split('-')[0]}-龍纹版" if "龍纹版" not in prev_version else prev_version
    meta["前一版本"] = prev_version
    meta["总字符数"] = total
    meta["水印编码"] = SOURCE_UNICODE
    meta["水印名称"] = source_glyph.get("名称", "龙纹")
    meta["水印缩放比例"] = WATERMARK_SCALE
    meta["水印中心位置"] = list(WATERMARK_TARGET)
    meta["水印笔画数"] = WATERMARK_STROKES
    meta["水印DNA"] = "#龍芯⚡️2026-06-22-LONGHUN-FONT-EMBED-WATERMARK-v1.0"
    meta["水印描述"] = (
        f"每个字形右下角（中心 {WATERMARK_TARGET}）嵌入 {SOURCE_UNICODE} "
        f"龙纹水印，缩放 {WATERMARK_SCALE}，约 45×45 大小，作为龍魂字体身份标识。"
    )
    meta["水印时间"] = datetime.now(timezone.utc).isoformat()

    # 顶层 DNA 与三色审计保留；新增顶层水印 DNA 字段便于检索
    library["水印DNA"] = "#龍芯⚡️2026-06-22-LONGHUN-FONT-EMBED-WATERMARK-v1.0"

    print(f"[5/6] 更新元数据: 版本={meta['版本']}, 总字符数={meta['总字符数']}")

    # -----------------------------------------------------------------------
    # 保存结果
    # -----------------------------------------------------------------------
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(library, f, ensure_ascii=False, indent=2)

    print(f"[6/6] 已保存到: {OUTPUT_PATH}")
    print("\n===== 水印嵌入摘要 =====")
    print(f"源水印字形:     {SOURCE_UNICODE}（{source_name}）")
    print(f"源水印中心:     ({cx:.2f}, {cy:.2f})")
    print(f"目标中心位置:   {WATERMARK_TARGET}")
    print(f"缩放比例:       {WATERMARK_SCALE}")
    print(f"嵌入字形数:     {embedded_count}")
    print(f"跳过字形数:     {skipped_count}")
    print(f"输出版本:       {meta['版本']}")
    print(f"总字符数:       {total}")
    print(f"输出文件:       {OUTPUT_PATH}")
    print("========================")


if __name__ == "__main__":
    main()
