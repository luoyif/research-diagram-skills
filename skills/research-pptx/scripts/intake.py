#!/usr/bin/env python3
from pathlib import Path
import sys, runpy
here=Path(__file__).resolve().parent
runtime=here/'runtime'
if not (runtime/'intake.py').exists():runtime=here.parents[2]/'engine'
if not (runtime/'intake.py').exists():raise SystemExit('Missing runtime: copy the complete skill folder')
sys.path.insert(0,str(runtime))
runpy.run_path(str(runtime/'intake.py'),run_name='__main__')
