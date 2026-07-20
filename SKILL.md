---
name: zymix-ui-prototype
description: 按 ZymixUI 设计系统生成高保真手机 UI 界面原型(HTML 单文件,单页面输出、深浅色跟随系统自动切换,内置 Button/Toast/玻璃材质组件层与合规检查)。凡是用户要画界面、出原型、做 mockup、设计某个页面/弹窗/组件效果图,或提到 ZYMIX/ZymixUI/设计规范/设计系统相关的界面产出时,务必使用本技能——哪怕用户没说"原型"二字,只要产出物是一个界面的样子,就用它。不用它生成的界面必然偏离设计规范。
---

# ZymixUI 界面原型生成(一期:tokens + Button/Toast/Materials)

按 ZymixUI 设计系统(ZYMIX iOS 社交/IM 产品)生成自包含 HTML 原型。目标:**生成的页面 100% 符合已有规范**——颜色、间距、字号、按钮、玻璃材质全部来自设计系统,零自造值。

## 工作流(顺序执行)

00. **需求获取阶段(生成前必过)**。使用者是设计师,输入形式多样,先判断输入属于哪类,再决定还原策略:

    **A. 规范源(照搬样式)**:本设计系统的 Figma 设计稿(截图/链接/node-id)。→ **1:1 还原**每个细节(圆角/间距/字重/图标)。

    **B. 意图源(只取意图,用规范重建)**:PRD 文档、产品经理用 AI 生成的原型(**不符合本规范**)、竞品/参考截图、纯文案清单。→ **只提取信息架构、内容、交互意图,一律用 ZymixUI 的 token/组件/文字角色重新落地,绝不照搬来源的样式**(它们本就不合规,照搬=把脏样式带进来)。要跟设计师点明:"我不复刻它的外观,只取结构和内容,用规范重做"。**双重分析定夺**:意图源(尤其网页/原型链接)不能只读 HTML/文本——文本会漏掉视觉精髓(如相册网格 vs 细横条、图上叠字沉浸卡 vs 图上文下小卡)。要**同时截图看它长什么样**(用浏览器工具或让设计师贴图),代码看结构+截图看视觉,两者结合再定每个模块怎么用规范实现,保留模块的布局精髓。

    **C. 自然语言 / 迭代反馈**:文字描述、"次要文字改 muted"这类调整。→ 按描述做,样式走规范。

    **PRD / 多屏输入的特别流程**:PRD 常描述整个流程(多个页面)。不要闷头一次全画。先**解析出它隐含的页面清单 + 每页要素**,列给设计师 → **确认范围、优先级、先做哪几屏** → 逐页生成、逐页过合规检查。

    **通用**:任何输入都先**分析布局结构 + 映射实现方案**(每区块用哪个组件/token/文字角色)。信息够→复述方案请设计师确认;不足(布局歧义、内容缺失、选型多解、资产不确定)→**主动提问或给选项**理清,别猜着生成。宁可多问一句。确认清楚才进下面的步骤。
0. **有设计稿必须 1:1 还原**:用户给了 Figma 截图/链接时,精确还原每个细节(不对称圆角、描边宽、缩进、字重、图标形状),不是"功能近似"。没给设计稿才自由发挥。**先读 `references/lessons.md`(历次还原经验),做完新页面把新学到的模式追加进去**。**做完必须回头对比设计稿逐项自检**(圆角/间距/字重/图标/行宽核算),对不上就修,不要等用户指出。
1. **从参考模板起步**:`assets/templates/discover.html`(发现流:金刚区分类/Hero 大图/活动卡/灵动岛多状态)、`assets/templates/chat.html`(IM 群聊)、`assets/templates/me.html`(个人主页)、`assets/templates/public.html`(公开动态流:Tab 页头/帖子卡片/点赞评论块/操作胶囊)是从 Figma 设计稿逐层转换的标准页面。新页面**复制最接近的模板改造**,不要白手起家——模板里的页头/导航/输入条/列表/气泡/灵动岛写法就是标准答案。
2. **读取规范**(模板没覆盖的部分再查):
   - `references/tokens.css` — 全部变量(颜色 Light/Dark、圆角、尺寸、字号)
   - `references/components.css` — 组件层:按钮 7 变体×3 尺寸、Toast、玻璃材质 .glass、导航、气泡、列表(注释即文档)
   - `references/color-rules.md` — 用色铁律;`references/typography.md` — 文字角色表
   - `references/motion.md` — **动效规范**(平台中立 token + Web/iOS 双映射):要不要动、缓动、时长、弹簧、按压/入场/stagger、reduced-motion。凡做交互/过渡先读它;时长用 `--duration-*`、缓动用 `--ease-*`,别写魔法数。动效值源 `tokens/motion.json`,同时服务真机(含 iOS/SwiftUI),不止 HTML。
   - `references/craft.md` — **工艺层(反 AI 味)**:把"高级/克制"翻成可执行规则 + 反面;合规查"对不对",craft 查"平庸不平庸"(禁渐变铺底/彩虹圈/等大白卡墙、accent 预算制、真实图片位、留白节奏)。**含多状态页面用「灵动岛切换器」单页演示的约定**(除非用户要求铺开多页)。
   - `references/spec.md` — **功能状态声明**:一页除主流程外必须定义的空/加载/失败/权限/成功反馈等状态(附四页型矩阵 + 阻断项)。有多状态的页面先按它过一遍,缺阻断项=没做完。
   - 布局惯例见 `references/patterns.md`
