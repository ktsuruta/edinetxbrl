# coding: utf8

from xml.etree import ElementTree
import requests as requests

import config

class Downloader():
    '''
    This class is to download xbrl zip files from EDINET using web api of
    'https://webapi.yanoshin.jp/edinet/'


    '''


    def __init__(self):
        self.url_list = []

    def get_request(self, url):
        '''

        :param <str> url to request
        :return: None. Store response in self.response as response object in requets.
        '''
        self.response = requests.get(url)

    def save_response_as_tmp(self):
        '''
        Save self.response.text in ./tmp/response
        :param [response object] response of requests.get()
        :return: [None]
        '''
        file = open(config.TMP_FILE_DIR,'w')
        file.write(self.response.content)



    def parse_for_serching_edinet_links(self):
        '''
        This method parses a file of TMP_FILR_DIR to get urls of EDINET.
        :return: [list] of urls
        '''
        print('Starting to parse ' + config.TMP_FILE_DIR)
        tree = ElementTree.parse(config.TMP_FILE_DIR)
        root = tree.getroot()
        ns = {'feed': 'http://purl.org/atom/ns#'}
        for item in root.findall('feed:entry', ns):
            if "有価証券報告書".decode('utf8') in item.find("feed:title", ns).text or "四半期報告書".decode('utf8')  in item.find("feed:title", ns).text:
                print(item.find("feed:title", ns).text)
                self.url_list.append(item.find("feed:link",ns).attrib['href'])

    def decode_url_list(self):
        '''

        :return:
        '''
