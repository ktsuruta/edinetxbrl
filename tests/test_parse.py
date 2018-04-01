import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
import unittest
from edinetxbrl import parse

class TestParser(unittest.TestCase):

    def test_can_parse_quarter_report_in_current_context(self):
        file = 'tests/jpcrp040300.xbrl'
        jpcrp = parse.JPCRPP()
        jpcrp.parse(file,contextref='current')

        self.assertEqual(jpcrp.net_sales,7605767)
        self.assertEqual(jpcrp.profit_before_tax,750940)
        self.assertEqual(jpcrp.eps,319.01)
        self.assertEqual(jpcrp.cash_and_cash_equivalents,2746661)
        self.assertEqual(jpcrp.equity_to_asset_ratio,0.371)
        self.assertEqual(jpcrp.cash_flow_from_operating, 2843881)
        self.assertEqual(jpcrp.cash_flow_from_investing,-2909744)
        self.assertEqual(jpcrp.cash_flow_from_financing,-213783)


    def test_can_parse_quarter_report_in_previous_context(self):

        file = 'tests/jpcrp040300.xbrl'
        jpcrp = parse.JPCRPP()
        jpcrp.parse(file,contextref='prior1')

        self.assertEqual(jpcrp.net_sales,7084187)
        self.assertEqual(jpcrp.profit_before_tax,587538)
        self.assertEqual(jpcrp.eps, 161.26)
        self.assertEqual(jpcrp.cash_and_cash_equivalents,2550786)
        self.assertEqual(jpcrp.equity_to_asset_ratio,0.359)
        self.assertEqual(jpcrp.cash_flow_from_operating, 2161288)
        self.assertEqual(jpcrp.cash_flow_from_investing,-2159208)
        self.assertEqual(jpcrp.cash_flow_from_financing,-377167)

    def test_can_parse_annual_report_in_current_context(self):
        file = 'tests/jpcrp030000.xbrl'
        jpcrp = parse.JPCRPP()
        jpcrp.parse(file,contextref='current')

        self.assertEqual(jpcrp.net_sales,25691911)
        self.assertEqual(jpcrp.profit_before_tax,2441080)
        self.assertEqual(jpcrp.eps,575.30)
        self.assertEqual(jpcrp.cash_and_cash_equivalents,2041170)
        self.assertEqual(jpcrp.equity_to_asset_ratio,0.349)
        self.assertEqual(jpcrp.cash_flow_from_operating, 3646035)
        self.assertEqual(jpcrp.cash_flow_from_investing,-4336248)
        self.assertEqual(jpcrp.cash_flow_from_financing,919480)
        self.assertEqual(jpcrp.net_assets, 41437473)

    def test_can_parse_annual_report_in_previous_context(self):

        file = 'tests/jpcrp030000.xbrl'
        jpcrp = parse.JPCRPP()
        jpcrp.parse(file,contextref='prior1')

        self.assertEqual(jpcrp.net_sales,22064192)
        self.assertEqual(jpcrp.profit_before_tax, 1403649)
        self.assertEqual(jpcrp.eps, 303.82)
        self.assertEqual(jpcrp.cash_and_cash_equivalents,1718297)
        self.assertEqual(jpcrp.equity_to_asset_ratio,0.342)
        self.assertEqual(jpcrp.cash_flow_from_operating, 2451316)
        self.assertEqual(jpcrp.cash_flow_from_investing,-3027312)
        self.assertEqual(jpcrp.cash_flow_from_financing,477242)
        self.assertEqual(jpcrp.net_assets, 35483317)

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
        self.assertEqual(jpcrp.dei.whether_consolidated_financial_statements, True)
        self.assertEqual(jpcrp.get_current_fiscal_year(), '2013')

    def test_can_parse_dei(self):
        file = 'tests/jpcrp040300.xbrl'
        jpcrp = parse.JPCRPP()
        jpcrp.parse(file,contextref='current')

        self.assertEqual(jpcrp.dei.current_fiscal_year_start_date, "2017-04-01")
        self.assertEqual(jpcrp.dei.current_fiscal_year_end_date, "2018-03-31")
        self.assertEqual(jpcrp.dei.company_name, "トヨタ自動車株式会社")
        self.assertEqual(jpcrp.dei.edinet_code, 'E02144')
        self.assertEqual(jpcrp.dei.security_code, '72030')
        self.assertEqual(jpcrp.dei.accounting_standard, "US GAAP")
        self.assertEqual(jpcrp.dei.english_company_name, "TOYOTA MOTOR CORPORATION")
        self.assertEqual(jpcrp.dei.type_of_current_period, 'Q3')
        self.assertEqual(jpcrp.dei.whether_consolidated_financial_statements, True)
        self.assertEqual(jpcrp.get_current_fiscal_year(), '2017')


    def test_can_parse_dei(self):
        file = 'tests/JAPAN-GAAP-jpcrp030000.xbrl'
        jpcrp = parse.JPCRPP()
        jpcrp.parse(file,contextref='current')

        self.assertEqual(jpcrp.pay_out_ratio, 0.1426)
        self.assertEqual(jpcrp.ordinary_revenue, 1622)
        self.assertEqual(jpcrp.operating_revenue, 2521)


if __name__ == '__main__':
    unittest.main()