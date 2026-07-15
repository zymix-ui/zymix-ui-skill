#!/usr/bin/env python3
"""把 references/tokens.css 的数值/动效 token 导出为 iOS 端常量映射。
用法: python3 scripts/export_swift_metrics.py > ZymixMetrics.swift
含 radius / size / leading / border-width / separator-width(CGFloat)、duration(秒)、ease(贝塞尔控制点)、font family + weight。颜色见 Color+ZymixTokens.swift。"""
import re, sys, os
CSS = os.path.join(os.path.dirname(__file__), '..', 'references', 'tokens.css')
src = open(CSS, encoding='utf-8').read()
light = src[src.find(':root'): src.find('[data-theme="dark"]')]
vars = dict(re.findall(r'--([a-z0-9-]+)\s*:\s*([^;]+);', light))

def camel(parts):
    parts = [p for p in parts if p]
    if not parts: return 'base'
    m = parts[0] + ''.join(p.capitalize() for p in parts[1:])
    mm = re.match(r'(\d+)([A-Za-z].*)$', m)          # "2xl" -> "xl2"
    if mm: return mm.group(2)[0].lower()+mm.group(2)[1:] + mm.group(1)
    if m[0].isdigit(): m = 's'+m                     # "16" -> "s16"
    return m

def px(v): 
    n=float(v.replace('px','').strip()); return str(int(n)) if n==int(n) else str(n)

radius, size, leading, bw, sw, dur, ease = ({} for _ in range(7))
weights={}; family=None
for name,val in vars.items():
    val=val.strip()
    if name.startswith('radius-'):        radius[camel(name.split('-')[1:])]=px(val)
    elif name.startswith('size-'):        size[camel(name.split('-')[1:])]=px(val)
    elif name.startswith('leading-'):     leading[camel(name.split('-')[1:])]=px(val)
    elif name.startswith('border-width'): bw[camel(name.split('-')[2:]) or 'base']=px(val)
    elif name.startswith('separator-width'): sw[camel(name.split('-')[2:]) or 'base']=px(val)
    elif name.startswith('duration-'):    dur[camel(name.split('-')[1:])]=round(float(val.replace('ms',''))/1000,3)
    elif name.startswith('ease-'):
        nums=re.findall(r'-?\d*\.?\d+', val); ease[camel(name.split("-")[1:])]=tuple(nums[:4])
    elif name.startswith('weight-'):      weights[name.split('-')[1]]=val.strip('"')
    elif name.startswith('family-'):      family=val.strip('"')

def emit_cg(title, d):
    o=[f'    public enum {title} {{']
    for k,v in d.items(): o.append(f'        public static let {k}: CGFloat = {v}')
    o.append('    }'); return o

out=['// ZymixMetrics.swift',
     '// 由 scripts/export_swift_metrics.py 从 references/tokens.css 生成 — 请勿手改。',
     '// 尺寸 / 圆角 / 行高 / 时长 / 缓动 / 字体 token(颜色见 Color+ZymixTokens.swift)。','',
     'import UIKit','','public enum ZymixMetrics {']
out += emit_cg('Radius', radius) + ['']
out += emit_cg('Size', size) + ['']
out += emit_cg('Leading', leading) + ['']
out += emit_cg('BorderWidth', bw) + ['']
out += emit_cg('SeparatorWidth', sw) + ['']
# Duration(秒)
out += ['    public enum Duration {'] + [f'        public static let {k}: TimeInterval = {v}' for k,v in dur.items()] + ['    }','']
# Easing(贝塞尔控制点 x1,y1,x2,y2)
out += ['    /// 三次贝塞尔控制点 (x1, y1, x2, y2);可传入 CAMediaTimingFunction(controlPoints:)',
        '    public enum Easing {']
for k,(a,b,c,dd) in ease.items():
    out.append(f'        public static let {k}: (Float, Float, Float, Float) = ({a}, {b}, {c}, {dd})')
out += ['    }','']
# Font
wmap={'Regular':'.regular','Semibold':'.semibold','Bold':'.bold','Black':'.black','Medium':'.medium'}
out += ['    public enum Font {',
        f'        public static let family = "{family}"',
        '        public enum Weight {']
for raw in weights.values():
    key = raw[0].lower()+raw[1:]
    out.append(f'            public static let {key}: UIFont.Weight = {wmap.get(raw, ".regular")}')
out += ['        }','    }','}','']
sys.stdout.write('\n'.join(out))
sys.stderr.write(f'radius={len(radius)} size={len(size)} leading={len(leading)} duration={len(dur)} ease={len(ease)}\n')
