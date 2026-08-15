# DESIGN.md — ZymixUI

> ZYMIX 移动端设计系统（iOS 风格社交 / IM 产品）。供 Google Stitch 及各类设计 AI 读取，生成符合规范的界面。
> 版本 v1.5.0 · 单位默认 px · 目标画布 iPhone 375×812。

---

## 1. Visual Theme & Atmosphere（视觉气质）

- **气质**：干净、克制、iOS 原生质感。颜色传达用途与状态，不做装饰。
- **底色哲学**：大面积留白 / 浅灰，靠层级与少量品牌绿点缀，而非彩色堆叠。
- **标志元素**：品牌绿 `#26D93E`；液态玻璃材质（导航条、悬浮按钮、Toast）；胶囊形按钮；0.5px 发丝分割线。
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
> **红色三分（玫红 vs 正红）**：积极强调用玫红 `feature/like #FF3B64`（点赞爱心、徽标通知红点与计数角标）；警示填充 danger/base（正红）；警示文字 danger/soft-foreground。
> 判据：**吸引注意但非警示 → 玫红；警示 / 危险 / 错误 → 正红。** 通知红点不是"危险"，不要借用 danger。

### 中性 / 文字（foreground）
| 角色 | Light | Dark | 用途 |
|---|---|---|---|
| foreground/base | `#000000` | `#FFFFFF` | 主文字/图标 |
| foreground/muted | `rgba(0,0,0,.60)` | `rgba(255,255,255,.60)` | 次要文字（达 AA；2026-08-01 由 .55 加深） |
| foreground/subtle | `rgba(0,0,0,.40)` | `rgba(255,255,255,.40)` | 辅助信息（仅小字，AA 豁免；2026-08-03 Dark 由 .35 改 .40） |
| foreground/placeholder | `rgba(0,0,0,.30)` | `rgba(255,255,255,.30)` | 输入占位 |
| foreground/disabled | `rgba(0,0,0,.20)` | `rgba(255,255,255,.20)` | 禁用文字（2026-08-01 由 浅.26/深.22 统一 .20） |
| foreground/inverse | `#FFFFFF` | `#000000` | 反色容器上的文字（随主题翻） |
| default/white | `#FFFFFF` | `#FFFFFF` | 恒白（图上叠字，不随主题翻）。样式 =「纯色 Solid/固定白 Static White」 |

> **2026-08-01「文字图标 Text&Icon/纯白 White」改名重建为「文字图标 Text&Icon/反色 Inverse #FFFFFF」**：它绑 `foreground/inverse`（Light 白 / **Dark 翻黑**），原名叫「纯白」有误导性 —— 曾导致 Foundations 色板 43 处 + Templates 1 处把它当恒定白用，深色模式下那些叠在彩色块上的标签全变黑（已全部改绑「纯色 Solid/固定白」）。
> **判据**：反色容器（黑底药丸、tinted 玻璃钮）上的文字 → `foreground/inverse`（会翻转）；彩色块 / 恒定深色块上的白字 → `default/white`（固定白）。两者不可互换。

> **2026-08-01 精简**：删掉 `foreground/emphasis`(.80)、`foreground/faint`(.15)、`foreground/ghost`(.08) 三档（含 on-dark 对应档）——梯子过密。需要极淡装饰线/遮罩块改用 `separator/base`(10%) 或 `ink/soft`·`ink/soft-pressed`(5%/15%)。

### 墨色 Ink（2026-08-01 新增）：黑色 CTA 与强调实底
| 角色 | Light | Dark | 用途 |
|---|---|---|---|
| ink/base | `#000000` | `#FFFFFF` | 黑色 CTA、强调实底（随主题翻转） |
| ink/pressed | `#2F2F34` | `#EBEBEB` | 按下（纯黑无法更深，提亮一档） |
| ink/foreground | `#FFFFFF` | `#000000` | 实底上的文字，随 base 翻转 |
| ink/soft | `rgba(0,0,0,.05)` | `rgba(255,255,255,.05)` | 极淡中性水洗底 |
| ink/soft-pressed | `rgba(0,0,0,.15)` | `rgba(255,255,255,.15)` | 浅底按下 |
| ink/soft-foreground | `#000000` | `#FFFFFF` | 浅底上的文字 |

> **与「中性 default」严格区分**：`default` 是**浅灰容器**语义（#EBEBEB，表单 secondary 档 / Kbd / Tag 底 / Chip default 都用它）；`ink` 是**黑色强调实底**。别拿 default 当黑底用，也别拿 ink 当浅灰容器用。

