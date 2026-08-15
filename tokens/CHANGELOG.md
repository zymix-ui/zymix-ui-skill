# Tokens 变更记录

## 2026-08-13
- 与 Figma(NxaWnZYT… 新基准文件)全量对账后归零:
  - 修 `default/soft`、`default/soft-pressed` 浅色基色 235,235,236 → **235,235,235**(此前 #EBEBEC→#EBEBEB 统一时遗漏的两处 rgba)
  - 补录 `size/2`、`size/14`(03 Layout 2026-08 新增)、`border/width-strong`(=2)
  - `border/white` 由硬值 #FFFFFF 改 alias `{default.white}`,与 Figma 对齐
  - `check_figma_sync.py` 增设有意差异白名单:`family/base`(系统字体栈)、`mode/is-*`(Figma 专用布尔)、`feature/nav/background`(skill 原型层专用)

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

## 2026-08-01

- **效果样式**:新建两个 Figma 效果样式「聚焦 Focus/焦点环 Ring」(accent/base spread 4 + separator/base spread 2)与「聚焦 Focus/输入聚焦 Field」(accent/base spread 2),内部绑变量(效果颜色只能绑变量,不能绑颜色样式)。Checkbox focus 六档、InputOTP focus 两档已改绑;Foundations 页的 Ring/Field 示例块也改绑,规范页自身成为样式实例。`effect.json` 的 Focus/Ring 第二层原记为 `background.secondary #F5F5F5`,与 Figma 实测不符,按实测校正为 `separator.base`。
- **Foundations 页 Shadows 一节改写为「已废弃」**并删掉 Base/Subtle/Floating/Thumb/Inner 五个示例块 —— 阴影体系 2026-07 已废弃、Figma 无对应效果样式、本地已归入 `zz_Deprecated Shadow`,只有该页说明文字未同步,造成"规范写了但样式库没有"的错觉。总述文案同步去掉"优先使用 Shadow"。
- **颜色样式改名**:`产品特性 Feature/点赞 Like #FF3B64` → `产品特性 Feature/积极强调 Positive #FF3B64`。语义早已扩展为通用积极强调红(点赞 + 徽标通知红点/计数角标,与 danger 区分),仅样式名滞后。变量名 `feature/like/base` 保留(历史命名,描述中已注明),故 `--feature-like-base` 与所有 CSS 不受影响。
- **`color-styles.json` 按 Figma 校正**:7 条键名补回 `#000000`(如 `次文字 Secondary 55%` → `次文字 Secondary #000000 55%`);补 `文字图标 Text&Icon/纯白 White #FFFFFF`;删 Figma 已无的 `导航 Nav/渐变遮罩 Fade`(Scroll Edge 改用 ProgressiveBlur)与 `纯色 Solid/纯白 White`(Figma 用「固定白 Static White」)。校正后 85 条,与 Figma 一致。
- **按钮文字样式归位**:Figma 的「按钮 Button/标准 Base」`fontStyle` 原绑 `weight/semibold` → 改绑 `weight/bold`;「按钮 Button/小 Sm」`fontSize`/`lineHeight` 原绑 `size/body-xs`(12)/`leading/label-xs`(16) → 改绑 `size/button-sm`(14)/`leading/button-sm`(20)。变量值本来就对,是样式绑错了变量,属 2026-07-31 字阶改版遗漏。修完把 Button 组件集 63 处标签改绑(lg→标准 Base ×21、sm/md→小 Sm ×42),另 `_Label - Text - Preferred|Default` 4 处裸 SF Pro Medium 17 也改绑标准 Base(17 Medium→16 Bold,真实视觉变化,方向与 Liquid Glass Text 一致)。**本地 text.json / typography.md / components.css 一直是对的,本次是 Figma 单边落后 —— 字阶层对账要双向比对,不能只信 Figma。**

## 2026-08-01 · 颜色体系调整(设计师批量指令)

**text&icon(foreground)**:删 `emphasis`(80%)、`faint`(15%)、`ghost`(8%) 三档 + 对应 on-dark 档(共 6 变量 / 6 样式);`muted` 55%→**60%**;`disabled` 浅26%/深22% → 统一 **20%**(on-dark 同改)。梯子由 8 档精简为 5 档。
**background**:删 `secondary`(雪白 #FCFCFC,与 base 太近);`inverse` #18181B → **纯黑**;新增 `inverse-tertiary`(反色页面第二层)。
**surface**:反色扩到三级 —— 新增 `inverse-secondary` #1C1C1F、`inverse-tertiary` #2A2A2E(深色列为 #F5F5F5 / #EBEBEB),用于浅色模式下深色容器的多层级。
**separator**:删 `strong`(40%)与 `width-strong`。
**border**:新增 `avatar`(浅黑3%/深白5%),头像描边,避免白色头像糊在白底上。
**新增「墨色 Ink」族 6 档**(base/pressed/foreground/soft/soft-pressed/soft-foreground)= 原指令里「base #000 + foreground #fff + soft 5%/15%」那套黑色强调实底。**没有改动「中性 Default」** —— 审计发现 Default/底 Base 仅前 40 页就有 359 处在用(Button tertiary、Chip default、Kbd、Tag 底,以及刚定稿的表单 secondary 档),改纯黑会与「表单浅灰底」定稿冲突,故按设计师裁决另立新族。

**删除前的重映射**(避免破绑定):Templates 的 faint 描边/`strong` 竖线 → `separator/base`;Templates 三个页面底 + Brand 白 logo → `background/base` / `纯色 Solid/固定白`;Materials 三个玻璃组件集的描边 → `分割线 Separator/底 Base`;输入类 11 页文档卡底 12 处 → `页面背景 Background/灰 Tertiary`;Foundations Radius 示例 20 处 → 刻度数字改「辅助文字 Tertiary」(同为 40%,零视觉变化)、预览方块描边改「描边 Border/底 Base」;Foundations 色板里被删档位的 12 张示例卡直接删除。
**Separator 组件删 `variant=strong` 两个变体**(横/竖)+ 文档展示实例,variant 收敛为 base/subtle。
删除前分两批全库复核零残留(含 `separator/width-strong`)。

**顺带清掉的本地 drift**:`feature/nav/fade-solid`·`fade-transparent` —— Figma 根本没有 `feature/nav/*` 变量,`.nav-fade` 机制早已作废(改 Scroll Edge / ProgressiveBlur),本地残留已删;`feature/nav/background` 保留但加注「Figma 无对应变量,仅供 skill 原型层近似还原」。`figma-display-names.json` 的 `Nav/Fade` 条目同步删除。
**`assets/templates/app.html` 内嵌三份 token 副本已同步**:删 9 处废变量定义 ×11 类、改 alpha、`background-inverse` 改纯黑、每处补 10 个新变量;消费端 `.island-div`→`on-dark-disabled`、`.scroll-ind`→`ink-soft-pressed`(与旧 faint 同值同翻转)、`.chev`→`foreground-disabled`、分栏竖线与会话页底改绑、`.nav-fade` 规则删除。两模板合规 PASS,浏览器渲染无报错。
- **Button 新增 `variant=ink` 黑底白字档**(18 变体,总数 126→144):底/按下/文字绑「墨色 Ink」三档,深色模式自动翻白底黑字。由 primary 克隆并**逐层拷回 `componentPropertyReferences`**(5 个非变体属性:label/prefix/suffix/showPrefix/showSuffix,clone 会丢),18 个变体引用数逐一比对一致;组件集为手动布局,按列步进 872 手动排位、集宽 6136→6968、页面 bg 扩到 7329 并补 ink/sm/md/lg 标注。skill 侧新增 `.btn-ink`。
- **修回归:Button 文档的玻璃按钮被染坏**(设计师报)。前一轮「给图标补文字色」的批量对齐,兜底分支「两边都没样式 → 按同实例文字色补」把**主组件是裸色值**的层也染了:玻璃材质 `Fill + Shadow` #FFFFFF@65% / `Tint + Shadow` / `Glass Effect` #808080@90% 变成文字色 → Light 黑底黑字、Dark 白底白字,文字与药丸全部消失;同批还染坏页眉页脚品牌 logo 的 #1A1A1A / #FFFFFF 层与 Chip 图标 source 层。共 32 处已按主组件还原(清样式 + 拷回 paints,单纯解绑不会回落)。SOP §5 已补正判据:**主组件是裸色值的层一律不动**。
- **input 系列圆角 12 → 24**:`Input`(6 变体)、`InputGroup`(36)、`_InputOTPCombinedField`(12)的外框圆角由绑 `radius/md`(12) 改绑 **`radius/3xl`(24)**,共 216 处角(每变体 4 角)。48 高 + 24 圆角 = 胶囊形。`TextField` / `TextArea` / `NumberField` / `SearchField` 四个壳内部的 Input/InputGroup 实例是**继承绑定而非覆写**,本体一改自动跟随(扫描时看到实例有 boundVariables 别误判成覆写)。**`_InputOTPField`(分离式单格)保持 12 —— 46×48 的格子在 24 圆角下会被吃成圆形**,已试改后回退,属有意例外。skill 侧 `.field` / `.otp-single` 改 `--radius-3xl`,`.otp-cell` 保持 `--radius-md` 并加注。
- **新增变量 scope 清零**(设计师发现遗漏):`createVariable()` 默认 `scopes=["ALL_SCOPES"]`,会让原始变量暴露在设计师取色器里,违反「绑样式不绑变量」。本次新增的 10 个 COLOR 变量(ink 六档 + background/inverse-tertiary + surface/inverse-secondary·tertiary + border/avatar)已全部 `scopes=[]`,与 02 Semantic 既有 77 个 COLOR 变量一致。顺带修正 03 Layout 的历史遗漏 `size/42`·`size/54`(`["ALL_SCOPES"]` → `["WIDTH_HEIGHT","GAP"]`,与同集合 size/* 对齐)。**分类型**:`[]` 对 COLOR 合法、对 BOOLEAN 非法(`mode/is-*` 保持原样);FLOAT 按用途给具体 scope。全库 scope 分布已复核一致。
- **`foreground/on-dark/subtle` 35% → 40%**(设计师指定),样式改名「辅助文字(深底) Tertiary On-Dark #FFFFFF 40%」。注意:此后它与 `foreground/subtle` 的 Dark 值(35%)不再逐档等值,DESIGN.md 里「档位对齐 foreground 深色列」那句已改为「大体对齐」。
- **删除「文字图标 Text&Icon/纯白 White #FFFFFF」样式**。删前审计发现它**有 44 处在用,且全是误用**:该样式绑的是 `foreground/inverse`(Light 白 / **Dark 翻黑**),名字却叫「纯白」,于是 Foundations 色板 43 处 + Templates 1 处把它当恒定白,给叠在彩色/深色块上的标签用 —— 深色模式下这些标签全变黑、糊在绿底红底上(已截图证实)。**先把 44 处改绑「纯色 Solid/固定白 Static White」修掉这个深色模式 bug,样式归零后才删。**
  遗留:`foreground/inverse` 现已无对应颜色样式,而 Button 页有 **8 处直绑该变量**(玻璃按钮 tinted 文字),与「每个语义色变量都要有颜色样式」「组件绑样式不绑变量」两条自定规则冲突 —— 若要合规,需补建一个「文字图标 Text&Icon/反色 Inverse #FFFFFF」样式并把那 8 处改绑。
- **补建「文字图标 Text&Icon/反色 Inverse #FFFFFF」**(= `foreground/inverse`),替代上一条删掉的「纯白 White」。名字如实反映"会随主题翻转",描述里写明与「纯色 Solid/固定白」的分工。Button 页 8 处直绑 `foreground/inverse` 变量的层(玻璃 Symbol 钮图标内部)已改绑该样式 —— **全库零直绑**,`foreground/inverse` 恢复"有对应颜色样式"。那 8 处是图标隐藏 source 层,浅/深双模式截图复验视觉零变化。样式总数 87。

## 2026-08-03

- **Chip 去掉 warning 概念,整档改 info**(与 Badge 同一裁定:体系无通用橙)。12 个变体 `type=warning` → `type=info`,66 处颜色由归档 `intent/warning/{base,foreground,soft,soft-foreground}` 改绑「信息 Info/{底 Base,文字 Foreground,浅底 Soft,浅底文字 Soft-foreground}」;**Chip 组件集归档绑定归零**。改名前记录了 14 处在用 `type=warning` 的实例(Chip 页 8 / Table 4 / Getting Started 2),改完逐个复核 —— Figma 重命名变体值时会自动同步实例属性,14 处全部落在 `info`,无失效。
- **`foreground/subtle` 的 Dark 值 35% → 40%**,与 `on-dark/subtle` 重新逐档等值(DESIGN 与 color-rules 里「不再等值」的注解已撤回)。`app.html` 六处内嵌副本同步。
- **补合并式验证码的文档说明**:InputOTP 文档新增「Layouts 两式布局」一节(插在 Composition 之后),含 separated / combined 并排演示与选型说明;Examples 的 Light / Dark 两张卡各补一个合并式实例(3 分离式 + 1 合并式)。
- **样式体检(颜色 87 / 文本 33)**:
  - 颜色样式全部绑变量、零归档、无多重填充;**87 语义色变量 ↔ 87 颜色样式 1:1 完全对应**,无缺失、无一变量多样式。
  - 修 1 处名实不符:「IM 气泡/好友弱文字 Friend Muted」名字写 55% 而实际 60% —— 它 alias `foreground/muted`,随全局次文字档一起加深了,只是名字滞后。已改名并在描述里注明 alias 关系。
  - **修回归:按钮两档文本样式的绑定被撤销过**。`按钮 Button/标准 Base` 的 `fontStyle` 退回 `weight/semibold`、`按钮 Button/小 Sm` 的 `fontSize` 退回 `size/body-xs`(12),而 `lineHeight` 保留了修正 —— **部分回退**,不像人工整体撤销,更像 `TextStyle.setBoundVariable` 未持久化。已重做并用「改完换一次脚本调用、重新 `getLocalTextStylesAsync` 再读回」的方式验证持久化(比同调用内读回严格)。Button 页文字分布 48 + 28 = 76(原 63 + ink 新增 9 + _Label 4),零裸字体。
  - 文本样式零归档、零"值与变量不符";11 个 lineHeight 未绑变量的样式经核实**全部是 AUTO 行高**(Title/Label/Body 三族),属设计使然。
- **ink 四档接上 Primitive alias**(铁律「语义层必须 alias 基础层」):`ink/base`→`color/black`·`color/white`、`ink/foreground`→反向、`ink/soft-foreground`→同 base 向、`ink/pressed`→`color/neutral/800`·`color/neutral/200`。值完全不变,`tokens.css` 输出无差异。只接两个模式都能精确对应的,避免制造「Light alias / Dark 直值」的混合态(全库混合态仍为 0)。
- **Primitive 校正 + 语义层大批接上 alias**(设计师指定):`color/neutral/200` #EBEBEC→**#EBEBEB**、`color/neutral/100` #F4F4F5→**#F5F5F5**,让 Primitive 与语义层实际用色对齐。
  借此把**所有「两个模式都能精确对应 Primitive」的直值语义色接上 alias,共 19 个** —— accent/base→brand.500、danger/base·pressed→red.500·600、info/base·pressed→blue.500·600、foreground/base·inverse→black·white、background/base→white·neutral.950、surface/base→white·eclipse、**surface/tertiary→neutral.200·neutral.800(靠本次改值才对上)**、background/inverse-tertiary→eclipse·**neutral.100(同上)**、backdrop/glass→alpha.white-1·alpha.black-2、default/white·black、surface/inverse、feature/wallet/unverified→orange.500·400、default/soft-foreground→eclipse·snow 等。
  **02 Semantic 颜色 alias 覆盖率 19/87 → 38/87,混合态(Light alias / Dark 直值)保持 0。** 逐字节比对 `tokens.css`:整个重构**只有 `--ink-pressed` 深色值 #EBEBEC→#EBEBEB** 一处变化(它 alias 了 neutral/200,属改 Primitive 的预期连带,1 单位无感),其余 19 个新接 alias **零值变化**,证明是纯语义重构。87 个颜色样式名实一致性复核**零不符**。
  > 踩坑:改变量值会触发 Figma 的字体加载检查,报 unloaded font 且**点名文件里 TEXT 节点上根本不存在的字体**(Noto Sans JP Black/Medium、Noto Sans Symbols2 Regular —— 它们不在任何 TEXT 的 fontName 上)。必须在**同一次脚本调用内**把这些字体也 loadFontAsync(跨调用不保留)。
  > 遗留:`#EBEBEC` 现在没有 Primitive 支撑了,但仍有 5 个语义色在用(`default/base`、`default/soft`、`default/soft-pressed`、`border/subtle`、`skeleton/base`),与新的 neutral/200(#EBEBEB)差 1 单位、接不上 alias。要不要一并统一到 #EBEBEB 待设计师定。
- **统一 #EBEBEC → #EBEBEB**(承接上一条):`default/base`、`default/soft`(50%)、`default/soft-pressed`(65%)、`border/subtle`、`skeleton/base` 五个语义色的 Light 值改为 #EBEBEB,对应 5 个颜色样式名同步改名。**全库 #EBEBEC 零残留**(Figma 变量 + 本地 JSON + tokens.css + DESIGN/color-rules 文档)。名实一致性复核零不符。
  > **纠正我上一条里的说法**:当时说「统一了这 5 个也能接上 alias」并不准确 —— 它们的 **Dark 值(#27272A / #333338)在 Primitive 里没有原子**,所以整条 alias 仍接不上,只有 Light 侧对得上 `neutral/200`。为不制造「Light alias / Dark 直值」的混合态,这三个非 alpha 档暂仍保持直值(alias 覆盖率仍 38/87,混合态 0)。
  > **根因是 Primitive 的深色中性梯子太粗**:900(#18181B) 直接跳到 800(#2F2F34),而语义层实际用到 #232327、#27272A、#333338、#3A3A40 四个中间值,全都没有原子。**只差 Dark 原子就能整条接上的有 7 个**:default/base、border/base·subtle、background/tertiary、surface/secondary、skeleton/base·highlight。补齐这 4 个中间档(命名如 neutral/850 等)即可,属结构调整,待设计师定。
- **架构口径纠正:01 Primitive 只是参考色板,02 Semantic 不需要绑定它**(设计师明确)。此前我按 CLAUDE.md 铁律 1 的字面理解一路推 alias 覆盖率,还提议往 01 补深色中性原子来"补齐"—— 方向错了。02 直接写值是允许的,01 的梯子有缺口是正常的;「禁硬编码色值」指的是**页面与组件层**不许写裸 hex。真正该复用的是 **02 内部的 alias**(success→accent、border/white→default/white 等)。`docs/SOP.md` 铁律 3 整条重写、验收清单相应改写,`tokens/README.md` 顺带修掉过时的「Figma 无 01 集合」(现有 68 个 Primitive 变量)。
  > 遗留:当前 38 个 alias 中有 19 个指向 01(本轮接上的),值全部正确、输出无差异,**未撤回**。若希望 02 完全独立不受 01 调整影响,可把这 19 个改回直值。
- **Button 说明文档补墨色档**:变体清单「7 种样式」→「8 种」并把 ink 插在 primary 之后(附选型说明);属性面板 `variant` 枚举加 ink;Light / Dark 两张示例卡各加一个墨色按钮(文案 Continue),深色卡自动翻白底黑字。
- **规范文件迁移到新链接**(设计师变更):Kit fileKey `dL2XGEOGAeKfXWhMRp7smR` → **`NxaWnZYT4ZidZuTs0UU44U`**(文件名 ZymixUI Figma Kit for AI),后续所有改动基于新文件。已核对内容一致:4 个集合(01=68 / 02=93 / 03=35 / 04=69)、颜色样式 87 / 文本 33 / 效果 3、99 页,**且 2026-08-13 当天全部改动都在新文件里**(neutral/200=#EBEBEB、neutral/100=#F5F5F5、default/base=#EBEBEB、foreground/subtle 深色 40%、accent/base→alias brand/500、ink/pressed→alias neutral/200、样式名零 EBEBEC 残留、Chip warning 档已清零)。**节点 ID 实测完整保留**,历史记录的节点 ID 仍可用。`docs/SOP.md` 对账口令里的 fileKey 已改。
- **全量样式/变量体检(新文件)**:变量侧 —— alias 断链 0、缺 mode 值 0、归档命名残留 0、命名不规范 0、COLOR 变量无 `ALL_SCOPES` 污染。样式侧 —— 87 个颜色样式全部绑变量,零裸值、零多层 paint、零名实不符、零重复(每变量恰好一个样式)、02 语义色 100% 覆盖;33 个文本样式名实零不符,字号/字体/字重 33/33 全绑,无绑错集合。
  > `letterSpacing`/`paragraphSpacing` 0/33 绑定是**正常的** —— 正是此前"20 个样式绑到 zz_Archive"那个 bug 修好后的样子(现走 Figma 默认值)。`lineHeight` 11/33 未绑也正常 —— 未绑的恰好是全部 11 个 AUTO 行高档,Figma 的 AUTO 行高绑不了数值变量。
  > 「孤立变量」多数是**误报,别删**:03 Layout 全部 35 个由组件直接绑(Figma 无间距样式)、01 Primitive 51 个是参考色板用不到的档、04 Font 10 个 `leading/*` 对应 AUTO 行高档(只被 tokens.css 消费)、`mode/is-light·is-dark` 绑玻璃图层可见性。
  > **唯一真残留:`weight/black`** —— 字阶改版已废 Black 900 改 Heavy,DESIGN.md 也写明"不再用 Black 900",但 04 Font 里该变量还在、零文本样式绑它,`tokens.css` 仍输出 `--weight-black: "Black"`。建议删(或在文档标注保留不用),待定。
- **删除已废字重档 `weight/black`**(体检发现的唯一真残留)。2026-07-31 字阶改版已把 Black 900 换成 Heavy 800,但该变量一直留在 **04 Font**(不是 01 参考层,是文本样式实际绑定的层),且 `tokens.css` 仍输出 `--weight-black: "Black"` —— **与 DESIGN.md「四档 Regular/Semibold/Bold/Heavy,不再用 Black 900」直接矛盾,而原型 AI 是把 tokens.css 当规范读的**,属会自己发作的坑,不是单纯占地方。
  删前验证:零文本样式绑定、零 alias 引用、**全库 99 页 16809 个 TEXT 节点零绑定** → 删除零风险。04 Font 69→68,剩 regular/semibold/bold/heavy 四档(与 DESIGN.md 一致)。
  同步五处:Figma 变量、`tokens/primitive/typography.json`、`references/tokens.css`(重新生成)、`assets/templates/app.html` 内嵌 token 副本、`TOKENS-GUIDE.md` 示例(`--weight-black`→`--weight-heavy`)。全库零残留,tokens.css 幂等已验,模板合规 PASS。
  > 顺带修两个过时描述:`weight/bold` 原写「场景专属字重(仅限 场景 Scene 排版);通用体系仅 Regular/Semibold/**Black**」—— 早就不对了,Bold 现在是 Title/Xs、Button/Base、Number/24·8、Scene 导航标题的字重;`weight/heavy` 补注它替代了废弃的 Black 900。
  > 另发现 **10 处裸用 SF Pro Black 字重的文字**(硬写 fontName、不经变量),全在「备份」与「Navbar 案例收集」两个归档页,不受本次删除影响,但本身违反「绑样式」规则。优先级低,未处理。
- **修 skill 主模板 `assets/templates/app.html` 的 token 副本严重脱节**(用户提醒同步 skill 时查出,是本轮最大的漏)。单文件原型必须自带 token 副本,而这份副本停在 **v1.4 字阶改版与 v1.5 颜色重构之前**:
  - **22 处值漂移**:`--size-title-lg` 30→28、`--size-title-xs` 15→16、`--size-button-base` 17→16、`--size-scene-header-title` 34→28、`--size-scene-nav-title`·`--size-scene-bubble` 17→16、`--size-body-2xs` 11→10、`--leading-title-lg` 36→34、`--leading-scene-header-title` 40→34、`--backdrop-base` .40→.20、`--background-tertiary` #161619→#060607、`--family-base` "SF Pro"→系统字体栈、`--feature-im-bubble-friend-muted` .55→.60、`--danger-soft`·`--danger-soft-pressed` 旧灰底配方→玫红 alpha、以及 13 处 `#EBEBEC`→`#EBEBEB`(default-base / border-subtle / skeleton-base / ink-pressed)。
  - **16 个已删档位仍在定义**:`--size-body-lg`·`--size-body-md`·`--size-label-lg`·`--size-number-base`·`--leading-scene-tab` 等,全是字阶改版删掉的档,且**无一处被引用**,已全部删除。
  - 结构真相:该文件把**三代 token 块层叠**在一个 `<style>` 里(旧 `:root` / 紧凑版 / 最新 `[data-theme]` 版),后者在级联里覆盖前者。**没删前两代** —— 块① 是 9 个 `--duration-*`·`--ease-*` 与 5 个 `--foreground-on-dark-*` 的**唯一来源**,删了会断。
  - 复查:值漂移 0、幽灵 token 0、内嵌 token 170 个。
- **检查器补第 8 条:内嵌 token 块 vs `references/tokens.css` 对账**。上面这些问题此前一路 PASS,根因是 `strip_token_blocks()` 会先把 `:root{...}` 整块剥掉(为免误报配方里的示例 hex),导致 token 定义区**天生在检查盲区**。新规则:值不匹配 → 报「token 值漂移」;**族在 tokens.css 里但档位不在 → 报「已删除的 token」**(精准命中废弃档,又不会误伤 `--vh` 这类模板本地变量,因为 `vh` 不是 tokens.css 的族)。已用注入测试验证三类问题都能抓到。
- **修 `references/lessons.md` 两条失效经验**:①「页头 Tab 双标题(选中 24 Black / 未选中 18 Bold)」—— 该两档随字阶改版删除,改写为 Brand-Tabs 现行做法(tab 统一 `Label/Sm` 14 Semibold + 下划线);②「统计数字是 Number/Base = 18px Black(900)」—— 既无 Base 档也无 Black 字重,改为 Number 9 档、卡片内金额用 `Number/24`。这类经验条会被原型 AI 当规范读,过期即误导。
- **头像形状改版:圆形 → squircle**(设计师给参考形状 `21179:1106`)。定参数用了几何反推 + 拟合:参考路径只有 13 顶点、顶边 y=0 仅在 x=18 一点 → **无平直段**,曲线自边中点起弯,即 `r(1+s)=18`(半边长)。归一化极坐标径向签名拟合的最优解是 r=13/s=0.4(最大偏差 0.83px),但 **13 不是 radius 档位**(铁律 5),故选 **`radius/md`(12) + `cornerSmoothing 0.5`** —— `12×1.5=18` 精确满足约束、用现有档位可绑变量,最大偏差 1.24px(36px 下约 3%)。
  尺寸规则:**圆角 ≈ 尺寸 ÷ 3,就近归 `radius/*`** —— 24/26→sm、32/36→md、48→lg、56→xl、68→2xl。
  Figma 侧改到位(全库残留圆形头像归零):Avatar 组件集 25 变体(**要改两处**:`base` 矩形 + 组件根节点,根节点 r=9999 会裁剪子层;`variant=img` 那 5 个无子节点,只能改根)、AvatarGroup(另有 `Avatar multiple` 实例自身的 r=9999 覆写要单独改)、NavBar `Type=Nav-Chat` 的裸 ELLIPSE(ELLIPSE 设不了圆角,**换成 RECTANGLE**;坑:3 个实例有 IMAGE 覆写,先存 fills 换完再补回)。
  > **例外:AvatarGroup 末尾的「+」保持圆形** —— 它是 Button 实例(secondary/md/iconOnly),按钮规范就是 round,不为了跟头像一致去改。
  > skill 侧同步:`DESIGN.md` 新增「头像 Avatar」节(尺寸→档位对照表 + CSS 无 cornerSmoothing 的说明)、`app.html` 13 处圆角改档(`.avatar` 基类 50%/round → radius-md,32px→md,56px 会话列表 3xl→xl,68px 3xl→2xl,圆形归零)、`patterns.md`「48px 圆形」、`components.css`「头像36圆」、`lessons.md`「32 倒角方形」描述统一。
