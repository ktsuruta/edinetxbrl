# coding: utf8
import sys
import requests
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import unittest
from xbrldownloader import downloader
import config

class TestRequest(unittest.TestCase):
    '''
    This is to ensure the request is success.
    '''

    def setUp(self):
        self.d = downloader.Downloader()
        self.d.get_request('https://webapi.yanoshin.jp/webapi/edinet/list/E02144.atom')

    def tearDown(self):
        pass

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
        self.d.parse_for_serching_edinet_links()
        self.assertIn('https://webapi.yanoshin.jp/rde.php?https%3A%2F%2Fdisclosure.edinet-fsa.go.jp%2FE01EW%2FBLMainController.jsp%3Fuji.verb%3DW00Z1010initialize%26uji.bean%3Dek.bean.EKW00Z1010Bean%26lgKbn%3D2%26syoruiKanriNo%3DS100CBLQ' ,self.d.url_list)

    def test_can_decode_a_url(self):
        '''
        This test ensure that decode method can decode all urls in url list.
        '''
        self.d.parse_for_serching_edinet_links()
        url = self.d._decode_url(self.d.url_list[0])
        print('decoded url ' + url)
        response = requests.get(url, verify=False)
        self.assertEqual(response.status_code, 200)

    def test_can_decode_urls(self):
        pass

if __name__ == '__main__':
    unittest.main()