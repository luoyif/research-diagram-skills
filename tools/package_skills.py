#!/usr/bin/env python3
"""Build three self-contained skill archives plus source archives and a full repository ZIP."""
from pathlib import Path
import argparse,copy,hashlib,json,shutil,zipfile,sys
from verify_sources import verify
ROOT=Path(__file__).resolve().parents[1]
SELECTION={
 'research-drawio':['jgraph/drawio-mcp','Agents365-ai/drawio-skill','sxy1499894281/drawio-reconstruction-skill'],
 'research-pptx':['HututuWorks/sci-diagram-pptx','sxy1499894281/drawio-reconstruction-skill'],
 'research-diagram-workflow':['jgraph/drawio-mcp','Agents365-ai/drawio-skill','sxy1499894281/drawio-reconstruction-skill','HututuWorks/sci-diagram-pptx']}
ALLOWED=['README.md','LICENSE','THIRD_PARTY_NOTICES.md','AGENTS.md','.gitignore','requirements.txt','sources.lock.json','docs','engine','examples','tests','tools','skills','vendor']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def safe_files(root):
 for p in sorted(root.rglob('*')):
  if p.is_symlink():raise ValueError('Symlink not packaged: '+str(p))
  if p.is_file() and not any(x in ['__pycache__','.git','.venv'] for x in p.parts) and p.suffix not in ['.pyc','.pyo']:
   if p.suffix.lower() in ['.ttf','.otf','.ttc','.woff','.woff2','.env','.key','.pem','.docx']:raise ValueError('Forbidden release asset: '+str(p))
   yield p
def zip_tree(root,out):
 with zipfile.ZipFile(out,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for p in safe_files(root):z.write(p,str(p.relative_to(root.parent)))
 with zipfile.ZipFile(out) as z:
  if z.testzip() is not None:raise ValueError('Corrupt zip')
def run(out):
 check=verify(ROOT)
 if check['status']!='PASS':raise ValueError(str(check))
 out.mkdir(parents=True,exist_ok=False);lock=json.loads((ROOT/'sources.lock.json').read_text());artifacts=[]
 for name,repos in SELECTION.items():
  dest=out/'expanded'/name;shutil.copytree(ROOT/'skills'/name,dest)
  shutil.copytree(ROOT/'engine',dest/'scripts/runtime',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
  shutil.copy2(ROOT/'requirements.txt',dest/'requirements.txt');shutil.copy2(ROOT/'LICENSE',dest/'LICENSE')
  manifest=copy.deepcopy(lock);manifest['sources']=[s for s in lock['sources'] if s['repository'] in repos]
  for source in manifest['sources']:shutil.copytree(ROOT/source['vendored_path'],dest/source['vendored_path'])
  (dest/'sources.lock.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
  (dest/'THIRD_PARTY_NOTICES.md').write_text('# Third-party notices\n\nOriginal integration: MIT, copyright 2026 小罗. Included upstream files retain these licenses:\n\n'+'\n'.join('- '+s['repository']+' — '+s['license']+' — '+s['vendored_path']+'/LICENSE' for s in manifest['sources'])+'\n',encoding='utf-8')
  (dest/'tools').mkdir();shutil.copy2(ROOT/'tools/verify_sources.py',dest/'tools/verify_sources.py')
  (dest/'README.md').write_text('# '+name+'\n\nRead SKILL.md. Install the entire folder, not SKILL.md alone.\n\nRun `python scripts/diagram.py doctor`. Use assets/ for generic demos.\n\nreferences/SOURCES.md is the whole project catalog; sources.lock.json is the exact subset physically included in THIS archive.\n\nNative outputs require actual per-format rendering and visual inspection. No customer data or fonts included.\n',encoding='utf-8')
  assert verify(dest)['status']=='PASS'
  archive=out/(name+'-v1.0.0.zip');zip_tree(dest,archive);artifacts.append(archive)
 upstream=out/'upstream';upstream.mkdir()
 for source in lock['sources']:
  archive=upstream/(source['repository'].replace('/','__')+'-'+source['commit'][:12]+'.zip');zip_tree(ROOT/source['vendored_path'],archive);artifacts.append(archive)
 full=out/'expanded/research-diagram-skills';full.mkdir()
 for name in ALLOWED:
  src=ROOT/name
  if not src.exists():continue
  if src.is_dir():shutil.copytree(src,full/name,ignore=shutil.ignore_patterns('__pycache__','*.pyc','.git','.venv'))
  else:shutil.copy2(src,full/name)
 archive=out/'research-diagram-skills-complete-v1.0.0.zip';zip_tree(full,archive);artifacts.append(archive)
 manifest={'version':'1.0.0','source_verification':check,'archives':[{'file':str(p.relative_to(out)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in artifacts]}
 (out/'release-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
 (out/'SHA256SUMS.txt').write_text('\n'.join(x['sha256']+'  '+x['file'] for x in manifest['archives'])+'\n',encoding='utf-8')
 return manifest
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--out',required=True,type=Path);args=p.parse_args()
 try:print(json.dumps(run(args.out),ensure_ascii=False,indent=2))
 except (ValueError,OSError) as e:print('ERROR:',e,file=sys.stderr);raise SystemExit(2)
