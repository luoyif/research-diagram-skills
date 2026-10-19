#!/usr/bin/env python3
from pathlib import Path
import sys, runpy
here=Path(__file__).resolve().parent
runtime=here/'runtime'
if not (runtime/'diagram.py').exists():runtime=here.parents[2]/'engine'
if not (runtime/'diagram.py').exists():raise SystemExit('Missing runtime: copy the complete skill folder')
sys.path.insert(0,str(runtime))
if len(sys.argv)>1 and sys.argv[1]=='build' and '--mode' not in sys.argv:sys.argv.extend(['--mode','drawio'])
runpy.run_path(str(runtime/'diagram.py'),run_name='__main__')
