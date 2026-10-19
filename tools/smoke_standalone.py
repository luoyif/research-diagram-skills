#!/usr/bin/env python3
"""Verify each archive works when extracted away from the parent repository."""
from pathlib import Path
import argparse,tempfile,zipfile,subprocess,sys,json,hashlib
NAMES=['research-drawio','research-pptx','research-diagram-workflow']
def test(release):
 results=[]
 for name in NAMES:
  with tempfile.TemporaryDirectory(prefix='skill-smoke-') as td:
   t=Path(td)
   with zipfile.ZipFile(release/(name+'-v1.0.0.zip')) as z:
    for f in z.namelist():
     if not (t/f).resolve().is_relative_to(t.resolve()):raise ValueError('Archive path traversal')
    z.extractall(t)
   root=t/name;commands=[['tools/verify_sources.py'],['scripts/diagram.py','doctor'],['scripts/diagram.py','validate','assets/reference-reconstruction.scene.json'],['scripts/diagram.py','build','assets/reference-reconstruction.scene.json','--out',str(t/'demo')]]
   for c in commands:
    p=subprocess.run([sys.executable,'-B']+c,cwd=root,capture_output=True,text=True,timeout=45)
    if p.returncode:raise RuntimeError(name+': '+str(c)+'\n'+p.stdout+p.stderr)
   state=json.loads((t/'demo/build-state.json').read_text())
   expected={'research-drawio':'drawio','research-pptx':'pptx','research-diagram-workflow':'both'}[name]
   assert state['mode']==expected and state['visual_review']=='PENDING'
   results.append({'skill':name,'status':'PASS','commands':4,'mode':state['mode'],'visual_status':'PENDING as designed'})
 return results
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('release',type=Path);a=p.parse_args();print(json.dumps(test(a.release),ensure_ascii=False,indent=2))
