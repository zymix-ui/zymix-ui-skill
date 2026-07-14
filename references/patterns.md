# ZymixUI 界面惯例(ZYMIX 产品长相)

ZYMIX 是 iOS 风格的社交/IM 产品。原型按 iPhone 375×812 画布(设计稿基准尺寸)。

## 基准规则(2026-07-10)
- 所有尺寸为 1x 逻辑 pt,与画布宽度无关。
- 组件宽度一律「左右边距 + 拉伸」定义,**禁止写死画布衍生固定宽**(Toast 343、底导 360 属历史遗留待治理)。
- 375 画布仅协作约定;大屏走查用 402 / 440 验证拉伸。
- Apple 402 kit(iOS 26/Liquid Glass)控件尺寸仅作形态参考,产品尺寸以线上 375 实测为准。
- 玻璃按钮两档均产品自有:48 = 按钮 lg 档玻璃版(特殊场景);42 = 玻璃圆钮(NavBar/TabBar 专用)。

## 页面骨架
- 状态栏: 9:41 + 信号/WiFi/电池(黑色图标,深色模式白色),高 47px(含刘海区)
- NavBar 顶部导航(透明底 375×58,内容行 42,从状态栏下沿拼页),4 变体:Brand(34 Black 大标题+可选右侧 42 玻璃圆钮)/ Brand-Tabs(选中24 Black+未选中18 Bold muted,间距20)/ Nav-Center(左返回42+绝对居中17 SB标题+右侧42常驻占位保居中)/ Nav-Chat(返回+头像36+昵称17SB+副标题13 muted+右侧42圆钮)。圆钮=Button-Liquid-Glass-Symbol(42),禁手绘;一级页页头不放返回按钮
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
- 底部 TabBar: 玻璃胶囊(高 62=4+54+4,左右边距 8,圆角 round),五 tab Chat/Mix/Video/Discover/Me,图标槽 32/字形 24;激活位单选互斥 = accent/soft-subtle(8%)底 + accent/base 图标,未激活 = 透明底 + foreground/base 图标(旧「accent 底白图/subtle 40%」作废);底部模糊已内置 .tabbar::before(等效 Show Scroll Edge;.no-edge 关),勿再叠 .nav-fade(已删)

## 图标
**只用 ZymixUI 图标库**(`references/icons-bundled.json` / Figma 导出),内联为 SVG,用 currentColor 继承文字色。**严禁手绘 / 几何拼凑自造任何图标 SVG**(仅状态栏系统 chrome:信号/WiFi/电池例外)。库里没有的图标,回报缺失、勿硬造。

## 骨架标配(每页必带)
- **移动端满屏**:`@media (max-width:440px){body{padding:0}.phone{width:100vw;height:100dvh;border-radius:0;box-shadow:none}}`——手机上铺满、无桌面舞台留白与边框。
- **隐藏原生滚动条**:滚动容器 `.screen{scrollbar-width:none}` + `.screen::-webkit-scrollbar{display:none}`;需要滚动反馈时用悬浮指示条 `.scroll-ind`(绝对定位、不占布局宽、滚动时淡入),参考 `assets/templates/discover.html`。
- **去点按闪色**:`html{-webkit-tap-highlight-color:transparent}`,交互元件不出现移动端默认高亮块。
- 以上 base 骨架 `assets/template.html` 已内置,套模板即自带。
