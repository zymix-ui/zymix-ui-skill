# 还原经验笔记(每次按设计稿 1:1 还原后追加,做同类页面先读这里)

## 总原则
- **给了设计稿 → 1:1 还原**(量准每个圆角/描边/缩进/字重,不是"功能差不多");**没给设计稿 → 按规范自由发挥**。
- 还原前先在 Figma 里量:圆角(注意四角可能不对称)、描边宽、块间距、文字样式名、图标形状。目测截图会骗人。
- **做完必回头逐项对比设计稿自检**(圆角/间距/字重/图标/行宽核算),对不上就修,不要等用户指出。

## 需求获取(生成前置,通用流程)
先判断输入类型再定策略:
- **规范源**(本系统 Figma 稿)→ 1:1 还原样式
- **意图源**(PRD/PM 的 AI 原型/竞品截图/文案清单,均不合规)→ 只提取信息架构+内容+交互意图,用 ZymixUI 规范重建,**绝不照搬来源样式**;跟设计师点明"不复刻外观,只取结构内容重做"
- **PRD/多屏** → 先解析页面清单+每页要素,确认范围优先级,逐页生成逐页合规
任何输入都先分析布局+映射实现方案,信息够→复述确认,不足→提问/给选项,别猜。
- **双重分析(意图源/网页链接必做)**:只读 HTML/文本会漏视觉精髓,必须同时截图看真实长相(浏览器工具或让设计师贴图),代码看结构+截图看视觉,结合定夺每个模块的实现,保留布局精髓

## ⭐ 元经验(多轮返工总结,优先内化,避免重蹈覆辙)
下面是测试案例来回多轮才收敛的教训,下次一步到位:

0. **纵向 flex 容器会压扁固定高子元素**(致命):`.screen`(display:flex;flex-direction:column)内容超高时子元素默认 flex-shrink:1 被挤扁(横滑卡 150px 压成一条缝),不是滚动。模板已加 `.screen>*{flex-shrink:0}`;自己新写 flex 列布局也要防。
1. **对齐方式先想清"三选一",别默认 space-between**:
   - 固定间距+靠左 → `gap:Npx`(默认左对齐)
   - 固定间距+整组靠右 → `justify-content:flex-end;gap:Npx`(左边留空)← 操作胶囊行就是这个
   - 撑满两端均匀分布 → `justify-content:space-between`(间距随宽度变,**不可控**,别拿它凑固定间距,字体渲染差异会溢出或留缝)
   设计稿标注的间距值是硬性的,优先保间距;"整组靠右"≠"均匀铺开",看清楚再写。

2. **单页面输出,不要并排双模式**:一台手机就好(手机上全屏预览);深浅色用 `prefers-color-scheme` 跟随系统,不输出两份内容。要强制模式才加 `data-theme`。

3. **交互优先于静态**:能点的就做成真交互(Toast 点击触发+3s 消失、按钮 :active),方便真机预览。预览卡片不跑 JS,验证交互必须去浏览器/真机——提醒用户。

4. **图标要贴语义**:玻璃圆钮图标随页面变(聊天=返回/更多,动态=编辑笔,Me=时钟);别无脑放"+"。SF Symbols 字符别当文字处理。

5. **配图用真图 + 兜底**:头像 `i.pravatar.cc/{尺寸}?img={1-70}`、通用图 `picsum.photos/seed/{种子}/{w}/{h}`(弃用 loremflickr);容器必给品牌渐变兜底 + img onerror 隐藏,图挂也不空。

6. **给了设计稿=契约**:只要有截图/链接,就是 1:1 复刻每个像素级细节,不是"做个功能类似的"。想法性需求才自由发挥。

## 2026-07-09 · public 动态流页
- **不对称圆角对**:点赞条 16/16/6/6 + 评论块 6/6/16/16,中间 2px 缝——ZYMIX 的"组合块"签名式样,两个块用 flex column gap:2px
- **操作胶囊行(定稿)**:`display:flex;justify-content:flex-end;gap:8px`——固定 8px 间距 + 整组靠右(末钮贴卡片内容右缘,左边留空);不缩进、不 space-between。胶囊:透明底 + border/base 0.66px 描边(box-shadow:inset 0 0 0 0.66px)、高 32、内边距 8、图标 16-18、图文间距 10、数字 Label/较小 Caption 半粗
- **点赞条**:↑ 上箭头图标(不是爱心!) + 人名 Label/较小 Caption 半粗
- **评论预览**:纯文本 Body/较小 Caption,人名不加粗;"N Comments ›" muted + 小箭头
- **作者行**:头像 32 倒角方形(radius-md 近似 squircle);昵称+官方绿标(五瓣星形 accent/base + surface/base 对勾);@handle·时间 muted;隐私锁图标;Follow 胶囊 = surface/secondary 底 + default/foreground 14 Semibold
- **页头**:Tab 双标题(选中 24 Black/未选中 18 Bold muted);右侧玻璃圆钮=编辑笔
- **Scroll Edge Effect - Soft(吸顶渐隐层)**:sticky 容器 top:0,`::before` 铺满容器宽、**高 108px**,从顶 `linear-gradient(bg 45%→transparent)` + `blur(8px)` + mask 渐隐,z-index:-1 垫页头下、pointer-events:none;内容上滑被顶部渐隐模糊遮住

