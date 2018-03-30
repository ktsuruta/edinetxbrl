import os
import glob
import zipfile
import config

class Unziper():
    '''
    This class to unzip files downloaded from yanoshin web api.
    '''


    @staticmethod
    def _unzip_a_file(file, dest=config.UNZIP_FILE_DIR):
        '''
        :param file: set a file to unzip
        :param dest: set a directory to extract a zip file.
        :return:
        '''
        with open(file, 'rb') as f:
            try:
                zf = zipfile.ZipFile(f)
                zf.extractall(dest)
                os.remove(file)
            except:
                print(file + ' cannot be unziped')
                os.remove(file)

    @staticmethod
    def unzip(dir=config.DOWNLOAD_DIR):
        '''

        :param dir: set a directory having zip files to unzip
        :return:
        '''
        for file in glob.glob((dir + '*')):
            Unziper._unzip_a_file(file)
