import datetime
import re
from xbrl import XBRLParser

class Parser():
    pass


# Base XBRL object
class JPCRPP(object):

    UNIT = 1000000

    def __init__(self,
                 contextref='current',
                 per = 0.0,#株価÷一株あたり純利益
                 roe = 0.0, #純利益÷自己資本
                 eps = 0.0, #earnings per share, １株あたり純利益
                 equity_to_asset_ratio = 0.0,#自己資産比率
                 net_sales = 0.0,#売上高
                 net_assets = 0.0, #純資産
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
        self._per = per
        self._roe = roe
        self._eps = eps
        self.equity_to_asset_ratio = equity_to_asset_ratio
        self._net_sales = net_sales
        self._net_assets = net_assets
        self._operating_revenue = operating_revenue
        self._profit_before_tax = profit_before_loss
        self.owners_equity_per_share = owners_equity_per_share
        self._cash_and_cash_equivalents = cash_and_cash_equivalents
        self._cash_flow_from_operating = cash_flow_from_operating
        self._cash_flow_from_investing = cash_flow_from_investing
        self._cash_flow_from_financing = cash_flow_from_financing
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

        # dei current fiscal year start date
        current_fiscal_year_start_date = parser.find(name=re.compile(("CurrentFiscalYearStartDateDEI"), re.IGNORECASE | re.MULTILINE))
        self.dei.current_fiscal_year_start_date = self._data_process_for_dei(current_fiscal_year_start_date)

        # dei current fiscal year end date
        current_fiscal_year_end_date = parser.find(name=re.compile(("CurrentFiscalYearEndDateDEI"), re.IGNORECASE | re.MULTILINE))
        self.dei.current_fiscal_year_end_date = self._data_process_for_dei(current_fiscal_year_end_date)

        # dei company name
        company_name = parser.find(name=re.compile(("FilerNameInJapaneseDEI"), re.IGNORECASE | re.MULTILINE))
        self.dei.company_name = self._data_process_for_dei(company_name)

        # dei edinet code
        edinet_code = parser.find(name=re.compile(("EDINETCodeDEI"), re.IGNORECASE | re.MULTILINE))
        self.dei.edinet_code = self._data_process_for_dei(edinet_code)

        # dei security code
        security_code = parser.find(name=re.compile(("SecurityCodeDEI"), re.IGNORECASE | re.MULTILINE))
        self.dei.security_code = self._data_process_for_dei(security_code)

        # dei accounting standard
        accounting_standard = parser.find(name=re.compile(("AccountingStandardsDEI"), re.IGNORECASE | re.MULTILINE))
        self.dei.accounting_standard = self._data_process_for_dei(accounting_standard)

        # dei english company name
        english_company_name = parser.find(name=re.compile(("FilerNameInEnglishDEI"), re.IGNORECASE | re.MULTILINE))
        self.dei.english_company_name = self._data_process_for_dei(english_company_name)

        # dei type of current period
        type_of_current_period = parser.find(name=re.compile(("TypeOfCurrentPeriodDEI"), re.IGNORECASE | re.MULTILINE))
        self.dei.type_of_current_period = self._data_process_for_dei(type_of_current_period)

        # dei whether_consolidated_financial_statements
        whether_consolidated_financial_statements = parser.find(name=re.compile(("WhetherConsolidatedFinancialStatementsArePreparedDEI"), re.IGNORECASE | re.MULTILINE))
        self.dei.whether_consolidated_financial_statements = self._data_process_for_dei(whether_consolidated_financial_statements)

        # per
        per = parser.find_all(name=re.compile(("riceEarningsRatioIFRSSummaryOfBusinessResults.?|PriceEarningsRatioSummaryOfBusinessResults.?|PriceEarningsRatioSummaryOfBusinessResults.?|PriceEarningsRatioIFRSSummaryOfBusinessResults.?|PriceEarningsRatioJMISSummaryOfBusinessResults.?"), \
                                                    re.IGNORECASE | re.MULTILINE))
        self.per = self._data_process_by_context(per)

        # roe
        roe = parser.find_all(name=re.compile(("RateOfReturnOnEquitySummaryOfBusinessResults.?|RateOfReturnOnEquitySummaryOfBusinessResults.?|RateOfReturnOnEquityUSGAAPSummaryOfBusinessResults.?"), \
                                                    re.IGNORECASE | re.MULTILINE))
        self.roe = self._data_process_by_context(roe)

        # eps                                  
        eps = parser.find_all(name=re.compile(("BasicEarningsLossPerShareSummaryOfBusinessResults.?|BasicEarningsLossPerShareUSGAAPSummaryOfBusinessResults.?|BasicEarningsLossPerShareIFRSSummaryOfBusinessResults.?"), \
                                                    re.IGNORECASE | re.MULTILINE))
        self.eps = self._data_process_by_context(eps)

        # equity to asset ratio
        equity_to_asset_ratio = parser.find_all(name=re.compile(("EquityToAssetRatioSummaryOfBusinessResults.?|EquityToAssetRatioUSGAAPSummaryOfBusinessResults.?"), \
                                                    re.IGNORECASE | re.MULTILINE))
        self.equity_to_asset_ratio = self._data_process_by_context(equity_to_asset_ratio)

        # owners equity per share
        owners_equity_per_share = parser.find_all(name=re.compile(("EquityToAssetRatioJMISSummaryOfBusinessResults.?|EquityToAssetRatioIFRSSummaryOfBusinessResults.?"), \
                                                    re.IGNORECASE | re.MULTILINE))
        self.owners_equity_per_share = self._data_process_by_context(owners_equity_per_share)

        # cash and cash equivalent
        cash_and_cash_equivalents = parser.find_all(name=re.compile(("CashAndCashEquivalentsIFRSSummaryOfBusinessResults.?|CashAndCashEquivalentsJMISSummaryOfBusinessResults.?|CashAndCashEquivalentsUSGAAPSummaryOfBusinessResults.?|CashAndCashEquivalentsSummaryOfBusinessResults.?"), \
                                                    re.IGNORECASE | re.MULTILINE))
        self.cash_and_cash_equivalents = self._data_process_by_context(cash_and_cash_equivalents)

        # net sales
        net_sales = parser.find_all(name=re.compile(("RevenuesUSGAAPSummaryOfBusinessResults.?|NetSalesSummaryOfBusinessResults.?"), \
                                                                   re.IGNORECASE | re.MULTILINE))
        self.net_sales = self._data_process_by_context(net_sales)

        # net assets
        net_assets = parser.find_all(name=re.compile(("NetAssetsSummaryOfBusinessResults.?|TotalAssetsSummaryOfBusinessResults.?|TotalAssetsIFRSSummaryOfBusinessResults.?|TotalAssetsJMISSummaryOfBusinessResults.?|TotalAssetsUSGAAPSummaryOfBusinessResults.?"), \
                                                    re.IGNORECASE | re.MULTILINE))
        self.net_assets = self._data_process_by_context(net_assets)

        #profit before tax
        profit_before_tax = parser.find_all(name=re.compile(("ProfitLossBeforeTaxJMISSummaryOfBusinessResults.?|ProfitLossBeforeTaxUSGAAPSummaryOfBusinessResults"), \
                                                          re.IGNORECASE | re.MULTILINE))
        self.profit_before_tax = self._data_process_by_context(profit_before_tax)

        #ordinary income
        operating_revenue = parser.find_all(name=re.compile((".?OperatingRevenue.?|OperatingIncomeLossUSGAAPSummaryOfBusinessResults.?|OrdinaryIncomeLossSummaryOfBusinessResults.?"), \
                                                                   re.IGNORECASE | re.MULTILINE))
        self.operating_revenue = self._data_process_by_context(operating_revenue)

        # cash flow from operating
        cash_flow_from_operating = parser.find_all(name=re.compile(("CashFlowsFromUsedInOperating.?|NetCashProvidedByUsedInOperating.?"), \
                                                                   re.IGNORECASE | re.MULTILINE))
        self.cash_flow_from_operating = self._data_process_by_context(cash_flow_from_operating)

        # cash flow from investing
        cash_flow_from_investing = parser.find_all(name=re.compile(("CashFlowsFromUsedInInvesting.?|NetCashProvidedByUsedInInvesting.?"), \
                                                                   re.IGNORECASE | re.MULTILINE))
        self.cash_flow_from_investing = self._data_process_by_context(cash_flow_from_investing)

        # cash flow from financing
        cash_flow_from_financing = parser.find_all(name=re.compile(("CashFlowsFromUsedInFinancing.?|NetCashProvidedByUsedInFinancing.?"), \
                                                                   re.IGNORECASE | re.MULTILINE))
        self.cash_flow_from_financing = self._data_process_by_context(cash_flow_from_financing)


    def _data_process_by_context(self,nodes):
        '''
        :return: the correct value according to the context
        Contextref has two types of words starting with current,which are YTD and current term.
        Current term is prioritized.
        '''
        condition1 = re.compile((self.contextref+"quarter.?"),re.IGNORECASE)
        condition2 = re.compile((self.contextref+".?"),re.IGNORECASE)
        if self.dei.whether_consolidated_financial_statements:
            for node in nodes:
                if condition1.match(node['contextref']):
                    if 'NonConsolidatedMember' not in node['contextref']:
                        return float(node.text)
            for node in nodes:
                if condition2.match(node['contextref']):
                    if 'NonConsolidatedMember' not in node['contextref']:
                        try:
                            return float(node.text)
                        except ValueError:
                            return 0
        for node in nodes:
            if condition1.match(node['contextref']):
                try:
                    return float(node.text)
                except ValueError:
                    return 0
        for node in nodes:
            if condition2.match(node['contextref']):
                try:
                    return float(node.text)
                except:
                    return 0
        return 0

    def _data_process_for_dei(self, node):

        if node is None:
            return ''
        elif node.text == 'true':
            return True
        elif node.text == 'false':
            return False
        else:
            return node.text

    def get_current_fiscal_year(self):
        return(self.dei.current_fiscal_year_start_date[:4])

    def get_type_of_current_period(self):
        return(datetime.datetime(int(self.dei.type_of_current_period),1,1))

    def get_current_fiscal_year_start_date(self):
        date_elements = self.dei.current_fiscal_year_start_date.split('-')
        return datetime.datetime(int(date_elements[0]), int(date_elements[1]), int(date_elements[2]))

    def get_current_fiscal_year_end_date(self):
        date_elements = self.dei.current_fiscal_year_end_date.split('-')
        return datetime.datetime(int(date_elements[0]), int(date_elements[1]), int(date_elements[2]))

    @property
    def per(self):
        if self._per < -999:
            return -999
        else:
            return self._per

    @per.setter
    def per(self, value):
        self._per = value

    @property
    def roe(self):
        if self._roe < -999:
            return -999
        else:
            return self._roe

    @roe.setter
    def roe(self, value):
        self._roe = value

    @property
    def eps(self):
        if self._eps < -999:
            return -999
        else:
            return self._eps

    @eps.setter
    def eps(self, value):
        self._eps = value

    @property
    def net_sales(self):
        return self._net_sales / JPCRPP.UNIT

    @net_sales.setter
    def net_sales(self, value):
        self._net_sales = value

    @property
    def net_assets(self):
        return self._net_assets / JPCRPP.UNIT

    @net_assets.setter
    def net_assets(self, value):
        self._net_assets = value

    @property
    def operating_revenue(self):
        return self._operating_revenue / JPCRPP.UNIT

    @operating_revenue.setter
    def operating_revenue(self, value):
        self._operating_revenue = value

    @property
    def profit_before_tax(self):
        return self._profit_before_tax / JPCRPP.UNIT

    @profit_before_tax.setter
    def profit_before_tax(self, value):
        self._profit_before_tax = value

    @property
    def cash_and_cash_equivalents(self):
        return self._cash_and_cash_equivalents / JPCRPP.UNIT

    @cash_and_cash_equivalents.setter
    def cash_and_cash_equivalents(self, value):
        self._cash_and_cash_equivalents = value

    @property
    def cash_flow_from_operating(self):
        return self._cash_flow_from_operating / JPCRPP.UNIT

    @cash_flow_from_operating.setter
    def cash_flow_from_operating(self, value):
        self._cash_flow_from_operating = value

    @property
    def cash_flow_from_investing(self):
        return self._cash_flow_from_investing / JPCRPP.UNIT

    @cash_flow_from_investing.setter
    def cash_flow_from_investing(self, value):
        self._cash_flow_from_investing = value

    @property
    def cash_flow_from_financing(self):
        return self._cash_flow_from_financing / JPCRPP.UNIT

    @cash_flow_from_financing.setter
    def cash_flow_from_financing(self, value):
        self._cash_flow_from_financing = value


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



