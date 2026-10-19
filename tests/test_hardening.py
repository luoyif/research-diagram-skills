import importlib.util,unittest,tempfile,copy
from pathlib import Path
R=Path(__file__).resolve().parents[1]
def module(name):
 s=importlib.util.spec_from_file_location(name,R/'engine'/f'{name}.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
D=module('diagram');I=module('intake')
class HardeningTests(unittest.TestCase):
 def setUp(self):self.s=D.load(R/'examples/reference-reconstruction.scene.json')
 def codes(self,s):return [x['code'] for x in D.validate(s)['errors']]
 def test_nonobject_scene(self):self.assertIn('SCHEMA',self.codes([]))
 def test_nondict_node(self):self.s['nodes'].append('bad');self.assertIn('SCHEMA',self.codes(self.s))
 def test_unhashable_font(self):self.s['font_sizes']=[{},21];self.assertIn('FONTS',self.codes(self.s))
 def test_missing_id(self):del self.s['nodes'][0]['id'];self.assertIn('IDS',self.codes(self.s))
 def test_stacked_edges(self):e=copy.deepcopy(self.s['edges'][0]);e['id']='stacked';self.s['edges'].append(e);self.assertIn('EDGE_STACKED',self.codes(self.s))
 def test_role_not_text_bypass(self):self.s['nodes'][0]['role']='background';self.assertIn('ROLE_TEXT',self.codes(self.s))
 def test_css_rejected(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'x.svg';p.write_text('<svg xmlns="http://www.w3.org/2000/svg"><style>@import url(https://example.com/x);</style></svg>')
   with self.assertRaises(ValueError):I.intake(p,Path(t)/'out')
 def test_css_attribute_rejected(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'x.svg';p.write_text('<svg xmlns="http://www.w3.org/2000/svg"><rect style="fill:url(https://example.com/a)"/></svg>')
   with self.assertRaises(ValueError):I.intake(p,Path(t)/'out')
if __name__=='__main__':unittest.main()
