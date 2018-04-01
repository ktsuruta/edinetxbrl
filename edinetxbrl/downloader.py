# coding: utf8

import datetime
from xml.etree import ElementTree
import requests as requests
import shutil
from urllib.parse import unquote

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
        file.write(self.response.text)
        file.close()

    def parse_for_serching_edinet_links(self):
        '''
        This method parses a file of TMP_FILR_DIR to get urls of EDINET.
        :return: [list] of urls
        '''
        tree = ElementTree.parse(config.TMP_FILE_DIR)
        root = tree.getroot()
        ns = {'feed': 'http://purl.org/atom/ns#'}
        for item in root.findall('feed:entry', ns):
            if "有価証券報告書" in item.find("feed:title", ns).text or "四半期報告書" in item.find("feed:title", ns).text:
                self.url_list.append(item.find("feed:link",ns).attrib['href'])

    def _decode_url(self, original_url):
        '''
        This method format param url to a genuin url to reach edinet server.
        :param original_url: A url starting with https://webapi.yanoshin.jp/rde.php?https%3A%2F%2
        :return: <str>: url starting with https://disclosure...
        '''
        undecoded_url = original_url.split('?')[1]
        return unquote(undecoded_url)

    def decode_url_list(self):
        '''
        This method remove unnecessary parts from the urls we got from 'https://webapi.yanoshin/edinet'
        :return: None
        '''
        self.url_list = list(map(self._decode_url, self.url_list))

    def _download_a_file(self, url):
        '''
        This method is to download a zip file of param url. Inner method.
        :param <str> url: A url of zip file to download
        :return:
        '''
        try:
            response = requests.get(url, verify=False, stream=True)
            file_dir = config.DOWNLOAD_DIR + str(datetime.datetime.now()).replace(' ','') + '.zip'
            with open(file_dir, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
                print(file_dir + " is downloaded")
        except:
            print('You got an error.')

    def download_files(self):
        for url in self.url_list:
            print(url)
            self._download_a_file(url)

    def main(self):
        pass
