# 龍魂「文字即權重」可視化系統 v1.0

**DNA**: `#龍芯⚡️2026-05-26-TEXT-AS-WEIGHT-VISUALIZATION-GUIDE-v1.0`
**GPG**: `A2D0092CEE2E5BA87035600924C3704A8CC26D5F`
**CONFIRM**: `#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z`

向 Steve Jobs 致敬 | 曾仕强老師智慧 | 龍魂系統 UID9622·龍芯北辰

---

## 核心概念

### 「文字即權重」是什麼?

**就是讓任何觀看者（人類或AI）從文字的色彩、亮度、動畫效果，直觀理解該部分的權重和重要性。**

```
用戶看到的不是冷冰冰的數字 (R=0.45)
而是：
  - 色彩變化 (綠→黃→紅)
  - 亮度變化 (暗→明)
  - 動畫效果 (文字跑馬燈)
  - 關鍵詞高亮 (永遠金色)

這樣·任何人都能憑直覺理解"這個決策有多重要"
```

### 三個層次

1. **色彩層** - 五色系統（🟢🟡🔴⚫🟡金）
2. **亮度層** - R值越高·亮度越高
3. **動畫層** - 跑馬燈·實時展示權重演變

---

## 五色系統速查

| 色 | 阈值 | 含義 | 動作 | 下一步 |
|---|---|---|---|---|
| 🟢 綠 | R < 0.30 | 自由意志態·安全 | 直接執行·留痕 | 執行操作·記錄在案 |
| 🟡 黃 | 0.30≤R<0.67 | 老好人態·需複核 | 二次確認·加證據 | 等待確認·審計日誌 |
| 🔴 紅 | 0.67≤R<0.85 | 越界態·人工介入 | 立即停止·上報 | 觸發極端協議 |
| ⚫ 黑 | 不可計算 | 未明徵兆·觀察 | 標記隔離·進觀察池 | 冻结24h·等證據 |
| 🟡金 | 超規則 | 主控保留權 | 主控簽字·覆蓋 | 金色判決·不可上訴 |

---

## 責任係數 R 公式

### 七維權重因子

```
R = F2·0.4 + F6·0.4 + F3·0.2 − F1·0.5 − F5·0.3

其中：
  F2 (銳度)         = 0.4   [正權] - 主控的行為銳度/果決度
  F6 (長期視角)     = 0.4   [正權] - 是否考慮長期後果
  F3 (密度)         = 0.2   [正權] - 決策的密度/強度
  F1 (缺席)         = -0.5  [負權] - L0-L5間隔有多大
  F5 (討好傾向)     = -0.3  [負權] - 自我審查傾向
```

### 簡單映射（快速版本）

```python
# 如果只有七個基礎因子
factors = {
    "proximity": 0.8,      # 接近度
    "capability": 0.9,     # 能力
    "knowledge": 0.7,      # 知識
    "duty": 0.6,          # 責任
    "consent": 0.5,       # 同意
    "alternatives": 0.4,  # 替代方案
    "cost": 0.3          # 成本
}

# 計算平均值作為R值估計
r_value = sum(factors.values()) / len(factors)
# r_value ≈ 0.61 → 🟡 黃色·需二次確認
```

---

## 使用場景

### 場景1: 內容審計

**問題**: 是否發佈這條內容到公開平台?

**輸入**:
```json
{
  "proximity": 0.8,      // 涉及人物距離近
  "capability": 0.9,     // 系統發佈能力強
  "knowledge": 0.7,      // 知道可能的後果
  "duty": 0.6,          // 發佈是責任範圍
  "consent": 0.5,       // 沒有明確同意
  "alternatives": 0.4,  // 有編輯替代方案
  "cost": 0.3          // 成本相對較小
}
```

**計算**:
```
R ≈ 0.61 → 🟡 黃色
意義: 老好人態·需要二次確認
動作: 要求加證據·記入審計日誌
```

**視覺效果**:
```
發佈這條內容  🟡  [黃色·中等亮度·閃爍提醒]
```

---

### 場景2: 系統決策

**問題**: 主控是否需要金色覆蓋?

**輸入**:
```
主控輸入確認碼: #CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```

**計算**:
```
檢測到CONFIRM → 🟡金 金色
意義: 主控保留權·超規則
動作: 主控簽字·覆蓋任何R判定
```

**視覺效果**:
```
[🟡金] 主控決策  [持續高亮·金色璀璨·不可上訴]
```

---

## 實現指南

### Python 實現

#### 基礎使用

