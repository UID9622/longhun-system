"""视觉识别示例 — 文化符号分析

⚠️ 视觉模块仍为 Preview，需对接本地视觉模型（Ollama/MLX）后可用。
"""

from longhun.vision import VisionAnalyzer, VisionBridge

va = VisionAnalyzer()

# 本地视觉桥接（Preview·可用）
print("=== 本地视觉桥 ===")
bridge = VisionBridge()
desc = bridge.describe("photo.jpg", "图中有什么文化符号？")
print(desc)

# 图像分析（Preview·需要本地视觉模型）
print("\n=== 图像分析 ===")
try:
    result = va.analyze("demo.jpg")
    print(f"物体: {result.objects}")
    print(f"符号: {result.culture_symbols}")
except NotImplementedError:
    print("视觉模型尚未对接，请确保 Ollama 或 MLX 已运行。")

# 文化符号识别（Preview）
print("\n=== 文化符号识别 ===")
try:
    symbol = va.recognize_symbol("taiji.png")
    print(f"符号: {symbol.symbol}")
    print(f"卦象: {symbol.trigram}")
    print(f"五行: {symbol.element}")
except NotImplementedError:
    print("文化符号识别引擎待对接。")
