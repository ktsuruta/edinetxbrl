import sys
import os
from os import path
import re
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import unittest
from edinetxbrl import parse
import config

class TestParser(unittest.TestCase):

    def test_can_parse_quarter_report_in_current_context(self):
        file = '/home/ken/xbrldownloader/work_dir/unzip/S100CBLQ/XBRL/PublicDoc/jpcrp040300-q3r-001_E02144-000_2017-12-31_01_2018-02-13.xbrl'
        jpcrp = parse.JPCRPP()
        jpcrp.parse(file,contextref='current')

        self.assertEqual(jpcrp.net_sales,7605767000000)
        self.assertEqual(jpcrp.profit_before_tax,750940000000)
        self.assertEqual(jpcrp.eps,319.01)
        self.assertEqual(jpcrp.cash_and_cash_equivalents,2746661000000)
        self.assertEqual(jpcrp.equity_to_asset_ratio,0.371)
        self.assertEqual(jpcrp.cash_flow_from_operating, 2843881000000)
        self.assertEqual(jpcrp.cash_flow_from_investing,-2909744000000)
        self.assertEqual(jpcrp.cash_flow_from_financing,-213783000000)


    def test_can_define_report_year(self):

        file = '/home/ken/xbrldownloader/work_dir/unzip/S100CBLQ/XBRL/PublicDoc/jpcrp040300-q3r-001_E02144-000_2017-12-31_01_2018-02-13.xbrl'
        jpcrp = parse.JPCRPP()
        jpcrp.parse(file,contextref='prior1')

        self.assertEqual(jpcrp.net_sales,7605767000000)
        self.assertEqual(jpcrp.profit_before_tax,750940000000)
        self.assertEqual(jpcrp.eps,319.01)
        self.assertEqual(jpcrp.cash_and_cash_equivalents,2746661000000)
        self.assertEqual(jpcrp.equity_to_asset_ratio,0.371)
        self.assertEqual(jpcrp.cash_flow_from_operating, 2843881000000)
        self.assertEqual(jpcrp.cash_flow_from_investing,-2909744000000)
        self.assertEqual(jpcrp.cash_flow_from_financing,-213783000000)


if __name__ == '__main__':
    unittest.main()