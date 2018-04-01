# coding: utf8
import glob, os, zipfile, requests
import sys
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import unittest
from edinetxbrl import downloader, unzip, parse, importer
import config

class TestFunctional(unittest.TestCase):

    def setUp(self):
        for f in glob.glob(config.DOWNLOAD_DIR + '*'):
            os.remove(f)

    def test_can_download_unzip_parse_and_import(self):
        edinet_codes = ['E04024', 'E03074']
        file_downloader = downloader.Downloader()
        for edinet_code in edinet_codes:
            request_url = 'https://webapi.yanoshin.jp/webapi/edinet/list/' + edinet_code + '.atom?hasXBRL=1'
            file_downloader.get_request(request_url)
            file_downloader.save_response_as_tmp()
            file_downloader.parse_for_serching_edinet_links()
            file_downloader.decode_url_list()
            file_downloader.download_files()

        unzip.Unziper.unzip()

        files = glob.glob(config.UNZIP_FILE_DIR+"**/**/PublicDoc/*.xbrl")


        file_num = len(files)
        jpcrp = parse.JPCRPP()
        data_importer = importer.Importer()
        counter = 1
        for file in files:
            print(str(counter) + ' / ' + str(file_num))
            try:
                jpcrp.parse(file, contextref='current')
                data_importer.import_dei_to_mysql(jpcrp)
                data_importer.import_report_to_mysql(jpcrp)
            except:
                print('Something wrong has happened.')
                print(file)
            counter += 1

if __name__ == '__main__':
    unittest.main()

