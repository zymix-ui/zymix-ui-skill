# DESIGN.md — ZymixUI

> ZYMIX 移动端设计系统（iOS 风格社交 / IM 产品）。供 Google Stitch 及各类设计 AI 读取，生成符合规范的界面。
> 版本 v1.0.0 · 单位默认 px · 目标画布 iPhone 375×812。

---

## 1. Visual Theme & Atmosphere（视觉气质）

- **气质**：干净、克制、iOS 原生质感。颜色传达用途与状态，不做装饰。
- **底色哲学**：大面积留白 / 浅灰，靠层级与少量品牌绿点缀，而非彩色堆叠。
- **标志元素**：品牌绿 `#26D93E`；液态玻璃材质（导航条、悬浮按钮、Toast）；胶囊形按钮；0.5px 发丝分隔线。
- **深浅色**：同一套语义变量，深浅色自动跟随系统（`prefers-color-scheme`），不做两套。
- **适用场景**：社交动态、IM 聊天、个人中心、钱包/设置、活动卡片等移动页面。

---

## 2. Color Palette & Roles（颜色角色 · 语义名 + 值 + 用途）

颜色**只用语义角色**，禁止在页面里写死 hex。每个角色都有 Light / Dark 两个值。

### 品牌 / 状态色
| 角色 | Light | Dark | 用途 |
|---|---|---|---|
| accent/base | `#26D93E` | `#26D93E` | 主按钮、选中、进度、可点强调 |
| accent/pressed | `#1FB432` | `#1FB432` | 主色按下态 |
| accent/soft | `rgba(38,217,62,.15)` | `rgba(38,217,62,.12)` | 浅底强调背景 |
| accent/soft-foreground | `#0F7A23` | `#74D88F` | 浅底上的强调文字 / 链接 |
| success/* | 同 accent | 同 accent | "告知结果"（到账/完成/校验通过） |
| danger/base | `#EA4B46` | `#EA4B46` | 危险按钮填充 |
| danger/pressed | `#C53936` | `#C53936` | 危险按下态 |
| danger/soft-foreground | `#AE0800` | `#FF9A96` | 危险文字/图标（红色以文字形态出现必须用深红，达 AA） |
| info/base | `#007AFF` | `#007AFF` | 信息提示 |

> **accent vs success 判据**：元素"让你去做"→accent；"告诉你结果"→success。
> **红色三分**：点赞情感色 `feature/like #FF3B64`；危险按钮填充 danger/base；危险文字 danger/soft-foreground。

### 中性 / 文字（foreground）
| 角色 | Light | Dark | 用途 |
|---|---|---|---|
| foreground/base | `#000000` | `#FFFFFF` | 主文字/图标 |
| foreground/muted | `rgba(0,0,0,.55)` | `rgba(255,255,255,.55)` | 次要文字（达 AA） |
| foreground/subtle | `rgba(0,0,0,.40)` | `rgba(255,255,255,.35)` | 辅助信息（仅小字，AA 豁免） |
| foreground/placeholder | `rgba(0,0,0,.30)` | `rgba(255,255,255,.30)` | 输入占位 |
| foreground/disabled | `rgba(0,0,0,.26)` | `rgba(255,255,255,.22)` | 禁用文字 |
| foreground/inverse | `#FFFFFF` | `#000000` | 反色容器上的文字（随主题翻） |
| default/white | `#FFFFFF` | `#FFFFFF` | 恒白（图上叠字，不随主题翻） |

### 层面（background / surface / border / separator）
| 角色 | Light | Dark | 用途 |
|---|---|---|---|
| background/base | `#FFFFFF` | `#0B0B0D` | 页面底 |
| background/secondary | `#FCFCFC` | `#09090B` | 雪白列表页底 |
| background/tertiary | `#F5F5F5` | `#060607` | 灰底 |
| surface/base | `#FFFFFF` | `#18181B` | 卡片/面板 |
| surface/secondary | `#F5F5F5` | `#232327` | 搜索框底 / 内嵌面 |
| surface/tertiary | `#EBEBEB` | `#2F2F34` | 三级面 |
| surface/pressed | `rgba(0,0,0,.08)` | `rgba(255,255,255,.08)` | 列表/卡片按压态 |
| border/base | `#DEDEE0` | `#3A3A40` | 组件描边（1px） |
| separator/base | `rgba(0,0,0,.10)` | `rgba(255,255,255,.10)` | 常规分隔线（0.5px） |
| separator/strong | `rgba(0,0,0,.40)` | `rgba(255,255,255,.40)` | 强分隔（1px，统计分栏竖线） |

### 场景专用（feature/im · 聊天）
好友气泡 `#E1FFBF`/暗 `#2E4212`；非好友气泡 `#C9FAFF`/暗 `#123C42`；已读 好友 `#58C138`、非好友 `#00BAD2`；非好友 Add 按钮 `#26D9F0`。气泡圆角 22px。

---

## 3. Typography Rules（排版）

- **字体**：`-apple-system, "SF Pro", "SF Pro Text", "SF Pro Display", system-ui, sans-serif`
- **字重**：全局仅 **Regular 400 / Semibold 600 / Black 900**；Bold 700 仅用于「场景 Scene」页头排版。
- **不发明字号**：只用下表档位；界面里其他尺寸就近归档。

| 角色 | 字号/行高 | 字重 | 用途 |
|---|---|---|---|
| Display | 36/40 | 900 | 超大标题 |
| Title/Lg · Md · Sm · Xs | 30/36 · 24/32 · 20/28 · 15/auto | 900 · 900 · 600 · 600 | 标题层级 |
| Label/Lg · Base · Sm · Caption · Xs | 18/28 · 16/24 · 14/20 · 13/auto · 12/16 | 600 | 强调文字 |
| Body/Lg · Base · Md · Sm · Caption · Xs · 2xs | 17/22 · 16/24 · 15/20 · 14/20 · 13/auto · 12/16 · 11/auto | 400 | 正文 |
| Link/Base · Sm | 16/24 · 14/20 | 600 | 链接（色 accent/soft-foreground） |
| Button/Base · Sm · Text | 17/22 · 14/20 · 15/auto | 600 | 按钮文字 |
| Number/Base · Md | 18/20 · 24/32 | 900 · 600 | 数字统计 |
| Scene 页头大标题 | 34/40 | 900 | 页面头部（首字大写） |

---

## 4. Component Stylings（组件 · 含状态）

### 按钮 Button（7 变体 × 3 尺寸）
- 尺寸：sm 高 32 圆角 16 / md 高 36 圆角 round / lg 高 48 圆角 round；文字 Button 角色。
- 变体（底色 + 文字，**必须同状态组配对，换底色文字联动**）：
  - primary：accent/base + accent/foreground(白)
  - secondary：default/base(灰) + accent/soft-foreground(绿字)
  - tertiary：default/base + default/foreground(黑)
  - outline：透明 + border/base 描边 + default/foreground
  - ghost：透明 + default/foreground
  - danger：danger/base + 白字
  - dangerSoft：灰底(default/soft) + danger/soft-foreground(深红字)
- 状态：default / pressed（换 *-pressed 底）/ disabled（整体 opacity .5）。移动端无 hover。触控热区 ≥44。

### Toast
胶囊形（343×66），底为**液态玻璃材质**（见第 6 节），图标+文字一律中性 foreground/base（不用状态色）。位置固定屏幕顶部、距顶 60px 居中；点击触发、显示 3 秒淡入淡出。

### 输入框 Input
底 surface/base 或 surface/secondary；占位 foreground/placeholder；文字 Field 角色（16/24）；圆角 md~lg。

### 页头 Header
① 品牌页头：大标题（Scene 34 Black）+ 右侧 42px 玻璃圆钮。② 导航页头：居中标题（17 Semibold）+ 左返回（42px 玻璃圆钮）。

### 底部导航 Nav
玻璃底（feature/nav/background + blur 20）；图标 24；激活态用 accent 胶囊（底 accent/base + 白字/图）；未激活 foreground/subtle。

### 列表 List / 卡片 Card
行高 ≥56、图标 24、标题 Body/Lg、右 chevron；组内 0.5px separator/base 左缩进；卡片 surface/base 圆角 lg(16)、无阴影（靠层级色区分）。

### 图标
用 ZymixUI 图标库（单色 currentColor，跟随文字色），npm `@zymix-ui/icons` 或 CDN `cdn.jsdelivr.net/gh/zymix-ui/zymix-icons`。禁止手绘不一致的图标。

---

## 5. Layout Principles（布局）

- **间距刻度**（size token，px）：0 4 6 8 12 16 20 24 28 32 36 40 44 48 56 64 72 96 128。页面左右边距通常 16。
- **圆角刻度**（radius）：none 0 · xs 6 · sm 8 · md 12 · lg 16 · xl 20 · 2xl 22 · 3xl 24 · 4xl 28 · 5xl 32 · 6xl 36 · round 9999。
- **画布**：iPhone 375 宽；内容单列纵向滚动；卡片/组卡分区。
- **对齐**：横向按钮组三选一——固定间距靠左 `gap`、固定间距整组靠右 `flex-end+gap`、两端均分 `space-between`；勿用 space-between 凑固定间距。

---

## 6. Depth & Elevation（深度与材质）

- **不用传统投影**做卡片层级（旧 Shadow 六档已废弃）；靠 surface 三级色（base→secondary→tertiary）表达层级。
- **液态玻璃材质**（导航/悬浮按钮/Toast）：半透明底 + 背景模糊 + 内高光 + 柔和投影。CSS 近似：
  ```css
  background: rgba(255,255,255,.65);            /* 暗色 rgba(24,24,27,.65) */
  backdrop-filter: blur(4px) saturate(1.6);
  box-shadow: 0 8px 40px rgba(0,0,0,.10),
              inset 0 1px 1px rgba(255,255,255,.8),
              inset 0 -1px 1px rgba(255,255,255,.3);
  ```
- **图上叠字**：底部黑渐变遮罩保证可读，文字用 default/white（恒白）。

---

## 7. Do's and Don'ts（守则）

**Do**
- 颜色/字号/圆角/间距一律用上面的角色与刻度。
- 按钮文字色随所在状态组的 foreground 走。
- 分隔线 0.5px，强分隔 1px；触控热区 ≥44。
- 深浅色只靠语义变量，交付前脑内过一遍深色（不许黑底黑字）。
- 图片/媒体容器给兜底底色（surface/secondary 或品牌渐变），图挂也不空。

**Don't**
- ❌ 写死 hex / rgba（除媒体遮罩渐变）。
- ❌ 自造字号字重（如标题 22px）；就近归档。
- ❌ 用传统卡片投影堆层级。
- ❌ Toast 用红绿状态色 / 放页面中部。
- ❌ 手绘风格不一的图标。

---

## 8. Responsive Behavior（响应式）

- 目标为移动单列；基准 375 宽，全宽自适应。
- 触控目标 ≥44×44（视觉小于 44 的加透明热区）。
- 横滑区（相册/卡片行）用 overflow-x 滚动；纵向容器为 flex 列时子元素设 `flex-shrink:0`，避免固定高卡片被压扁。
- 深浅色跟随系统；可用 `data-theme="light|dark"` 强制。

---

## 9. Agent Prompt Guide（给 AI 的速用参考）

**核心色速记**：品牌绿 `#26D93E`；主文字黑/白；次文字 55% 灰；卡片白/`#18181B`；页面底白/`#0B0B0D`；危险红 `#EA4B46`（文字用 `#AE0800`）。

**可直接用的 prompt 例**
- 「做一个 ZYMIX 转账成功页：居中大对勾（success 绿）、金额用 Number 角色、底部主按钮 Done、上方 View details 文字按钮。」
- 「做一个 ZYMIX 消息列表页：品牌页头 + 搜索框 + 8 条会话（头像/昵称/末条 muted/时间/未读徽标）+ 玻璃底部导航。」
- 「做一个 ZYMIX 好友聊天页：导航页头带头像、来回气泡（好友色）、已读回执、玻璃输入条。」

**给非规范原型/PRD**：只提取信息架构与内容，用本规范的角色/组件重建，不照搬来源样式。
