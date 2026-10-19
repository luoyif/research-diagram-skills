#!/usr/bin/env python3
"""Check the exact original source snapshot; does not execute vendored code."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[1]
def verify(root=ROOT):
 lock=json.loads((root/'sources.lock.json').read_text(encoding='utf-8'));errors=[];count=0
 for source in lock['sources']:
  base=(root/source['vendored_path']).resolve()
  if not base.is_relative_to(root.resolve()):raise ValueError('Unsafe vendor path')
  expected=set()
  for f in source['files']:
   p=(base/f['path']).resolve();expected.add(p)
   if not p.is_relative_to(base):raise ValueError('Unsafe source file path')
   count+=1
   if not p.is_file():errors.append(source['repository']+': missing '+f['path']);continue
   if p.stat().st_size!=f['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=f['sha256']:errors.append(source['repository']+': changed '+f['path'])
  actual={p.resolve() for p in base.rglob('*') if p.is_file()}
  for p in sorted(actual-expected):errors.append(source['repository']+': unexpected '+str(p.relative_to(base)))
 result={'status':'FAIL' if errors else 'PASS','sources':len(lock['sources']),'verified_files':count,'errors':errors}
 return result
if __name__=='__main__':
 try:r=verify();print(json.dumps(r,ensure_ascii=False,indent=2));raise SystemExit(0 if r['status']=='PASS' else 2)
 except (ValueError,OSError,KeyError) as e:print('ERROR:',e,file=sys.stderr);raise SystemExit(2)
