# Tokens 变更记录

## 2026-07-29 · v0.8.0 配套:IM 客态气泡 + on-dark 纠错 + nav 清理

- **新增** `feature/im/bubble-guest`:客态气泡底(对方消息气泡),alias → `surface/secondary`(Light #F5F5F5 / Dark #232327),IM 专用;同步新增颜色样式「IM 气泡/客态 Guest」。
- **修复(Figma 端)** `foreground/on-dark/*` 全组 8 个变量的 Dark 值曾被错配为黑色系,已改回与 Light 相同的恒白(该组定义即"恒白·不随主题翻转");tokens 源与 tokens.css 本就正确,无需变更。
- **删除(Figma 端)** `feature/nav/background`、`fade-solid`、`fade-transparent` 与「导航 Nav」两个颜色样式(渐进模糊拆出后导航玻璃由 Liquid Glass 材质组件承担,全库零使用)。**skill/CSS 端 `--feature-nav-*` 保留**:模板 `.nav-fade` 等仍需字面量,属 CSS 实现 token,与 Figma 变量层解耦。
- **新增(Figma 端,内部管线)** `mode/is-light`、`mode/is-dark` 布尔变量:绑定玻璃材质图层可见性,实现深浅模式全自动切换;不进 CSS。

## 2026-07-20 · Materials Scroll Edge 明暗自适应修复

- **缺陷**:Materials「Scroll Edge Effect - Soft / Hard」的压暗层为固定黑色(Soft 的 Blur 矩形黑填充走 SCREEN、Hard 节点白填充走 MULTIPLY——两者对结果均为「无着色,只有模糊」),浅色页面下顶部/底部内容被模糊成灰暗,黑色前景字(如状态栏、页头标题)看不清。
- **修复**:把两组件所有变体的着色填充改为绑 `background/base`(Light #FFFFFF / Dark #0B0B0D)、blend 改 NORMAL——内容淡入页面背景色:**浅色→白、深色→黑**。Soft 保留渐变遮罩(柔和渐隐),Hard 为均匀磨砂边(节点 opacity 0.9)。
- **影响**:共享组件,NavBar(Edge=Top)与 TabBar(Edge=Bottom)自动联动;Leading/Trailing 一并处理。Light/Dark 均截图验证通过。
- 无 token 增删(仅组件填充绑定/blend 变更)。

## 2026-07-13 · Backdrop 组件化

- 新增 `backdrop/strong`:强调压暗遮罩,Light rgba(0,0,0,.60) / Dark rgba(0,0,0,.75)(暗色推测值待实机复核)——特殊场景(活动运营等需强调弹层元素)用;`backdrop/base`(20%/60%)为一般情况默认,描述同步补用途分工
- 规模:semantic +1(backdrop/strong)

## 2026-07-10 · 增量(待收口发版)

- 改 `size.body-2xs` 11→10、`leading.body-2xs` 13→12:极小字号回归产品原稿值,TabBar 底部文字等极小字场景专用,一般情况不用;样式「正文 Body/极小 2xs」描述同步,行高固定 12(新建 leading/body-2xs 并绑定)
- **行高政策定稿(2026-07-10 更正)**:特殊场景固定行高,其余一律 AUTO——此前「行高去 AUTO/全库 0 AUTO」批次记录作废。落地:固定组=Scene/Nav-Title 20、Scene/Bubble 20、Body/2xs 12(均新建 leading 变量并绑样式);Button/Text 由 Figma 固定 18 改回 AUTO;leading token 删 4 个(title-xs/label-caption/body-caption/button-text);Figma 现状 17/32 样式 AUTO 与政策相符
- ⚠️ 对账待办:styles/text.json 多数通用样式仍记显式行高(16/24 等)而 Figma 实际为 AUTO,text.json 行高字段需按政策全面对齐(跑 check_figma_sync 时处理)
- 新增 `size/54`:TabBar 标签项高度(产品线上尺寸,TabBar 组件化)
- 新增 `size/42`:玻璃圆钮尺寸,NavBar 页头 / TabBar 底部导航专用(沿用产品线上 42px;button.md 原「将来换 48 Symbol」计划作废,Symbol 加 Size=48/42 轴——48=按钮 lg 档玻璃版示例,42=圆钮,均为产品自有尺寸)
- 新增 `feature/wallet/unverified`:钱包未验证状态色,Light=orange.500 #FD7C02 / Dark=orange.400 #F79E68(暗色微调,可调);scope 清零;颜色样式并入「产品特性 Feature」组(与 点赞 Like 同组),名「产品特性 Feature/钱包未验证 Wallet Unverified #FD7C02」,fill 绑变量
- 修 `danger/soft`·`soft-pressed`:解除对 default 灰的 alias,改用 danger.base 红 #EA4B46 —— soft 15%/12%、soft-pressed 20%/16%(与 accent/info soft 同规律,修历史遗留:危险浅底原指向中性灰)
- 新增 `danger/soft-subtle`(设计师在 Figma 建变量,JSON 对齐):8%/6%,类 accent/soft-subtle,极浅红底提示;补对应颜色样式「危险 Danger/最浅底 Soft-subtle #EA4B46 8%」
- 样式名同步:danger soft/soft-pressed 由旧灰值名改为 #EA4B46 15%/20%
- 规模:semantic 78→80(+wallet/unverified、+danger/soft-subtle)
- 行高策略定稿(按文本性质分,非统一):**正文 Body / 标题 Title / 强调 Label(含超大标题 Display)→ AUTO**(内容型文本,随字体度量,匹配设计稿实际用法;iOS/安卓走字体默认、Web 走 `line-height:normal`);**场景 Scene / 数字 Number / 输入 Field / 按钮 Button / 链接 Link → 固定值**(排版/控件需确定行高)。JSON 18 个样式改 AUTO,Figma 17 个同步(Figma 缺 Label/Footnote 样式,JSON 有,待补);曾短暂把 7 个 auto 固化为 px 的动作已回退。多行正文原"保松 1.5"改为 auto≈1.2,正文整体变紧(设计取向:跟设计稿实际)。遗留:18 个内容型 `leading.*` token 因样式转 auto 变孤儿(display/title-*/label-*/body-*),待确认后清理(JSON + Figma 04 Font)

## 2026-07-07 · v2.0 定稿(初版→新系统迁移 + 全面瘦身)

结构:两层(JSON:primitive 参考 + semantic;Figma:01 参考不发布/02 语义/03 Layout/04 Font)。

- 命名对齐 HeroUI v3 + TDesign 双语分组;透明度全部整数百分比
- 删 hover 全系(移动端,pressed/focus 保留)、_legacy、04_Docs、green 色阶、opacity 刻度
- foreground 改绑 alpha 文字梯子(black/white 1-4 级,Dark 主文字 white-1 90%)
- radius 档位词化并加 2xl=22;space+size 合并为数字刻度,加 96/128;删 touch-target/control/icon/avatar 细分(转组件规格)
- 04 Font:字号/行高改 21 文字角色命名,删 medium/bold/字距/段距;21 个 Text Styles 全量绑定
- 语义层瘦身:删 focus-ring、control/disabled-opacity(转约定)、overlay(并入 surface)、segment、field 全组(转 Input 规格)、static(黑白并入 default);加 surface/pressed(8%)、backdrop/glass、separator/width(0.5)·width-strong(1)、foreground/brand、default/white·black
- 派生绑定:link→accent/soft-foreground、四白字→default/white、default/foreground→black/white
- 旧集合归档 zz_Archive/*,17/84 页已换绑(组件页跳过),删除脚本见 scripts/delete-archive.md
- 待办:danger/pressed 与 base 几乎同值,做 Button 时改 red/600

## 2026-07-07 · v2.1 设计稿试金石校准(demo 两画板比对)

- feature/im/* 新增 5 个:bubble-self(#E4FFC2)/foreground(#274700)/muted(#85A361)、accent(#62C400)/accent-soft 25%(IM 场景绿,独立于品牌绿;暗色值待定)
- foreground/base 90% → 纯黑/纯白;foreground/solid 删除(与 base 重复),样式 Solid/Black 删除(与 Primary 重复);inverse 保留(反色场景)
- background 插层:secondary=#FCFCFC/#09090B(雪白),原 secondary(#F5F5F5)顺延为 tertiary
- 画布规范(不动 token):#6A6C6C→muted;输入条/大头像圆角绑 round;Medium 字重规范为 Regular/Semibold;黑15/18/35/50%、F7F7F7/F0F0F0 等自造值逐案处理
- v2.1 更正:气泡为上下渐变——好友 #E1FFBF→#E4FFC2、非好友 #C9FAFF→#D0FAFF;端点入 token,渐变做成颜色样式(色标绑变量);accent 对称化 accent-friend(#62C400)/accent-stranger(#26D9F0,Add按钮);新增 bubble-stranger-foreground #006673(待确认)
- IM 组人工优化(设计师):删 accent-friend/-soft;bubble-friend-muted 改绑 foreground/muted(值从#85A361变为黑60%);新增 read-friend #58C138、read-stranger #00BAD2;画布上原 #62C400 元素待规范
- 测试页试点收尾:加 accent/soft-subtle(8%/6%)、feature/nav/background(玻璃底66%,暗色待定)、foreground/placeholder(30%);surface/inverse 反色容器;红色三分裁决(like/danger base/soft-foreground);01 Primitive 全量清 scope 退出选择器;F0F0F0/F6F6F6 归一 surface/secondary
- 效果体系更新:旧 Shadow 六档废弃(zz_Deprecated,新设计零使用);新增 Glass 玻璃三档样式(Button/Nav/Field,液态玻璃配方);Nav 渐变遮罩样式+fade-solid(→bg/secondary)/fade-transparent token,10 处 Fake HDR Gradient 归一;彩色光晕(紫/绿/红)按一次性特殊处理豁免
- IM 气泡去渐变改纯色:保留 start 值(好友 #E1FFBF/非好友 #C9FAFF),end token 删除,两个气泡样式改为纯色绑定,画布经样式自动更新
- foreground 加 faint(15%)/ghost(8%);气泡及其前景补深色值(推测):friend #2E4212/#D7F5B8,stranger #123C42/#9FE8F2
- 样式命名规范统一:中文前/英文数值后,颜色9+文字21+效果6全部改名;描述与当前变量值同步(修正 base 90%→纯黑的过时描述)
- 设计师改值对账:foreground/muted Light 60%→50%(样式名/描述同步);surface/secondary Dark→#18181B(与base同值,待确认);旧Shadow六档已由设计师删除;样式命名统一为中文前英文数值后
- muted 定稿55%(4.7:1达AA);surface/secondary Dark同值确认有意;新增 Placeholder/Faint/Ghost 三个颜色样式;文字样式数值 18/28→18-28(斜杠致三层bug修复)
- 文字样式名去数值后缀(Figma 选择器自带字号显示),颜色样式保留值标注

## 2026-07-08 · v2.2 发版审计定稿

- warning 警告组删除(设计师决策:警告场景并入 info/danger)
- 发版修复:zz_Archive/04_Docs 设为不发布(01_Base/02_Theme/03_Typography 归档已由设计师删除);废弃样式 Link/Sm Hover 删除;30 个变量补描述
- 全量 scope 配置:154 个变量按用途限定选择器(描边色只入描边、字号只入字号栏等),规范入 README
- 发版说明:IM 气泡/导航玻璃暗色值为推测待定稿;danger/pressed 待组件阶段改 red/600;subtle 40% 仅限辅助信息(AA 豁免)
- 颜色样式补齐 40 个:状态色五组(base/pressed/soft/soft-pressed/soft-foreground)+背景4+表面5+描边2+分割线3,全部绑变量带值命名;分割线组显示名更正为"分割线"(设计师改)
- 新增"场景 Scene"排版分类:页头大标题(34 Black/40,原auto显式化)、页头Tab选中(24 Black/19)/未选中(18 Bold/19,恢复bold字重);行高19为设计精调标记组件化复核;画布回绑4处
- 场景 Scene 三个样式设 textCase=TITLE 首字大写(设计师手动配置,已同步数据源)
- 修正排除规则误伤:Zymix 页头(名含"顶部状态栏")非系统件,改精确匹配;页头按钮/文字/图标补绑;新增 surface/glass(FAFAFA 20%)token;玻璃圆钮14处留按钮组件阶段统一处理
- 颜色样式命名升级:带透明度的统一为「hex+百分比」(21个改名,自动从绑定变量解析生成)

## 2026-07-08 · v2.3 入口架构定稿

- 变量层全英文化(229个,与 tokens JSON 完全同名,双语映射层废除)
- 02 Semantic 颜色变量→颜色样式 100% 映射:补 21 个(Foreground 系/Solid 固定黑白/玻璃/遮罩/骨架屏/Like/IM 全组/Nav),fade 渐变端点豁免
- 设计师入口=中文样式,工程接口=英文变量,中文语义保留在变量描述
- 02 Semantic 全部74个颜色变量 scope 清零:选色器只显示颜色样式,变量退居工程接口;数字变量(线宽等)保留 scope
- 描述终审:修正 default/black 引用已删的 foreground/solid、separator/base 引用旧线宽名;统一"好友"术语;清理迁移期注释;补 04 Font 空描述;42个颜色样式描述补"= 变量名"标注
- 状态色 Foreground 样式定位澄清:与同组底色配对使用(按钮字色随按钮组取),5个样式描述补配对说明;保留不删
- ⚠️事故记录:样式化升级未检查 paint 级 visible,隐藏填充被样式激活致测试页视觉损坏;恢复方案=版本历史回滚后重跑修正版;排除规则新增第⑤条(隐藏填充永不处理)
- 字重终裁:全产品仅 Regular/Semibold/Black;画布清洗 Medium×39/Bold×4→Semibold,Heavy×1→Black;weight/bold token 删除,页头Tab未选中改 18 Semibold
- 更正:Bold 保留为场景专属字重(仅场景 Scene 排版用,页头Tab未选中恢复 18 Bold);通用体系仍三字重
- 行高治理:新增 Caption 备注角色(13/auto,Body Regular+Label Semibold,auto行高由样式承载因变量无法表达);画布归位 59 处(caption 40 零位移+body-md 16+label-sm 3 微位移);15 Semibold×7 与零散紧行高23处待设计师定夺
- 新增 按钮 Button/文字 Text 角色(15 Semibold/auto,文字按钮如 See translation,区别于链接);画布套用4处
- Caption 改名「较小 Caption」(位置词+iOS官方英文);Title 加最小档(15 Semibold/auto,列表项标题,Cash gift×2 套用);立按钮文字用色铁律(必须用状态组配对 Foreground)
- 紧行高23处(Profile区昵称20/20、统计数字、快捷卡片12/12、列表项14/17等)确认为有意的紧凑排版设计,保留裸值;待做 Profile/列表组件时随组件固化为规格
- Profile 场景排版定稿(基准=Me Page):立6场景样式(昵称20/20、账号15/15、数字18/20=Number同值、标签12/14、快捷卡12/12、列表项14/17)+12 token;两画板归一20处,漂移(26/20昵称、14/14标签、20/20数字)全部拉回 Me 基准
- 设计师精简资料区场景样式(5删,改绑通用角色:昵称→Title/Sm、数字→Number、标签→Xs、卡片→Caption);孤儿token×10清理;设计师新增 Number/Md(24/32)补token绑定;裸文本收尾:Semibold17×3→Button/Base、15×1→Button/Text;Share/Expired 按钮 Inter Medium 字族违规修正为 SF Pro Semibold 并套 Button/Sm
- test 页(17233-2242)全流程验证:颜色绑定55+归一6(F7F7F7/F0F0F0→surface/secondary、E4FFC2旧渐变端点→bubble-friend、85A361→bubble-friend-muted)+样式化143+文字27;Medium×20清洗;系统件/隐藏244排除、隐藏填充53节点跳过(规则⑤)
- 场景新增:导航标题 Nav Title(17 Semibold/auto,iOS惯例,套10处)、气泡正文 Bubble(17 Regular/auto,保auto避免气泡高度位移,IM组件阶段复核,套13处);正文加极小 2xs(11/auto,套3处);列表项 List Item 设 textCase=TITLE 与场景组统一(再套3处);24 Bold×1 字重违规改 Black 归 Title/Md
- demo 页零散收尾:Add 15.86 变形字号改回 15 套 Button/Text;Search 占位→Field/Sm;20 Regular×3 为 SF Symbols 图标字符留待图标组件阶段;用色裁决:消息列表置顶行背景=surface/secondary,普通行=surface/base
- surface 改真梯子:tertiary Light #FFFFFF→#EBEBEB、secondary Dark #18181B→#232327(推翻"Dark同值有意"),两模式单调递进;撤销 Apple 抬升逻辑(tertiary 新稿零使用,仅旧Kit参考页受影响);样式「三级 Tertiary」改名 #EBEBEB,描述同步
- Foundations 规范页遗留绑定全量迁移:颜色 167 处换绑本地 02 Semantic(含发布库旧远程副本 warning→info、field/overlay/segment/static、归档 foreground/bg/muted 等映射);圆角"6"→radius/xs、width→size/32;死变量(已删集合:font/font-medium/字距/段距/旧阴影)绑定清除 499 处保值解绑;文档框架组件(_HeaderDocs2/_FooterDocs/Chip)主组件死绑定同步清理;终检:全页死绑定 0、远程样式引用 0
- 超范围修改备案(用户仅要求换绑,以下为本次多做的,待用户裁决保留或回退):Foreground/Surface/Other 区补行至全覆盖、Warning区改Info、删Form field区、Hover标签改Pressed、补13个文字标本、删失效Footnote标本、简介文案改三字重

- Figma↔JSON 对账机制建立(check_figma_sync.py):导出 Figma 变量与本地 JSON 逐项 diff;首次全量对账发现 backdrop/base Light 漂移(Figma 0.20 / JSON 0.40 滞后),按"Figma 为设计师最新"对齐 JSON→0.20 并重生成快照

## 2026-07-08 · v2.4 Stage③ 组件启动:Button

- danger/pressed 改绑 {color.red.600} #C53936(v2.0 待办完成,双模式同值);样式「危险/按下 Pressed」名与描述同步;误伤的浅底按下样式名已修回
- Button 组件集(2218:6175)全量迁移:删 hover 变体×42(移动端无 hover,剩 168=7变体×4状态×3尺寸×iconOnly);颜色/描边换绑本地 1008 处(intent/*→同名、intent/*/hover→*/pressed、line/border/base→border/base);布局绑定 2669 处(space→size、radius 16/full→lg/round、control-* 按值映射、线宽→border/width);已删概念解绑保值(焦点环效果×42、禁用透明度×42→硬值50%、字距/段距×168);零死绑定终验通过
- 规格文档 components/specs/button.md;待定:secondary/dangerSoft 底色配对、Focus 样式重建、玻璃圆钮归属
- Focus 态删除(设计师裁决:iOS 无键盘焦点环)×42,变体 126=7×3状态×3尺寸×iconOnly;变体栅格补位(pressed/disabled 行上移224),页面行标签同步,set 高度 560→336
- dangerSoft 配对方案落地:danger/soft alias→{default.soft}(灰底红字为设计意图)、danger/soft-pressed alias→{default.pressed}(按压实灰视觉不变);按钮底/按压×18 回绑 danger 组,配对铁律成立;样式名值同步(#EBEBEC 50% / #D4D4D6)
- 液态玻璃按钮两组件集(Text 85×48/Symbol 48×48,Tinted 开关)治理:颜色换绑18处(intent/accent→accent/base、content/*→foreground 系、归档 foreground-inverse→foreground/inverse,含 _Label 辅助集)、Medium 17×2→按钮 Button/标准 Base、字距段距解绑;Liquid Glass 调参绑定有意保留(社区库,Materials 页为源头)
- Toast 组件集治理:warning 变体删除(按 v2.2 裁决,渐变为纯白无损);content/on-glass×17→foreground/base;布局绑定→size×15;字距段距解绑;零死绑定
- Toast 色彩裁决(设计师):图标与文字一律中性 foreground/base,不用状态色,五类型仅图标图形区分
- 材质引用架构落地:玻璃不做效果样式,Materials 页 Liquid Glass 组件为唯一源头,组件嵌套实例引用——Toast 底从假玻璃(白渐变+模糊15+投影y22/b64)改为 Small 实例×5,过渡期「阴影 Shadow/提示 Toast」样式建后即废;玻璃按钮 BG 本就是 Small 实例(模式确认);Small Primary 着色层(LINEAR_BURN 混合)换绑 accent/base;Materials 页死绑定清理63处(intent/content/layer/line→本地),Liquid Glass 调参与 Subcomponent 槽位有意保留;effect.json 记录材质架构,Glass 三档旧配方标记"逐步被材质实例取代"

## 2026-07-09 · v2.5 feature/wallet + danger 配对修正

- feature/wallet/unverified 新增(02 Semantic):Light={color.orange.500} #FD7C02、Dark={color.orange.400} #F79E68;钱包/资产「未验证」状态色,仅钱包场景,不参与通用状态色;JSON 与 Figma 一致,DESIGN.md 颜色表同步
- **danger/soft-pressed 修正**:v2.4 误绑 {default.pressed}(实色灰 #D4D4D6 / #3A3A40),与 soft 家族脱节——soft 是半透明 {default.soft} 而按下态却跳到实色。改绑 {default.soft-pressed}(浅 rgba .65 / 暗 rgba .70),与 accent/success 的 soft↔soft-pressed 逻辑对齐。⚠ Figma 侧需同步把 danger/soft-pressed 别名从 default/pressed 改为 default/soft-pressed
- 技能 tokens.css 快照重生成,打包 v6.4

## 2026-07-10 · v2.6 Motion 层引入(平台中立 · Web+iOS)

- 新增 `tokens/motion.json`(概念上的 05 Motion):平台无关动效 token——时长 duration(instant/fast/base/moderate/slow/drawer,UI ≤300ms 铁律)、缓动 ease(out/in-out/drawer/standard,贝塞尔控制点)、弹簧 spring(Apple duration/bounce,直接对应 SwiftUI)、gesture(press-scale 0.97、swipe 速度阈值 0.11)
- 定位:不止 HTML 原型,值设计为**多端消费**——Web 出 `--duration-*`/`--ease-*` CSS 变量,iOS 出 SwiftUI `.timingCurve`/`.spring`/`.scaleEffect` 映射
- 技能侧:sync_tokens.py 注入 motion 变量;新增 references/motion.md(决策框架+双端映射+组件写法+性能/无障碍);components.css 按钮加 press-scale + reduced-motion;check_compliance.py 加动效规则(transition:all / UI ease-in → FAIL;scale(0) 入场、时长>400ms → WARN);SKILL.md/DESIGN.md 同步;打包 v6.5
- Figma 侧:motion 暂不建变量(Figma 变量不原生存贝塞尔/弹簧),以本地 motion.json 为唯一源
