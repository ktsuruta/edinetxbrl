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
        file = 'tests/jpcrp040300.xbrl'
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


    def test_can_parse_quarter_report_in_previous_context(self):

        file = 'tests/jpcrp040300.xbrl'
        jpcrp = parse.JPCRPP()
        jpcrp.parse(file,contextref='prior1')

        self.assertEqual(jpcrp.net_sales,7084187000000)
        self.assertEqual(jpcrp.profit_before_tax,587538000000)
        self.assertEqual(jpcrp.eps, 161.26)
        self.assertEqual(jpcrp.cash_and_cash_equivalents,2550786000000)
        self.assertEqual(jpcrp.equity_to_asset_ratio,0.359)
        self.assertEqual(jpcrp.cash_flow_from_operating, 2161288000000)
        self.assertEqual(jpcrp.cash_flow_from_investing,-2159208000000)
        self.assertEqual(jpcrp.cash_flow_from_financing,-377167000000)

    def test_can_parse_annual_report_in_current_context(self):
        file = 'tests/jpcrp030000.xbrl'
        jpcrp = parse.JPCRPP()
        jpcrp.parse(file,contextref='current')

        self.assertEqual(jpcrp.net_sales,25691911000000)
        self.assertEqual(jpcrp.profit_before_tax,2441080000000)
        self.assertEqual(jpcrp.eps,575.30)
        self.assertEqual(jpcrp.cash_and_cash_equivalents,2041170000000)
        self.assertEqual(jpcrp.equity_to_asset_ratio,0.349)
        self.assertEqual(jpcrp.cash_flow_from_operating, 3646035000000)
        self.assertEqual(jpcrp.cash_flow_from_investing,-4336248000000)
        self.assertEqual(jpcrp.cash_flow_from_financing,919480000000)


    def test_can_parse_annual_report_in_previous_context(self):

        file = 'tests/jpcrp030000.xbrl'
        jpcrp = parse.JPCRPP()
        jpcrp.parse(file,contextref='prior1')

        self.assertEqual(jpcrp.net_sales,22064192000000)
        self.assertEqual(jpcrp.profit_before_tax, 1403649000000)
        self.assertEqual(jpcrp.eps, 303.82)
        self.assertEqual(jpcrp.cash_and_cash_equivalents,1718297000000)
        self.assertEqual(jpcrp.equity_to_asset_ratio,0.342)
        self.assertEqual(jpcrp.cash_flow_from_operating, 2451316000000)
        self.assertEqual(jpcrp.cash_flow_from_investing,-3027312000000)
        self.assertEqual(jpcrp.cash_flow_from_financing,477242000000)

    def test_can_parse_dei(self):
        file = 'tests/jpcrp030000.xbrl'
        jpcrp = parse.JPCRPP()
        jpcrp.parse(file,contextref='current')

        self.assertEqual(jpcrp.dei.current_fiscal_year_start_date, "2013-04-01")
        self.assertEqual(jpcrp.dei.current_fiscal_year_end_date, "2014-03-31")
        self.assertEqual(jpcrp.dei.company_name, "トヨタ自動車株式会社")
        self.assertEqual(jpcrp.dei.edinet_code, 'E02144')
        self.assertEqual(jpcrp.dei.security_code, '72030')
        self.assertEqual(jpcrp.dei.accounting_standard, "US GAAP")
        self.assertEqual(jpcrp.dei.english_company_name, "TOYOTA MOTOR CORPORATION")
        self.assertEqual(jpcrp.dei.type_of_current_period, 'FY')
        self.assertEqual(jpcrp.dei.whether_consolidated_financial_statements, 'true')

if __name__ == '__main__':
    unittest.main()