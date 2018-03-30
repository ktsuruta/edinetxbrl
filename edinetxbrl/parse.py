import re
from xbrl import XBRLParser

class Parser():
    pass


# Base XBRL object
class JPCRPP(object):
    def __init__(self,
                 contextref='current',
                 per = 0.0,#株価÷一株あたり純利益
                 roe = 0.0, #純利益÷自己資本
                 eps = 0.0, #earnings per share, １株あたり純利益
                 equity_to_asset_ratio = 0.0,#自己資産比率
                 net_sales = 0.0,#売上高
                 operating_revenue = 0.0, #営業利益
                 profit_before_loss = 0.0, #税引前利益
                 owners_equity_per_share = 0.0, #１株あたり資産
                 cash_and_cash_equivalents = 0.0, #流動資産
                 cash_flow_from_operating = 0.0,
                 cash_flow_from_investing = 0.0,
                 cash_flow_from_financing = 0.0,
                 company_name = '',
                 edinet_code = '',
                 security_code = '',
                 english_company_name = '',
                 type_of_current_period = '',
                 accounting_standard = '',
                 whether_consolidated_financial_statements = '',
                 current_fiscal_year_start_date = '',
                 current_fiscal_year_end_date = ''
                 ):
        self.contextref = contextref
        self.per = per
        self.roe = roe
        self.eps = eps
        self.equity_to_asset_ratio = equity_to_asset_ratio
        self.net_sales = net_sales
        self.operating_revenue = operating_revenue
        self.profit_before_tax = profit_before_loss
        self.owners_equity_per_share = owners_equity_per_share
        self.cash_and_cash_equivalents = cash_and_cash_equivalents
        self.cash_flow_from_operating = cash_flow_from_operating
        self.cash_flow_from_investing = cash_flow_from_investing
        self.cash_flow_from_financing = cash_flow_from_financing
        self.dei = DEI()
        self.dei.company_name = company_name,
        self.dei.edinet_code = edinet_code,
        self.dei.security_code = security_code,
        self.dei.english_company_name = english_company_name,
        self.dei.type_of_current_period = type_of_current_period,
        self.dei.accounting_standard = accounting_standard,
        self.dei.whether_consolidated_financial_statements = whether_consolidated_financial_statements,
        self.dei.current_fiscal_year_start_date = current_fiscal_year_start_date,
        self.dei.current_fiscal_year_end_date = current_fiscal_year_end_date


    def parse(self, file='', contextref=None):
        '''

        :param <str> file: set xbrl file
        :param <str> contextref: current, prior1, prior2, prior3, prior4
        :return: None. Set values in correponding variables accodding to xbrl file.
        '''
        self.__init__()

        if contextref is not None:
            self.contextref = contextref

        xbrl_parser = XBRLParser()
        parser = xbrl_parser.parse(open(file))

        # per
        per = parser.find_all(name=re.compile(("PriceEarningsRatioSummaryOfBusinessResults.?|PriceEarningsRatioIFRSSummaryOfBusinessResults.?|PriceEarningsRatioJMISSummaryOfBusinessResults.?"), \
                                                    re.IGNORECASE | re.MULTILINE))
        self.per = self._data_process_by_context(per)
        print('per => ' + str(self.per))

        # roe
        roe = parser.find_all(name=re.compile(("RateOfReturnOnEquitySummaryOfBusinessResults.?|RateOfReturnOnEquityUSGAAPSummaryOfBusinessResults.?"), \
                                                    re.IGNORECASE | re.MULTILINE))
        self.roe = self._data_process_by_context(roe)
        print('roe => ' + str(self.roe))

        # eps
        eps = parser.find_all(name=re.compile(("BasicEarningsLossPerShareUSGAAPSummaryOfBusinessResults.?|BasicEarningsLossPerShareIFRSSummaryOfBusinessResults.?"), \
                                                    re.IGNORECASE | re.MULTILINE))
        self.eps = self._data_process_by_context(eps)
        print('eps => ' + str(self.eps))

        # equity to asset ratio
        equity_to_asset_ratio = parser.find_all(name=re.compile(("EquityToAssetRatioSummaryOfBusinessResults.?|EquityToAssetRatioUSGAAPSummaryOfBusinessResults.?"), \
                                                    re.IGNORECASE | re.MULTILINE))
        self.equity_to_asset_ratio = self._data_process_by_context(equity_to_asset_ratio)
        print('equity to asset ratio => ' + str(self.equity_to_asset_ratio))

        # owners equity per share
        owners_equity_per_share = parser.find_all(name=re.compile(("EquityToAssetRatioJMISSummaryOfBusinessResults.?|EquityToAssetRatioIFRSSummaryOfBusinessResults.?"), \
                                                    re.IGNORECASE | re.MULTILINE))
        self.owners_equity_per_share = self._data_process_by_context(owners_equity_per_share)
        print('owners equity per share => ' + str(self.owners_equity_per_share))

        # cash and cash equivalent
        cash_and_cash_equivalents = parser.find_all(name=re.compile(("CashAndCashEquivalentsIFRSSummaryOfBusinessResults.?|CashAndCashEquivalentsJMISSummaryOfBusinessResults.?|CashAndCashEquivalentsUSGAAPSummaryOfBusinessResults.?"), \
                                                    re.IGNORECASE | re.MULTILINE))
        self.cash_and_cash_equivalents = self._data_process_by_context(cash_and_cash_equivalents)
        print('cash and cash equivalents => ' + str(self.cash_and_cash_equivalents))

        # net sales
        net_sales = parser.find_all(name=re.compile(("RevenuesUSGAAPSummaryOfBusinessResults.?|NetSalesSummaryOfBusinessResults.?"), \
                                                                   re.IGNORECASE | re.MULTILINE))
        self.net_sales = self._data_process_by_context(net_sales)
        print('net sales => ' + str(self.net_sales))

        #profit before tax
        profit_before_tax = parser.find_all(name=re.compile(("ProfitLossBeforeTaxJMISSummaryOfBusinessResults.?|ProfitLossBeforeTaxUSGAAPSummaryOfBusinessResults"), \
                                                          re.IGNORECASE | re.MULTILINE))
        self.profit_before_tax = self._data_process_by_context(profit_before_tax)
        print('profit before tax => ' + str(self.profit_before_tax))

        #ordinary income
        operating_revenue = parser.find_all(name=re.compile((".?OperatingRevenue.?|OperatingIncomeLossUSGAAPSummaryOfBusinessResults.?"), \
                                                                   re.IGNORECASE | re.MULTILINE))
        self.operating_revenue = self._data_process_by_context(operating_revenue)
        print('operating revenue => ' + str(self.operating_revenue))

        # cash flow from operating
        cash_flow_from_operating = parser.find_all(name=re.compile(("CashFlowsFromUsedInOperating.?"), \
                                                                   re.IGNORECASE | re.MULTILINE))
        self.cash_flow_from_operating = self._data_process_by_context(cash_flow_from_operating)
        print('cash flow operating=> ' + str(self.cash_flow_from_operating))

        # cash flow from investing
        cash_flow_from_investing = parser.find_all(name=re.compile(("CashFlowsFromUsedInInvesting.?"), \
                                                                   re.IGNORECASE | re.MULTILINE))
        self.cash_flow_from_investing = self._data_process_by_context(cash_flow_from_investing)
        print('cash flow investing => ' + str(self.cash_flow_from_investing))

        # cash flow from financing
        cash_flow_from_financing = parser.find_all(name=re.compile(("CashFlowsFromUsedInFinancing.?"), \
                                                                   re.IGNORECASE | re.MULTILINE))
        self.cash_flow_from_financing = self._data_process_by_context(cash_flow_from_financing)
        print('cash flow financing => ' + str(self.cash_flow_from_financing))

    def _data_process_by_context(self,nodes):
        '''
        :return: the correct value according to the context
        Contextref has two types of words starting with current,which are YTD and current term.
        Current term is prioritized.
        '''
        condition1 = re.compile((self.contextref+"quarter.?"),re.IGNORECASE)
        condition2 = re.compile((self.contextref+".?"),re.IGNORECASE)
        for node in nodes:
            if condition1.match(node['contextref']):
                return float(node.text)
        for node in nodes:
            if condition2.match(node['contextref']):
                return float(node.text)
        return 0

class DEI(object):

    def __init__(self):
        self.company_name = ''
        self.edinet_code = ''
        self.security_code = ''
        self.english_company_name = ''
        self.type_of_current_period = ''
        self.accounting_standard = ''
        self.whether_consolidated_financial_statements = ''
        self.current_fiscal_year_start_date = ''
        self.current_fiscal_year_end_date = ''



