import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import unittest
from edinetxbrl import parse, importer
import config

class TestImporter(unittest.TestCase):

    def setUp(self):
        importer.Importer().table_clear()

    def test_can_import_company(self):
        file = 'tests/jpcrp040300.xbrl'
        jpcrp = parse.JPCRPP()
        jpcrp.parse(file,contextref='current')
        sql_excuter = importer.Importer()
        sql_excuter.import_dei_to_mysql(jpcrp)
        self.assertEqual(sql_excuter.count_company(), 1)

    def test_can_import_report(self):
        file = 'tests/jpcrp040300.xbrl'
        jpcrp = parse.JPCRPP()
        jpcrp.parse(file,contextref='current')
        sql_excuter = importer.Importer()
        sql_excuter.import_report_to_mysql(jpcrp)
        self.assertEqual(sql_excuter.count_report(), 1)

        


if __name__ == '__main__':
    unittest.main()
