# Tokens 接入指南（技术）

> 面向工程师：如何拿到、引入并使用 ZymixUI 的设计变量（Design Tokens）。
> 设计师 / 产品请看 [PROTOTYPE-GUIDE.md](./PROTOTYPE-GUIDE.md)。

---

## 最新 tokens 在哪(单一真源)

**`references/tokens.css`** —— 唯一真源，直接引用它即可。

- 共 **347 个 CSS 变量**，含 Light + Dark 两套值。
- 文件头写着 `由 sync_tokens.py 生成，勿手改`：它是从 Figma 变量同步出来的**快照**，不要手工改值；要改去改 Figma，再跑同步脚本（见文末）。
- 语义规范、每个角色的用途判据看 [DESIGN.md](./DESIGN.md)。

> 一句话：**值只信 `references/tokens.css`，语义只信 `DESIGN.md`。**

---

## 怎么引入

### 1. 直接引入 CSS 变量

```html
<link rel="stylesheet" href="references/tokens.css">
```

或打包进你的全局样式：

```css
@import "./tokens.css";
```

引入后，所有变量在 `:root` 下可用，直接 `var(--*)`：

```css
.btn-primary{
  background: var(--accent-base);
  color: var(--accent-foreground);
  border-radius: var(--radius-round);
}
```

### 2. 命名规则(Figma 角色 → CSS 变量)

Figma 里是 `组/角色` 的斜杠层级，落到 CSS 全部**扁平化 + 连字符 + 加 `--` 前缀**：

| Figma 角色 | CSS 变量 |
|---|---|
| `accent/base` | `--accent-base` |
| `accent/soft-foreground` | `--accent-soft-foreground` |
| `foreground/muted` | `--foreground-muted` |
| `radius/round` | `--radius-round` |
| `size/16` | `--size-16` |

规则:斜杠 `/` → 连字符 `-`，整体前缀 `--`，全小写。

---

## 深浅色机制(重要)

tokens.css 用**属性选择器**分层，一套语义变量两套值：

```css
:root, [data-theme="light"] { /* Light 值 */ }
[data-theme="dark"]         { /* Dark  值 */ }
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]) { /* 系统深色时自动套 Dark */ }
}
```

- **默认跟随系统**：不加任何属性，浅色环境用 Light、深色环境自动用 Dark。
- **强制浅色**：给根元素 `<html data-theme="light">`（或 JS `documentElement.setAttribute('data-theme','light')`）。
- **强制深色**：`data-theme="dark"`。
- 你的组件只写 `var(--foreground-base)` 这类语义变量，**不用关心当前是深是浅**，值会自动切。

---

## 变量分类速览(347 个)

| 类别 | 变量数(Light) | 前缀示例 |
|---|---|---|
| 尺寸 size | 54 | `--size-16` `--size-48` |
| 行高 leading | 26 | `--leading-body-base` |
| 功能色 feature | 13 | `--feature-like-base` `--feature-im-bubble-friend` |
| 圆角 radius | 12 | `--radius-md` `--radius-round` |
| 文字 foreground | 10 | `--foreground-base` `--foreground-muted` |
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

> 完整角色语义（每个角色的用途、accent vs success 判据、红色三分等）见 [DESIGN.md](./DESIGN.md) 第 2 节。

### 核心色彩角色(最常用)

| 角色 | Light | Dark | 用途 |
|---|---|---|---|
| `--accent-base` | `#26D93E` | `#26D93E` | 主按钮 / 选中 / 强调 |
| `--accent-soft` | `rgba(38,217,62,.15)` | `rgba(38,217,62,.12)` | 浅底强调背景 |
| `--foreground-base` | `#000000` | `#FFFFFF` | 主文字 |
| `--foreground-muted` | `rgba(0,0,0,.55)` | `rgba(255,255,255,.55)` | 次要文字 |
| `--background-base` | `#FFFFFF` | `#0B0B0D` | 页面底 |
| `--surface-base` | `#FFFFFF` | `#18181B` | 卡片 / 面板 |
| `--separator-base` | `rgba(0,0,0,.10)` | `rgba(255,255,255,.10)` | 0.5px 发丝分隔线 |
| `--danger-base` | `#EA4B46` | `#EA4B46` | 危险按钮填充 |
| `--radius-round` | `9999px` | `9999px` | 胶囊 / 圆 |

---

## 接入代码示例

### 原生 HTML / CSS
```html
<link rel="stylesheet" href="tokens.css">
<button style="background:var(--accent-base);color:var(--accent-foreground);
               height:48px;border-radius:var(--radius-round);border:none">Confirm</button>
```

### React（inline / styled）
```jsx
// 引入一次:import './tokens.css'
export const Card = ({children}) => (
  <div style={{
    background: 'var(--surface-base)',
    borderRadius: 'var(--radius-lg)',
    color: 'var(--foreground-base)',
    padding: 16,
  }}>{children}</div>
);
```

### Tailwind（映射到语义变量）
```js
// tailwind.config.js
theme: { extend: { colors: {
  accent: 'var(--accent-base)',
  'fg': 'var(--foreground-base)',
  'fg-muted': 'var(--foreground-muted)',
  surface: 'var(--surface-base)',
}}}
```

原则:**永远引用变量，绝不写死 hex**。深浅色、后续改版都靠变量自动生效。

---

## 与 Figma 同步 / 更新机制

tokens 的源头是 Figma 变量，本地 `tokens.css` 是它的快照。规范更新流程：

1. **对账**：用 `use_figma` 导出当前 Figma 变量为 `figma-export.json`，再跑
   ```bash
   python3 scripts/check_figma_sync.py <figma-export.json> <tokens 目录>
   ```
   它会报出 Figma 与本地 JSON 值不一致 / 一方缺失的 token。
2. **对齐后重新生成**：
   ```bash
   python3 scripts/sync_tokens.py /path/to/dsv2/tokens
   ```
   从 tokens JSON 重新生成 `references/tokens.css` 快照。
3. 重新打包 `zymix-ui-prototype.skill` 发布。

> 记住：**不要手改 `tokens.css`**（会被下次同步覆盖），改值一律回 Figma。