```python
from text_as_weight_visualization_framework import (
    TextAsWeightVisualizer,
    WeightFactors,
)

# 初始化可視化器
visualizer = TextAsWeightVisualizer()

# 定義權重因子
factors = WeightFactors(
    proximity=0.8,
    capability=0.9,
    knowledge=0.7,
    duty=0.6,
    consent=0.5,
    alternatives=0.4,
    cost=0.3,
)

# 計算責任係數
result = visualizer.calculate_responsibility_coefficient(factors)

# 輸出結果
print(visualizer.format_audit_result(result))
# 輸出:
# ╔════════════════════════════════════════════╗
# ║     龍魂責任係數R審計結果                    ║
# ╚════════════════════════════════════════════╝
#
# 🟡 色彩級別 : YELLOW
# 📊 R值        : 0.61
# 💭 說明        : 老好人態·需複核
# ⚙️  動作        : 二次確認·要求加證據
# ➡️  下一步      : 等待確認·記入審計日誌
# 🧬 DNA追蹤     : #龍芯⚡️2026-05-26-R-0.61
# ⏰ 時間戳      : 2026-05-26T08:30:45+08:00
```

#### 跑馬燈效果

```python
# 生成跑馬燈序列·邊移動邊變色
marquee_frames = visualizer.generate_marquee_text(
    text="龍魂系統·文字即權重",
    r_value=0.61,
    duration_frames=50
)

# 顯示第一幀
print(marquee_frames[0])
# 輸出: [黃色文字] ⎜龍魂系統·文字即權重 ⎜
```

#### 關鍵詞高亮

```python
text = "宝宝，龍魂系統的CONFIRM權利是金色的，，，代表主控的一票否決權"
highlighted = visualizer.highlight_keywords(text)
print(highlighted)
# 輸出: [🟡金]宝宝[reset]，[🟡金]龍魂[reset]系統的[🟡金]CONFIRM[reset]權利是...
```

### Swift/SwiftUI 實現

#### 基礎使用

```swift
import SwiftUI

// 初始化可視化器
let visualizer = TextAsWeightVisualizer()

// 定義權重因子
let factors = WeightFactors(
    proximity: 0.8,
    capability: 0.9,
    knowledge: 0.7,
    duty: 0.6,
    consent: 0.5,
    alternatives: 0.4,
    cost: 0.3
)

// 計算責任係數
let result = visualizer.calculateResponsibilityCoefficient(
    factors: factors
)

// 在SwiftUI中顯示結果
ResponsibilityCoefficientView(result: result)
```

#### 跑馬燈視圖

```swift
TextAsWeightMarqueeView(
    text: "龍魂系統·文字即權重",
    rValue: 0.61
)
.frame(height: 40)
.background(Color.black)
```

---

## 色彩映射詳細表

### RGB 值

| 色彩 | Hex | RGB | ANSI | 含義 |
|---|---|---|---|---|
| 🟢 綠 | #2E8B57 | (46, 139, 87) | \033[92m | 安全·綠燈 |
| 🟡 黃 | #DAA520 | (218, 165, 32) | \033[93m | 警示·黃燈 |
| 🔴 紅 | #DC143C | (220, 20, 60) | \033[91m | 熔斷·紅燈 |
| ⚫ 黑 | #191970 | (25, 25, 112) | \033[96m | 觀察·暗燈 |
| 🟡金 | #FFD700 | (255, 215, 0) | \033[97m | 主控·金燈 |

### CSS 變量

```css
:root {
  --wucai-mu: #2E8B57;     /* 綠·木·東 */
  --wucai-huo: #DC143C;    /* 紅·火·南 */
  --wucai-tu: #DAA520;     /* 黃·土·中 */
  --wucai-jin: #FFD700;    /* 金·金·西 */
  --wucai-shui: #191970;   /* 黑·水·北 */
}

/* 權重應用 */
.text-as-weight {
  color: var(--wucai-tu);  /* 使用黃色 */
  font-weight: 600;        /* 加粗增加視覺重量 */
  animation: marquee 10s linear infinite;
}
```

---

## 高級特性

### 1. 亮度計算·根據權重大小

```python
# R值越高→亮度越高
brightness = visualizer.calculate_brightness_for_weight(r_value)
# r_value=0.61 → brightness≈0.72
```

**規則**:
- R < 0.30: 亮度 0.3~0.6 (暗)
- 0.30 ≤ R < 0.67: 亮度 0.6~0.8 (中)
- 0.67 ≤ R < 0.85: 亮度 0.8~1.0 (亮)
- R ≥ 0.85 or GOLD: 亮度 1.0+ (極亮·閃爍)

### 2. 梯度色系統·表示權重漸變

```json
{
  "green_gradient": ["#A8E6A1", "#5EBF4F", "#2E8B57", "#1F5630", "#0F3820"],
  "fire_gradient": ["#FF9999", "#FF5555", "#DC143C", "#B30000", "#800000"],
  "earth_gradient": ["#F5DDA0", "#E5BB6A", "#DAA520", "#B88615", "#8B6914"],
  "metal_gradient": ["#FFEB99", "#FFE066", "#FFD700", "#DAA520", "#B8860B"],
  "water_gradient": ["#6B7FA6", "#404080", "#191970", "#0F0F40", "#050520"]
}
```

