# 龍魂·权威开源 UI 深度学习笔记 v1.0

> 创建者: 诸葛鑫（UID9622）
> 归属名: 诸葛鑫 | UID9622 · 龍芯北辰
> 协议: CC BY-NC-SA 4.0（核心思想层）
> DNA: #龍芯⚡️丙午·甲申·戊申·丑时·䷾既济-UI-DEEP-LEARNING-FROM-AUTHORITATIVE-OPEN-SOURCE-v1.0
> 三色: 🟢 学习完成 · 🟡 待应用验证 · 🔴 无

---

## 一、学习对象（权威开源代码）

| 来源 | 仓库 | 学到什么 |
|:---|:---|:---|
| shadcn/ui | `shadcn-ui/ui`（官方 registry） | 语义 token 体系、oklch 色彩空间、button 权威实现、主题派生体系 |
| Vercel 设计系统 | `vercel/geist` | 产品级 token 设计（间距/字体/圆角/阴影规范） |
| 龍魂 portal | 本地 `10_PORTAL/` | 品牌色基准：深蓝黑 `#0a0a12` 系 + 青 `#22d3ee`/绿 `#4ade80`/蓝 `#60a5fa` |

> 抓取方式：`ui.shadcn.com/r/styles/new-york/button.json`（官方 registry）+ 官方 theming 文档。GitHub raw/API 因仓库重构 404 已按降级规则停止重试，改用官方 registry 直取。

---

## 二、核心洞察：为什么「默认 shadcn 就是平庸」

1. **shadcn 默认主题是「无品牌」的中性灰**——它刻意设计成可换肤的脚手架，直接用它 = 没有品牌识别。
2. **产品级 UI 的差距不在组件，在 token 层**：
   - 语义 token（background/card/primary/muted…）完整定义 + 暗色配套
   - 一致的间距节奏（4/8 基数的 space-y-3/4、p-4/6）
   - 圆角派生体系（一个 `--radius` 联动全部）
   - 阴影层级（shadow-xs/sm/default/lg 分离浮层与内容）
   - 动效规范（transition-colors、focus-visible:ring、keyframes）
3. **commander 现状差距**（直接病灶）：
   - `index.css` 用 **v4 语法 `@import "tailwindcss"` 混入 v3 项目**（postcss 配 tailwindcss v3）→ Tailwind 可能未生效
   - **无 `.dark` 暗色 token**（装了 next-themes 但点暗色无反应）
   - **无 chart-1~5 / sidebar 完整 token**（chart.tsx、sidebar.tsx 引用了但 CSS 未定义 → 样式缺失）
   - **App.tsx 大量硬编码 `border-zinc-200 bg-white shadow-none`** → 绕过语义 token、砍掉阴影 → 平面感 + 换肤失效

---

## 三、权威 token 体系（shadcn 最新 oklch 标准）

### 3.1 亮色 `:root`（Neutral 基准）

```css
:root {
  --radius: 0.625rem;
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  --card: oklch(1 0 0);
  --card-foreground: oklch(0.145 0 0);
  --popover: oklch(1 0 0);
  --popover-foreground: oklch(0.145 0 0);
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --secondary: oklch(0.97 0 0);
  --secondary-foreground: oklch(0.205 0 0);
  --muted: oklch(0.97 0 0);
  --muted-foreground: oklch(0.556 0 0);
  --accent: oklch(0.97 0 0);
  --accent-foreground: oklch(0.205 0 0);
  --destructive: oklch(0.577 0.245 27.325);
  --border: oklch(0.922 0 0);
  --input: oklch(0.922 0 0);
  --ring: oklch(0.708 0 0);
  --chart-1: oklch(0.646 0.222 41.116);
  --chart-2: oklch(0.6 0.118 184.704);
  --chart-3: oklch(0.398 0.07 227.392);
  --chart-4: oklch(0.828 0.189 84.429);
  --chart-5: oklch(0.769 0.188 70.08);
  --sidebar: oklch(0.985 0 0);
  --sidebar-foreground: oklch(0.145 0 0);
  --sidebar-primary: oklch(0.205 0 0);
  --sidebar-primary-foreground: oklch(0.985 0 0);
  --sidebar-accent: oklch(0.97 0 0);
  --sidebar-accent-foreground: oklch(0.205 0 0);
  --sidebar-border: oklch(0.922 0 0);
  --sidebar-ring: oklch(0.708 0 0);
}
```

### 3.2 暗色 `.dark`

