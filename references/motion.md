# 动效规范 Motion(平台中立 · Web + iOS/SwiftUI 双映射)

> 目标不止 HTML 原型——同一套动效 token 要能落到真实产品(含 iOS)。所以值是**平台无关的抽象**(时长 ms、缓动=贝塞尔控制点、弹簧=Apple duration/bounce),下面给 Web(CSS)和 iOS(SwiftUI)两套映射。

动效 token 源:`tokens/motion.json`;Web 变量已注入 `references/tokens.css`(`--duration-*` / `--ease-*`)。

---

## 决策框架(写任何动画前依次自问)

### 1. 该不该动?看**用户一天看几次**
| 频率 | 决策 |
|---|---|
| 100+ 次/天(键盘快捷键、命令面板) | **永不做动画** |
| 几十次/天(hover、列表切换) | 去掉或大幅削弱 |
| 偶发(模态、抽屉、Toast) | 标准动画 |
| 罕见/首次(引导、庆祝) | 可加惊喜 |

**键盘触发的操作永不加动画**——一天重复几百次,动画只会让它显得慢、脱节。

### 2. 目的是什么?每个动画都要能答"为什么动"
有效目的:空间一致性(Toast 同向进出→滑动消除符合直觉)、状态指示、解释说明、反馈(按钮按下缩放)、避免突兀(元素凭空出现/消失像坏了)。若只是"看着酷"且用户常看到 → 不做。

### 3. 用什么缓动?
- 入场/退场 → **ease-out**(`--ease-out`)起步快=响应感
- 屏内移动/形变 → **ease-in-out**(`--ease-in-out`)
- hover/颜色 → **standard**(`--ease-standard`,≈CSS ease)
- 匀速(跑马灯/进度) → linear
- **UI 一律禁用 `ease-in`**:起步慢,正是用户最盯着看的那一刻延迟,300ms 的 ease-in 比同时长 ease-out *感觉*更慢。
- 内建 CSS 缓动太软,一律用上面的自定义曲线 token。

### 4. 多快?(UI 铁律:<300ms)
| 元素 | 时长 token |
|---|---|
| 按钮按压反馈 | `--duration-fast` 120ms(100-160) |
| tooltip / 小弹层 | `--duration-base` 180ms(125-200) |
| 下拉 / 选择 | `--duration-base`~`moderate` 180-240ms |
| 模态 / 抽屉 | `--duration-drawer` 400ms(退场更快→用 base) |
| 营销 / 解释 | 可更长 |

感知性能:更快的 spinner 让加载"感觉"更快;180ms 的下拉比 400ms 更跟手。

---

## Token → 平台映射

### 时长 duration
| token | 值 | CSS | SwiftUI |
|---|---|---|---|
| fast | 120ms | `var(--duration-fast)` | `.easeOut(duration: 0.12)` |
| base | 180ms | `var(--duration-base)` | `.easeOut(duration: 0.18)` |
| moderate | 240ms | `var(--duration-moderate)` | `0.24` |
| slow | 300ms | `var(--duration-slow)` | `0.30` |
| drawer | 400ms | `var(--duration-drawer)` | `0.40` |

### 缓动 ease(贝塞尔控制点)
| token | 控制点 | CSS | SwiftUI |
|---|---|---|---|
| out | 0.23,1,0.32,1 | `var(--ease-out)` | `.timingCurve(0.23, 1, 0.32, 1, duration: 0.2)` |
| in-out | 0.77,0,0.175,1 | `var(--ease-in-out)` | `.timingCurve(0.77, 0, 0.175, 1, duration: 0.3)` |
| drawer | 0.32,0.72,0,1 | `var(--ease-drawer)` | `.timingCurve(0.32, 0.72, 0, 1, duration: 0.4)` |
| standard | 0.25,0.1,0.25,1 | `var(--ease-standard)` | `.easeInOut(duration: …)` |

### 弹簧 spring(Apple duration/bounce,自然物理感、可打断)
| token | 值 | SwiftUI | CSS |
|---|---|---|---|
| subtle | duration 0.4 / bounce 0.1 | `.spring(duration: 0.4, bounce: 0.1)` | 无直接等价,用 out 曲线近似 |
| default | 0.5 / 0.2 | `.spring(duration: 0.5, bounce: 0.2)` | — |
| playful | 0.5 / 0.3 | `.spring(duration: 0.5, bounce: 0.3)` | — |

