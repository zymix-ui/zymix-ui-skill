#!/usr/bin/env python3
"""Figma ↔ 本地 tokens JSON 对账。
用法:
  1. 让 Claude 用 use_figma 导出当前 Figma 变量 → 存成 figma-export.json
     (格式: {"02 Semantic|Light|accent/base":"#26D93E", "03 Layout|Value|size/8":8, ...})
  2. python3 check_figma_sync.py <figma-export.json> <tokens目录>
报告 Figma 与 JSON 值不一致 / 一方缺失的 token。对齐后再跑 sync_tokens.py 重新生成 css。"""
import json,sys,os,re

def flat(d,p=''):
    o={}
    for k,v in d.items():
        if k.startswith('$'):continue
        if isinstance(v,dict) and '$value' in v:o[p+k]=v['$value']
        elif isinstance(v,dict):o.update(flat(v,p+k+'.'))
    return o

def norm(v):
    """归一化用于比较:颜色统一大写无空格,rgba 统一格式,数字转 float"""
    if isinstance(v,(int,float)):return float(v)
    if not isinstance(v,str):return v
    s=v.strip()
    m=re.match(r'rgba?\(([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)\)',s)
    if m:
        r,g,b,a=m.groups()
        return f'rgba({int(float(r))},{int(float(g))},{int(float(b))},{round(float(a),2)})'
    if s.startswith('#'):return s.upper()
    if s.startswith('{'):return s  # alias 保持
    return s

def main(exp_path,tok):
    fig=json.load(open(exp_path))
    L=flat(json.load(open(os.path.join(tok,'semantic/color.light.json'))))
    D=flat(json.load(open(os.path.join(tok,'semantic/color.dark.json'))))
    lay=flat(json.load(open(os.path.join(tok,'layout.json'))))
    ty=flat(json.load(open(os.path.join(tok,'primitive/typography.json'))))
    prim=flat(json.load(open(os.path.join(tok,'primitive/color.json'))))
    # 本地扁平表: 用与 figma key 相同的命名空间
    local={}
    for k,v in L.items():local[f'02 Semantic|Light|{k.replace(".","/")}']=v
    for k,v in D.items():local[f'02 Semantic|Dark|{k.replace(".","/")}']=v
    for k,v in lay.items():local[f'03 Layout|Value|{k.replace(".","/")}']=v
    for k,v in ty.items():local[f'04 Font|Value|{k.replace(".","/")}']=v
    def resolve_prim(v):
        # JSON 里 {color.brand.500} 这类指向 primitive,Figma 存的是解析后硬值
        seen=set()
        while isinstance(v,str) and v.startswith('{'):
            ref=v.strip('{}')
            if ref in seen:break
            seen.add(ref)
            if ref in prim:v=prim[ref]
            else:break
        return v
    mism=[];only_fig=[];only_loc=[]
    for k,fv in fig.items():
        if k not in local:only_fig.append(k);continue
        lv=local[k]
        # 语义层内部 alias(如 {accent/base}):两边都应是 alias,比较名字
        lv_r=resolve_prim(lv)
        a,b=norm(fv),norm(lv_r if not (isinstance(lv,str) and lv.startswith('{') and not lv.strip('{}') in prim) else lv)
        # alias 名归一: JSON 用点, figma 用斜杠
        if isinstance(b,str) and b.startswith('{'):b=b.replace('.','/')
        if a!=b:
            mism.append((k,fv,lv))
    for k in local:
        if k not in fig:only_loc.append(k)
    print(f'对账: Figma {len(fig)} 项 / 本地 {len(local)} 项')
    if mism:
        print(f'\n⚠ 值不一致 ({len(mism)}):')
        for k,f,l in mism:print(f'  {k}\n     Figma={f}  JSON={l}')
    if only_fig:print(f'\n⚠ 仅 Figma 有 ({len(only_fig)}): '+', '.join(only_fig[:20]))
    if only_loc:print(f'\n⚠ 仅 JSON 有 ({len(only_loc)}): '+', '.join(only_loc[:20]))
    if not(mism or only_fig or only_loc):print('\n✅ 完全一致')
    else:print('\n处理: 以设计师在 Figma 的最新改动为准 → 手动改 JSON 对齐 → 跑 sync_tokens.py')

if __name__=='__main__':
    main(sys.argv[1],sys.argv[2] if len(sys.argv)>2 else '.')
