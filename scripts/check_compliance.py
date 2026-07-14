#!/usr/bin/env python3
"""ZymixUI 原型合规检查:python3 check_compliance.py <page.html>
生成每个页面后必须跑,全部 PASS 才能交付。"""
import re,sys

ALLOWED_FONT_SIZES={36,34,30,24,20,18,17,16,15,14,13,12,11,10}  # 10 = Body/2xs(2026-07-10)
ALLOWED_WEIGHTS={400,600,700,900}
ALLOWED_RADII={0,6,8,12,16,20,22,24,28,32,36}
CHROME_HEX={'#8E8E93','#1C1C1E'}  # 模板手机壳装饰,豁免

def strip_token_blocks(css_or_html):
    s=re.sub(r':root[^{]*\{[^}]*\}','',css_or_html)
    s=re.sub(r'\[data-theme="dark"\][^{]*\{[^}]*\}','',s)
    s=re.sub(r'\[data-theme="dark"\]\s*\.glass[^{]*\{[^}]*\}','',s)
    # 模板手机壳装饰豁免(.phone 54px / .statusbar / .home-indicator 3px)
    s=re.sub(r'\.(phone|home-indicator|statusbar)[^{]*\{[^}]*\}','',s)
    return s

def main(path):
    html=open(path,encoding='utf-8').read()
    body=strip_token_blocks(html)
    errors=[]
    # 1) 裸 hex(token 区外)
    hx=[h.upper() for h in re.findall(r'#[0-9A-Fa-f]{6}\b',body)]
    bad_hex=sorted(set(h for h in hx if h not in CHROME_HEX))
    if bad_hex:errors.append('裸 hex 颜色: '+', '.join(bad_hex[:10]))
    # 2) 字号(emoji 插画豁免:font-size 后紧跟 line-height:1 视为图标,不校验)
    body_no_emoji=re.sub(r'font-size:\s*\d+(?:\.\d+)?px;\s*line-height:1\b','',body)
    for s in set(re.findall(r'font-size:\s*(\d+(?:\.\d+)?)px',body_no_emoji)):
        if float(s) not in ALLOWED_FONT_SIZES:errors.append(f'非规范字号: {s}px')
    # 3) 字重
    for w in set(re.findall(r'font-weight:\s*(\d+)',body)):
        if int(w) not in ALLOWED_WEIGHTS:errors.append(f'非规范字重: {w}')
    # 4) 圆角硬值(应使用 var(--radius-*))
    for r in set(re.findall(r'border-radius:\s*(\d+(?:\.\d+)?)px',body)):
        v=float(r)
        if v not in ALLOWED_RADII and v<100:errors.append(f'非规范圆角硬值: {r}px(用 var(--radius-*))')
    # 5) rgba 硬值(正文中直接写 rgba 而非变量;豁免 .glass 材质配方与阴影)
    body_no_glass=re.sub(r'\.glass[^{]*\{[^}]*\}','',body)
    body_no_glass=re.sub(r'linear-gradient\([^)]*\)','',body_no_glass)  # 媒体遮罩渐变豁免
    body_no_glass=re.sub(r'box-shadow:[^;]*;','',body_no_glass)
    raw_rgba=re.findall(r'(?:background|color|border-color):\s*rgba\([^)]*\)',body_no_glass)
    if raw_rgba:errors.append(f'裸 rgba 用色 ×{len(raw_rgba)}(应用 var(--*)): '+raw_rgba[0][:60])
    # 6) 单页面铁律:只能有一台 .phone;禁止并排输出浅色+深色两份
    phones=re.findall(r'class\s*=\s*["\'][^"\']*\bphone\b',html)
    if len(phones)>1:
        errors.append(f'多个 .phone 容器 ×{len(phones)}:必须单页面输出,深浅色靠跟随系统,不要并排双模式')
    # 只看 HTML 元素属性(前面不是 '[',排除 CSS 选择器 [data-theme="dark"])
    if re.search(r'(?<!\[)data-theme\s*=\s*["\']light',html) and re.search(r'(?<!\[)data-theme\s*=\s*["\']dark',html):
        errors.append('同时出现 data-theme="light" 与 "dark":这是并排双模式,只保留一台跟随系统的手机')
    # 7) 动效规则(motion.md);tokens :root 块已被 strip,故不误伤 --ease-* 变量定义
    warnings=[]
    if re.search(r'transition:\s*all\b',body):
        errors.append('transition: all:必须写具体属性(如 transition:transform var(--duration-base) var(--ease-out))')
    # UI 禁 ease-in(排除 ease-in-out 与 cubic-bezier;排除 --ease-in 变量引用)
    for m in re.finditer(r'(?<![\w-])ease-in(?!-out)\b',body):
        seg=body[max(0,m.start()-40):m.start()]
        if 'cubic-bezier' in seg or 'var(' in seg:continue
        errors.append('UI 动画用了 ease-in(起步慢=迟钝):改 var(--ease-out) 或自定义曲线');break
    # 软警告:从 scale(0) 入场
    if re.search(r'transform:\s*scale\(0\)',body):
        warnings.append('从 scale(0) 入场:现实里没有东西凭空出现,改 scale(0.95)+opacity')
    # 软警告:单条过渡/动画时长 >400ms(营销可豁免)
    for d in re.findall(r'(?:transition|animation)[^;{}]*?(\d+(?:\.\d+)?)(m?s)\b',body):
        val=float(d[0])*(1000 if d[1]=='s' else 1)
        if val>400:warnings.append(f'过渡时长 {d[0]}{d[1]}(>400ms):UI 动画应 ≤300ms,收一下(营销/解释类可忽略)');break
    if warnings and not errors:
        print('⚠ WARN',path)
        for w in warnings:print('  -',w)
    if errors:
        print('❌ FAIL',path)
        for e in errors:print('  -',e)
        sys.exit(1)
    print('✅ PASS',path)

if __name__=='__main__':
    for p in sys.argv[1:]:main(p)
