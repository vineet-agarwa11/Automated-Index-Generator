import os
import glob
from lib.index_calculator import index_calculator_landsat_8, index_calculator_sentinel, index_calculator_landsat_7, index_calculator_landsat_5


def generate_indices(down_dir_dict=dict, test=False, sat_choice=None):
    """
    Creates all the indices for a sub-folder in subdir_list in which relevant bands are found

    :type down_dir_dict: dict
    # :type base_path: string
    # :param root: root directory
    # :type root: string
    # :type landsat_list_len: integer
    # :type sentinel_list_len: integer
    :param test: bool for test case
    :type test: bool
    """
    print("==================")
    print("Generating Indices")
    base_dir = os.getcwd()
    image_dir_list = []
    for (name, d_dir) in down_dir_dict.items():
        path = os.path.join(d_dir, name)
        os.chdir(path)

        tif_list = glob.glob('*.TIF')
        jp2_list = glob.glob('**/*.jp2', recursive=True)

        if tif_list:
            print('Landsat images found in .{}'.format(path))
            if not test:
                print('Calculating Indices.....')
                try:
                    prefix = path.split('/')[-1]
                    if sat_choice=='1':
                        # noinspection PyTypeChecker
                        index_calculator_landsat_8.execute_landsat_8(prefix=prefix)
                    elif sat_choice=='2':
                        # noinspection PyTypeChecker
                        index_calculator_landsat_7.execute_landsat_7(prefix=prefix)
                    elif sat_choice == '3':
                        # noinspection PyTypeChecker
                        index_calculator_landsat_5.execute_landsat_5(prefix=prefix)
                    else:
                        pass
                    image_dir_list.append(os.getcwd())
                except ValueError:
                    print('Unable to make all indices')

        if jp2_list:
            sent_path = jp2_list[0].split('/')[:-2]
            os.chdir('/'.join(sent_path))
            os.chdir('IMG_DATA')
            print('Sentinel images found in .{}'.format(path))
            if not test:
                print('Calculating Indices.....')
                try:
                    prefix = os.getcwd().split('/')[-4].split('.')[0]
                    # noinspection PyTypeChecker
                    index_calculator_sentinel.execute_sentinel(prefix=prefix)
                    image_dir_list.append(os.getcwd())
                except ValueError:
                    print('Unable to make all indices')

        os.chdir(base_dir)
    print("Indices created successfully!!!")
    # return image_dir_list


def scourer(subdir_list=None, landsat_list_len=3, sentinel_list_len=3, test=False):
    root = os.getcwd()

    for sub in subdir_list:
        caps_tif_list = glob.glob(sub+'**/*.TIF', recursive=True)
        if len(caps_tif_list) >= landsat_list_len:
            path = '/'.join(caps_tif_list[0].split('/')[:-1])
            os.chdir(path)
            current_dir = os.getcwd()
            print('Landsat images found in .{}'.format(current_dir))
            if not test:
                print('Calculating Indices.....')
                try:
                    prefix = sub.split('/')[-1]
                    index_calculator_landsat_8.execute_landsat_8(prefix=prefix)
                except ValueError:
                    print('Unable to make all indices')
        os.chdir(root)

    for sub in subdir_list:
        tif_list = glob.glob(sub + '/*.tif')
        if len(tif_list) >= landsat_list_len:
            os.chdir(root + sub[1:])
            print('Landsat images found in .{}'.format(os.getcwd()))
            if not test:
                print('Calculating Indices.....')
                try:
                    index_calculator_landsat_8.execute_landsat_8()
                except ValueError:
                    print('Unable to make all indices')
        os.chdir(root)

    for sub in subdir_list:
        caps_jp2_list = glob.glob(sub + '/*.JP2')
        if len(caps_jp2_list) >= sentinel_list_len:
            os.chdir(root + sub[1:])
            print('Sentinel images found in .{}'.format(os.getcwd()))
            if not test:
                print('Calculating Indices.....')
                try:
                    index_calculator_sentinel.execute_sentinel()
                except ValueError:
                    print('Unable to make all indices')
        os.chdir(root)

    for sub in subdir_list:
        jp2_list = glob.glob(sub + '/*.jp2')
        if len(jp2_list) >= sentinel_list_len:
            os.chdir(root + sub[1:])
            print('Sentinel images found in .{}'.format(os.getcwd()))
            if not test:
                print('Calculating Indices.....')
                try:
                    index_calculator_sentinel.execute_sentinel()
                except ValueError:
                    print('Unable to make all indices')
        os.chdir(root)
