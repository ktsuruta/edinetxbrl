import sys
import os
from os import path
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )

import unittest
from edinetxbrl import unzip
import config

class TestUnzip(unittest.TestCase):

    def test_can_unzip_a_file(self):
        file = '/home/ken/xbrldownloader/work_dir/tmp_download/2018-03-2920:38:53.048241.zip'
        unzip.Unziper._unzip_a_file(file)

    def test_can_unzip_all_files_in_a_directory(self):
        unzip.Unziper.unzip(dir='/home/ken/xbrldownloader/work_dir/tmp_download/*.zip')

    def test_can_return_list_of_unziped_files(self):
        pass



if __name__ == '__main__':
    unittest.main()
