# ZymixUI Tokens(单一数据源)

改这里的 JSON → 运行校验 → 生成 Figma 变量。**禁止在 Figma 里手改值。**

| 文件 | 对应 Figma | mode |
|---|---|---|
| `primitive/color.json` | 集合 01 Primitive(参考用,发布忽略,scope 已清空不入选择器) | 1 |
| `primitive/typography.json` | 集合 04 Font(隐藏) | 1 |
| `layout.json` | 集合 03 Layout | 1 |
| `semantic/color.light.json` + `color.dark.json` | 集合 02 Semantic | Light / Dark |
| `styles/color-styles.json` | Color Styles(设计师入口,fill 绑变量) | — |
| `styles/text.json` | Text Styles | — |
| `styles/effect.json` | Effect Styles | — |

同步规则:写入 Figma 时,`{color.*}` alias 解析为硬值(Figma 无 01 集合);语义层内部 alias(如 `{accent.base}`)保留为 Figma alias。格式:W3C DTCG(`$value` / `$type` / `$description`),alias 写 `{color.brand.500}`(引用 primitive)或 `{accent.base}`(引用语义层同 mode)。

**入口架构(v3)**:设计师只用「样式」(中文命名,全覆盖 02 语义色);变量层纯英文与 JSON 同名,供组件绑定与代码同步;中文说明在变量描述。

**样式命名规则**:中文在前、英文和数值在后(如「文字图标 Text&Icon/主文字 Primary #000000」「正文 Body/标准 Base 16/24」);纯色显 hex、透明度显百分比;**变量改值时必须同步更新样式名与描述**。

**按钮文字用色铁律**:按钮上的文字/图标颜色必须用所在状态组的「文字 Foreground」样式(主色按钮→主色/文字 Foreground,危险按钮→危险/文字 Foreground),禁止用「文字图标」「中性」等其他颜色样式——保证换按钮底色时文字配对联动。

**同值 token 用色裁决**:accent 与 success 同为品牌绿,判据看语义——元素"让你去做"(按钮/选中/进度/链接)→accent;"告诉你结果"(Toast/校验/完成/到账)→success;拿不准→accent 并标记待审。分开绑定是为将来成功色独立分叉时能一键切换。

**插画豁免**:插画/品牌图形的固有色不进 token,自动绑定永久跳过(误用业务色的插画按个案修正)。

**红色裁决**:点赞爱心→feature/like(#FF3B64,情感色);危险按钮填充→danger/base(#EA4B46);危险**文字/图标**→danger/soft-foreground(#AE0800)——base 做文字仅 3.75:1 不达 AA,红色以文字形态出现必须切深红。

**自动绑定排除规则**(所有"画布套变量"操作必须遵守):① 系统组件不绑(精确匹配:Bars/、Status Bar、iPhone X状态栏、Notch、Home Indicator、键盘/Keyboard 及 iOS UI Kit 远程实例)——注意 Zymix 页头组件名含"顶部状态栏"字样,不属于系统件,曾被宽泛关键词误伤;② 隐藏图层(visible=false 及其子树)不绑;③ 黑色填充按节点类型分流——矢量图形→foreground/base,容器→surface/inverse;④ 反色容器上的白字绑 foreground/inverse 而非 default/white;⑤ **填充/描边级隐藏(paint.visible=false)绝不处理**——含任何隐藏 paint 的节点整体跳过样式化(setFillStyleId 会替换整个填充数组,把隐藏填充变为可见,视觉灾难);隐藏图层与隐藏填充,除非用户明确要求,永远不动。

**Scope 规范**:所有颜色变量 scope 清零——设计师选色只见「颜色样式」,变量不进选色器(样式已100%覆盖语义色;组件经 API 绑定不受影响);数字变量保留 scope——线宽→描边宽度;size→宽高+间距;radius→圆角;字号→FONT_SIZE;行高→LINE_HEIGHT;字重→FONT_STYLE;字族→FONT_FAMILY;01 Primitive→无(仅查阅)。

**画布与尺寸基准**(2026-07-10 裁决):token 均为 1x 逻辑 pt,与画布宽度无关——设计系统不选画布,选规则。① 组件宽度一律用「边距 + 拉伸」定义(如 NavBar:左右 padding size/16 + 全宽拉伸),**禁止内嵌画布衍生的固定宽**(Toast 343、底部导航 360 均为 375−边距 反推值,属历史隐患待治理);② 稿面默认 375 画布仅为协作约定(最窄主流,窄屏安全),非系统依赖,大屏走查另拉 402/440 验证拉伸;③ Apple 402 kit(iOS 26/Liquid Glass)的控件尺寸(Tab Bar 95、Toolbar 105 等)是那代设计语言的规格,仅作形态参考,**产品组件尺寸以线上 375 实测为准**。新组件立项须标明尺寸来源(产品实测/Apple 参考)。玻璃按钮两档均为产品自有尺寸:48=按钮体系 lg 档的玻璃材质版(特殊场景按钮也可用玻璃);42=玻璃圆钮,NavBar/TabBar 专用。

**插层规则**:序数命名的梯子(background/secondary·tertiary、radius 档位等)在**组件库发布/代码接入之前**允许整理重排;**发布之后禁止顺延插层**——序数名是对外契约,顺延=名字不变值变,会静默改动所有存量绑定。发布后新增层级一律用特征名/场景名/数字名追加(如 background/snow、radius/22),不动已有名字。

规模(v2.2 发版):semantic 77×2 + layout 31 + font 46 + primitive 68(参考,不发布)。
架构与命名规则见 `docs/01-token-architecture.md`。
