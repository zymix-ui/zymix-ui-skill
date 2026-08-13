# ZYMIX-UI 原型技能

**版本 v1.5.0** · tokens + Button/Toast/玻璃材质 + 图标库 + App(多屏外壳,含 Chat 会话列表→对话下钻)

> 一句话说清需求，AI 就给你一张**完全符合 ZYMIX 设计规范**的高保真手机页面。

---

## 按角色查阅

| 角色 | 需求 | 文档 |
|---|---|---|
| 设计师 / 产品 | 用技能做原型、产出高保真页面 | **[PROTOTYPE-GUIDE.md](./PROTOTYPE-GUIDE.md)** — 上手步骤与需求写法 |
| 技术 / 工程师 | 获取并接入设计变量(Tokens) | **[TOKENS-GUIDE.md](./TOKENS-GUIDE.md)** — 引入、变量表、代码示例、Figma 同步 |
| 设计系统维护者 | 改规范 / 建组件 / 发新版技能 | **[docs/SOP.md](./docs/SOP.md)** — 从 Figma 设计稿到 skill 的全流程、铁律、API 踩坑清单 |
| 设计 AI(Stitch 等) | 按规范生成界面 | **[DESIGN.md](./DESIGN.md)** — 设计系统规范文档 |

**两个关键位置:**

- **设计变量(Tokens)** 使用方请引用 **[`references/tokens.css`](./references/tokens.css)** —— 206 个变量、含深浅色,由 `sync_tokens.py` 从本仓库 `tokens/` 的 JSON 真源生成,**请勿手改快照**;改规范请改 `tokens/` 下的 JSON。
- **组件样式** 位于 **[`references/components.css`](./references/components.css)** —— Button / NavBar / TabBar / Toast / 玻璃材质等,依赖上述变量。

---

## 这是什么

一个装进 AI(Claude 等)的「技能包」。装上后你只要说「做一个 ZYMIX 的 XX 页面」,AI 就会:

- 用设计系统里**真实的**颜色、字号、间距、按钮、图标来画;
- 自动跑一遍**合规检查**,不符合规范的绝不交付;
- 产出能直接在手机/浏览器打开的 HTML 页面,深浅色跟随系统。

**把"想法"变成"符合规范的界面",中间不用逐个像素去调。**

技能自带样例页(`assets/templates/`):**App**(`app.html`:单页多屏外壳,底部 TabBar(**Chat / Discover / AI / Mix / Me**)一键切换 **Mix / Discover / Me** 三屏 + **Chat**(会话列表→点行全屏对话:气泡/已读回执/输入条)+ AI 占位;含状态栏、灵动岛外观切换、Scroll Edge、移动端满屏)。IM 群聊已并入 app.html,不再单独出 chat.html。

---

## 怎么安装

### 方式一:Claude(最简单)
1. 下载本仓库的 **`zymix-ui-prototype.skill`**;
2. 发给 Claude / 在 Claude 里打开,点 **Save skill**;
3. 装好。之后说「用 ZYMIX 做个登录页」自动触发。

### 方式二:发一句话让 AI 自己装(能联网的 AI)
把下面这段直接发给 Claude / Cursor / Agent:
```
请把这个 ZymixUI 原型技能加载为你的能力:
先读 https://raw.githubusercontent.com/zymix-ui/zymix-ui-skill/main/SKILL.md,
再按 SKILL.md 的指引读取同目录 references/、assets/、scripts/ 下被引用的文件
(基址 https://raw.githubusercontent.com/zymix-ui/zymix-ui-skill/main/)。
之后我说"做一个 ZYMIX 的 XX 页面",就按这套规范生成。
```
> 锁版本把 `main` 换成对应 tag。命令行工具可直接 `git clone https://github.com/zymix-ui/zymix-ui-skill.git`。

