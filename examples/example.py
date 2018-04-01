import glob
from os import path
import sys
sys.path.append(path.dirname( path.dirname( path.abspath(__file__) ) ) )
from edinetxbrl import parse, importer

def main():
    #files = ['tests/jpcrp040300.xbrl','tests/jpcrp030000.xbrl']
    files =  glob.glob("../Desktop/git/xbrl_files/*")
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
    main()
