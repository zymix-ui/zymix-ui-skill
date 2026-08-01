# ZymixUI 文字角色速查

字体一律 SF Pro:`font-family:-apple-system,"SF Pro","SF Pro Text","SF Pro Display",system-ui,sans-serif`。
在用字重四种:**Regular(400) / Semibold(600) / Bold(700) / Heavy(800)**。标题与数字用 Heavy,不再用 Black。
不要发明新字号——下表没有的组合就近归入最接近的角色。行高 `auto` 表示交给字体默认(CSS 不写 line-height)。

> 2026-07-31 字阶改版:Title 全面转 Heavy 且 Lg 降到 28、Xs 升到 16 Bold;Body 删 17/15/13;Label 删 18/13 并加 10px 两档;Button 标准改 16 Bold;Scene 页头大标题降到 28、导航标题与气泡改 16;Number 重建为 9 档阶梯。

## 标题 Title

| 角色 | 字号/行高 | 字重 | 用途 |
|---|---|---|---|
| Display | 36/auto | Heavy | 超大标题(一页最多一个) |
| Title/Lg | 28/auto | Heavy | 大标题、一级内容标题 |
| Title/Md | 24/auto | Heavy | 中标题 |
| Title/Sm | 20/auto | Heavy | 小标题、卡片标题 |
| Title/Xs | 16/auto | **Bold** | 最小标题、列表项标题 |

## 正文 Body

| 角色 | 字号/行高 | 字重 | 用途 |
|---|---|---|---|
| Body/Base | 16/auto | Regular | 默认正文,长文本与描述 |
| Body/Sm | 14/auto | Regular | 次级信息、说明文字 |
| Body/Xs | 12/auto | Regular | 辅助信息、高密度 UI |
| Body/2xs | 10/12 | Regular | 极小文字,仅极端密度 |

## 强调 Label

| 角色 | 字号/行高 | 字重 | 用途 |
|---|---|---|---|
| Label/Base | 16/auto | Semibold | 标准强调、表单标题 |
| Label/Sm | 14/auto | Semibold | 小强调、状态文字、操作入口 |
| Label/Xs | 12/auto | Semibold | 最小强调、高密度场景 |
| Label/2xs | 10/12 | Semibold | **徽标与标签**内文字 |
| Label/2xs Bold | 10/12 | **Bold** | **勋章数字** |

## 链接 / 输入 / 按钮

| 角色 | 字号/行高 | 字重 | 用途 |
|---|---|---|---|
| Link/Base · Sm | 16/24 · 14/20 | Semibold | 链接(跳转);颜色 `--foreground-link` |
| Field/Base · Sm | 16/24 · 14/20 | Regular | 输入框内文字/占位 |
| Button/Base | 16/22 | **Bold** | 标准按钮文字 |
| Button/Sm | 14/20 | Semibold | 小按钮文字、文字按钮(无底色可点击,如 See translation) |

## 数字 Number(9 档阶梯)

计数、金额、统计数字专用。除最小档外全部 Heavy;字号越小行高越紧。

| 角色 | 字号/行高 | 字重 | 用途 |
|---|---|---|---|
| Number/36 | 36/42 | Heavy | 资产总额等主视觉数字 |
| Number/28 | 28/34 | Heavy | 卡片内主要金额 |
| Number/24 | 24/28 | Heavy | 卡片内金额与计数 |
| Number/20 | 20/24 | Heavy | 列表内金额与计数 |
| Number/16 | 16/20 | Heavy | 常规计数 |
| Number/14 | 14/18 | Heavy | 紧凑计数 |
| Number/12 | 12/16 | Heavy | 密集列表计数 |
| Number/10 | 10/12 | Heavy | 角标计数 |
| Number/8 | 8/10 | **Bold** | 极小角标(最小档) |

> 数字阶梯与 Title 在 20/24/28/36 上字号字重相同,语义不同:**Number 专供数字**(计数、金额、统计),Title 用于文本标题。别混用。

## 场景 Scene 专属(带首字大写 `text-transform:capitalize`)

| 角色 | 字号/行高 | 字重 | 用途 |
|---|---|---|---|
| 页头大标题 | 28/34 | Heavy | 页面头部大标题(如 ZYMIX 用全大写 logo 字) |
| 导航标题 | 16/20 | **Bold** | 导航栏居中标题(iOS 惯例) |
| 气泡正文 | 16/20 | Regular | IM 聊天气泡内文字 |
| 列表项 | 14/17 | Semibold | 设置/资料页列表项标题 |

> 原「页头Tab选中 24 Black / 未选中 18 Bold」两档已删除 —— NavBar Brand-Tabs 改版后 tab 统一用 `Label/Sm`(14 Semibold),选中靠字色 + 下划线区分,不再靠字号字重。