3. **组装页面**:tokens.css + components.css 全文内嵌到 assets/template.html 骨架;**只生成一个页面(单台手机),画布基准 375×812(设计稿尺寸)**——手机上打开即全屏预览,桌面浏览器自动居中带壳;深浅色跟随系统(prefers-color-scheme),不要输出两份内容;用户明确要强制某模式时才给 .phone 加 data-theme。
4. **跑合规检查(必须)**:`python3 scripts/check_compliance.py <生成的.html>`,**全部 PASS 才能交付**;FAIL 就按报错修正后重跑。
5. **配图**:头像用 `https://i.pravatar.cc/{尺寸}?img={1-70}`,通用图用 `https://picsum.photos/seed/{种子}/{w}/{h}`(每图不同种子),弃用 loremflickr。**占位铁律**:每个图位必须留**兜底色块**(`--skeleton-base` / `--surface-secondary`)表达"此处有图"——首选用容器 `background-image` + 底色(图加载不出时自动露底色,预览器/离线都有占位);若用 `<img>`,`onerror` 只清 `src` 保留容器底色,**严禁 `visibility:hidden`/`display:none` 把整块藏没**(图挂了也不能变空白)。参见 scripts/pick_images.py。
6. 交付单个自包含 .html。

## 组件使用规则

- **按钮**:只用 `.btn .btn-{primary|secondary|tertiary|outline|ghost|danger|danger-soft} .btn-{sm|md|lg}` 组合;玻璃按钮 `.btn-glass`(胶囊)/`.btn-glass-42 .glass`(页头圆钮)。禁止自造按钮样式;底色与文字色已按状态组配对,不要覆盖 color。
- **Toast**:`<div class="toast glass">` + 图标 + `.toast-text`。图标/文字一律中性黑(设计裁决:Toast 不用状态色的红绿),类型只换图标图形。**位置铁律:永远在屏幕顶部,距手机顶 60px 水平居中(样式已内置),不要放页面中间或底部**。**默认隐藏,点击触发**:toast 加 `id="toast"`,触发按钮加 `onclick="showToast()"`,页面 `</body>` 前带一段脚本:`<script>function showToast(){const t=document.getElementById('toast');t.classList.add('show');clearTimeout(t._h);t._h=setTimeout(()=>t.classList.remove('show'),3000)}</script>`(显示 3 秒自动消失,方便预览真实交互)。
- **页头返回按钮**:与右侧操作钮同规格,必须玻璃底:`<button class="back btn btn-glass-42 glass">`,禁止裸箭头。
- **图标(ZymixUI 图标库,721 个)**:**禁止手绘 SVG**。常用 ~66 个已内置 `references/icons-bundled.json`(name→SVG内部),按名取、内联进 `<svg viewBox="0 0 16 16">`、用 currentColor 上色(用法见 references/icons.md);内置里没有的走 CDN 的 `.zi` mask 引用(见「图标库(CDN)」)。库里无 wallet(用 credit-card),share=arrow-shape-turn-up-right。3D 彩色图标(转盘/礼物等品牌插画)不在图标库,用 emoji 占位或让用户导出 PNG。
- **玻璃材质**:一切玻璃质感只用 `.glass`(Figma 液态玻璃的 CSS 近似,自带投影和内高光),着色玻璃加 `.glass-primary`。不要手写 backdrop-filter。
- **状态**:按下 `:active` 已内置;禁用 `disabled` 属性(整体 50% 透明度);44pt 热区已由伪元素扩展。

## 硬规则(违反=不合格,checker 会拦)

