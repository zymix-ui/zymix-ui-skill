# ZymixUI 用色规则(铁律)

变量在 tokens.css,规则决定用哪个变量。

## 按钮文字用色铁律
按钮上的文字/图标颜色必须用**所在状态组的 foreground**,禁止用 foreground-base/muted 等通用色:
- 实心主色按钮: bg=--accent-base + 文字=--accent-foreground
- 浅底主色按钮: bg=--accent-soft + 文字=--accent-soft-foreground
- 危险按钮: bg=--danger-base + 文字=--danger-foreground;浅底: --danger-soft + --danger-soft-foreground
- 中性按钮: bg=--default-base + 文字=--default-foreground
- 黑色 CTA: bg=--ink-base + 文字=--ink-foreground(深色模式自动翻白底黑字);按下 --ink-pressed
- 按下态换 pressed/soft-pressed 底,文字不变
这样换按钮底色时文字自动配对联动。

## accent 与 success 同为品牌绿,按语义分流
元素"让你去做"(按钮/选中/进度/链接)→accent;"告诉你结果"(Toast/校验通过/完成/到账)→success。拿不准用 accent。

## 恒定深色面上的文字用 foreground/on-dark(不用会翻转的 foreground)
蒙层、媒体遮罩、深色玻璃、灵动岛这类**表面恒为深**(与 app 主题无关)的地方,文字/线用 `--foreground-on-dark-*`(固定白层级:base/muted/subtle/placeholder/disabled,档位对齐 foreground 深色列;2026-08-01 已删 emphasis/faint/ghost 三档,subtle 两侧均 40%)。**禁止**用会随主题翻转的 `--foreground-*`(浅色模式下会变黑、在深底上消失),也不要为此把模块单独切深色。需要白色半透明(分割线等)也用它,别写裸 rgba。

**底色同理:恒定深底用 `--default-black`(恒黑),禁止用 `--background-inverse` / `--surface-inverse`** —— inverse 系列的定义就是"随主题翻转"(Light 深 / Dark 白),深色模式下会翻成白底,叠在上面的恒白描边与 on-dark 文字全部消失。描边用 `--border-white`(恒白)。

