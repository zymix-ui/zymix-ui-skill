#!/usr/bin/env python3
"""ZymixUI tokens 校验:alias 解析 / Light-Dark 对齐 / 整数透明度 / AA 报告。改 JSON 后必跑。"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load = lambda p: json.load(open(os.path.join(ROOT, p)))

def flatten(d, pfx=''):
    out = {}
    for k, v in d.items():
        if k.startswith('$'): continue
        if isinstance(v, dict) and '$value' in v: out[pfx + k] = v['$value']
        elif isinstance(v, dict): out.update(flatten(v, pfx + k + '.'))
    return out

light, dark = flatten(load('semantic/color.light.json')), flatten(load('semantic/color.dark.json'))
prim = flatten(load('primitive/color.json'))
errors = []

# 1) Light/Dark key 对齐
if set(light) != set(dark):
    errors.append('Light/Dark key 不一致: ' + str(set(light) ^ set(dark)))

# 2) alias 可解析
for tag, flat in [('L', light), ('D', dark)]:
    for n, v in flat.items():
        if isinstance(v, str) and v.startswith('{') and v.strip('{}') not in flat and v.strip('{}') not in prim:
            errors.append(f'{tag}:{n} → {v} 无法解析')

# 3) 整数透明度
for tag, flat in [('L', light), ('D', dark), ('P', prim)]:
    for n, v in flat.items():
        m = isinstance(v, str) and re.search(r'rgba\(\d+,\d+,\d+,(0?\.\d+|1)\)', v)
        if m and abs(round(float(m.group(1)) * 100) - float(m.group(1)) * 100) > 1e-6:
            errors.append(f'{tag}:{n} 透明度非整数百分比 {v}')

# 4) AA 报告(信息性)
def rgba(v, flat):
    seen = set()
    while isinstance(v, str) and v.startswith('{'):
        ref = v.strip('{}')
        if ref in seen: return None
        seen.add(ref)
        v = flat.get(ref, prim.get(ref))
    if isinstance(v, str):
        m = re.match(r'rgba\((\d+),(\d+),(\d+),([\d.]+)\)', v)
        if m: return [int(m.group(1)), int(m.group(2)), int(m.group(3)), float(m.group(4))]
        if v.startswith('#'):
            h = v.lstrip('#')
            return [int(h[0:2],16), int(h[2:4],16), int(h[4:6],16), int(h[6:8],16)/255 if len(h)==8 else 1]
    return None
def lum(c):
    f = lambda x: x/12.92 if x <= 0.03928 else ((x+0.055)/1.055)**2.4
    r, g, b = [f(x/255) for x in c[:3]]
    return 0.2126*r + 0.7152*g + 0.0722*b
def contrast(fg, bg):
    a = fg[3]
    blend = [fg[i]*a + bg[i]*(1-a) for i in range(3)] + [1]
    l1, l2 = sorted([lum(blend), lum(bg)], reverse=True)
    return (l1+0.05)/(l2+0.05)
print('AA 报告(on background.base):')
for mode, flat in [('Light', light), ('Dark', dark)]:
    bg = rgba(flat['background.base'], flat)
    for role in ['foreground.base', 'foreground.muted', 'foreground.subtle', 'foreground.link']:
        fg = rgba(flat[role], flat)
        if fg and bg:
            c = contrast(fg, bg)
            mark = 'PASS' if c >= 4.5 else ('LARGE-ONLY' if c >= 3 else 'FAIL')
            print(f'  {mode} {role}: {c:.2f}:1 {mark}')

if errors:
    print('\n❌ 错误:'); [print(' ', e) for e in errors]; sys.exit(1)
print('\n✅ 校验通过 (semantic %d×2, primitive %d)' % (len(light), len(prim)))
