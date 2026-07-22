# 图标使用(ZymixUI 图标库)

## 内置常用(离线,~66 个) references/icons-bundled.json
name→SVG 内部。生成页面时按名取,内联:
```html
<span style="display:inline-flex;width:24px;height:24px;color:var(--foreground-base)">
  <svg width="24" height="24" viewBox="0 0 16 16" fill="none"><g transform="translate(-16,-8)">…</g></svg>
</span>
```
JSON 里存的就是含 `<g transform>` 的内部,直接塞进 `<svg viewBox="0 0 16 16">` 即可;色用 currentColor 跟随父级 color。
内置清单(grep icons-bundled.json 取键名):magnifier bell gear house person persons person-gear person-plus plus minus xmark check chevron-* heart(-fill) comment(-fill) comments paper-plane camera picture envelope lock lock-open gift qr-code ellipsis(-vertical) arrow-left/right/up/down bookmark star(-fill) trash-bin pencil pencil-to-square eye eye-slash clock calendar map-pin planet-earth globe thumbs-up face-smile microphone video handset circle-plus/check/xmark/info sliders share credit-card shield key flag tag at ban

## 底部导航(TabBar)专用图标
TabBar 只能用 `tab-` 前缀的标签栏图标,**不用普通图标顶替**,且**只用本地内置、不走 CDN**。内置 tab 组:`tab-chat` `tab-mix` `tab-video` `tab-discover` `tab-me` `tab-ai`,每个都配 `-fill` 面性变体。未激活用线性、激活切 `-fill` + accent 着色(模板 `.ic-line`/`.ic-fill` 已内置这套切换)。需要新的 tab 图标时,从全量库补一个 `tab-xxx` 进 `icons-bundled.json`,别挑普通图标或接 CDN。除非用户特殊要求才可偏离。

## 长尾(721 个全量) CDN 引用
内置里没有的图标走 CDN(mask 上色,见 SKILL.md「图标库(CDN)」的 .zi):
```html
<i class="zi" style="--zi:url(https://cdn.jsdelivr.net/gh/zymix-ui/zymix-icons@v1.0.2/svgs/<name>.svg)"></i>
```
全部图标名见 CDN 仓库 svgs/ 或让用户提供清单。库里无 wallet(用 credit-card 代),share=arrow-shape-turn-up-right。
