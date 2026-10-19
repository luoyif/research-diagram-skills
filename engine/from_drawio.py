#!/usr/bin/env python3
"""Import a supported uncompressed Draw.io page into Scene v1.
Fail explicitly on unsupported shapes/HTML/icons, never flatten or drop content.
Designed for files produced by this kit and compatible simple native diagrams.
"""
from __future__ import annotations
import argparse, json, xml.etree.ElementTree as ET
from pathlib import Path
from diagram import validate, save_json

def parse_style(s):
    d={}
    for p in s.split(';'):
        if p:k,_,v=p.partition('=');d[k]=v
    return d

def convert(source: Path, page: int=0) -> dict:
    data=source.read_bytes()
    if len(data)>10_000_000 or b'<!DOCTYPE' in data.upper() or b'<!ENTITY' in data.upper():raise ValueError('Input too large or contains DTD/entity')
    r=ET.fromstring(data)
    if r.tag=='mxfile':
        pages=r.findall('diagram')
        if not 0<=page<len(pages):raise ValueError('Page index out of bounds')
        pg=pages[page];model=pg.find('mxGraphModel');title=pg.get('name','Diagram')
        if model is None:raise ValueError('Compressed Draw.io unsupported in this importer: save uncompressed XML, or use the upstream workflow')
    elif r.tag=='mxGraphModel':model=r;title='Diagram'
    else:raise ValueError('Expected mxfile or mxGraphModel')
    root=model.find('root')
    if root is None:raise ValueError('Missing root')
    if any(e.tag!='mxCell' for e in root):raise ValueError('Custom wrappers are unsupported; preserve source and use upstream editing')
    scene={'schema_version':1,'title':title,'author':'小罗','width':float(model.get('pageWidth',1400)),'height':float(model.get('pageHeight',860)),'font_family':'Songti SC','font_sizes':[26,21],'monochrome':True,'nodes':[],'edges':[]}
    fontset=set();sizes=set();unsupported=[]
    for c in root:
        i=c.get('id');g=c.find('mxGeometry');s=parse_style(c.get('style',''))
        if i in ['0','1']:continue
        if g is None:unsupported.append(i+':missing geometry');continue
        if c.get('edge')=='1':
            if not c.get('source') or not c.get('target') or c.get('value') or c.get('parent')!='1' or s.get('edgeStyle') not in [None,'none']:
                unsupported.append(i+':unbound/labeled/nested/auto-routed edge');continue
            scene['edges'].append({'id':i,'source':c.get('source'),'target':c.get('target'),'source_port':[float(s.get('exitX',1)),float(s.get('exitY',.5))],'target_port':[float(s.get('entryX',0)),float(s.get('entryY',.5))],'waypoints':[[float(p.get('x')),float(p.get('y'))] for p in g.findall("Array[@as='points']/mxPoint")],'dashed':s.get('dashed')=='1','arrow':s.get('endArrow','block')!='none'})
            continue
        if s.get('html','0')!='0' or s.get('shape') not in [None,'rectangle','ellipse'] or 'swimlane' in s or s.get('rotation','0')!='0':unsupported.append(i+':unsupported style/HTML/rotation');continue
        kind='group' if 'group' in s else ('text' if 'text' in s else ('ellipse' if 'ellipse' in s or s.get('shape')=='ellipse' else 'rect'))
        n={'id':i,'kind':kind,'parent':'root' if c.get('parent')=='1' else c.get('parent'),'x':float(g.get('x',0)),'y':float(g.get('y',0)),'w':float(g.get('width',0)),'h':float(g.get('height',0))}
        if kind!='group':n.update(fill=s.get('fillColor','#FFFFFF'),stroke=s.get('strokeColor','#333333'),stroke_width=float(s.get('strokeWidth',1.5)),rounded=s.get('rounded')=='1')
        if i.endswith('_background') or i.endswith('_bg'):n['role']='background'
        if c.get('value'):
            n.update(text=c.get('value'),font_size=float(s.get('fontSize',21)),color=s.get('fontColor','#111111'),bold=s.get('fontStyle')=='1',align=s.get('align','center'));sizes.add(n['font_size']);fontset.add(s.get('fontFamily','Songti SC'))
        scene['nodes'].append(n)
    if unsupported:raise ValueError('Unsupported objects (nothing dropped): '+', '.join(unsupported))
    if len(fontset)!=1:raise ValueError('Use one font family before import')
    if len(sizes)!=2:raise ValueError('Use exactly two font sizes before import')
    scene['font_family']=next(iter(fontset));scene['font_sizes']=sorted(sizes,reverse=True)
    report=validate(scene)
    if report['status']!='PASS':raise ValueError(json.dumps(report,ensure_ascii=False))
    return scene

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);p.add_argument('--page',type=int,default=0);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    if a.out.exists():raise SystemExit('Refusing to overwrite destination')
    save_json(a.out,convert(a.source,a.page));print(a.out)
