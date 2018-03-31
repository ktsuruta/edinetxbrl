import datetime
import pymysql.cursors

class Importer():
    '''

    '''

    def __init__(self):
        # Connect to the database
        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password='Tarutsunnke0331',
                                          db='xbrl',
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

    def table_clear(self):
        with self.connection.cursor() as cusor:
            sql = "DELETE from company"
            cusor.execute(sql)
            sql = "DELETE from report"
            cusor.execute(sql)
            self.connection.commit()


    def import_dei_to_mysql(self, jpcrp):
        with self.connection.cursor() as cursor:
            sql = "REPLACE into company ( edinet_code, \
                company_name, \
                english_company_name, \
                security_code) VALUES(%s,%s,%s,%s)"
            cursor.execute(sql, (jpcrp.dei.edinet_code,
                                 jpcrp.dei.company_name,
                                 jpcrp.dei.english_company_name,
                                 jpcrp.dei.security_code))
        self.connection.commit()

    def count_company(self):
        with self.connection.cursor() as cusor:
            sql = "select count(*) from company"
            cusor.execute(sql)
            result = cusor.fetchone()
            count = result['count(*)']
            return count

    def import_report_to_mysql(self, jpcrp):
        with self.connection.cursor() as cursor:
            sql = "REPLACE into report (\
                edinet_code,\
                year,\
                per,\
                roe,\
                eps,\
                equity_to_asset_ratio,\
                net_sales,\
                net_assets,\
                operating_revenue,\
                profit_before_tax,\
                owners_equity_per_share,\
                cash_and_cash_equivalents,\
                cash_flow_from_operating,\
                cash_flow_from_investing,\
                cash_flow_from_financing,\
                type_of_current_period,\
                accounting_standard,\
                whether_consolidated_financial_statements,\
                current_fiscal_year_start_date,\
                current_fiscal_year_end_date)\
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,\
                       %s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            print(jpcrp.net_sales)
            cursor.execute(sql,(
            jpcrp.dei.edinet_code,
            jpcrp.get_current_fiscal_year(),
            jpcrp.per,
            jpcrp.roe,
            jpcrp.eps,
            jpcrp.equity_to_asset_ratio,
            jpcrp.net_sales,
            jpcrp.net_assets,
            jpcrp.operating_revenue,
            jpcrp.profit_before_tax,
            jpcrp.owners_equity_per_share,
            jpcrp.cash_and_cash_equivalents,
            jpcrp.cash_flow_from_operating,
            jpcrp.cash_flow_from_investing,
            jpcrp.cash_flow_from_financing,
            jpcrp.dei.type_of_current_period,
            jpcrp.dei.accounting_standard,
            jpcrp.dei.whether_consolidated_financial_statements,
            jpcrp.get_current_fiscal_year_start_date(),
            jpcrp.get_current_fiscal_year_end_date(),
            ))
            self.connection.commit()

    def count_report(self):
        with self.connection.cursor() as cusor:
            sql = "select count(*) from report"
            cusor.execute(sql)
            result = cusor.fetchone()
            count = result['count(*)']
            return count