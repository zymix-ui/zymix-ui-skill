# ZymixUI 用色规则(铁律)

变量在 tokens.css,规则决定用哪个变量。

## 按钮文字用色铁律
按钮上的文字/图标颜色必须用**所在状态组的 foreground**,禁止用 foreground-base/muted 等通用色:
- 实心主色按钮: bg=--accent-base + 文字=--accent-foreground
- 浅底主色按钮: bg=--accent-soft + 文字=--accent-soft-foreground
- 危险按钮: bg=--danger-base + 文字=--danger-foreground;浅底: --danger-soft + --danger-soft-foreground
- 中性按钮: bg=--default-base + 文字=--default-foreground
- 按下态换 pressed/soft-pressed 底,文字不变
这样换按钮底色时文字自动配对联动。

## accent 与 success 同为品牌绿,按语义分流
元素"让你去做"(按钮/选中/进度/链接)→accent;"告诉你结果"(Toast/校验通过/完成/到账)→success。拿不准用 accent。

## 恒定深色面上的文字用 foreground/on-dark(不用会翻转的 foreground)
蒙层、媒体遮罩、深色玻璃、灵动岛这类**表面恒为深**(与 app 主题无关)的地方,文字/线用 `--foreground-on-dark-*`(固定白层级:base/muted/subtle/placeholder/disabled/faint/ghost,对齐 foreground 深色列)。**禁止**用会随主题翻转的 `--foreground-*`(浅色模式下会变黑、在深底上消失),也不要为此把模块单独切深色。需要白色半透明(分隔线等)也用它,别写裸 rgba。

## 红色三分
点赞爱心→--feature-like-base(情感色);危险按钮填充→--danger-base;危险**文字/图标**→--danger-soft-foreground(danger-base 做文字对比度不达 AA,红色以文字形态出现必须用深红)。

## 文字梯子(foreground)
base 主文字(纯黑/白)→muted 55% 次文字→subtle 40% 辅助(仅限辅助信息)→placeholder 30% 占位→disabled 26% 禁用→faint 15% 极弱→ghost 8% 最弱。
链接→--foreground-link;品牌绿文字→--foreground-brand;反色容器(黑底药丸等)上的文字→--foreground-inverse,不要用 --default-white。

## 层面
- 页面背景: --background-base;雪白层 secondary(#FCFCFC);灰层 tertiary(#F5F5F5)
- 容器表面梯子(单调递进): --surface-base 卡片 → secondary 搜索框底/内嵌面 → tertiary 三级
- 按压反馈: --surface-pressed(8% 叠加);反色容器(选中 tab 黑药丸): --surface-inverse;玻璃钮底: --surface-glass
- 消息列表置顶行背景=--surface-secondary,普通行=--surface-base

## 线
- 常规分隔线: 0.5px --separator-base(10%);强分隔(统计分栏竖线): 1px --separator-strong(40%)
- 组件描边: 1px --border-base;弱描边 --border-subtle

## IM 场景专用色
好友气泡 --feature-im-bubble-friend + 文字 --feature-im-bubble-friend-foreground(次要信息 bubble-friend-muted);
非好友气泡 bubble-stranger + bubble-stranger-foreground;非好友 Add 按钮 --feature-im-add-stranger;
已读回执:好友 --feature-im-read-friend,非好友 --feature-im-read-stranger。
气泡圆角 22px(--radius-2xl)。

## 底部导航
玻璃底 --feature-nav-background + backdrop-filter:blur(20px);列表滚入导航区用 fade 渐变遮罩(--feature-nav-fade-solid → fade-transparent)。

## 状态约定
- disabled: 组件整体 opacity:0.5(不改颜色变量),文字级禁用用 --foreground-disabled
- 触控热区 ≥44px(视觉小于 44 的加透明热区)
- 对比度: 正文 AA(4.5:1);绿底/橙底白字仅限大字号或图标;subtle 40% 仅限辅助信息