### 方式三:其他工具 / 离线
`.skill` 本质是 zip,解压即本仓库文件。把 **`SKILL.md` + `references/` + `scripts/` + `assets/`** 放进工具的技能/规则/知识库目录;核心是让 AI 读到 `SKILL.md`(总入口)。

### 方式四:Google Stitch / 设计 AI
[`DESIGN.md`](./DESIGN.md) 是 Stitch DESIGN.md 格式的设计系统文档,导入 Stitch 项目或提供给设计 AI,注明「按 DESIGN.md 生成页面」即可。

---

## 里面有什么

```
SKILL.md              技能总入口(AI 首先读这个)
PROTOTYPE-GUIDE.md    🎨 设计/产品:怎么用技能做原型
docs/SOP.md           🔧 维护者:设计系统运作流程(不打进技能包)
TOKENS-GUIDE.md       🛠 技术:怎么拿 & 接入 tokens
DESIGN.md             🤖 设计系统规范(Stitch 格式)
references/           设计规范(真源)
  tokens.css            ⭐ 颜色/间距/字号/圆角变量(200 个,单一真源)
  components.css        ✅ 组件类:Button/NavBar/TabBar/Toast/玻璃材质/气泡/列表(依赖 tokens,见 TOKENS-GUIDE 组件层)
  color-rules.md        用色规则   typography.md 文字样式
  patterns.md           页面布局惯例(骨架标配、TabBar/NavBar)
  craft.md              工艺层(反 AI 味 + 灵动岛约定)
  spec.md               功能状态声明(空/加载/失败…)
  lessons.md            还原经验(避坑清单)
  icons-bundled.json    81 个常用图标(离线可用,含 tab-* 标签栏图标)
assets/
  template.html         手机页面骨架
  templates/            标准模板:app(多屏应用外壳:Mix/Discover/Me 切换 + Chat 会话列表/对话下钻)
scripts/
  check_compliance.py   合规检查(拦不规范样式)
  sync_tokens.py        从 Figma 同步 tokens
  check_figma_sync.py   Figma ↔ 本地 token 对账
```