## 红色三分:玫红管积极,正红管警示
判据:**吸引注意但非警示→玫红;警示/危险/错误→正红。**
- 积极强调(玫红 #FF3B64)→`--feature-like-base`:点赞爱心、徽标**通知红点与计数角标**(未读数/New/99+)。通知红点不是"危险",别借用 danger。
- 警示填充(正红)→`--danger-base`
- 警示**文字/图标**→`--danger-soft-foreground`(danger-base 做文字对比度不达 AA,红色以文字形态出现必须用深红)

**徽标一律玫红,不用绿色。** 未读数、New、99+、纯红点全部 `--feature-like-base` + 恒白字(`--default-white`,玫红 Light=Dark 同值,不能用会翻转的 foreground)。徽标**没有 danger 语义** —— 徽标上的红是通知提醒,不是错误警示;警示归按钮 / Toast / 表单校验。

`feature/like` 是历史命名(原仅点赞用),2026-07-31 语义已扩展为通用积极强调红;**颜色样式名 2026-08-01 已改为「产品特性 Feature/积极强调 Positive」**,变量名保留。

## 文字梯子(foreground,2026-08-01 精简为 5 档)
base 主文字(纯黑/白)→**muted 60%** 次文字→subtle 40% 辅助(仅限辅助信息)→placeholder 30% 占位→**disabled 20%** 禁用。
> 2026-08-01 删掉 **emphasis 80%**、**faint 15%**、**ghost 8%** 三档(含 on-dark 对应档):梯子过密、实际用不到那么多层。muted 由 55% 加深到 60%,disabled 由「浅 26% / 深 22%」统一为 20%。
> 需要极淡的装饰线/遮罩块(原 faint/ghost 的场合)→用 `--separator-base`(10%) 或 `--ink-soft` / `--ink-soft-pressed`(5% / 15%)。

链接→--foreground-link;品牌绿文字→--foreground-brand;反色容器(黑底药丸等)上的文字→--foreground-inverse,不要用 --default-white。

> **反过来也成立**:**彩色块 / 恒定深色块上的白字要用 `--default-white`(固定白),不要用 `--foreground-inverse`** —— inverse 在深色模式会翻成黑。
> 2026-08-01 把「文字图标 Text&Icon/纯白 White」**改名重建为「文字图标 Text&Icon/反色 Inverse #FFFFFF」** —— 原名叫「纯白」却绑 `foreground/inverse`(会翻转),害 Foundations 色板 43 处误用成恒白、深色下标签全变黑(已改绑「纯色 Solid/固定白」)。Button 玻璃钮里 8 处直绑变量的层也已改绑这个新样式。

## 墨色 Ink(2026-08-01 新增):黑色 CTA 与强调实底
| token | 值 | 用途 |
|---|---|---|
| `--ink-base` | 浅 #000 / 深 #FFF | 黑色 CTA、强调实底(随模式翻转) |
| `--ink-pressed` | 浅 #2F2F34 / 深 #EBEBEB | 纯黑无法更深,按下提亮一档 |
| `--ink-foreground` | 浅 #FFF / 深 #000 | 实底上的文字,随 base 翻转 |
| `--ink-soft` | 5% | 极淡中性水洗底 |
| `--ink-soft-pressed` | 15% | 浅底按下 |
| `--ink-soft-foreground` | 浅 #000 / 深 #FFF | 浅底上的文字 |

**与「中性 Default」严格区分**:Default 是**浅灰容器**语义(#EBEBEC 底,表单 secondary 档、Kbd、Tag 底、Chip default 都用它);Ink 是**黑色强调实底**。别拿 Default 当黑底用,也别拿 Ink 当浅灰容器用。

## 层面
- 页面背景: --background-base;灰层 tertiary(#F5F5F5)。**2026-08-01 删掉 --background-secondary(雪白 #FCFCFC)** —— 与 base 太近,页面底一律用 base,要灰底页用 tertiary
- 容器表面梯子(单调递进): --surface-base 卡片 → secondary 搜索框底/内嵌面 → tertiary 三级
- 按压反馈: --surface-pressed(8% 叠加);反色容器(选中 tab 黑药丸): --surface-inverse;玻璃钮底: --surface-glass
- **浅色模式下的深色容器多层级**(2026-08-01 新增): --surface-inverse → --surface-inverse-secondary → --surface-inverse-tertiary;页面级用 --background-inverse(**已由 #18181B 改纯黑**)→ --background-inverse-tertiary
- 消息列表置顶行背景=--surface-secondary,普通行=--surface-base

## 线
- 常规分割线: 0.5px --separator-base(10%);弱 --separator-subtle(5%)。**2026-08-01 删掉 --separator-strong(40%)** —— 原「强分割/统计分栏竖线」改用 --separator-base;需要更明显的分栏用 --border-base
- 组件描边: 1px --border-base;弱描边 --border-subtle;**头像描边 --border-avatar**(浅黑3%/深白5%,避免白色头像糊在白底上);恒白描边 --border-white

## IM 场景专用色
好友气泡 --feature-im-bubble-friend + 文字 --feature-im-bubble-friend-foreground(次要信息 bubble-friend-muted);
非好友气泡 bubble-stranger + bubble-stranger-foreground;非好友 Add 按钮 --feature-im-add-stranger;
客态气泡(对方消息)--feature-im-bubble-guest(= surface/secondary)+ 文字 --foreground-base;
已读回执:好友 --feature-im-read-friend,非好友 --feature-im-read-stranger。
气泡圆角 22px(--radius-2xl)。

## 底部导航
玻璃底 --feature-nav-background + backdrop-filter:blur(20px)。**旧的 fade 渐变遮罩(--feature-nav-fade-*)已作废并删除** —— 顶/底模糊改用 Scroll Edge / ProgressiveBlur,见 patterns.md。

## 状态约定
- disabled: 组件整体 opacity:0.5(不改颜色变量),文字级禁用用 --foreground-disabled
- 触控热区 ≥44px(视觉小于 44 的加透明热区)
- 对比度: 正文 AA(4.5:1);绿底/橙底白字仅限大字号或图标;subtle 40% 仅限辅助信息
