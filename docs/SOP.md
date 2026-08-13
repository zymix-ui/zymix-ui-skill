# ZymixUI 运作 SOP：从 Figma 设计稿 → 组件规范 → skill

> 本文管**流程与顺序**：谁是真源、按什么次序改、每步怎么验、产出落在哪。
> **协作前提**：Figma 规范由另一位设计师负责、skill 由 AI 设计师维护 —— **Figma 先更新，本地再同步**。日常主流程见 [§3 反向同步](#3-反向同步figma-先变时的主流程)。
> 具体规范内容不在这里 —— 色/字/间距看 [`DESIGN.md`](../DESIGN.md)，用色判据看 [`references/color-rules.md`](../references/color-rules.md)，
> 组件规格看 [`dsv2/components/specs/`](../../components/specs/)，Figma 页面组织看 [`dsv2/docs/03-figma-pages.md`](../../docs/03-figma-pages.md)。

---

## 1. 两条链与唯一真源

系统有两条并行的链，**同一份设计意图在两边各有一套载体**。搞清谁是真源，是不出错的前提。

```
真源链(代码交付)                          Figma 链(设计协作)
tokens/*.json  ← 唯一真源 ───同步──→   ① 变量 Variables(4 个集合)
      │ sync_tokens.py                        │ alias
      ↓                                       ↓
references/tokens.css (快照)            ② 颜色/文本/效果样式 Styles
      │                                       │ 绑定
      ↓                                       ↓
原型 HTML / 研发取用                    ③ 组件 Components → ④ 页面
```

| 层 | 真源在哪 | 谁消费 | 备注 |
|---|---|---|---|
| Token 值 | `tokens/*.json` | `sync_tokens.py` → `tokens.css` → 研发/原型 | **JSON 是唯一真源**，`tokens.css` 是生成快照，勿手改 |
| 语义/描述 | `tokens/*.json` 的 `$description` | 人 + Figma 变量描述 | 快照里没有，只在 JSON 和 Figma |
| 文本样式组合 | `tokens/styles/text.json` | Figma 文本样式 | 快照只有原子值（size/weight/leading），不表达组合 |
| 样式名映射 | `tokens/styles/color-styles.json` | Figma 颜色样式 | 85 条「中文双语名 ↔ 变量」，快照里没有 |
| 组件结构 | **Figma 组件本身** | 设计师 + 规格文档 | 代码侧只有 `components.css` 的近似实现 |
| 组件规格 | `dsv2/components/specs/*.md` | 人（换对话也能接上） | 决策理由、配方表、踩坑、待定事项 |
| 原型能力 | `SKILL.md` + `references/` | AI 生成原型 | 打包为 `.skill` |

> ⚠️ `dsv2/components/specs/` 和 `dsv2/DESIGN.md` 目前**在版本控制之外**（只有 `zymix-ui-skill2` 是 git 仓库）。

### 1.1 两个角色，同步方向是 Figma → 本地

| 角色 | 负责 | 工作位置 |
|---|---|---|
| **Figma 规范设计师** | 变量、颜色/文本样式、组件、Kit 文件页面 | Figma Kit 文件 |
| **AI 设计师**（本仓库维护者） | tokens JSON、skill 包、原型能力 | 本地 git 仓库 |

**现实次序：Figma 先更新，AI 设计师看到后再在本地同步。** 所以真源要分两层看：

| | 设计意图的源头 | 代码交付的真源 |
|---|---|---|
| 是谁 | **Figma Kit 文件** | **`tokens/*.json`** |
| 为什么 | 规范设计师在那里工作、在那里做决定 | 它生成 `tokens.css`，是研发与原型的取用口 |
| 关系 | — | **单向拉取**：Figma 变了 → 落到 JSON → 生成快照 |

也就是说，**本地 JSON 不是设计决策的发起地，而是 Figma 决策的落地载体**。它仍然是"代码侧唯一真源"（别手改 `tokens.css`），但内容以 Figma 为准。

---

## 2. 六条铁律

按被违反的频率排序，前两条最容易踩。

1. **`tokens.css` 永不手改；改动必须经过 `tokens/*.json`。** 快照是 `sync_tokens.py` 的输出，手改会在下次生成时被冲掉。
   - 日常（Figma 规范设计师先改）→ 走 [§3 反向同步](#3-反向同步figma-先变时的主流程)：从 Figma 拉取 → 落到 JSON → 生成快照。
   - 当你被要求**直接改 Figma**（如整轮字阶改版）→ 改完 Figma 与 JSON **两边都要落地**，并告知规范设计师改了什么，避免他在 Figma 里按旧值继续。
2. **组件颜色绑「颜色样式」，不绑原始变量。** 样式自身 alias 到变量，深浅色照样自动切换；但组件层只认样式，才能在 Figma 面板成组管理、跨文件复用、换配方时批量生效。
3. **01 Primitive 只是参考色板，02 Semantic 不需要绑定它。**（2026-08-03 设计师明确口径，纠正此前"语义层必须 alias 基础层"的理解）
   - 02 的值可以直接写死，**不必**为了"能 alias"去补 01 的原子档位 —— 深色中性梯子缺 `#232327`/`#27272A`/`#333338`/`#3A3A40` 等中间值是**正常的**，不用补。
   - 真正该复用的是 **02 内部的 alias**：`success/*` → `accent/*`、`border/white` → `default/white`、`feature/im/bubble-guest` → `surface/secondary`、`foreground/link` → `accent/soft-foreground`。新增语义色先看能不能引用同层已有的。
   - ⚠️ 一旦 02 绑了 01，**改 01 会连带改 02**。既然 01 是可自由调整的参考色板，这种耦合要当心（曾把 `neutral/200` 从 #EBEBEC 调成 #EBEBEB，连带改掉了 `ink/pressed` 的深色值）。
   - 「禁硬编码色值」这条仍然成立，但指的是**页面与组件层**不许写裸 hex，不是要求 02 必须 alias 01。
4. **恒定深底用 `default/black`，禁用 `background/inverse` / `surface/inverse`。** inverse 系列的定义就是随主题翻转，深色模式下会翻成白底，叠在上面的恒白描边和 on-dark 文字全部消失。文字同理：恒定深底上用 `foreground/on-dark/*`。
5. **不发明档位。** 字号只用 `10/12/14/16/20/24/28/36`（数字另有 8），圆角只用 `radius/*`，间距只用 `size/*`。表里没有的就近归入最接近的档。
6. **每个阶段的产出要留下文档记录**，保证换个对话能接上进度。

---

## 3. 反向同步：Figma 先变时的主流程

这是 AI 设计师的**日常主工作模式**（比主动改规范频繁得多）。

### 3.1 怎么知道 Figma 变了

按可靠性排序：

1. **规范设计师主动告知**（最可靠，建议约定为默认动作：改完在群里说一句"改了什么"）
2. **Kit 文件的「更新日志」页** —— 见 [`dsv2/docs/03-figma-pages.md`](../../docs/03-figma-pages.md) 的页面组织约定
3. **定期对账**（发版前必做）：见下

> 别指望"看出来"。变量值、样式描述、组件属性这类改动在画布上往往不可见 —— 必须对账。

### 3.2 四层对账

Figma 侧有四层内容，`check_figma_sync.py` 只覆盖第一层，其余靠 MCP 读取后比对：

| 层 | 本地对应 | 怎么对 |
|---|---|---|
| ① 变量值 | `tokens/primitive/*.json`、`semantic/color.*.json`、`layout.json` | 导出 → `check_figma_sync.py` |
| ② 颜色样式 | `tokens/styles/color-styles.json`（85 条名↔变量） | MCP 读 `getLocalPaintStylesAsync()` + 各自 `boundVariables` 后比对条目数与映射 |
| ③ 文本样式 | `tokens/styles/text.json` | MCP 读 `getLocalTextStylesAsync()`，比对字号/字重/行高/家族的绑定组合 |
| ④ 组件 | `dsv2/components/specs/*.md` + `references/components.css` | 读组件集变体名/属性/配方，与规格文档核对 |

**可以直接把这段交给 Claude 执行：**

```
对账 ZymixUI Kit(fileKey NxaWnZYT4ZidZuTs0UU44U)与本地 tokens/：
1. 用 use_figma 读 4 个变量集合的全部变量(名、各 mode 的值、alias 指向)
2. 读全部颜色样式与文本样式，以及各自绑定的变量
3. 与 tokens/ 下的 JSON 逐项比对，只报差异：值不同 / Figma 有本地无 / 本地有 Figma 无
4. 不要直接改文件，先给我差异清单
```

拿到清单后再决定哪些落地 —— **不是所有 Figma 改动都要跟**（对方可能在试验中）。

### 3.3 落地

```bash
cd dsv2/zymix-ui-skill2
# 1. 差异落到 tokens/ 下的 JSON(真源)——不要直接编辑 tokens.css
# 2. 生成快照
python3 scripts/sync_tokens.py
# 3. 判断影响面(见下表)，同步 skill 侧文件
# 4. 合规检查 + 打包 + 提交
python3 scripts/check_compliance.py assets/template.html
bash scripts/pack.sh
```

**影响面判断** —— 这一步最容易漏，Figma 改一个值往往牵连多个 skill 文件：

| Figma 改了什么 | 除 tokens.css 外还要改 |
|---|---|
| 字号 / 字重 / 行高 | `references/typography.md`、`DESIGN.md` 字阶表、**`assets/template.html` 的 `.t-*` 类**、`assets/templates/app.html`（内嵌副本！）、`scripts/check_compliance.py` 白名单 |
| 语义色新增 / 改名 | `references/color-rules.md`、`DESIGN.md` 颜色表、`tokens/styles/color-styles.json` |
| 组件形态（尺寸/配方/变体） | `references/components.css`、`patterns.md`、`spec.md`、`DESIGN.md` 组件节、`dsv2/components/specs/<组件>.md` |
| 图标 | `references/icons-bundled.json`、`icons.md`、CDN 版本号 |

### 3.4 冲突与回头改 Figma

- **本地已按旧值改过 skill**：以 Figma 为准，重新同步；若认为 Figma 那边不对，**先沟通再改**，别单方面在 Figma 里改回去。
- **落地时发现 Figma 有问题**（如样式绑错变量、命名不合规、档位缺失）：记进对应的 `components/specs/*.md` 待定事项 + 告知规范设计师，不要默默绕过。本轮就发现过 8 个 specimen 的 sample 绑错样式、`Show Action 2` 布尔没接节点可见性这类问题。
- **你直接改了 Figma**（用户要求时）：两边都落地 + 告知对方，见铁律 1。

---

## 4. 阶段流程（主动改规范时）

> 当你**直接改 Figma + 本地**时走这套（如整轮字阶改版、新建组件）。日常从 Figma 拉取走 [§3](#3-反向同步figma-先变时的主流程)。

### 阶段 A · 需求输入

**输入形态**（本项目常见三种）：

| 形态 | 处理方式 |
|---|---|
| 改版 Figma 稿（另一个文件） | 用 `get_screenshot` 看视觉 + `use_figma` 读结构（fills / textStyle / layout / 变量绑定）。**先确认它用的是不是 ZymixUI 的样式** —— 若设计师已按规范绑定，配方可直接沿用 |
| 参考截图 / 竞品 | 放 `references/`，只读不改 |
| 一句话需求 | 直接进阶段 D 或 F（看是改组件还是出原型） |

**读改版稿时必查三件事**：

1. 颜色是绑**样式**还是绑**变量**还是裸值 —— 决定搬过来要不要改绑
2. 引用的组件是 `remote: true`（来自 Kit 库，可直接用）还是 `remote: false`（对方文件本地组件，**跨文件无法 import，只能按结构重建**）
3. 有没有「深色模式」这类**手动变体维度** —— ZymixUI 惯例是靠 02 Semantic 的 Dark mode 自动翻转，不做深色变体

### 阶段 B · Token 层改动

```bash
cd dsv2/zymix-ui-skill2
# 1. 改 tokens/ 下的 JSON(真源)
# 2. 生成快照
python3 scripts/sync_tokens.py
# 3. 核对 Figma 与本地是否一致(可选)
python3 scripts/check_figma_sync.py <figma-export.json> tokens
```

**然后同步到 Figma 变量**（`use_figma`）。改值用 `setValueForMode`，新增用 `createVariable` + **显式设 `scopes`**（默认 ALL_SCOPES 会污染所有属性选择器）。

**清理变量的判据 —— 别只看 Figma。** 「没有样式绑定」不等于「没人用」：`tokens.css` 是另一个消费方。行高变量常因样式用 AUTO 行高而没被绑定，但 CSS 侧一直在输出 `--leading-*`。删之前两边都查。

**验证**：`tokens.css` 逐项比对预期值、该删的确实没了、该留的都在。

### 阶段 C · 样式层（颜色 / 文本 / 效果）

**命名规则**（`color-styles.json` 的 `$rule`）：中文在前、英文+数值在后；纯色显 hex，透明度显 %。

```
描边 Border/纯白 White #FFFFFF        →  border/white
文字图标 Text&Icon/次文字 Secondary #000000 55%  →  foreground/muted
```

> 名字里带 hex 是双刃：设计师查色方便，但**改色值就要改样式名**（85 个样式里带 hex 的都算）。改名对代码侧无影响（研发引用变量），纯粹是设计侧返工。

**同步 `tokens/styles/color-styles.json`** —— 新增/删除样式都要在这里登记，它是「样式名 ↔ 变量」的映射真源。

### 阶段 D · Figma 组件

**开工前先 inspect**：读现有变体、属性、绑定，match 已有约定，不要另起一套。

#### D1. 变体设计的三个判据

| 情况 | 做法 | 理由 |
|---|---|---|
| 某档语义错配（如徽标的红叫 danger） | **整档改名 + 改配方** | 改名不碰实例、不丢覆写。新增档要 clone（丢属性引用）+ swap 实例（丢文字覆写），两个坑都得踩 |
| 某维度只剩一个值（如 variant 只剩 primary） | **移除该维度** | 单值 VARIANT 是面板噪音 |
| 某维度只对部分 type 有意义（如 Active Tab 只对 tabs 有意义） | **拆成独立组件集** | Figma **无法按 Type 过滤 VARIANT 属性** —— 混在一起会让其他 Type 也显示那个下拉，选了就跳变体。补全矩阵要造大量冗余副本，不可取 |

#### D2. 属性面板整洁（用户最常抱怨的点）

- **关掉嵌套实例的属性冒泡**：`n.isExposedInstance = false`。一个玻璃圆钮会把 `Tinted / Size / icon / BG.State / icon.style / icon.keywords` 六项冒到面板、还带折叠层级。代价是换图标要双击进实例内部。
- **属性顺序 = 定义顺序，API 只能追加不能插入。** 想重排只能删了重建 —— 而 `combineAsVariants` 本来就会重建属性 key，**拆组件集时是重排的唯一免费时机**。
- **按对象分组**：`Tab 1 → Show Dot 1 → Tab 2 → Show Dot 2 …`，改哪个 tab 就看哪一段，而不是把所有 Tab 排一起、所有 Show Dot 排一起。
- **哪些做属性、哪些交给图层**：会反复切换的状态（红点开关）做属性；配置一次的数量（显示几个 tab）交给图层面板隐藏 —— 少 3 个属性。判据是「元素好不好在图层里找」：8×8 的红点难找，整个 tab 好找。

#### D3. 绑定与验收

- 颜色绑样式（铁律 2）、几何绑 `03 Layout`、文字绑文本样式
- 视觉微调值（2px 指示条厚度、7px 间距）用硬值即可 —— 档位化无意义，但要在规格文档写明
- **验收**：`node.screenshot()` 看视觉（`get_screenshot` 可能返回缓存旧图）+ 程序审计（零裸 hex、零原始变量绑定、零归档残留、零裸字体）+ Light/Dark 双模式

### 阶段 E · 组件规格文档

落在 `dsv2/components/specs/<组件>.md`，用 [`_template.md`](../../components/specs/_template.md) 起步。**除了配方表，必须写这四类**：

1. **决策理由** —— 为什么这么定（如「徽标没有 danger，因为徽标上的红是通知提醒不是警示」）
2. **踩过的坑** —— 下次同类操作能绕开
3. **待定事项** —— 需要谁定、定什么、代价是什么
4. **出厂检查** —— 勾选式，含未完成项

> 写给「换一个对话的自己」看。判断标准：只读这份文档能不能重现所有决策。

### 阶段 F · skill 同步与打包

改动落到 skill 的**哪些文件**取决于改了什么：

| 改了什么 | 要同步的 skill 文件 |
|---|---|
| Token 值 | `references/tokens.css`（跑 `sync_tokens.py`） |
| 字阶 | `references/typography.md`、`DESIGN.md` 字阶表、**`assets/template.html` 的 `.t-*` 类**、`assets/templates/app.html`（它内嵌了副本！）、`scripts/check_compliance.py` 白名单 |
| 用色规则 | `references/color-rules.md`、`DESIGN.md` |
| 组件形态 | `references/components.css`、`references/patterns.md`、`references/spec.md`、`DESIGN.md` 组件节 |
| 图标 | `references/icons-bundled.json`、`icons.md`、CDN 版本号 |

**易漏点**：`assets/templates/app.html` 内嵌了一份 tokens 和 components CSS 的**副本**（三处重复的 `.t-*` 定义），改 `references/` 不会自动生效。徽标改玫红那次就漏了它。

```bash
# 合规检查(每个模板 + 生成的页面都要跑)
python3 scripts/check_compliance.py <page.html>
# 版本号:README 头部 + CHANGELOG 表 + DESIGN.md 头部
# 打包(固化了压缩与排除规则,勿手写 zip 命令)
bash scripts/pack.sh
```

**提交**：commit message 用中文、分号分隔要点、结尾注明重打包；正文写清「为什么」和「影响面」。

---

## 5. Figma Plugin API 踩坑清单

本项目实测，都造成过静默错误或返工。

| 坑 | 症状 | 对策 |
|---|---|---|
| `component.clone()` 不复制 `componentPropertyReferences` | 实例上 `setProperties` 返回成功、`componentProperties` 有值，但**文字不变**，永远显示主组件字面值 | 加完变体逐个子层拷回：`dst.children[i].componentPropertyReferences = src.children[i].componentPropertyReferences` |
| `instance.swapComponent()` 清掉实例属性覆写 | 文字回落默认值、`showXxx` 布尔失效 | 换主组件前记下覆写，换完 `setProperties` 补回 |
| `isExposedInstance` **写入会静默失败** | 写完读回仍是 `true`，不报错 | 必须读回校验 + retry（clone 出来的实例尤其容易） |
| 删组件属性后实例上剩余同类型属性**按位置重映射** | `Show Action` 莫名变 false、按钮消失 | 删属性后逐个复核受影响实例的同类型属性值 |
| 隐藏 auto-layout 里的文字后 HUG **不收缩** | 纯圆点宽度停在带文字时的值，切换 sizing 也不重算 | 显式 `layoutSizingHorizontal='FIXED'` + `resize()` |
| GRID 布局的 `gridRowAnchorIndex` **只读**，位置由变体属性笛卡尔积顺序决定 | 矩阵不完整（删了部分组合）时连续填充、整张规范矩阵错行 | 改 `layoutMode='NONE'` 手动设 x/y（手动布局才能留空格） |
| `getMainComponentAsync()` 在嵌套实例（id 带 `;`）上抛 "Node not found" | 遍历报错中断 | 只遍历顶层：`findAll(n => n.type==='INSTANCE' && !n.id.includes(';'))` + try/catch |
| `skipInvisibleInstanceChildren` 默认 `true` | 实例内隐藏子层 `findAll` 找不到 | 脚本开头设为 `false` |
| `setBoundVariable` 报 unloaded font（含无关字体如 Noto Sans JP） | 改字重时抛错 | 把文件里可能用到的字体全部 `loadFontAsync` 后再改 |
| 继承来的绑定改不动 | 节点层解绑会让文字**脱离文本样式变裸字体**，重新应用又继承回来 | 继承的绑定只能在**源头（样式层）**改：`TextStyle.setBoundVariable(field, null)` |
| INSTANCE_SWAP 不继承颜色覆写 | 换完图标变默认黑 | swap 后手动把填充指到与文字相同的样式 |
| `get_screenshot` 可能返回缓存旧图 | 验收看到旧状态 | 用 `node.screenshot()` |
| `figma.notify()` 抛 "not implemented" | — | 用 `return` 输出 |
| 模式覆写指向**已删除的 collection**，等于没设 | 文档页那张「Dark」演示卡里全按 Light 解析：黑底黑字、白方框；肉眼像是"组件深色模式坏了"，其实是卡片没真的切到 Dark | 校验 `node.explicitVariableModes` 的每个 key 是否还在 `getLocalVariableCollectionsAsync()` 里；**补**上 `02 Semantic → Dark` 的覆写（旧 key 留着无害，别删——可能还有僵存的归档变量靠它解析） |
| 页面 `bg` 衬底 / 文档演示卡是裸灰 `#F5F5F5` | 与浅灰底控件同色 → 控件在自己的规范页上看不见 | 衬底绑「页面背景 Background/底 Base」，文档演示卡绑「容器表面 Surface/底 Base」，都是白 |
| **说明文档模板自己绑原始变量** | `Information` 卡的正文/边框/卡底几乎整片绑归档变量 → 文档页本身深色模式就是坏的，且违反「绑样式」铁律 | 文档层与页面标注层一律改绑颜色样式；**嵌套实例内部的层要回源头组件改**（Chip / Tag / Kbd / Link / Spinner / _HeaderDocs / _FooterDocs），在实例上改只会堆覆写 |
| 删阴影时把聚焦光环一起删了 | focus 态失去反馈 | 按 `spread` 区分：老微阴影 = `spread 0` + `alpha ≤ 0.06`（blur 0.5/1/2/4）；聚焦光环 = `spread 2/4`、alpha 1.00。只删前者 |
| 状态描边绑错档（`hover` 拿到 accent、`focus` 拿到透明变量） | 聚焦态**从来没有描边**，而移动端根本没有 hover；因为透明所以肉眼看不出绑错 | 治理时逐档打印 `state → fill/stroke 样式名`对照表，别只看有没有归档残留 |
| 壳组件自己画状态样式 | 同一状态在「壳」和「本体」两处实现，改本体时壳不跟 | 优先让本体（Input）提供 state，壳只透传；做不到时在规格文档里写明状态由壳覆写 |
| 拿「带文字的 OR 分隔线」组件当小短横用 | 该组件是 `Line + 文字 + Line`；压窄到几 px 后中间文字一隐藏，**两条线并排挤在一起**，渲染出来像 bug | 小短横直接用一条 `LINE`。替换实例时把原实例的 `componentPropertyReferences` 转到新节点上，否则控制显隐的布尔属性直接失效 |
| **新建变量默认 `scopes = ["ALL_SCOPES"]`，会暴露在设计师的取色器里** | 设计师本该只看到「颜色样式」，却在变量列表里看到 `ink/base` 这类原始变量，容易被直接选用（违反「绑样式不绑变量」铁律） | 建完变量立刻 **scope 清零**：`v.scopes = []`。这是本项目的既有约定 —— 02 Semantic / 01 Primitive 的**所有 COLOR 变量都是 `[]`**。<br>**注意分类型**：`[]` 对 COLOR 合法，对 **BOOLEAN 非法**（会抛 `Invalid scope for this variable type`）；FLOAT 按用途给具体 scope（描边宽 `["STROKE_FLOAT"]`、圆角 `["CORNER_RADIUS"]`、尺寸/间距 `["WIDTH_HEIGHT","GAP"]`、字号 `["FONT_SIZE"]`、行高 `["LINE_HEIGHT"]`）。别无脑全清 |
| 跨语义族混搭（底绑 A 族、文字绑 B 族） | 两族解析值相同时**完全看不出来**（Button 的 `secondary` 底绑「成功 Success/浅底」、文字绑「主色 Accent/浅底文字」，都是 `#26D93E @15%`） | 审计时按"同一元素的底/文字/描边是否同族"对照，别只看有没有归档残留。改绑前后逐一比对解析值确认视觉零变化 |
| 文档实例上的游离颜色覆写 | 同一 variant 在两张示例卡里颜色不一样；或文档绑了原始变量而组件绑的是样式 | 与主组件逐层对照后对齐，规则见下一条 —— **对齐时必须把「主组件是裸色值」的层排除在外** |
| **「给图标补文字色」的批量对齐把材质层一起染了**（本项目真实事故） | 玻璃按钮在文档里变成纯黑药丸 + 看不见的文字（Light 黑底黑字 / Dark 白底白字）；品牌 logo 的 `#FFFFFF` 层被染成会翻转的「主文字 Primary」 | 批量对齐的兜底分支（两边都没样式 → 按同实例文字色补）**只对图标可见层成立**。**判据：主组件对应层是「裸色值」（既无样式也无变量）→ 一律不动**，那是玻璃材质（`Fill + Shadow`/`Tint + Shadow`/`Glass Effect`）、品牌 logo、图标内部 source 层。主组件绑变量的层改成样式属升级，可以做。<br>还原方法：清掉实例样式后**再把主组件的 paints 拷回来** —— 单纯 `setFillStyleIdAsync('')` 只解绑、颜色会停在被染后的值，不会自动回落 |
| 用「–」字形当占位短横 | 笔画粗细跟着字号字重走（24 Bold 下约 2.4px），比正文数字还抢眼 | 用 `LINE` + `border/width`，粗细独立可控 |
| **图标不跟文字变色** | 文字每档都绑对了 foreground 样式，但图标实例没有填充样式、内部 `VECTOR:icon` 绑着 `foreground/base` → 图标永远黑（实心彩底档最明显：白字黑图标）。`foreground/base` 是**现存**变量、深浅也正常跟随，**审计报告看起来完全清白** | 把图标实例的填充指到**该变体文字用的同一个样式**（在图标实例上设样式是正当覆写）。检查方法：逐变体对比「文字样式 vs 图标样式」，别只看有没有归档残留。已修 Chip / Tag |

**通用姿势**：脚本原子执行（报错则完全不生效，可安全重试）；每步 `return` 受影响的 node id；小步验证而非一次做完。

---

## 6. 验收清单

**Token / 样式层**

- [ ] `tokens.css` 值与 JSON 一致（跑一次 `sync_tokens.py` 应无 diff，即幂等）
- [ ] `color-styles.json` 条目数 = Figma 颜色样式数；`text.json` = Figma 文本样式数
- [ ] 无占位键名（`(见Figma双语名)` 这类）
- [ ] 组件与页面层零裸 hex（**注意**：02 语义层允许直接写值，不要求 alias 01 —— 01 只是参考色板）
- [ ] **新建变量已 scope 清零**（COLOR → `[]`；FLOAT 给具体 scope）—— 设计师取色器里只该出现颜色样式，不该出现原始变量

**组件层**

- [ ] 颜色 100% 绑样式，零原始变量绑定、零裸 hex
- [ ] 几何绑 `03 Layout`，文字绑文本样式，零裸字体
- [ ] 零 `zz_Archive/*` 归档残留（含经文本样式继承的）
- [ ] 变体结构同构；矩阵零重叠
- [ ] 属性面板无冗余折叠分组（嵌套实例已 unexpose）
- [ ] Light / Dark 双模式截图验证
- [ ] 触控热区 ≥ 44pt（视觉 < 44 的要补透明热区）
- [ ] 规范页自身干净：`bg` 衬底为白、文档演示卡为白、Dark 演示卡的模式覆写指向**现存**的 `02 Semantic`
- [ ] **说明文档与页面标注层也绑样式**（`Information` 卡正文/边框/卡底、变体矩阵旁的小灰字与分区线）
- [ ] 逐档核对 `state → fill/stroke 样式名`，确认 focus/error 的描边没绑错档
- [ ] **带图标的组件：逐变体对比「文字样式 vs 图标样式」是否一致**（图标绑 `foreground/base` 时审计看不出问题）
- [ ] 删阴影后 focus 光环仍在（按 `spread` 区分，别一刀切）

**skill 层**

- [ ] `check_compliance.py` 对所有模板 + 生成页 PASS
- [ ] `.t-*` 文字角色类与字阶一致（含 `app.html` 内嵌副本）
- [ ] 版本号三处同步（README 头部、CHANGELOG、DESIGN.md）
- [ ] `bash scripts/pack.sh` 通过，包内容抽查为新版

---

## 7. 常用命令

```bash
cd dsv2/zymix-ui-skill2

python3 scripts/sync_tokens.py                          # JSON 真源 → tokens.css
python3 scripts/check_compliance.py <page.html>          # 原型合规(字号/字重/圆角/裸值)
python3 scripts/check_figma_sync.py <export.json> tokens # Figma 与本地 token 对账
bash scripts/pack.sh                                     # 打包 .skill
python3 tokens/scripts/validate.py                       # token JSON 结构校验
```

---

## 8. 各文档读者对照

| 文档 | 谁读 | 管什么 |
|---|---|---|
| 本文 `docs/SOP.md` | 设计系统维护者 | 流程与顺序 |
| [`DESIGN.md`](../DESIGN.md) | 设计 AI / 设计师 | 规范事实源（色/字/组件/材质） |
| [`SKILL.md`](../SKILL.md) | AI（生成原型时） | 原型生成规则与基线组件 |
| [`README.md`](../README.md) | 所有人 | 总览 + 版本历史 |
| [`TOKENS-GUIDE.md`](../TOKENS-GUIDE.md) | 研发 | 怎么取用 token |
| [`PROTOTYPE-GUIDE.md`](../PROTOTYPE-GUIDE.md) | 设计师 / 产品 | 怎么用 skill 出原型 |
| [`references/*.md`](../references/) | AI | 分模块细则（用色、排版、图案、工艺、动效） |
| [`dsv2/components/specs/*.md`](../../components/specs/) | 设计系统维护者 | 单个组件的规格与决策记录 |
| [`dsv2/docs/03-figma-pages.md`](../../docs/03-figma-pages.md) | 设计师 | Figma 文件页面组织规范 |