**foreground/on-dark**（固定白前景层级，Light=Dark 同值，**不随主题翻转**）：用于恒定深色表面上的文字/线——蒙层、媒体遮罩、深色玻璃、灵动岛。

> 档位对齐 foreground 深色列（2026-08-03 起 `foreground/subtle` 的 Dark 也改 40%，与 `on-dark/subtle` 重新等值）。

| 角色 | 值(Light=Dark) | 用途 |
|---|---|---|
| foreground/on-dark/base | `#FFFFFF` | 深底主文字 |
| foreground/on-dark/muted | `rgba(255,255,255,.60)` | 深底次要文字 |
| foreground/on-dark/subtle | `rgba(255,255,255,.40)` | 深底辅助信息（2026-08-01 由 .35 改） |
| foreground/on-dark/placeholder | `rgba(255,255,255,.30)` | 深底占位 |
| foreground/on-dark/disabled | `rgba(255,255,255,.20)` | 深底禁用 |

> 判据:文字所在表面**恒定为深**(与 app 主题无关)→用 `foreground/on-dark/*`;文字随主题翻转(普通页面)→用 `foreground/*`。切忌为此给模块单独切深色。
> **底色同理**:恒定深底用 `default/black`(恒黑),**禁用 `background/inverse` / `surface/inverse`** —— inverse 系列随主题翻转(Light 深 / Dark 白),深色下会翻成白底,叠在上面的恒白描边与 on-dark 文字全部消失。恒白描边用 `border/white`。

### 层面（background / surface / border / separator）
| 角色 | Light | Dark | 用途 |
|---|---|---|---|
| background/base | `#FFFFFF` | `#0B0B0D` | 页面底 |
| background/tertiary | `#F5F5F5` | `#060607` | 灰底 |
| background/inverse | `#000000` | `#FFFFFF` | 页面级反色底（2026-08-01 由 #18181B 改纯黑） |
| background/inverse-tertiary | `#18181B` | `#F5F5F5` | 反色页面的第二层 |
| surface/base | `#FFFFFF` | `#18181B` | 卡片/面板 |
| surface/secondary | `#F5F5F5` | `#232327` | 搜索框底 / 内嵌面 |
| surface/tertiary | `#EBEBEB` | `#2F2F34` | 三级面 |
| surface/inverse · inverse-secondary · inverse-tertiary | `#000000` · `#1C1C1F` · `#2A2A2E` | `#FFFFFF` · `#F5F5F5` · `#EBEBEB` | **反色容器三级梯子**，主要用于浅色模式下深色容器的多层级（2026-08-01 扩到三级） |
| surface/pressed | `rgba(0,0,0,.08)` | `rgba(255,255,255,.08)` | 列表/卡片按压态 |
| border/base | `#DEDEE0` | `#3A3A40` | 组件描边（1px） |
| border/avatar | `rgba(0,0,0,.03)` | `rgba(255,255,255,.05)` | **头像描边**（2026-08-01 新增）：极淡，避免白色头像糊在白底上 |
| separator/base | `rgba(0,0,0,.10)` | `rgba(255,255,255,.10)` | 常规分割线（0.5px） |
| separator/subtle | `rgba(0,0,0,.05)` | `rgba(255,255,255,.05)` | 弱分割线 |
| backdrop/base | `rgba(0,0,0,.20)` | `rgba(0,0,0,.60)` | 普通压暗遮罩 |
| backdrop/strong | `rgba(0,0,0,.60)` | `rgba(0,0,0,.75)` | 强压暗遮罩 |

### 场景专用（feature · 聊天 / 钱包）
好友气泡 `#E1FFBF`/暗 `#2E4212`；非好友气泡 `#C9FAFF`/暗 `#123C42`；已读 好友 `#58C138`、非好友 `#00BAD2`；非好友 Add 按钮 `#26D9F0`。气泡圆角 22px。

| 角色 | Light | Dark | 用途 |
|---|---|---|---|
| feature/like/base | `#FF3B64` | `#FF3B64` | **积极强调红（玫红）**：点赞爱心、徽标通知红点与计数角标（未读数 / New / 99+）。凡"吸引注意但非警示"都用它。历史命名为 like（原仅点赞用），2026-07-31 语义扩展 |
| feature/wallet/unverified | `#FD7C02` | `#F79E68` | 钱包/资产「未验证 Unverified」状态色（橙）。**仅钱包/资产场景**，不参与通用状态色 |

