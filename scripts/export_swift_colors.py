#!/usr/bin/env python3
"""把 references/tokens.css 的颜色变量导出为 iOS 端 UIColor 映射(displayP3, light/dark)。
用法: python3 scripts/export_swift_colors.py > Color+ZymixTokens.swift
tokens 更新后重跑,保持与设计变量一致。"""
import re, sys, os

CSS = os.path.join(os.path.dirname(__file__), '..', 'references', 'tokens.css')
src = open(CSS, encoding='utf-8').read()

def block(sel_start, sel_end):
    i = src.find(sel_start); j = src.find(sel_end, i)
    return src[i:j]

light_txt = block(':root, [data-theme="light"] {', '\n}')
dark_txt  = block('[data-theme="dark"] {', '\n}')

def parse(txt):
    d = {}
    for name, val in re.findall(r'--([a-z0-9-]+)\s*:\s*([^;]+);', txt):
        d[name] = val.strip()
    return d

light, dark = parse(light_txt), parse(dark_txt)

def to_p3(v):
    v = v.strip()
    m = re.match(r'#([0-9a-fA-F]{6})$', v)
    if m:
        r = int(m.group(1)[0:2],16); g=int(m.group(1)[2:4],16); b=int(m.group(1)[4:6],16)
        return f'displayP3({r}, {g}, {b}, 100)'
    m = re.match(r'rgba?\(\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*(?:,\s*([\d.]+)\s*)?\)$', v)
    if m:
        r=int(float(m.group(1))); g=int(float(m.group(2))); b=int(float(m.group(3)))
        a=round(float(m.group(4))*100) if m.group(4) is not None else 100
        return f'displayP3({r}, {g}, {b}, {a})'
    return None  # 非颜色

def camel(parts):
    return parts[0] + ''.join(p.capitalize() for p in parts[1:])

# 只保留颜色变量,按首段分组,保序
groups = {}   # group -> list[(member, light_p3, dark_p3)]
order = []
for name, lv in light.items():
    lp = to_p3(lv)
    if lp is None:
        continue
    dv = dark.get(name, lv)
    dp = to_p3(dv) or lp
    parts = name.split('-')
    grp = parts[0]
    member = camel(parts[1:]) if len(parts) > 1 else 'base'
    if not member[0].isalpha():
        member = 'v' + member
    if grp not in groups:
        groups[grp] = []; order.append(grp)
    groups[grp].append((member, lp, dp))

out = []
out.append('// Color+ZymixTokens.swift')
out.append('// 由 scripts/export_swift_colors.py 从 references/tokens.css 生成 — 请勿手改。')
out.append('// 颜色取自 ZymixUI Design Tokens(单一真源:tokens.css),含 Light / Dark 两套值。')
out.append('')
out.append('import SwiftUI')
out.append('')
out.append('extension UIColor {')
for grp in order:
    out.append(f'    public struct {grp.capitalize()} {{')
    for member, lp, dp in groups[grp]:
        out.append(f'        public static let {member} = UIColor(light: "{lp}", dark: "{dp}")')
    out.append('    }')
    out.append('')
out.append('}')
out.append('')
out.append('// MARK: - displayP3 便捷初始化(与现有 Color+Tokens 规格一致)')
out.append('''extension UIColor {
    public convenience init(light: String, dark: String) {
        self.init { traitCollection in
            let colorString = traitCollection.userInterfaceStyle == .dark ? dark : light
            return UIColor(displayP3String: colorString) ?? .black
        }
    }
    public convenience init?(displayP3String: String) {
        let c = displayP3String.replacingOccurrences(of: "displayP3(", with: "")
            .replacingOccurrences(of: ")", with: "")
            .split(separator: ",").map { $0.trimmingCharacters(in: .whitespaces) }
        guard c.count == 4, let r = Float(c[0]), let g = Float(c[1]), let b = Float(c[2]), let a = Float(c[3]) else { return nil }
        self.init(displayP3Red: CGFloat(r/255), green: CGFloat(g/255), blue: CGFloat(b/255), alpha: CGFloat(a/100))
    }
}''')

txt = '\n'.join(out) + '\n'
sys.stdout.write(txt)
sys.stderr.write(f'groups={len(order)} colors={sum(len(v) for v in groups.values())}\n')
