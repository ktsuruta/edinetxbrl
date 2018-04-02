import glob, os, shutil
from os import path
import sys, time
import pymongo
from pymongo import MongoClient
from distutils.dir_util import copy_tree

sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ) )
from edinetxbrl import selenium_downloader, unzip, parse, importer
import config

def batch(start=0, end=10, edinet_code_list=['E02505','E04024'], period='全期間', download_dir=config.DOWNLOAD_DIR):
    '''
    :param start:
    :param end:
    :param list
    :return: None
    Download all files from ofiicial edinet website and import mysql.
    '''
    if end > len(edinet_code_list):
        end = len(edinet_code_list) - 1
    for edinet_code in edinet_code_list[start:end]:
        try:
            selenium_downloader.edinet_downloader(edinet_code=edinet_code,period=period,download_dir=download_dir)
            time.sleep(3)
        except:
            'error occured'

    unzip.Unziper.unzip()

    files = glob.glob(config.UNZIP_FILE_DIR+"**/**/PublicDoc/*.xbrl")
    print(files)

    file_num = len(files)
    jpcrp = parse.JPCRPP()
    data_importer = importer.Importer()
    counter = 1
    for file in files:
        try:
            print(str(counter) + ' / ' + str(file_num))
            jpcrp.parse(file, contextref='current')
            data_importer.import_dei_to_mysql(jpcrp)
            data_importer.import_report_to_mysql(jpcrp)
        except:
            print('error occured')
        counter += 1
    for directory in glob.glob(config.UNZIP_FILE_DIR):
        copy_tree(directory, config.IMPORTED_DIR)
        shutil.rmtree(directory)
        os.mkdir(config.UNZIP_FILE_DIR)

def main():
    client = MongoClient()
    db = client.data_base
    collection = db.Corporation
    edinet_codes = collection.distinct('code')
    print(len(edinet_codes))

    number_of_codes_at_once = 10
    operating_times = len(edinet_codes) / number_of_codes_at_once
    operating_times = int(operating_times) + 1
    print(operating_times)
    for i in range(0, operating_times):
        start=i * number_of_codes_at_once
        end=start + number_of_codes_at_once
        batch(start=start,end=end, edinet_code_list=edinet_codes)
        print(i)


if __name__ == '__main__':
    main()
