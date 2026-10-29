import unittest, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from labmate import analyze as base_analyze, render
def analyze(text,*args,**kwargs):
 lines=text.splitlines()
 if lines and lines[0].lstrip("\ufeff")=="sample_id,group,parameter,value,unit":
  counts={}
  out=["reading_id,"+lines[0].lstrip("\ufeff")]
  for i,line in enumerate(lines[1:]):
   sid=line.split(",")[0]
   out.append(sid+","+line)
  text="\n".join(out)
 return base_analyze(text,*args,**kwargs)
H='sample_id,group,parameter,value,unit\n'
class Tests(unittest.TestCase):
 def test_valid(self):
  r=analyze(H+'a,A,Moisture,2,%\nb,A,Moisture,4,%\n',True)
  self.assertEqual(r['summaries'][0]['mean'],3)
  self.assertAlmostEqual(r['summaries'][0]['sample_sd'],2**0.5)
 def test_duplicates(self):
  self.assertEqual(analyze(H+'a,A,pH,3,pH\na,A,pH,4,pH\n')['included_rows'],0)
 def test_nonfinite(self):
  self.assertEqual(analyze(H+'a,A,pH,NaN,pH\nb,A,pH,inf,pH')['excluded_rows'],2)
 def test_missing(self):
  self.assertEqual(analyze(H+'a,A,pH,,pH')['excluded_rows'],1)
 def test_schema(self):
  with self.assertRaises(ValueError):analyze('a,b\n1,2')
 def test_empty(self):
  with self.assertRaises(ValueError):analyze(H)
 def test_units(self):
  r=analyze(H+'a,A,x,2,g\nb,A,x,2,kg')
  self.assertEqual(len(r['summaries']),2);self.assertEqual(r['issues'][0]['severity'],'warning')
 def test_single(self):self.assertIsNone(analyze(H+'a,A,x,2,g')['summaries'][0]['sample_sd'])
 def test_escape(self):self.assertNotIn('<script>alert',render(analyze(H+'a,<script>alert,A,2,g')))
 def test_extra_cells(self):self.assertEqual(analyze(H+'a,A,x,2,g,extra')['excluded_rows'],1)
 def test_synthetic(self):self.assertIn('Synthetic demonstration data',render(analyze(H+'a,A,x,2,g',True)))
 def test_shared_sample(self):
  r=base_analyze('reading_id,sample_id,group,parameter,value,unit\nr1,s1,A,Moisture,4,%\nr2,s1,A,pH,5,pH')
  self.assertEqual(r['included_rows'],2)
 def test_bom(self):self.assertEqual(analyze('\ufeff'+H+'a,A,x,2,g')['included_rows'],1)
if __name__=='__main__':unittest.main()
