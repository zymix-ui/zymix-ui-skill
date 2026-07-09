# ZymixUI 界面惯例(ZYMIX 产品长相)

ZYMIX 是 iOS 风格的社交/IM 产品。原型按 iPhone 390×844 画布。

## 页面骨架
- 状态栏: 9:41 + 信号/WiFi/电池(黑色图标,深色模式白色),高 47px(含刘海区)
- 页头两种: ①品牌页头「ZYMIX」34 Black 大标题+右侧圆形操作钮(44px,--surface-secondary 底);②导航栏页头:居中 17 Semibold 导航标题+左返回箭头
- 搜索框: 胶囊形(--radius-round),--surface-secondary 底,占位文字 --foreground-placeholder,内有 16px 放大镜图标
- Home indicator: 底部 134×5px 圆条 --foreground-base

## 列表
- 行高 ≥64px,头像 48px 圆形,标题 列表项角色(14 Semibold),副文字 Body/Sm + --foreground-muted
- 行间分隔线 0.5px --separator-base,左缩进对齐文字起点
- 时间戳/badge 靠右,Body/Xs + --foreground-subtle
- 未读徽标: --accent-base 圆形,白字 11px

## IM 聊天页
- 对方消息靠左,自己靠右;气泡 max-width 70%,padding 10px 16px,圆角 22
- 好友会话用 friend 组色,陌生人会话用 stranger 组色(详见 color-rules.md)
- 底部输入条: 胶囊形 --surface-secondary,配 + 号和发送按钮
- 已读回执: 小对勾 + read-friend/read-stranger 色

## 按钮
- 主按钮: 高 48-56px,胶囊(--radius-round),--accent-base 底 --accent-foreground 白字 17 Semibold
- 次按钮: --accent-soft 底 --accent-soft-foreground 字
- 小按钮: 高 36px,14 Semibold
- 文字按钮: 无底色,15 Semibold,颜色跟场景状态组

## 弹层/卡片
- 卡片: --surface-base 底,圆角 12-16,无阴影(阴影体系已废弃),靠层级色区分
- 模态: 遮罩 --backdrop-base,面板 --surface-base 圆角 24+ 顶部圆角
- 底部导航: 玻璃底见 color-rules.md,图标 24px,选中 --foreground-base,未选中 --foreground-subtle

## 图标
线性图标为主,stroke 1.5-2px,用 currentColor 继承文字色。原型里用内联 SVG 画简单几何图标,不要引外部图标库。