弹簧用于:拖拽带动量、需要"活"的元素(Dynamic Island)、可中途打断的手势。bounce 保守 0.1-0.3,多数 UI 不加弹。**弹簧维持速度、可打断**;CSS transition/keyframe 打断会从零重启——手势场景优先弹簧。

---

## 组件写法(CSS + SwiftUI)

### 按压反馈:scale(0.97)
```css
.btn{transition:transform var(--duration-fast) var(--ease-out)}
.btn:active{transform:scale(0.97)}   /* press-scale token = 0.97 */
```
```swift
.scaleEffect(isPressed ? 0.97 : 1)
.animation(.easeOut(duration: 0.12), value: isPressed)
```
subtle 缩放 0.95-0.98,任何可按压元素都该有。

### 入场:禁止 scale(0),从 0.95 + opacity 起
```css
/* 坏:凭空出现 */  .in{transform:scale(0)}
/* 好 */           .in{transform:scale(0.95);opacity:0}
```
```swift
.scaleEffect(shown ? 1 : 0.95).opacity(shown ? 1 : 0)
```
现实里没有东西从零出现;哪怕极小初始尺寸也更自然。

### @starting-style 入场(纯 CSS,替代 useEffect mounted)
```css
.toast{opacity:1;transform:translateY(0);
  transition:opacity var(--duration-drawer) var(--ease-out),transform var(--duration-drawer) var(--ease-out)}
@starting-style{.toast{opacity:0;transform:translateY(-100%)}}
```

### 弹层从触发点缩放(origin-aware)
弹层/气泡从触发点缩放,不从中心;`transform-origin` 设到触发处(Radix 用 `var(--radix-popover-content-transform-origin)`)。**例外:模态居中,保持 center。**

### 进出不对称:决策慢、响应快
按住要慢(hold-to-delete 2s linear),松手要快(200ms ease-out)。用户在决策处放慢,系统响应处提速。

### stagger 入场(多元素依次)
每个比前一个延迟 30-80ms 级联;别太长否则显慢;stagger 是装饰,不能挡交互。