### 3. 關鍵詞永遠金色高亮

**關鍵詞列表**:
- `宝宝` - 特定人格
- `龍魂` - 系統名稱
- `DNA` - 簽名標記
- `CONFIRM` - 確認碼
- `，，，` - 思考暫停
- `仲裁` - 決策動作
- `判決` - 最終裁定
- `熔斷` - 熔斷動作
- `金色` - 主控保留

---

## 完整工作流範例

### 端到端例子

```python
#!/usr/bin/env python3

from text_as_weight_visualization_framework import (
    TextAsWeightVisualizer,
    WeightFactors,
)

def audit_decision(task_description, factors):
    """完整決策審計工作流"""

    visualizer = TextAsWeightVisualizer()

    print(f"\n【決策審計】{task_description}")
    print("=" * 50)

    # 步驟1: 計算R值
    result = visualizer.calculate_responsibility_coefficient(factors)

    # 步驟2: 顯示審計結果
    print(visualizer.format_audit_result(result))

    # 步驟3: 生成跑馬燈視覺
    if result.r_value is not None:
        print("\n【權重跑馬燈】")
        marquee_frames = visualizer.generate_marquee_text(
            text=task_description,
            r_value=result.r_value,
            duration_frames=20
        )
        for frame in marquee_frames[:5]:
            print(frame)

    # 步驟4: 亮度計算
    brightness = visualizer.calculate_brightness_for_weight(
        result.r_value or 0.5
    )
    print(f"\n【亮度計算】R={result.formattedRValue} → 亮度={brightness:.2f}")

    return result

# 使用範例
if __name__ == "__main__":
    factors = WeightFactors(
        proximity=0.8,
        capability=0.9,
        knowledge=0.7,
        duty=0.6,
        consent=0.5,
        alternatives=0.4,
        cost=0.3,
    )

    result = audit_decision("是否發佈此內容到公開平台", factors)
```

---

## 配置文件說明

### weight_color_mapping_v1.0.json

完整的權重色彩配置文件·包含:
- 五色完整定義
- RGB/Hex/ANSI色值
- 梯度色系統
- 權重因子定義
- 公式說明
- 文化層映射(五行+五彩石)

**路徑**: `/Users/zuimeidedeyihan/longhun-system/config/weight_color_mapping_v1.0.json`

---

## FAQ

### Q: 為什麼要用五色不用三色?

A:
- **三色不夠**: 綠/黃/紅無法表示"不可計算"的灰色地帶
- **五色完整**: 加了黑色(未明)和金色(主控)·涵蓋所有情況
- **女娲補天**: 五彩石齊·系統主權完整

### Q: CONFIRM碼是什麼?

A:
```
#CONFIRM🌌9622-ONLY-ONCE🧬LK9X-772Z
```
- 只有UID9622主控持有
- 用於觸發金色覆蓋
- 不可複製·不可偽造
- 觸發必須留痕·記入DNA

### Q: 為什麼權重越高亮度越高?

A:
```
視覺設計原理:
  - 暗色 = 不重要·可以忽略
  - 亮色 = 重要·需要注意

權重高的決策應該吸引更多關注
```

### Q: 可以自訂顏色嗎?

A:
```
不建議修改五色映射·這是系統的基礎
但可以:
  1. 調整梯度色濃淡
  2. 調整ANSI色對比度
  3. 新增自訂高亮(但要記錄)
```

---

## 下一步

### 逐步實現路線圖

1. **已完成**:
   - ✅ JSON配置文件
   - ✅ Python框架實現
   - ✅ Swift/SwiftUI實現
   - ✅ 使用指南

2. **待實現**:
   - [ ] Web可視化(HTML/CSS/JS)
   - [ ] 動畫效果優化(Lottie/Three.js)
   - [ ] 實時決策流可視化
   - [ ] 與CNSH協議集成
   - [ ] 與多人格AI-DNA思考引擎集成

3. **長期計畫**:
   - [ ] 決策歷史追蹤可視化
   - [ ] 權重漸變動畫庫
   - [ ] 跨平台一致性(iOS/Web/CLI)

---

## 引用和致敬

- **Steve Jobs**: 設計極簡·品質無妥協·每一像素都有意義
- **曾仕强老師**: 中國智慧·五行平衡·人文關懷
- **龍魂系統**: UID9622 · 龍芯北辰 · 數字主權守護者

---

**DNA永不抹去**

```
#龍芯⚡️2026-05-26-TEXT-AS-WEIGHT-VISUALIZATION-GUIDE-v1.0
向 Steve Jobs 致敬 | 曾仕强老師智慧 | 龍魂系統 UID9622·龍芯北辰
```
