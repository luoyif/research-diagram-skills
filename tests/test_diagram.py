import copy, importlib.util, json, tempfile, unittest, zipfile, sys
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('diagram',ROOT/'engine/diagram.py');D=importlib.util.module_from_spec(spec);spec.loader.exec_module(D)
spec=importlib.util.spec_from_file_location('intake',ROOT/'engine/intake.py');I=importlib.util.module_from_spec(spec);spec.loader.exec_module(I)

sys.path.insert(0,str(ROOT/'engine'))
from from_drawio import convert

class DiagramTests(unittest.TestCase):
 def setUp(self):self.s=D.load(ROOT/'examples/reference-reconstruction.scene.json')
 def assert_bad(self,s,code):self.assertIn(code,[e['code'] for e in D.validate(s)['errors']])
 def test_all_examples(self):
  for p in (ROOT/'examples').glob('*.json'):self.assertEqual(D.validate(D.load(p))['status'],'PASS',str(p))
 def test_unique_ids(self):self.s['nodes'][1]['id']=self.s['nodes'][0]['id'];self.assert_bad(self.s,'DUPLICATE_ID')
 def test_reserved_id(self):self.s['nodes'][0]['id']='root';self.assert_bad(self.s,'IDS')
 def test_unknown_shape(self):self.s['nodes'][0]['kind']='image';self.assert_bad(self.s,'UNSUPPORTED_NODE')
 def test_missing_parent(self):self.s['nodes'][1]['parent']='missing';self.assert_bad(self.s,'PARENT')
 def test_cycle(self):self.s['nodes'][1]['parent']='input';self.assert_bad(self.s,'CONTAINMENT')
 def test_negative_size(self):self.s['nodes'][1]['w']=-1;self.assert_bad(self.s,'GEOMETRY_SIZE')
 def test_nan(self):self.s['nodes'][1]['x']=float('nan');self.assert_bad(self.s,'GEOMETRY')
 def test_outside(self):self.s['nodes'][0]['x']=10000;self.assert_bad(self.s,'OUT_OF_BOUNDS')
 def test_third_font(self):self.s['nodes'][0]['font_size']=13;self.assert_bad(self.s,'FONT_COUNT')
 def test_same_font_sizes(self):self.s['font_sizes']=[21,21];self.assert_bad(self.s,'FONTS')
 def test_no_color(self):self.s['nodes'][0]['color']='#FF0000';self.assert_bad(self.s,'MONOCHROME')
 def test_nonstring_text(self):self.s['nodes'][0]['text']=[];self.assert_bad(self.s,'TEXT_TYPE')
 def test_group_text(self):self.s['nodes'][1]['text']='hidden';self.assert_bad(self.s,'GROUP_TEXT')
 def test_text_height(self):self.s['nodes'][0]['text']='a\nb\nc\nd\ne';self.assert_bad(self.s,'TEXT_HEIGHT')
 def test_missing_edge_target(self):self.s['edges'][0]['target']='missing';self.assert_bad(self.s,'MISSING_ENDPOINT')
 def test_bad_port(self):self.s['edges'][0]['source_port']=[.5,.5];self.assert_bad(self.s,'PORT')
 def test_waypoint(self):self.s['edges'][0]['waypoints']=[[0]];self.assert_bad(self.s,'WAYPOINT')
 def test_self_loop(self):self.s['edges'][0]['target']=self.s['edges'][0]['source'];self.assert_bad(self.s,'SELF_LOOP')
 def test_label_contract(self):f=D.contract(self.s);self.s['nodes'][0]['text']='changed';self.assertEqual(D.validate(self.s,f)['errors'][-1]['code'],'CONTRACT_DRIFT')
 def test_direction_contract(self):f=D.contract(self.s);e=self.s['edges'][0];e['source'],e['target']=e['target'],e['source'];self.assertIn('CONTRACT_DRIFT',[x['code'] for x in D.validate(self.s,f)['errors']])
 def test_overlap(self):self.s['nodes'].append(dict(id='conflict',kind='text',x=65,y=310,w=100,h=50,text='冲突',font_size=21));self.assert_bad(self.s,'SIBLING_OVERLAP')
 def test_edge_through_text(self):self.s['nodes'].append(dict(id='blocker',kind='text',x=300,y=245,w=80,h=55,text='阻断',font_size=21));self.assert_bad(self.s,'EDGE_THROUGH_NODE')
 def test_bound_endpoints(self):
  root=ET.fromstring(D.drawio(self.s));es=[e for e in root.iter('mxCell') if e.get('edge')=='1'];self.assertEqual(len(es),4)
  for e in es:self.assertTrue(e.get('source') and e.get('target'));self.assertEqual(e.find('mxGeometry').get('relative'),'1')
 def test_svg_editable(self):
  data=D.vector_svg(self.s,D.drawio(self.s));r=ET.fromstring(data);self.assertEqual(len(r.findall('.//{http://www.w3.org/2000/svg}image')),0);self.assertEqual(len(r.findall('.//{http://www.w3.org/2000/svg}text')),10);self.assertIn('<mxfile',r.get('content'))
 def test_pixels_units(self):
  from pptx import Presentation
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'a.pptx';D.native_ppt(self.s,p);r=Presentation(p);self.assertAlmostEqual(r.slide_width/914400,1400/96,places=4)
   with zipfile.ZipFile(p) as z:
    root=ET.fromstring(z.read('ppt/slides/slide1.xml'));ns={'p':'http://schemas.openxmlformats.org/presentationml/2006/main','a':'http://schemas.openxmlformats.org/drawingml/2006/main'}
    self.assertEqual(len(root.findall('.//p:pic',ns)),0);sizes={e.get('sz') for e in root.findall('.//a:rPr',ns)};self.assertEqual(sizes,{'1950','1575'})
 def test_author(self):
  from pptx import Presentation
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'a.pptx';D.native_ppt(self.s,p);self.assertEqual(Presentation(p).core_properties.author,'小罗')
 def test_no_overwrite(self):
  with tempfile.TemporaryDirectory() as t:
   with self.assertRaises(FileExistsError):D.build(ROOT/'examples/reference-reconstruction.scene.json',Path(t),'drawio')
 def test_pending_not_fake_approval(self):
  with tempfile.TemporaryDirectory() as t:
   out=Path(t)/'pass';state=D.build(ROOT/'examples/reference-reconstruction.scene.json',out,'both');self.assertEqual(state['visual_review'],'PENDING')
   with self.assertRaises(ValueError):D.review(out,'test','没有实际预览，不能通过检查。','PASS')
 def test_intake_rejects_script(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'evil.svg';p.write_text('<svg xmlns="http://www.w3.org/2000/svg"><script>alert(1)</script></svg>')
   with self.assertRaises(ValueError):I.intake(p,Path(t)/'out')
 def test_intake_rejects_fetch(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'evil.svg';p.write_text('<svg xmlns="http://www.w3.org/2000/svg"><image href="https://example.com/secret"/></svg>')
   with self.assertRaises(ValueError):I.intake(p,Path(t)/'out')
 def test_intake_dtd(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'evil.svg';p.write_text('<!DOCTYPE svg><svg xmlns="http://www.w3.org/2000/svg"/>')
   with self.assertRaises(ValueError):I.intake(p,Path(t)/'out')
 def test_intake_safe(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'source.svg';p.write_bytes(D.vector_svg(self.s,D.drawio(self.s)));rec=I.intake(p,Path(t)/'out');self.assertEqual(rec['status'],'AWAITING_VISUAL_INVENTORY');self.assertEqual(len(rec['elements']),10)
 def test_font_injection(self):self.s['font_family']='Songti;image=https://evil';self.assert_bad(self.s,'FONT_NAME')
 def test_native_roundtrip_contract(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'a.drawio';p.write_bytes(D.drawio(self.s));s=convert(p);self.assertEqual(D.contract(s),D.contract(self.s));self.assertEqual(D.bounds(s),D.bounds(self.s))
 def test_unsupported_import_rejected(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'a.drawio';r=ET.fromstring(D.drawio(self.s));c=next(e for e in r.iter('mxCell') if e.get('id')=='input_title');c.set('style',c.get('style')+'shape=cloud;');p.write_bytes(ET.tostring(r))
   with self.assertRaises(ValueError):convert(p)
 def test_compressed_import_rejected(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'a.drawio';p.write_text('<mxfile><diagram>compressed_payload</diagram></mxfile>')
   with self.assertRaises(ValueError):convert(p)
 def test_edited_scene_invalidates_approval(self):
  with tempfile.TemporaryDirectory() as t:
   out=Path(t)/'pass';D.build(ROOT/'examples/reference-reconstruction.scene.json',out,'drawio');(out/'scene.json').write_text('{}')
   with self.assertRaises(ValueError):D.review(out,'test','已变更内容，应当拒绝审批记录。','PASS')
 def test_source_unchanged(self):
  with tempfile.TemporaryDirectory() as t:
   p=ROOT/'examples/reference-reconstruction.scene.json';h=D.sha(p);D.build(p,Path(t)/'new','pptx');self.assertEqual(D.sha(p),h)

if __name__=='__main__':unittest.main(verbosity=2)