- **单页面铁律**:一个 HTML 只输出**一台手机(一个 `.phone`)**。深浅色靠 `prefers-color-scheme` 跟随系统自动切换——**绝不并排画"浅色一台+深色一台"两份**,也不要在同一文件里同时用 `data-theme="light"` 和 `data-theme="dark"` 造双份。要给用户看深色,让他切系统外观或口头说"锁定深色"(那时才给唯一的 `.phone` 加 `data-theme="dark"`)。checker 检测到多个 `.phone` 或双 data-theme 直接 FAIL。
- 颜色一律 `var(--xxx)`,禁止裸 hex/裸 rgba
- 字号只能是 36/34/30/24/20/18/17/16/15/14/13/12/11/10(10=Body/2xs,行高 12,TabBar 底部文字等极小字专用;一般不用);字重只有 400/600/900(场景 Tab 700)
- 圆角用 `var(--radius-*)`,不写硬值
- 分隔线 0.5px `var(--separator-base)`;强分隔 1px `var(--separator-strong)`
- Dark 模式必须同时正确——只用语义变量自然双模(跟随系统切换,交付前脑内过一遍深色:黑底黑字/白底白字都是错)
- **动效**(详见 motion.md):时长用 `--duration-*`、缓动用 `--ease-*`;禁 `transition:all`、禁 UI 用 `ease-in`;只动 transform/opacity;UI 过渡 ≤300ms;禁从 `scale(0)` 入场(用 scale(0.95)+opacity);高频/键盘操作不加动画;加 `prefers-reduced-motion` 兜底。checker 会拦 transition:all 与 ease-in。
- **TabBar(底部导航)**:玻璃胶囊 `.tabbar > .pill.glass`,`.tab` 等分,激活位加 `.active`(=accent/soft-subtle 底 + accent 图标),**有且只有一个激活位**;五 tab Chat/Mix/Video/Discover/Me;图标槽 32/字形 24;底部模糊**已内置** `.tabbar::before`(等效 Figma Show Scroll Edge,`.no-edge` 可关),勿再叠任何渐变层;旧 `.nav-bar`(accent 底白图)与 `.nav-fade`(线性渐变)均已删除作废。
- **NavBar(页头)**:用 `.header-brand`/`.header-tabs`/`.header-nav`/`.header-chat` 四变体;圆钮一律 `.btn-glass-42 .glass`(Button-Liquid-Glass-Symbol 42),禁手绘;**一级页页头不放返回按钮**;Nav-Center 标题绝对居中,不受右侧动作显隐影响;**页头区(含状态栏)必须包进 `.scroll-edge-top`**(顶部模糊,对应 Figma NavBar 内置 Scroll Edge),内容从其下滚过时正确渐隐。
- **Backdrop(遮罩)**:`.backdrop`(--backdrop-base,一般默认)/`.backdrop.strong`(--backdrop-strong,活动运营等强调弹层的特殊场景);纯黑压暗无模糊,弹层底下垫。
- **组件宽度**:一律「左右边距 + 拉伸」,禁写死 343/360 等画布衍生固定宽(基准规则见 patterns.md)。
- **图标铁律**:**只用 ZymixUI 图标库**——内置 `icons-bundled.json` 按名内联,库里没有的走 CDN `.zi` mask;**严禁手绘/自造任何图标 SVG**(几何拼凑也算),仅状态栏信号/WiFi/电池等系统 chrome 例外。库里无 wallet→用 credit-card;3D 彩色品牌插画(转盘/礼包等)不在库,用导出的 PNG,不用手绘。
- **配图铁律**:一切"配图/照片"(hero、卡片图、缩略图、封面)都用**免版权图**(`picsum.photos` 每图不同种子 + 容器 `background-image` + `--skeleton-base` 兜底),**严禁用手绘 SVG 插画/线条画当配图**。图标归图标库,照片归 picsum,两者不混。
- **英文铁律**:**输出页面的一切可见文案一律英文**(面向英国市场)——标题、正文、占位符、按钮、`aria-label`、toast、状态标签、JS 里参与展示的字符串全部英文;示例地点/人名用英国/伦敦语境(如 Shoreditch、Victoria Park)。代码注释可留中文,但**渲染出来的一个中文字都不能有**。

## 图标库(CDN)

内置 `icons-bundled.json` 没有的图标走 CDN(ZymixUI 图标库 721 个,已发布 jsDelivr)。用 mask 方式按需引、currentColor 上色:
```css
.zi{display:inline-block;width:24px;height:24px;background:currentColor;
  -webkit-mask:var(--zi) center/contain no-repeat;mask:var(--zi) center/contain no-repeat}
```
```html
<i class="zi" style="--zi:url(https://cdn.jsdelivr.net/gh/zymix-ui/zymix-icons@v1.0.0/svgs/rocket.svg)"></i>
```
base URL:`https://cdn.jsdelivr.net/gh/zymix-ui/zymix-icons@v1.0.0/svgs/<name>.svg`(`.zi` 已在 components.css)。⚠CDN 图标需联网,预览卡片不显示、真机/浏览器正常。全部图标名见图标仓库 svgs/。

## 规范更新

tokens 变更后:`python3 scripts/sync_tokens.py <tokens目录>` 重新生成 tokens.css → 重跑模板合规检查 → 重新打包技能。
图标更新后:图标仓库 `npm run export`(或手动导出+`clean-svgs.py`)→ push → 打新 tag → 更新技能里的 CDN base 版本号。