### TabBar 切换:iOS 原生微动效(默认必带)
底部导航切换 tab 时**默认**带三段克制的 iOS 风格微动效(模板 app.html 已内置,直接复用):
1. **激活底板滑动(还原 iOS 26 TabBar 选中胶囊,关键)**——激活色块**不是每个 tab 各自 toggle 背景(那样是硬切)**,而是**一个共享的指示条 `.tab-indicator`** 平滑滑到选中 tab。手感**克制**(iOS 26 原生风,不是夸张的橡皮筋横跨):切换时做两段式的**小幅方向性拉伸 + spring 回弹**——第一段前缘先落到目标、后缘略滞后形成一点顺向拉伸(`lean = min(|dist|*0.4, 单宽*0.5)`,与距离挂钩但**封顶**,永不横跨整条),~90ms 后第二段收拢到目标单宽;过渡用带轻微过冲的 spring 曲线 `cubic-bezier(.34,1.3,.64,1)`(`--duration-slow` 300ms),落位自然回弹。`.tab.active` 本身 `background:transparent`,底色只由这个指示条承担。指示条绝对定位在 `.pill` 内(`top/bottom:4px`,圆角 round);**首帧与 resize 用 `.no-anim` 直接落位不动画**。
2. **图标 pop**——新激活 tab 的面性图标做一次轻弹:`scale .82→1.08→1`,`--duration-moderate`(240ms)、`--ease-out`,近似 iOS SF Symbol `.bounce`。**只在"从别的 tab 切过来"时放一次,重复点当前 tab 不重放**。
3. **内容淡入**——新屏 `opacity 0→1 + translateY(6px)→0`,`--duration-base`(180ms)`--ease-out`,类似原生页面切换的轻推淡入;切到同一屏不重放。
```css
.tab-indicator{position:absolute;top:4px;bottom:4px;left:0;width:0;border-radius:var(--radius-round);background:var(--accent-soft-subtle);transition:transform var(--duration-slow) cubic-bezier(.34,1.3,.64,1),width var(--duration-slow) cubic-bezier(.34,1.3,.64,1);pointer-events:none;z-index:0} /* spring 缓动带回弹 */
.tab-indicator.no-anim{transition:none}
.tab{position:relative;z-index:1}
.tab.active{background:transparent}   /* 底色交给滑动指示条 */
@keyframes tabPop{0%{transform:scale(.82)}55%{transform:scale(1.08)}100%{transform:scale(1)}}
.tab.pop .ic-fill{animation:tabPop var(--duration-moderate) var(--ease-out)}
@keyframes screenEnter{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
.phone .screen.is-active.enter{animation:screenEnter var(--duration-base) var(--ease-out)}
@media (prefers-reduced-motion:reduce){ .tab-indicator{transition:none} .tab.pop .ic-fill{animation:none} .phone .screen.is-active.enter{animation:screenFade var(--duration-base) linear} }
```
```js
// 切 tab:两段式液态拉伸(先跨度桥接,再收拢到目标);首帧/resize 传 noAnim=true 直接落位
function place(l,w){ ind.style.transform='translateX('+l+'px)'; ind.style.width=w+'px'; }
function moveInd(noAnim){ var at=document.querySelector('.tab.active'); if(!ind||!at) return;
  var nl=at.offsetLeft, nw=at.offsetWidth; clearTimeout(indT);
  if(noAnim||!indInit){ ind.classList.add('no-anim'); place(nl,nw); void ind.offsetWidth; ind.classList.remove('no-anim'); indInit=true; indL=nl; indW=nw; return; }
  if(nl===indL) return;
  var dist=nl-indL, lean=Math.min(Math.abs(dist)*0.4, nw*0.5); // 克制拉伸,封顶,不横跨整条
  place(dist>0 ? nl-lean : nl, nw+lean);             // ① 前缘落到目标、后缘略滞后 → 小幅顺向拉伸
  indT=setTimeout(function(){ place(nl,nw); }, 90);  // ② 收拢到目标(spring 回弹)
  indL=nl; indW=nw; }
```
```swift
// iOS: 底板用 matchedGeometryEffect 让选中背景在 tab 间滑动;图标 .symbolEffect(.bounce, value: selected);内容 .transition(.opacity.combined(with:.offset(y:6)))
```
底板滑动用**可打断的 transition**(连点也能顺滑重定向,别用 keyframe);pop/淡入用一次性 keyframe(切 tab 偶发)。**只动 transform/opacity/width**(width 在导航条这种小元素上开销可接受),`prefers-reduced-motion` 下三者全关、只保留淡入。除非用户明确要求"无动效/瞬切",否则默认带上。

---

## 性能铁律
- **只动 `transform` 和 `opacity`**(跳过 layout/paint,走 GPU);别动 width/height/margin/padding。
- 动态/可快速触发的 UI(Toast 连发、状态切换)用 **CSS transition**(可打断、可重定向),别用 keyframe(从零重启)。
- SwiftUI 同理:值驱动 `.animation(_, value:)` 天然可打断。
- 只写具体属性:`transition:transform 200ms var(--ease-out)`,**禁止 `transition:all`**。

## 无障碍
```css
@media (prefers-reduced-motion:reduce){
  .x{transition:opacity var(--duration-base) var(--ease-standard)}  /* 保留透明度/颜色,去掉位移 */
}
@media (hover:hover) and (pointer:fine){ .x:hover{/* hover 动画只在真鼠标 */} }
```
```swift
@Environment(\.accessibilityReduceMotion) var reduceMotion
// reduceMotion ? nil : .spring(...)
```
减少动效 ≠ 零动效:保留帮助理解的透明度/颜色,去掉位移。

---

## 硬规则(合规检查会拦)
- ❌ `transition: all` → 必须写具体属性
- ❌ UI 用 `ease-in`(非 ease-in-out)→ 改 `--ease-out` 或自定义曲线
- ⚠ 单条 UI 过渡时长 >400ms(营销除外)→ 收进 ≤300ms
- ⚠ 从 `scale(0)` 入场 → 改 `scale(0.95)+opacity`
- 时长/缓动一律用 token(`--duration-*` / `--ease-*`),别写魔法数
