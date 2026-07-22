# ZYMIX-UI 原型技能

**版本 v1.2.2** · tokens + Button/Toast/玻璃材质 + 图标库 + App(多屏外壳,含 Chat 会话列表→对话下钻)

> 一句话说清需求，AI 就给你一张**完全符合 ZYMIX 设计规范**的高保真手机页面。

---

## 按角色查阅

| 角色 | 需求 | 文档 |
|---|---|---|
| 设计师 / 产品 | 用技能做原型、产出高保真页面 | **[PROTOTYPE-GUIDE.md](./PROTOTYPE-GUIDE.md)** — 上手步骤与需求写法 |
| 技术 / 工程师 | 获取并接入设计变量(Tokens) | **[TOKENS-GUIDE.md](./TOKENS-GUIDE.md)** — 引入、变量表、代码示例、Figma 同步 |
| 设计 AI(Stitch 等) | 按规范生成界面 | **[DESIGN.md](./DESIGN.md)** — 设计系统规范文档 |

**两个关键位置:**

- **设计变量(Tokens)** 的单一真源为 **[`references/tokens.css`](./references/tokens.css)** —— 347 个变量、含深浅色,由 `sync_tokens.py` 从 Figma 生成,请勿手改。
- **组件样式** 位于 **[`references/components.css`](./references/components.css)** —— Button / NavBar / TabBar / Toast / 玻璃材质等,依赖上述变量。

---

## 这是什么

一个装进 AI(Claude 等)的「技能包」。装上后你只要说「做一个 ZYMIX 的 XX 页面」,AI 就会:

- 用设计系统里**真实的**颜色、字号、间距、按钮、图标来画;
- 自动跑一遍**合规检查**,不符合规范的绝不交付;
- 产出能直接在手机/浏览器打开的 HTML 页面,深浅色跟随系统。

**把"想法"变成"符合规范的界面",中间不用逐个像素去调。**

技能自带样例页(`assets/templates/`):**App**(`app.html`:单页多屏外壳,底部 TabBar 一键切换 **Mix / Discover / Me** 三屏 + **Chat**(会话列表→点行全屏对话:气泡/已读回执/输入条)+ Video 占位;含状态栏、灵动岛外观切换、Scroll Edge、移动端满屏)。IM 群聊已并入 app.html,不再单独出 chat.html。

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
TOKENS-GUIDE.md       🛠 技术:怎么拿 & 接入 tokens
DESIGN.md             🤖 设计系统规范(Stitch 格式)
references/           设计规范(真源)
  tokens.css            ⭐ 颜色/间距/字号/圆角变量(347 个,单一真源)
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

**规范更新了怎么办?** 技术侧改 Figma → 跑 `check_figma_sync.py` 对账 → `sync_tokens.py` 重新生成 `tokens.css` → 重打包发新版(见 [TOKENS-GUIDE](./TOKENS-GUIDE.md))。

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
