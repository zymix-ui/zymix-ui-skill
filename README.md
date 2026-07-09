# ZYMIX-UI 原型技能

**版本 v1.0.0** · 一期(tokens + Button/Toast/玻璃材质 + 图标库)· 更新于 2026-07-09

> 一句话说清需求，AI 就给你一张**完全符合 ZYMIX 设计规范**的高保真手机页面。
> 产品、设计、技术都能用——不用会画图，也不用写代码。

---

## 这是什么

一个装进 AI（Claude 等）的「技能包」。装上后，你只要说「做一个 ZYMIX 的 XX 页面」，AI 就会：

- 用设计系统里**真实的**颜色、字号、间距、按钮、图标来画
- 自动跑一遍**合规检查**，不符合规范的绝不交付
- 产出一个能直接在手机/浏览器打开的 HTML 页面，深色浅色跟随系统

简单说：**把"想法"变成"符合规范的界面"，中间不用设计师逐个像素去调。**

---

## 能做出什么

技能里自带 4 个真实产出的样例：

| 页面 | 说明 |
|---|---|
| 个人主页 Me | 资料区、三栏统计、快捷卡、列表、玻璃底部导航 |
| 公开动态流 | 帖子卡、点赞评论、操作按钮 |
| 聊天会话页 | 气泡、已读回执、输入条 |
| 删好友确认页 | 弹出 Toast、危险按钮（可点击交互） |

---

## 怎么安装

### 方式一：Claude（最简单）
1. 下载本仓库里的 **`zymix-ui-prototype.skill`**
2. 发给 Claude / 在 Claude 里打开它，点 **「Save skill」**
3. 装好了。之后说「用 ZYMIX 做个登录页」就会自动触发。

### 方式二：其他 AI 工具（Cursor / 通用 Agent 等）
`.skill` 本质是个 zip，解压后就是这个仓库的文件。把 **`SKILL.md` + `references/` + `scripts/` + `assets/`** 一起放进该工具的"技能/规则/知识库"目录即可。核心是让 AI 能读到 `SKILL.md`——它是总入口，会告诉 AI 去读哪些规范文件。

### 方式三：发一句话让 AI 自己装（能联网的 AI）

对能读取网页的 AI(Claude、Cursor、各类 Agent),把下面这段**直接发给它**即可,它会自己抓取并加载技能:

```
请把这个 ZymixUI 原型技能加载为你的能力:
先读 https://raw.githubusercontent.com/zymix-ui/zymix-ui-skill/main/SKILL.md,
再按 SKILL.md 里的指引读取同目录 references/、assets/、scripts/ 下被引用的文件
(基址 https://raw.githubusercontent.com/zymix-ui/zymix-ui-skill/main/)。
之后我说"做一个 ZYMIX 的 XX 页面",就按这套规范生成。
```

> 锁定版本可把 `main` 换成 `v1.0.0`。能跑命令行的工具也可直接 `git clone https://github.com/zymix-ui/zymix-ui-skill.git`。

### 方式五：Google Stitch / 设计 AI(DESIGN.md)

仓库里的 [`DESIGN.md`](DESIGN.md) 是 [Google Stitch DESIGN.md 规范](https://stitch.withgoogle.com/docs/design-md/overview/)格式的设计系统文档。把它丢进 Stitch 项目或发给任意设计 AI,说「按 DESIGN.md 生成页面」,即可产出符合 ZymixUI 视觉语言的界面(颜色/字号/组件/布局全带上)。

### 方式四：直接给 AI 读（离线/贴内容）

把 `SKILL.md` 的内容贴给任意 AI 对话，让它「按这份规范生成页面」，也能用（效果取决于该 AI 能否读取 references 里的文件）。

---

## 怎么用（说人话）

你不用懂设计术语，把**页面类型 + 要放什么内容**说清楚就行：

> 做一个 ZYMIX 的转账成功页：居中一个大对勾、金额 ¥1,280、下面明细，底部一个 Done 按钮。

AI 会先跟你确认方案，再生成。**支持五种给需求的方式：**

1. **一句话描述**（最常用）
2. **贴 ZYMIX 的设计稿**（截图/链接）→ AI 会 1:1 精确还原
3. **丢一份 PRD 文档** → AI 拆成多个页面，一页页做
4. **贴别的 AI 生成的原型 / 竞品截图** → AI 只学它的结构，用 ZYMIX 规范重做（不照搬它不规范的样式）
5. **在已有页面上改** →「次要文字改浅一点」「这个按钮换成次要按钮」


---

## 里面有什么

```
SKILL.md              技能总入口（AI 首先读这个）
references/           设计规范
  tokens.css            颜色/间距/字号/圆角变量
  components.css        按钮/Toast/玻璃材质/导航等组件
  color-rules.md        用色规则
  typography.md         文字样式
  patterns.md           页面布局惯例
  lessons.md            还原经验（避坑清单）
  icons-bundled.json    66 个常用图标（离线可用）
assets/
  template.html         手机页面骨架
  templates/            4 个标准页面模板
scripts/
  check_compliance.py   合规检查（拦截不规范的样式）
  sync_tokens.py        从设计系统同步 token
```

图标库另见：[zymix-ui/zymix-icons](https://github.com/zymix-ui/zymix-icons)（721 个图标，npm `@zymix-ui/icons`）

---

## 常见问题

**Q：生成的页面为什么图片/图标不显示？**
A：图标和网络图片需要联网。手机或浏览器打开正常；某些预览窗口不联网会显示占位。

**Q：我能让它偏离规范吗（比如用个非标字号）？**
A：不能，这是特性。技能会把它归到最接近的规范档，保证全团队产出一致。

**Q：设计规范更新了怎么办？**
A：由维护者更新技能包并发新版本，重新安装即可。

---

## 版本历史

| 版本 | 日期 | 说明 |
|---|---|---|
| **v1.0.0** | 2026-07-09 | 一期首发:全量 tokens、文字角色、Button(7×3)、Toast、液态玻璃材质、4 个页面模板、66 内置图标 + 721 CDN 图标、合规检查、需求获取流程 |

> 二期规划:Input / Dialog 等更多组件、更多页面模板。
