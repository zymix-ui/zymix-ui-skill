# ZymixUI Design Tokens 接入指南

面向工程师的设计变量(Design Tokens)接入文档:如何获取、引入并在代码中使用 ZymixUI 的颜色、尺寸、字号、圆角等设计变量,以及配套组件层的用法与更新机制。

---

## 1. 单一真源

设计变量的唯一真源为 **`references/tokens.css`**。

- 共 **199 个 CSS 变量**,包含 Light / Dark 两套值。
- 该文件为 **Figma 变量的同步快照**,由 `scripts/sync_tokens.py` 生成,**不应手动修改**(改动会在下次同步时被覆盖)。变量值的调整需在 Figma 完成后重新同步。
- 变量的语义定义与用途判据(如 accent 与 success 的区分、危险色的使用场景)见 `DESIGN.md` 第 2 节。

原则:**变量值以 `references/tokens.css` 为准,变量语义以 `DESIGN.md` 为准。**

---

## 2. 引入方式

通过标准 CSS 引入,变量即在 `:root` 下全局可用:

```html
<link rel="stylesheet" href="references/tokens.css">
```

或在全局样式中导入:

```css
@import "./tokens.css";
```

使用时以 `var(--*)` 引用:

```css
.btn-primary{
  background: var(--accent-base);
  color: var(--accent-foreground);
  border-radius: var(--radius-round);
}
```

---

## 3. 命名规则(Figma 角色 → CSS 变量)

Figma 中的 `组/角色` 斜杠层级,在 CSS 中统一扁平化为连字符,并加 `--` 前缀、全小写:

| Figma 角色 | CSS 变量 |
|---|---|
| `accent/base` | `--accent-base` |
| `accent/soft-foreground` | `--accent-soft-foreground` |
| `foreground/muted` | `--foreground-muted` |
| `radius/round` | `--radius-round` |
| `size/16` | `--size-16` |

规则:斜杠 `/` 转连字符 `-`,整体加前缀 `--`,全部小写。

---

## 4. 深浅色机制

同一套语义变量对应两套值,通过属性选择器分层。组件只需引用语义变量,无需关心当前主题:

```css
:root, [data-theme="light"] { /* Light 值 */ }
[data-theme="dark"]          { /* Dark  值 */ }
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]) { /* 系统深色时自动套用 Dark */ }
}
```

- **跟随系统(默认)**:不设置任何属性,浅色环境使用 Light,深色环境自动切换 Dark。
- **强制浅色**:根元素设 `data-theme="light"`。
- **强制深色**:根元素设 `data-theme="dark"`。

例如 `color: var(--foreground-base)` 在浅色下为黑、深色下为白,值随主题自动切换,无需在业务代码中判断。

---

## 5. 变量分类

| 类别 | 数量(Light) | 前缀示例 |
|---|---|---|
| 尺寸 size | 54 | `--size-16` `--size-48` |
| 行高 leading | 26 | `--leading-body-base` |
| 功能色 feature | 13 | `--feature-like-base` `--feature-im-bubble-friend` |
| 圆角 radius | 12 | `--radius-md` `--radius-round` |
| 文字 foreground | 11 | `--foreground-base` `--foreground-emphasis` `--foreground-muted` |
| 中性 default | 8 | `--default-base` `--default-white` |
| 危险 danger | 7 | `--danger-base` `--danger-soft-foreground` |
| 强调 accent | 7 | `--accent-base` `--accent-soft` |
| 表面 surface | 6 | `--surface-base` `--surface-secondary` |
| 成功 success | 6 | `--success-base` |
| 信息 info | 6 | `--info-base` |
| 动效时长 duration | 6 | `--duration-*` |
| 分隔 separator | 5 | `--separator-base` `--separator-strong` |
| 字重 weight | 4 | `--weight-regular` `--weight-black` |
| 缓动 ease | 4 | `--ease-*` |
| 描边 border | 4 | `--border-base` `--border-subtle` |
| 背景 background | 4 | `--background-base` `--background-secondary` |
| 骨架 skeleton | 2 | `--skeleton-base` |
| 遮罩 backdrop | 2 | `--backdrop-base` |
| 字体族 family | 1 | `--family-base` |

完整角色语义见 `DESIGN.md` 第 2 节。常用核心角色:

| 角色 | Light | Dark | 用途 |
|---|---|---|---|
| `--accent-base` | `#26D93E` | `#26D93E` | 主按钮 / 选中 / 强调 |
| `--accent-soft` | `rgba(38,217,62,.15)` | `rgba(38,217,62,.12)` | 浅底强调背景 |
| `--foreground-base` | `#000000` | `#FFFFFF` | 主文字 |
| `--foreground-emphasis` | `rgba(0,0,0,.80)` | `rgba(255,255,255,.80)` | 强调文字 / 标题副文 |
| `--foreground-muted` | `rgba(0,0,0,.55)` | `rgba(255,255,255,.55)` | 次要文字 |
| `--background-base` | `#FFFFFF` | `#0B0B0D` | 页面底 |
| `--surface-base` | `#FFFFFF` | `#18181B` | 卡片 / 面板 |
| `--separator-base` | `rgba(0,0,0,.10)` | `rgba(255,255,255,.10)` | 0.5px 发丝分隔线 |
| `--danger-base` | `#EA4B46` | `#EA4B46` | 危险按钮填充 |
| `--radius-round` | `9999px` | `9999px` | 胶囊 / 圆 |

