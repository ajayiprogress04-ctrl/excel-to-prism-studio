import tempfile
import unittest
from pathlib import Path
import xml.etree.ElementTree as ET
import pandas as pd
from excel_to_prism import convert_excel_to_prism

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.base=Path(self.tmp.name)/'Research α data'; self.base.mkdir()
        self.source=self.base/'book.xlsx'
    def tearDown(self): self.tmp.cleanup()
    def book(self, rows): pd.DataFrame(rows).to_excel(self.source,index=False,header=False)
    def test_column_values_blanks(self):
        self.book([['A','B'],[1,4],[None,5],[3,6]])
        root=ET.parse(convert_excel_to_prism(self.source)).getroot()
        self.assertEqual(root.find('Table').get('TableType'),'OneWay')
        self.assertEqual([e.text for e in root.findall('Table/YColumn')[0].findall('Subcolumn/d')],['1',None,'3'])
    def test_xy(self):
        self.book([['Time','Y'],[0,2.5],[1,7]])
        root=ET.parse(convert_excel_to_prism(self.source,table_type='xy')).getroot()
        self.assertEqual(root.find('Table').get('TableType'),'XY')
        self.assertEqual([e.text for e in root.findall('Table/XColumn/Subcolumn/d')],['0','1'])
        self.assertEqual([e.text for e in root.findall('Table/YColumn/Subcolumn/d')],['2.5','7'])
    def test_sheets_and_skip_empty(self):
        with pd.ExcelWriter(self.source) as w:
            for name,rows in [('One',[['A'],[2]]),('Two',[['B'],[8]]),('Empty',[])]:
                pd.DataFrame(rows).to_excel(w,sheet_name=name,index=False,header=False)
        out=convert_excel_to_prism(self.source)
        self.assertEqual(len(ET.parse(out).getroot().find('TableSequence')),2)
        one=convert_excel_to_prism(self.source,self.base/'one.pzfx',sheet_name='Two')
        self.assertEqual(ET.parse(one).find('Table/Title').text,'Two')
    def test_invalid(self):
        self.book([['A'],['bad']])
        with self.assertRaisesRegex(ValueError,'A2'): convert_excel_to_prism(self.source)
        self.assertFalse(self.source.with_suffix('.pzfx').exists())
    def test_overwrite(self):
        self.book([['A'],[1]])
        out=self.source.with_suffix('.pzfx'); out.write_text('preserve')
        with self.assertRaises(FileExistsError): convert_excel_to_prism(self.source)
        self.assertEqual(out.read_text(),'preserve')
    def test_missing_unsupported(self):
        with self.assertRaises(FileNotFoundError): convert_excel_to_prism(self.source)
        bad=self.base/'bad.csv'; bad.write_text('a\n1')
        with self.assertRaises(ValueError): convert_excel_to_prism(bad)
    def test_xy_single_column(self):
        self.book([['A'],[1]])
        with self.assertRaisesRegex(ValueError,'at least one Y'): convert_excel_to_prism(self.source,table_type='xy')
    def test_missing_sheet(self):
        self.book([['A'],[1]])
        with self.assertRaisesRegex(ValueError,'Worksheet not found'): convert_excel_to_prism(self.source,sheet_name='missing')

if __name__=='__main__': unittest.main()