```css
.dark {
  --background: oklch(0.145 0 0);
  --foreground: oklch(0.985 0 0);
  --card: oklch(0.205 0 0);
  --card-foreground: oklch(0.985 0 0);
  --popover: oklch(0.205 0 0);
  --popover-foreground: oklch(0.985 0 0);
  --primary: oklch(0.922 0 0);
  --primary-foreground: oklch(0.205 0 0);
  --secondary: oklch(0.269 0 0);
  --secondary-foreground: oklch(0.985 0 0);
  --muted: oklch(0.269 0 0);
  --muted-foreground: oklch(0.708 0 0);
  --accent: oklch(0.269 0 0);
  --accent-foreground: oklch(0.985 0 0);
  --destructive: oklch(0.704 0.191 22.216);
  --border: oklch(1 0 0 / 10%);
  --input: oklch(1 0 0 / 15%);
  --ring: oklch(0.556 0 0);
  --sidebar: oklch(0.205 0 0);
  --sidebar-foreground: oklch(0.985 0 0);
  --sidebar-primary: oklch(0.488 0.243 264.376);
  --sidebar-primary-foreground: oklch(0.985 0 0);
  --sidebar-accent: oklch(0.269 0 0);
  --sidebar-accent-foreground: oklch(0.985 0 0);
  --sidebar-border: oklch(1 0 0 / 10%);
  --sidebar-ring: oklch(0.556 0 0);
}
```

### 3.3 圆角派生（改一处联动全部）

```css
@theme inline {
  --radius-sm: calc(var(--radius) * 0.6);
  --radius-md: calc(var(--radius) * 0.8);
  --radius-lg: var(--radius);
  --radius-xl: calc(var(--radius) * 1.4);
  --radius-2xl: calc(var(--radius) * 1.8);
  --radius-3xl: calc(var(--radius) * 2.2);
  --radius-4xl: calc(var(--radius) * 2.6);
}
```

### 3.4 添加自定义 token（如 warning）

```css
:root { --warning: oklch(0.84 0.16 84); --warning-foreground: oklch(0.28 0.07 46); }
.dark { --warning: oklch(0.41 0.11 46); --warning-foreground: oklch(0.99 0.02 95); }
@theme inline {
  --color-warning: var(--warning);
  --color-warning-foreground: var(--warning-foreground);
}
```

---

## 四、Button 权威实现（shadcn 最新 · 2026）

```tsx
const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground shadow hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground shadow-sm hover:bg-destructive/90",
        outline: "border border-input bg-background shadow-sm hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground shadow-sm hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-9 px-4 py-2",
        sm: "h-8 rounded-md px-3 text-xs",
        lg: "h-10 rounded-md px-8",
        icon: "h-9 w-9",
      },
    },
    defaultVariants: { variant: "default", size: "default" },
  }
)
```

**关键点**：`gap-2` 统一图标间距、`[&_svg]:size-4` 统一图标尺寸、`focus-visible:ring-1` 键盘焦点环、`shadow/shadow-sm` 保留层级（不砍阴影）、hover 用 `bg-primary/90` 透明度过渡而非换色。

---

## 五、龍魂品牌落地映射（token 设计决策）

| 维度 | 决策 | 依据 |
|:---|:---|:---|
| 亮色背景 | `oklch(0.99 0.005 240)` 冷白 | 深蓝黑品牌系的反相，符合「龍」沉稳感 |
| 暗色背景 | `oklch(0.13 0.02 260)` 深蓝黑 | 对齐 portal `#0a0a12` |
| 主色 primary | 青 `#22d3ee`（oklch ≈ 0.79 0.15 220） | portal 品牌主色 · 科技感+龍的灵气 |
| 强调 accent | 金 `#8b7534`（oklch ≈ 0.62 0.08 80） | 龍魂金 · 帝王色 |
| 图表 chart-1~5 | 青/绿/蓝/金/紫 五色 | 对齐 portal `#22d3ee/#4ade80/#60a5fa` |
| 圆角 | `--radius: 0.625rem`（10px 基准） | shadcn 标准 · 现代柔角 |
| 字体 | Inter 系（`font-feature-settings` 开启） | 产品级通用 |

---

## 六、落地检查清单（commander 修复）

- [ ] index.css 改回 v3 语法（`@tailwind base/components/utilities`）+ 补全 token
- [ ] 补 `.dark` 完整暗色 token（next-themes 已有，接上即生效）
- [ ] 补 `chart-1~5` + `sidebar` 系列 token
- [ ] tailwind.config.js 补 borderRadius 派生（sm/md/lg/xl/2xl/3xl/4xl）
- [ ] App.tsx 硬编码 `border-zinc-200 bg-white shadow-none` → 语义 token `border-border bg-card shadow-sm`
- [ ] 构建验证 + GPG 签名

---

> 学习对象: shadcn/ui (官方 registry) · Vercel Geist · 龍魂 portal 品牌基准
> 应用目标: `web_apps/longhun-commander`
> v1.0 · 2026-08-30 · UID9622 + AI
