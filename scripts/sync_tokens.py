#!/usr/bin/env python3
"""从 ZymixUI tokens 文件夹重新生成 references/tokens.css 快照。
用法: python3 sync_tokens.py /path/to/dsv2/tokens
规范更新后运行一次,再重新打包技能。"""
import json,sys,os,re

def flat(d,p=''):
    out={}
    for k,v in d.items():
        if k.startswith('$'):continue
        if isinstance(v,dict) and '$value' in v:out[p+k]=v['$value']
        elif isinstance(v,dict):out.update(flat(v,p+k+'.'))
    return out

def resolve(val,flatmap,prim,depth=0):
    while isinstance(val,str) and val.startswith('{') and depth<10:
        ref=val.strip('{}')
        val=flatmap.get(ref,prim.get(ref))
        depth+=1
        if val is None:return None
    return val

def css_color(v):
    if isinstance(v,str):
        m=re.match(r'rgba\((\d+),(\d+),(\d+),([\d.]+)\)',v)
        if m:return f'rgba({m.group(1)}, {m.group(2)}, {m.group(3)}, {m.group(4)})'
        return v
    return str(v)

def main(tok):
    prim=flat(json.load(open(os.path.join(tok,'primitive/color.json'))))
    L=flat(json.load(open(os.path.join(tok,'semantic/color.light.json'))))
    D=flat(json.load(open(os.path.join(tok,'semantic/color.dark.json'))))
    lay=flat(json.load(open(os.path.join(tok,'layout.json'))))
    ty=flat(json.load(open(os.path.join(tok,'primitive/typography.json'))))
    def block(flatmap):
        lines=[]
        for k,v in flatmap.items():
            r=resolve(v,flatmap,prim)
            if r is None:continue
            name='--'+k.replace('.','-')
            if isinstance(r,(int,float)) and ('width' in k):
                lines.append(f'  {name}: {r}px;')
            else:
                lines.append(f'  {name}: {css_color(r)};')
        return '\n'.join(lines)
    out=[]
    out.append('/* ZymixUI tokens 快照 — 由 sync_tokens.py 生成,勿手改 */')
    out.append(':root, [data-theme="light"] {\n'+block(L))
    for k,v in lay.items():out.append(f'  --{k.replace(".","-")}: {v}px;')
    for k,v in ty.items():
        n='--'+k.replace('.','-')
        if isinstance(v,(int,float)):out.append(f'  {n}: {v}px;')
        else:out.append(f'  {n}: "{v}";')
    out.append('}')
    out.append('[data-theme="dark"] {\n'+block(D)+'\n}')
    out.append('/* 跟随系统:未显式指定 data-theme 时自动深色 */')
    out.append('@media (prefers-color-scheme: dark) {\n:root:not([data-theme="light"]) {\n'+block(D)+'\n}\n}')
    css='\n'.join(out)
    dest=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','references','tokens.css')
    open(dest,'w').write(css)
    print('written',dest,len(css),'bytes')

if __name__=='__main__':
    main(sys.argv[1] if len(sys.argv)>1 else '.')