## 2026-07-09 · 通用
- **图标一律用 ZymixUI 图标库**(内置 icons-bundled.json 按名取,别手绘);内置无的走 CDN;图标从 Figma Icons 页导出(展示单元 48×32 紫底,需清洗:去紫底 rect、translate(-16,-8) 裁到 16×16、fill→currentColor)
- 玻璃圆钮图标随页面语义变:聊天页=返回/更多,动态页=编辑,Me页=时钟/设置
- Toast:顶部 60px、点击触发、3s 消失(已内置组件层)
- 页面背景:动态流/聊天等列表页用 background/secondary(雪白),卡片用 surface/base
- **画布基准 375×812**(设计稿尺寸):模板 .phone 桌面框架用 375×812;手机全屏模式自适应;量设计稿间距以 375 宽为参照

## 2026-07-09 · 意图源重做(PM 的 lovable 原型 → Profile 页)
- **意图源不只搬内容,要保留模块的视觉精髓**:相册是舒展 3 列网格(2行大图 radius-lg)不是细横条;事件卡是"图铺满+底部渐变遮罩+文字压图上"的沉浸卡,不是"图在上文字在下"的小卡。只换皮(token/组件),不丢布局意图
- **浮出元素别放 overflow:hidden 容器里**:头像/徽标探出封面(bottom:负值)时,若放在封面的 overflow:hidden 容器内会被裁掉。结构:外层 relative(不裁)包 [封面 .media(overflow:hidden 只管封面图) + 头像(absolute,z-index)],头像与封面同级、不在封面内
- **图上文字用 `var(--default-white)`**(恒白,深浅色都不翻转);普通反色文字才用 foreground/inverse(会随主题翻)
- **媒体遮罩** `.scrim-b`(components.css):图上叠字的底部黑渐变,rgba 是媒体属性、合规豁免(checker 已豁免 linear-gradient 内 rgba)
- 配图用 picsum.photos/seed/<种子>/W/H(每图不同种子);真机/浏览器联网才显示,预览卡不显示
- **图片必须有兜底底色**(铁律):所有 <img> 或媒体容器加 `background:var(--surface-secondary)`。否则图慢/被墙/失败时,透明卡+白字压白底=整块隐形(事件卡就这么消失过)。图上叠字的沉浸卡尤其要给容器兜底
- **入口卡图标带徽底**:重要入口(Wallet 等)图标放 40px accent-soft 圆形徽底(圆底 accent-soft + 图标 accent-soft-foreground),比裸图标更醒目,符合原型意图
- **底部导航激活态用胶囊**:当前 tab 不只是变色,用 accent 胶囊(accent-base 底+accent-foreground 字/图 + 标签),其余竖排 subtle;对齐 iOS 社交产品惯例

## 2026-07-09 · Me 个人主页(异形快捷卡 + 统计)
- **快捷卡是"异形",不是方卡**:灰圆角矩形(surface-secondary,radius-md)只占卡下部(111×88 卡里灰块 106×66、离顶 22px),**3D 图标探出在灰块上方**(72px 图标 top:0,盖过灰块顶缘),标签 Xs(12) 在灰块底部。做法:卡 position:relative;灰块 absolute top:22;图标 absolute top:0 居中;标签 absolute bottom。别做成"方卡里居中图标+文字"
- **3D 图标带同色系投影**:filter:drop-shadow(0 4px 16px 色/30%)——Figma 实测统一 #B754FF 30% y4 b16(紫);emoji 占位时按图标色调给投影(转盘紫/勾绿/礼物橙)
- **统计数字是 Number/Base = 18px Black(900)**,不是 24;别被截图"看起来大"骗了,回 Figma 量样式名。字重 Black=CSS 900
- **图标 emoji 插画豁免**:用 `font-size:Npx;line-height:1` 标记,合规检查跳过字号校验(文字角色从不用 line-height:1)