---

## 3. Typography Rules（排版）

- **字体**：`-apple-system, "SF Pro", "SF Pro Text", "SF Pro Display", system-ui, sans-serif`
- **字重**：**Regular 400 / Semibold 600 / Bold 700 / Heavy 800** 四种。标题与数字用 Heavy，不再用 Black 900。
- **不发明字号**：只用下表档位（10 / 12 / 14 / 16 / 20 / 24 / 28 / 36，数字另有 8）；界面里其他尺寸就近归档。

> 2026-07-31 字阶改版：Title 转 Heavy、Lg 降 28、Xs 升 16 Bold；Body 删 17/15/13；Label 删 18/13、加 10px 两档；Button 标准改 16 Bold；Scene 页头大标题降 28、导航标题与气泡改 16；Number 重建为 9 档。

| 角色 | 字号/行高 | 字重 | 用途 |
|---|---|---|---|
| Display | 36/auto | 800 | 超大标题（一页最多一个） |
| Title/Lg · Md · Sm | 28/auto · 24/auto · 20/auto | 800 | 标题层级 |
| Title/Xs | 16/auto | **700** | 最小标题、列表项标题 |
| Label/Base · Sm · Xs | 16/auto · 14/auto · 12/auto | 600 | 强调文字 |
| Label/2xs · 2xs Bold | 10/12 · 10/12 | 600 · **700** | 徽标标签 · 勋章数字 |
| Body/Base · Sm · Xs · 2xs | 16/auto · 14/auto · 12/auto · 10/12 | 400 | 正文 |
| Link/Base · Sm | 16/24 · 14/20 | 600 | 链接（色 foreground/link） |
| Field/Base · Sm | 16/24 · 14/20 | 400 | 输入框文字/占位 |
| Button/Base | 16/22 | **700** | 标准按钮文字 |
| Button/Sm | 14/20 | 600 | 小按钮、文字按钮 |
| Number（9 档） | 36/42 · 28/34 · 20/24 · 16/20 · 14/18 · 12/16 · 10/12 | 800 | 计数 / 金额 / 统计 |
| Number/24 | 24/28 | **700** | 卡片内金额与计数、验证码数字位（2026-08-01 由 800 改 700） |
| Number/8 | 8/10 | **700** | 极小角标（最小档） |
| Scene 页头大标题 | 28/34 | 800 | 页面头部（首字大写） |
| Scene 导航标题 · 气泡正文 | 16/20 · 16/20 | 700 · 400 | 导航栏居中标题 · IM 气泡 |
| Scene 列表项 | 14/17 | 600 | 设置/资料页列表项 |

> Number 与 Title 在 20/24/28/36 上字号字重相同但语义不同：**Number 专供数字**，Title 用于文本标题，勿混用。
> 原「Scene 页头Tab 选中 24 Black / 未选中 18 Bold」已删——NavBar Brand-Tabs 改版后 tab 统一 14 Semibold，选中靠字色 + 下划线。

---

## 4. Component Stylings（组件 · 含状态）

### 按钮 Button（8 变体 × 3 尺寸）
- 尺寸：sm 高 32 圆角 16 / md 高 36 圆角 round / lg 高 48 圆角 round；文字 Button 角色。
- 变体（底色 + 文字，**必须同状态组配对，换底色文字联动**）：
  - primary：accent/base + accent/foreground(白)
  - secondary：default/base(灰) + accent/soft-foreground(绿字)
  - tertiary：default/base + default/foreground(黑)
  - outline：透明 + border/base 描边 + default/foreground
  - ghost：透明 + default/foreground
  - danger：danger/base + 白字
  - dangerSoft：灰底(default/soft) + danger/soft-foreground(深红字)
  - **ink（2026-08-01 新增）：ink/base 黑底 + ink/foreground 白字**；按下 ink/pressed。深色模式自动翻成白底黑字。用于需要比 primary 更中性、比 tertiary 更强的黑色 CTA
- 状态：default / pressed（换 *-pressed 底）/ disabled（整体 opacity .5）。移动端无 hover。触控热区 ≥44。

### Toast
胶囊形（343×66），底为**液态玻璃材质**（见第 6 节），图标+文字一律中性 foreground/base（不用状态色）。位置固定屏幕顶部、距顶 60px 居中；点击触发、显示 3 秒淡入淡出。

