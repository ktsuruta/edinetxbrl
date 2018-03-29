# coding: utf8
import glob
import sys
import requests
import os
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import unittest
from edinetxbrl import downloader
import config

class TestRequest(unittest.TestCase):
    '''
    This is to ensure the request is success.
    '''

    def setUp(self):
        self.d = downloader.Downloader()
        self.d.get_request('https://webapi.yanoshin.jp/webapi/edinet/list/E02144.atom?hasXBRL=1')

    def tearDown(self):
        for f in glob.glob(config.DOWNLOAD_DIR + '*'):
            os.remove(f)

    def test_can_open_a_requested_page(self):
        '''
        This test ensure Downloader can open a requested page.
        '''
        self.assertEqual(self.d.response.status_code, 200)

    def test_can_save_a_response_in_tmp_dir(self):
        '''
        This test ensure that response.text is stored in tmp dir.
        '''
        self.d.save_response_as_tmp()
        self.assertTrue(path.isfile(config.TMP_FILE_DIR))


    def test_can_find_a_url_in_the_response(self):
        '''
        This test ensure that parse method get a correct url list from the response.
        The urls include only annual report and quarter report.
        '''
        self.d.save_response_as_tmp()
        self.d.parse_for_serching_edinet_links()
        self.assertIn('https://webapi.yanoshin.jp/rde.php?https%3A%2F%2Fdisclosure.edinet-fsa.go.jp%2FE01EW%2Fdownload%3Fuji.verb%3DW0EZA104CXP001006BLogic%26uji.bean%3Dee.bean.parent.EECommonSearchBean%26lgKbn%3D2%26no%3DS100CBLQ' ,self.d.url_list)

    def test_can_decode_a_url(self):
        '''
        This test ensure that decode method can decode a url in url list.
        '''
        self.d.save_response_as_tmp()
        self.d.parse_for_serching_edinet_links()
        url = self.d._decode_url(self.d.url_list[0])
        response = requests.get(url, verify=False)
        self.assertEqual(response.status_code, 200)

    def test_can_decode_urls(self):
        '''
        This test eunsures that url list is decoded correctly, calling internlly _decode_a_url method.
        :return:
        '''
        self.d.save_response_as_tmp()
        self.d.parse_for_serching_edinet_links()
        self.d.decode_url_list()
        url = self.d.url_list[0]
        self.assertNotIn('https://webapi.yanoshin.jp', url)
        response = requests.get(url, verify=False)
        self.assertEqual(response.status_code, 200)

    def test_can_download_a_file_in_url_list(self):
        '''
        This test ensures that internal downloading method functions correctly.
        :return:
        '''
        self.d.save_response_as_tmp()
        self.d.parse_for_serching_edinet_links()
        self.d.decode_url_list()
        self.d._download_a_file(self.d.url_list[0])
        file_num = len(os.listdir(config.DOWNLOAD_DIR))
        self.assertEqual(file_num, 1)

    def test_can_download_all_files(self):
        '''
        This test ensures that all files of self.url_list are downloaded
        :return:
        '''
        self.d.save_response_as_tmp()
        self.d.parse_for_serching_edinet_links()
        self.d.decode_url_list()
        self.d.download_files()
        url_num = len(self.d.url_list)
        download_file_num = len(glob.glob(config.DOWNLOAD_DIR + '*'))
        self.assertEqual(url_num, download_file_num)

if __name__ == '__main__':
    unittest.main()