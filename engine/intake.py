#!/usr/bin/env python3
"""Archive a user-authorized reference locally and record an inventory for a vision agent.
This is not OCR, a semantic image parser, or an arbitrary SVG converter.
"""
from __future__ import annotations
import argparse, hashlib, json, re, shutil, xml.etree.ElementTree as ET
from pathlib import Path

def intake(source: Path, out: Path) -> dict:
    if source.suffix.lower() not in ['.png','.jpg','.jpeg','.svg']:raise ValueError('PNG/JPG/SVG only')
    if source.stat().st_size>50_000_000:raise ValueError('Reference exceeds 50 MB')
    data=source.read_bytes(); record={'source_name':source.name,'sha256':hashlib.sha256(data).hexdigest(),'status':'AWAITING_VISUAL_INVENTORY','elements':[],'relationships':[],'unresolved':[]}
    if source.suffix.lower()=='.svg':
        if b'<!DOCTYPE' in data.upper() or b'<!ENTITY' in data.upper():raise ValueError('DTD/entity declarations are not accepted')
        root=ET.fromstring(data);ns={'s':'http://www.w3.org/2000/svg'}
        if root.tag!='{http://www.w3.org/2000/svg}svg':raise ValueError('Not a namespaced SVG')
        record['source_viewBox']=root.get('viewBox');record['svg_shape_tags']={k:len(root.findall('.//s:'+k,ns)) for k in ['rect','ellipse','circle','path','line','polyline','image','text']}
        for e in root.iter():
            if e.tag.split('}')[-1] in ['style','animate','set','animateTransform']:raise ValueError('CSS/animation requires separate static review; no rendering performed')
            for value in e.attrib.values():
                safe_value=re.sub(r'url\(\s*#[A-Za-z_][A-Za-z0-9_.-]*\s*\)', '', value, flags=re.I)
                if any(token in safe_value.lower() for token in ['url(', '@import', 'javascript:', 'file:', 'http:', 'https:']):raise ValueError('External or dynamic SVG resource reference rejected')
            if e.tag.split('}')[-1] in ['script','foreignObject']:raise ValueError('Active SVG content is not accepted; provide a static reference')
            if any(k.split('}')[-1].lower().startswith('on') for k in e.attrib):raise ValueError('SVG event handler rejected')
            for k,v in e.attrib.items():
                if k.split('}')[-1]=='href' and not v.startswith('#'):raise ValueError('External/embedded assets require explicit ownership review; no fetch performed')
        for i,t in enumerate(root.findall('.//s:text',ns)):
            record['elements'].append({'source_id':t.get('id',f'text-{i}'),'verbatim_text':''.join(t.itertext()),'x':t.get('x'),'y':t.get('y'),'transform':t.get('transform'),'note':'Raw SVG text; transforms/CSS/relationships need visual interpretation'})
    else:
        from PIL import Image
        with Image.open(source) as im:im.verify()
        with Image.open(source) as im:record['pixels']=list(im.size)
    out.mkdir(parents=True,exist_ok=False);shutil.copy2(source,out/('reference'+source.suffix.lower()))
    (out/'inventory.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (out/'NEXT_STEP.md').write_text('使用支持视觉的代理查看reference文件，补充inventory中所有可见元素、箭头方向与未决项，再写scene.json。不能直接把文件贴进PPT称为可编辑。\n',encoding='utf-8')
    return record

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    print(json.dumps(intake(a.source,a.out),ensure_ascii=False,indent=2))