---

## 6. 组件层(components.css)

Tokens 为原子变量层。组件规范(Button、NavBar、TabBar、Toast、玻璃材质、气泡、列表等)位于 **`references/components.css`**,提供可直接复用的组件类,并全部以 `var(--*)` 消费 tokens 变量(如 `.btn-primary{ background: var(--accent-base) }`)。

引入顺序:先 `tokens.css`(变量),后 `components.css`(组件),不可颠倒。

```html
<link rel="stylesheet" href="references/tokens.css">
<link rel="stylesheet" href="references/components.css">

<button class="btn btn-primary btn-lg">Confirm</button>
<button class="btn btn-glass-42 glass">…</button>
```

### 组件类清单

| 组件 | 类名 | 说明 |
|---|---|---|
| 按钮 Button | `.btn` + `.btn-primary` / `-secondary` / `-tertiary` / `-outline` / `-ghost` / `-danger` / `-danger-soft`;尺寸 `.btn-lg` / `-md` / `-sm` | 7 变体 × 3 尺寸,胶囊形 |
| 玻璃圆钮 | `.btn-glass-42`(配 `.glass`) | NavBar / TabBar 专用 42px 液态玻璃圆钮 |
| 液态玻璃材质 | `.glass` / `.glass-clear` / `.glass-primary` | 导航、悬浮、Toast 底材 |
| NavBar 页头 | `.header-brand` / `.header-nav` / `.header-tabs` / `.header-chat` | 4 变体:品牌大标题 / 居中标题+返回 / 标签栏 / 聊天页头 |
| TabBar 底部导航 | `.tabbar` + `.tab`(激活态 `.tab.active`) | 玻璃胶囊,内置 Scroll Edge 底部模糊(`.no-edge` 关闭) |
| Toast | `.toast`(配 `.glass`) | 顶部胶囊,中性色 |
| IM 气泡 | `.bubble` + `.bubble-friend` / `-stranger` / `-other`;回执 `.read-friend` / `.read-stranger` | 好友 / 陌生人 / 系统气泡 |
| 列表 | `.list-row` | 行高 ≥64、头像 48、0.5px 分隔线 |
| 其它 | `.badge`(未读徽标)、`.input-bar`(输入条)、`.media` + `.scrim-b`(媒体 + 底渐变)、`.phone`(手机骨架)、`.zi`(图标位) | — |

组件的尺寸与用法规则(TabBar 高 62、NavBar 42 圆钮、骨架标配等)见 `references/patterns.md`;视觉语义见 `DESIGN.md`。图标不在 CSS 内,取自图标库 `references/icons-bundled.json`(69 个常用)或完整图标库 [zymix-ui/zymix-icons](https://github.com/zymix-ui/zymix-icons)(721 个)。

---

## 7. 接入示例

### 原生 HTML / CSS
```html
<link rel="stylesheet" href="tokens.css">
<button style="background:var(--accent-base);color:var(--accent-foreground);
               height:48px;border-radius:var(--radius-round);border:none">Confirm</button>
```

### React
```jsx
// 全局引入一次:import './tokens.css'
export const Card = ({ children }) => (
  <div style={{
    background: 'var(--surface-base)',
    borderRadius: 'var(--radius-lg)',
    color: 'var(--foreground-base)',
    padding: 16,
  }}>{children}</div>
);
```

### Tailwind(映射到语义变量)
```js
// tailwind.config.js
theme: { extend: { colors: {
  accent: 'var(--accent-base)',
  fg: 'var(--foreground-base)',
  'fg-muted': 'var(--foreground-muted)',
  surface: 'var(--surface-base)',
}}}
```

原则:**始终引用变量,不写死具体色值**。深浅色切换与后续版本更新均通过变量自动生效。

---

## 8. 与 Figma 同步 / 更新

Tokens 的源头为 Figma 变量,`references/tokens.css` 是其快照。规范更新流程:

1. **对账**:导出当前 Figma 变量为 `figma-export.json`,运行
   ```bash
   python3 scripts/check_figma_sync.py <figma-export.json> <tokens 目录>
   ```
   报告 Figma 与本地 token 值不一致或缺失的项。
2. **重新生成**:对齐后运行
   ```bash
   python3 scripts/sync_tokens.py /path/to/tokens
   ```
   从 tokens 源重新生成 `references/tokens.css`。
3. 发布更新后的技能包 `zymix-ui-prototype.skill`。

`references/tokens.css` 为生成产物,请勿手动编辑;所有变量调整在 Figma 完成后经上述流程同步。