图标库另见 [zymix-ui/zymix-icons](https://github.com/zymix-ui/zymix-icons)(721 个图标,npm `@zymix-ui/icons`)。

---

## 常见问题

**图片/图标不显示?** 需联网;手机/浏览器打开正常,某些不联网的预览窗口显示占位色块(这是刻意的兜底)。

**能偏离规范吗(用非标字号)?** 不能,这是特性——会归到最近规范档,保证团队产出一致。

**规范更新了怎么办?** 日常是 **Figma 先变、本地再同步**(Figma 规范组件由另一位设计师负责,skill 由 AI 设计师维护):对账 Figma 与 `tokens/` → 差异落到 **JSON 真源** → `python3 scripts/sync_tokens.py` 生成 `tokens.css` → 同步 skill 侧受影响文件(字阶还要改模板 `.t-*` 类与合规白名单)→ `bash scripts/pack.sh` 重打包发新版。**切勿手改 `tokens.css`** —— 它是快照,下次生成会被冲掉。完整流程、四层对账与验收清单见 **[docs/SOP.md](./docs/SOP.md)**;取用方式见 [TOKENS-GUIDE](./TOKENS-GUIDE.md)。

---

## 版本历史

| 版本 | 日期 | 说明 |
|---|---|---|
| v1.0.0 | 2026-07-09 | 首发:全量 tokens、文字角色、Button(7×3)、Toast、液态玻璃、页面模板、图标库、合规检查、需求获取流程 |
| **v1.1.0** | 2026-07-14 | Discover 改版;四模板统一(纯库图标 / 圆头像 / 灵动岛外观切换 / 移动端满屏);输出页全英文(英国市场);文档按"设计-产品 / 技术"两类使用者重梳理 |
| **v1.1.1** | 2026-07-20 | NavBar 顶部模糊落地:页头区包进 `.scroll-edge-top`(渐变绑 `--background-base` 随明暗翻转,浅→白/深→黑),对应 Figma NavBar 内置 Scroll Edge;明确"skill 用页面层 / Figma 用组件内置"为有意为之的架构差异(SKILL.md · patterns.md · components.css);与 Figma Kit v0.7.0 对齐(NavBar 图标暗色翻白、Backdrop base/strong、Materials Scroll Edge 明暗自适应均已核对一致) |
| **v1.2.0** | 2026-07-22 | 语义层新增 `foreground/emphasis`(黑/白 80%,填补 base↔muted 空档;含 `on-dark/emphasis`)+ 对应颜色样式;tokens 源(`dsv2/tokens`)、`tokens.css`、DESIGN、TOKENS-GUIDE、color-rules 同步。`app.html` 补齐 Chat 会话列表屏(搜索 + 会话行,复用 `.list-row`/`.header-brand`/`.tabbar` 规范类,头像圆角 24)。SKILL 强化 NavBar/TabBar 为**强制基线**(自然语言输入亦然,禁止临时手搓页头圆钮)+ 新增交付前基线组件自检 |
| **v1.2.1** | 2026-07-22 | 系统状态栏统一为一套 iOS 标准(高 47、时间 15/600、信号+WiFi+电池全套图标、跟随主题),多屏 `app.html` 共用;TabBar 采用专用标签栏图标(本地化到 `icons-bundled.json`);灵动岛设为默认必备;补 iOS26 切屏动效;修正 Scroll Edge 渐隐磨砂;DESIGN 版本号同步 |
| **v1.2.2** | 2026-07-22 | **命名修正**:底部标签栏(TabBar)图标此前误用 `nav-` 前缀(nav 应专指顶部 NavBar),统一改为 `tab-*`(tab-chat/mix/video/discover/me/ai + `-fill`)——含 Figma 图标库组件集 + 分类标签(navigation→tabbar)、`icons-bundled.json`、SKILL/DESIGN/icons.md 约定文本、Claude Design 同步;公开图标库 `zymix-icons` svgs 同步改名 + 重建 React 组件 + 发版 `v1.0.2`(skill CDN 引用升 @v1.0.2)。`feature-nav-*`(顶/底两栏共用的导航层玻璃底/渐隐)非图标、语义无误,保留不变 |
| **v1.3.0** | 2026-07-29 | **图标 1px 全库同步**:对齐 Figma Kit v0.8.0——全库图标描边 1.5px→1px 重新导出,公开库 `zymix-icons` 发版 **v1.1.0**(714 个更新 + 10 个新增:headset/comment-dots/person-key/lock-simple/paper-plane-fill 等;清理 19 个 Figma 已删图标);`icons-bundled.json` 81 个内联图标全量刷新(share 源→arrow-shape-turn-up-right);CDN 引用升 `@v1.1.0`(SKILL/icons.md/components.css)。注:Figma 端 feature/nav 变量与「导航 Nav」样式已删除(导航玻璃改由 Liquid Glass 材质组件承担),skill 端 `--feature-nav-*` 作为 CSS 实现 token 保留 |
| **v1.5.0** | 2026-08-13 | **TabBar 改版对齐 Figma 定稿**:tab 顺序改为 **Chat/Discover/AI/Mix/Me**(video 频道移除,`tab-video` 图标保留备用);新增 **AI 徽章位**(40×30 绿胶囊 `.ai-badge` 恒绿,对应 Figma 私有组件 `_TabBar Item AI`);**恒带底部文字**(无文字形态下线,Figma TabBar/Item 的 Label 轴已删);`tab-ai` 字形换新(Ai✦ 徽章字形,原水晶球作废,`icons-bundled.json` 双变体同步);`app.html` TabBar 重排 + Video 占位屏改 AI 占位屏;Figma 侧另有 Android 通栏形态(375×68 含 12px 底部系统导航间距),skill 默认 iOS |
| **v1.4.0** | 2026-07-31 | **字阶改版 + 徽标玫红定稿**:字重体系 Black→**Heavy**(在用四档 Regular/Semibold/Bold/Heavy)。Title 全档转 Heavy(Lg 30→**28**)、Xs 15 Semibold→**16 Bold**;Body 删 17/15/13(留 16/14/12/10);Label 删 18/13,新增 **10px 两档**(Semibold=徽标与标签、Bold=勋章数字);Button 标准 17 Semibold→**16 Bold**、删文字按钮 15 档;Scene 页头大标题 34→**28 Heavy**、导航标题 17→**16 Bold**、气泡正文 17→**16**、删页头Tab 两档;**Number 重建为 9 档阶梯**(36/42·28/34·24/28·20/24·16/20·14/18·12/16·10/12 全 Heavy + 8/10 Bold)。文本样式 32→33,04 Font 变量 67→71;共 63 个 Figma 节点按最接近字号迁移。**徽标统一玫红**:`.badge` 由 accent 绿改 `--feature-like-base` + 恒白字,字号 11→**10**(Label/2xs);Figma Badge 组件删 danger 档(改名 notice 玫红)、收敛为纯实心 15 变体。**新增 `border/white`** 恒白描边(alias default/white)+「描边 Border/纯白 White」样式。NavBar Brand-Tabs 按「一级框架改版」重做并拆为独立组件集(5 tab 槽 + alpha mask 渐隐截断 + 红点)。同步:tokens 源 JSON、`tokens.css`、`typography.md`(重写)、DESIGN、patterns、spec、components.css、`template.html`/`app.html` 的 `.t-*` 全量文字角色类 |
| **v1.5.0** | 2026-08-03 | **颜色体系重构 + 墨色 Ink 新族 + 表单形态定稿**:foreground 梯子精简为 5 档(删 emphasis .80 / faint .15 / ghost .08 三档含 on-dark 对应档),muted .55→**.60**、disabled 浅.26/深.22→**统一 .20**、on-dark subtle .35→**.40**;删 `background/secondary`(雪白,与 base 太近),`background/inverse` #18181B→**纯黑**并新增 `inverse-tertiary`;`surface` 反色扩为**三级**(Inverse / 反色次级 / 反色三级,供浅色模式下的深色容器分层);删 `separator/strong`(连带删 Separator 组件 strong 变体);新增 `border/avatar`(浅黑3%/深白5%,防白头像糊白底)。**新增「墨色 Ink」六档语义族**(base/pressed/foreground/soft/soft-pressed/soft-foreground,浅黑深白翻转)+ Button 新增 **`variant=ink`** 黑底白字档(126→144 变体);与「中性 Default」严格区分(Default 仍是浅灰容器语义,未改)。样式改名:点赞 Like→**积极强调 Positive**、纯白 White→**反色 Inverse**(原名误导,曾害色板 43 处误用成恒白、深色下全变黑)。**表单形态**:输入框圆角 12→**24**(Input/InputGroup/合并式验证码;分离式单格保持 12——24 会吃成圆形);验证码新增**合并式** `layout=combined`(单框+2px 短线占位);Number/24 字重 Heavy→**Bold**;按钮两档文本样式修正绑错的变量(Base 补 bold、Sm 由 12/16 改 14/20)。**效果样式**新建「聚焦 Focus/焦点环 Ring」「输入聚焦 Field」并接入 Checkbox/OTP;Foundations 的 Shadows 一节改写为「已废弃」(阴影体系早已废,仅文案滞后)。样式 85→**87**,新增变量已全部 scope 清零。同步 tokens 源 JSON、tokens.css、DESIGN、color-rules、patterns、typography、components.css、app.html |
| **v1.3.1** | 2026-07-29 | **图标 1.2px 全库同步**:全库描边 1→1.2px(用户定稿规格;tab-* 与纯填充图标不变),公开库 `zymix-icons` 发版 **v1.2.0**(656 个更新);`icons-bundled.json` 81 个内联图标全量刷新;CDN 引用升 `@v1.2.0` |