### 输入框 Input / InputGroup / InputOTP / Checkbox（统一形态，2026-08-01 定稿）
**浅灰底 + 无描边**，适配白色背景：底 `surface/secondary`(#F5F5F5，与搜索框同底)，稍深一档用 `default/base`(#EBEBEB)。
高度统一 **48**；圆角 **`radius/3xl`(24)**（2026-08-01 由 12 改；48 高 + 24 圆角 = 胶囊形）；占位 `foreground/placeholder`；文字 Field 角色（16/24）。
**常态不要描边** —— 之前的「白底 + 浅灰描边」是为灰底页面设计的反差方案，而产品以白色场景为主，白底白框等于看不见。
描边只表达**状态**：focus 用 `accent/base`、error 用 `danger/base`（1px inset，不挤布局）；disabled 整体 opacity 50%。
前后缀与输入区**同底**，靠 `separator/base` 竖线分隔，不用色块区分。多选框同为浅灰底无描边（16×16，勾选转 `accent/base`）。
**验证码 InputOTP 两式**：① **分离式**（六格并排）单格 46×48、**圆角仍为 `radius/md`(12)**（24 圆角会把 46×48 的格子吃成圆形，是有意的例外），**空格灰底无描边，一有内容就翻白底 `surface/base` + 1px 描边**（filled 用 `border/base`、focus 用 `accent/base` 加发光环、error 用 `danger/base`）——"已填 / 未填"用底色区分比用描边直观，这是刻意与其他控件不同。② **合并式**（单框）一个灰底容器高 48、圆角 **`radius/3xl`(24)**、左右内距 24、槽距 8，内含 6 个 16 宽居中槽位：已输入=数字 24 Bold `foreground/base`，未输入=**12×2px 短线** `foreground/placeholder`（用线，不用「–」字形——字形在 24px 下太粗；线宽取 `border/width-strong`=2，1px 显细）；**容器恒灰底不翻白**，只有 focus（`accent/base`）/ error（`danger/base`）上 1px 描边。配系统数字键盘、不需要逐格点选时用。

### 页头 NavBar（透明底 375×58，内容行 42，从状态栏下沿拼页；4 变体）
① Brand：大标题（Scene 28 Heavy）+ 可选右侧 42px 玻璃圆钮。② Brand-Tabs（2026-07-31 改版）：左搜索圆钮 + 居中 tabs + 右加号圆钮；tab 统一 14 Semibold，选中=主文字色 + 下方 24×2 下划线，未选中=muted，间距 20；5 个 tab 槽默认全显示、用不到的隐藏，超宽时两端渐隐截断。③ Nav-Center：左返回 42 + 绝对居中标题 16 Bold（Scene 导航标题）+ 右侧 42 常驻占位（保居中，不受动作显隐影响）。④ Nav-Chat：返回 + 头像 36（兜底 surface/secondary）+ 昵称 16 Bold + 副标题 12 muted（Body/Xs）+ 右侧 1–2 个 42 圆钮。圆钮一律 Button-Liquid-Glass-Symbol(42)，禁手绘；一级页页头不放返回按钮。**Scroll Edge（顶部渐隐模糊）= 半透明磨砂底（feature/nav-background ≈66%）+ backdrop-blur + 向下线性渐隐**，不是不透明纯白；状态栏须悬浮透明、内容滚到其下，才呈现 iOS 沉浸式的"内容从状态栏背后模糊滑过"。

### 底部导航 TabBar
玻璃胶囊（Liquid Glass Regular Small；高 62=4+54+4、左右边距 8、圆角 round）；五 tab **Chat / Discover / AI / Mix / Me**（2026-08-13 定稿：video 频道移除、AI 居中第 3 位）；图标槽 32/字形 24；**激活位单选互斥 = accent/soft-subtle(8%) 底 + accent/base 图标；未激活 = 透明底 + foreground/base 图标**（旧「accent 底白图 / subtle 40%」作废）；**恒带底部文字**（10/12，激活字色 accent；无文字形态已下线，Figma 组件 Label 轴已删）；**AI 位是徽章不是普通图标**：40×30 绿胶囊（`.ai-badge`，foreground/brand 底 + accent/foreground 字形，圆角 round），两种状态恒绿、只有标签随激活变色，激活胶囊照常从徽章后面滑过（对应 Figma 私有组件 `_TabBar Item AI`）；底部模糊用 Scroll Edge Soft(Edge=Bottom)，半透明磨砂底（feature/nav-background）+ backdrop-blur + 向上渐隐，勿手动叠层、勿用不透明纯白。**图标只用本地内置图标库（icons-bundled.json），禁止走 CDN**——底部导航是每页常驻元素，不能有离线/预览缺图的风险，CDN 长尾图标只给非导航区域用。**且只能用图标库里 `tab-` 前缀的专用标签栏图标**（默认组合 `tab-chat`/`tab-discover`/`tab-ai`/`tab-mix`/`tab-me`，各配 `-fill` 面性变体，未激活线性、激活切 fill + accent 着色；`tab-video` 仍内置备用但已不在默认频道；`tab-ai` 字形 2026-08-13 换新为 Ai✦ 徽章字形，且 AI 频道用徽章形态不走线/面切换），**不许拿普通图标（house/comments/person 等）顶替**；除非用户特殊要求，tab 图标只在这组 tab 图标里选。

**默认套用**：任何页面只要有页头或底部导航，NavBar / TabBar 都**默认**直接照搬本规范整套写法与效果（含 Scroll Edge、玻璃材质、激活态着色），不需要用户特别点名要求；只有用户明确要求不同效果时才偏离。

**Android 通栏形态**（Figma 组件 `Platform=Android`）：375×68 = 56 栏体 + 12px 底部系统导航安全间距（绑 size/12），surface/base 底、直角、无玻璃，选中指示条 70×48 r26 绑 accent/soft-subtle，图标 28、AI 徽章 36×27。skill 原型默认 iOS 形态，Android 仅在用户点名安卓时使用（skill 暂无现成类，按上述参数手写）。

**切换微动效**（默认必带，iOS 原生风，参考 iOS 26）：①**激活底板滑动（还原 iOS 26 TabBar 选中胶囊）**——激活色块用一个共享指示条平滑滑到选中 tab，手感克制：小幅方向性拉伸（前缘先到、后缘略滞后，封顶不横跨整条）+ spring 回弹落位（cubic-bezier(.34,1.3,.64,1)，300ms），**不是每 tab 各自 toggle 背景硬切、也不是夸张橡皮筋横跨**；②图标轻弹 pop（scale .82→1.08→1，近似 SF Symbol bounce）；③新屏轻推淡入（opacity + translateY(6px)，180ms）。跨屏切换时各放一次、同屏不重放，底板滑动可打断，`prefers-reduced-motion` 退化为纯淡入。除非用户要求瞬切才去掉。详见 motion.md。

### 灵动岛 Dynamic Island
**每个项目默认都要带灵动岛**，作用是让设计师在预览里一键切换系统/浅色/深色三态自测深浅色表现。黑底白字、`position:absolute` 锚在状态栏中间、不占布局。分两型：**A 型**（多状态页，药丸展开成状态切换菜单 + 外观图标）、**B 型**（静态页，药丸本身就是外观开关，点击循环 系统/浅/深）。**除非用户明确要求去掉（如说"去掉灵动岛"），否则任何情况下都不得省略**，包括"最终交付版"——交付时最多去掉 A 型的多状态演示菜单，外观切换本体必须保留。

### 列表 List / 卡片 Card
行高 ≥56、图标 24、标题 Label/Base、右 chevron；组内 0.5px separator/base 左缩进；卡片 surface/base 圆角 lg(16)、无阴影（靠层级色区分）。

### 头像 Avatar（2026-08-15 改版：圆形 → 大圆角方形）
**头像一律大圆角方形，不再用圆形。** 形状 = **标准圆角矩形，平滑度 0**（不是 iOS squircle —— 实测设计基准就是普通圆角矩形，别加 cornerSmoothing）。

**圆角随尺寸走「≈ 尺寸 × 5/12」（41.7%），就近归入 `radius/*` 档**（不发明档位）：

| 头像尺寸 | 5/12 理论值 | 实用档位 |
|---|---|---|
| 24 / 26 / 32 | 10 / 10.8 / 13.3 | `radius/md` (12) |
| 36 | 15 | `radius/lg` (16) |
| 48 | 20 | `radius/xl` (20) |
| 56 | 23.3 | `radius/3xl` (24) |
| 68 | 28.3 | `radius/4xl` (28) |

> **36px 基准档用 `radius/lg`(16)**：设计基准实测是 15，但阶梯里 12→16 之间是空的，取最近的 16（45° 处差 0.4px，肉眼不可辨）。**不要为此新增 15 档。**
> **例外：Button 不跟这条。** 圆形加号按钮（如 AvatarGroup 末尾的「+」）是 Button 组件，按钮规范就是 `round`，不要为了和头像一致去改它。
> 描边用 `border/avatar`（极淡），避免白色头像糊在白底上。

### 图标
用 ZymixUI 图标库（单色 currentColor，跟随文字色），npm `@zymix-ui/icons` 或 CDN `cdn.jsdelivr.net/gh/zymix-ui/zymix-icons`。禁止手绘不一致的图标。**底部导航（TabBar）图标例外：只用本地内置图标，不用 CDN**——CDN 依赖网络，导航是常驻元素不能有缺图风险；CDN 仅用于非导航场景的长尾图标。

---

## 5. Layout Principles（布局）

- **间距刻度**（size token，px）：0 4 6 8 12 16 20 24 28 32 36 40 44 48 56 64 72 96 128。页面左右边距通常 16。
- **圆角刻度**（radius）：none 0 · xs 6 · sm 8 · md 12 · lg 16 · xl 20 · 2xl 22 · 3xl 24 · 4xl 28 · 5xl 32 · 6xl 36 · round 9999。
- **画布**：iPhone 375 宽；内容单列纵向滚动；卡片/组卡分区。
- **基准规则**（2026-07-10）：尺寸均 1x 逻辑 pt，与画布无关；组件宽度一律「左右边距 + 拉伸」，**禁写死画布衍生固定宽**（Toast 343、底导 360 属遗留待治理）；375 仅协作约定，大屏走查用 402/440；玻璃按钮 48=lg 玻璃版、42=玻璃圆钮(NavBar/TabBar)。
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

## 6.5 Motion（动效 · 平台中立）

> 动效 token 平台无关，同一套值映射 Web(CSS) 与 iOS(SwiftUI)。

- **该不该动**：高频/键盘操作（100+次/天）永不加动画；偶发（模态/抽屉/Toast）标准动画；罕见/首次可加惊喜。每个动画都要有明确目的（反馈/空间一致/避免突兀），不为"酷"而动。
- **缓动**：入场/退场用强 ease-out `cubic-bezier(0.23,1,0.32,1)`；屏内移动用 ease-in-out `cubic-bezier(0.77,0,0.175,1)`；抽屉用 `cubic-bezier(0.32,0.72,0,1)`。**UI 禁用 ease-in**（起步慢=迟钝）。
- **时长**（UI 铁律 ≤300ms）：按压 120ms、下拉/tooltip 180ms、模态/抽屉 400ms（退场更快）。
- **弹簧**（拖拽/可打断手势）：Apple 语义 `duration + bounce`，直接对应 SwiftUI `.spring(duration:bounce:)`；bounce 保守 0.1-0.3。
- **组件**：可按压元素按下 `scale(0.97)`；禁从 `scale(0)` 入场（用 `scale(0.95)+opacity`）；弹层从触发点缩放（模态除外，居中）。
- **性能**：只动 `transform`/`opacity`；动态 UI 用可打断的 transition，不用 keyframe；禁 `transition:all`。
- **无障碍**：`prefers-reduced-motion` 下去掉位移、保留透明度/颜色。
- **iOS 映射示例**：`.timingCurve(0.23,1,0.32,1, duration:0.2)`、`.spring(duration:0.5, bounce:0.2)`、`.scaleEffect(pressed ? 0.97 : 1)`。

---

## 7. Do's and Don'ts（守则）

**Do**
- 颜色/字号/圆角/间距一律用上面的角色与刻度。
- 按钮文字色随所在状态组的 foreground 走。
- 分割线 0.5px，强分割 1px；触控热区 ≥44。
- 深浅色只靠语义变量，交付前脑内过一遍深色（不许黑底黑字）。
- 图片/媒体容器给兜底底色（surface/secondary 或品牌渐变），图挂也不空。
- 默认给每个项目带上灵动岛（外观切换），除非用户明确要求去掉。
- NavBar / TabBar 默认整套套用模板效果（含 Scroll Edge），不用等用户点名。

**Don't**
- ❌ 写死 hex / rgba（除媒体遮罩渐变）。
- ❌ 自造字号字重（如标题 22px）；就近归档。
- ❌ 用传统卡片投影堆层级。
- ❌ Toast 用红绿状态色 / 放页面中部。
- ❌ 手绘风格不一的图标。
- ❌ 没有用户明确要求就拿掉灵动岛。
- ❌ TabBar（底部导航）图标走 CDN——必须用本地内置图标。
- ❌ TabBar 用普通图标顶替——只用 `tab-` 前缀的专用标签栏图标（除非用户特殊要求）。

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
