import glob, os, shutil
from os import path
import sys, time
from distutils.dir_util import copy_tree

sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ) )
from edinetxbrl import unzip, parse, importer
import config

def main():
    unzip.Unziper.unzip()

    files = glob.glob(config.UNZIP_FILE_DIR+"**/**/PublicDoc/*.xbrl")
    print(files)

    file_num = len(files)
    print(file_num)
    jpcrp = parse.JPCRPP()
    data_importer = importer.Importer()
    for file in files:
        try:
            jpcrp.parse(file, contextref='current')
            data_importer.import_dei_to_mysql(jpcrp)
            data_importer.import_report_to_mysql(jpcrp)
        except Exception as ex:
            print('error occured', ex)
    for directory in glob.glob(config.UNZIP_FILE_DIR):
        copy_tree(directory, config.IMPORTED_DIR)
        shutil.rmtree(directory)
        os.mkdir(config.UNZIP_FILE_DIR)

if __name__ == '__main__':
    main()
