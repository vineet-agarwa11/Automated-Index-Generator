from rasterio import open
from rasterio.plot import show
import numpy as np
import glob

np.seterr(divide='ignore', invalid='ignore')


def band_returner_sentinel(show_list=False):
    """
    Returns the list of relevant bands as per the truth value of input parameters

    :param show_list: setting to show the list of bands
    :type show_list: bool
    :return: dictionary of bands
    :rtype: dict
    """
    _list = glob.glob('*')
    _list.sort()
    ret_dict = {}

    for band in _list:
        if '8A.jp2' in band[-7:]:
            ret_dict['8a'] = band  # nir
        if '11.jp2' in band[-7:]:
            ret_dict['11'] = band  # swir
        if '8.jp2' in band[-7:]:
            ret_dict['8'] = band  # nir
        if '4.jp2' in band[-7:]:
            ret_dict['4'] = band  # red
        if '3.jp2' in band[-7:]:
            ret_dict['3'] = band  # green
    if show_list:
        print(ret_dict)
    if len(_list) >= 4:
        return ret_dict
    else:
        return False


def ndmi_calc_sentinel(prefix=None, show_flag=False):
    """
    Calculates and saves the Normalised Difference Moisture Index (NDMI) raster image

    :param prefix: Prefix to be added to the saved indices
    :type prefix: string
    :param show_flag: setting to show index after calculation
    :type show_flag: bool
    """
    # get bands relevant to ndvi
    band_dict = band_returner_sentinel()

    if band_dict:
        # read bands
        band8a = open(band_dict['8a'])  # nir
        band11 = open(band_dict['11'])  # swir
        nir = band8a.read(1).astype('float64')
        swir = band11.read(1).astype('float64')

        # calculate ndmi raster image
        ndmi = np.where(
            (swir + nir) == 0.,
            0,
            (nir - swir) / (nir + swir)
        )

        # save ndmi raster image
        ndmi_image = open('./{}_ndmi_sentinel.tiff'.format(prefix), 'w', driver='GTiff',
                          width=band8a.width, height=band8a.height,
                          count=1,
                          crs=band8a.crs,
                          transform=band8a.transform,
                          dtype='float64')
        ndmi_image.write(ndmi, 1)
        ndmi_image.close()

        if show_flag:
            ndmi = open('{}_ndmi_sentinel.tiff'.format(prefix))
            show(ndmi, cmap='Blues')


def ndvi_calc_sentinel(prefix=None, show_flag=False):
    """
    Calculates and saves the Normalised Difference Vegetation Index (NDVI) raster image

    :param prefix: Prefix to be added to the saved indices
    :type prefix: string
    :param show_flag: setting to show index after calculation
    :type show_flag: bool
    """
    # get bands relevant to ndvi
    band_dict = band_returner_sentinel()

    if band_dict:
        # read bands
        band4 = open(band_dict['4'])  # red
        band8 = open(band_dict['8'])  # nir
        red = band4.read(1).astype('float64')
        nir = band8.read(1).astype('float64')

        # calculate ndvi raster image
        ndvi = np.where(
            (nir + red) == 0.,
            0,
            (nir - red) / (nir + red)
        )

        # save ndvi raster image
        ndvi_image = open('./{}_ndvi_sentinel.tiff'.format(prefix), 'w', driver='GTiff',
                          width=band8.width, height=band8.height,
                          count=1,
                          crs=band8.crs,
                          transform=band8.transform,
                          dtype='float64')
        ndvi_image.write(ndvi, 1)
        ndvi_image.close()

        if show_flag:
            ndvi = open('{}_ndvi_sentinel.tiff'.format(prefix))
            show(ndvi, cmap='Greens')


def savi_calc_sentinel(prefix=None, show_flag=False):
    """
    Calculates and saves the Soil Adjusted Vegetation Index (SAVI) raster image

    :param prefix: Prefix to be added to the saved indices
    :type prefix: string
    :param show_flag: setting to show index after calculation
    :type show_flag: bool
    """
    # get bands relevant to ndvi
    band_dict = band_returner_sentinel()

    if band_dict:
        # read bands
        band4 = open(band_dict['4'])  # red
        band8 = open(band_dict['8'])  # nir
        red = band4.read(1).astype('float64')
        nir = band8.read(1).astype('float64')

        # calculate savi raster image
        savi = np.where(
            (nir + red) == 0.,
            0,
            ((nir - red) / (nir + red + 0.5)) * 1.5
        )

        # INSERT CHECKING CONDITION
        savi[savi > 1] = 1
        savi[savi < -1] = -1

        # save savi raster image
        savi_image = open('./{}_savi_sentinel.tiff'.format(prefix), 'w', driver='GTiff',
                          width=band8.width, height=band8.height,
                          count=1,
                          crs=band8.crs,
                          transform=band8.transform,
                          dtype='float64')
        savi_image.write(savi, 1)
        savi_image.close()

        if show_flag:
            savi = open('{}_savi_sentinel.tiff'.format(prefix))
            show(savi, cmap='Greens')


def msavi_calc_sentinel(prefix=None, show_flag=False):
    """
    Calculates and saves the Modified Soil Adjusted Vegetation Index (MSAVI) raster image

    :param prefix: Prefix to be added to the saved indices
    :type prefix: string
    :param show_flag: setting to show index after calculation
    :type show_flag: bool
    """
    # get bands relevant to ndvi
    band_dict = band_returner_sentinel()

    if band_dict:
        # read bands
        band4 = open(band_dict['4'])  # red
        band8 = open(band_dict['8'])  # nir
        red = band4.read(1).astype('float64')
        nir = band8.read(1).astype('float64')

        # calculate msavi raster image
        msavi = np.where(
            (nir + red) == 0.,
            0,
            (2 * nir + 1 - np.sqrt((2 * nir + 1) ** 2 - 8 * (nir - red))) / 2
        )

        # INSERT CHECKING CONDITION
        msavi[msavi > 1] = 1
        msavi[msavi < -1] = -1

        # save msavi raster image
        msavi_image = open('./{}_msavi_sentinel.tiff'.format(prefix), 'w', driver='GTiff',
                           width=band8.width, height=band8.height,
                           count=1,
                           crs=band8.crs,
                           transform=band8.transform,
                           dtype='float64')
        msavi_image.write(msavi, 1)
        msavi_image.close()

        if show_flag:
            msavi = open('{}_msavi_sentinel.tiff'.format(prefix))
            show(msavi, cmap='Greens')


def ndwi_calc_sentinel(prefix=None, show_flag=False):
    """
    Calculates and saves the Normalised Difference Water Index (NDWI) raster image

    :param prefix: Prefix to be added to the saved indices
    :type prefix: string
    :param show_flag: setting to show index after calculation
    :type show_flag: bool
    """
    # get bands relevant to ndvi
    band_dict = band_returner_sentinel()

    if band_dict:
        # read bands
        band3 = open(band_dict['3'])  # green
        band8 = open(band_dict['8'])  # nir
        green = band3.read(1).astype('float64')
        nir = band8.read(1).astype('float64')

        # calculate ndwi raster image
        ndwi = np.where(
            (nir + green) == 0.,
            0,
            (green - nir) / (green + nir)
        )

        # INSERT CHECKING CONDITION
        ndwi[ndwi > 1] = 1
        ndwi[ndwi < -1] = -1

        # save ndwi raster image
        ndwi_image = open('./{}_ndwi_sentinel.tiff'.format(prefix), 'w', driver='GTiff',
                          width=band8.width, height=band8.height,
                          count=1,
                          crs=band8.crs,
                          transform=band8.transform,
                          dtype='float64')
        ndwi_image.write(ndwi, 1)
        ndwi_image.close()

        if show_flag:
            ndwi = open('{}_ndwi_sentinel.tiff'.format(prefix))
            show(ndwi, cmap='Greens')


def image_display_sentinel():
    """
    Displays the images of landsat indices in a folder one at a time
    """
    ndmi = open('ndmi_sentinel.tiff')
    ndvi = open('ndvi_sentinel.tiff')
    savi = open('savi_sentinel.tiff')
    msavi = open('msavi_sentinel.tiff')
    ndwi = open('ndwi_sentinel.tiff')
    show(ndmi, cmap='Blues')
    show(ndvi, cmap='Greens')
    show(savi, cmap='Greens')
    show(msavi, cmap='Greens')
    show(ndwi, cmap='BrBG')


def execute_sentinel(prefix=None, show_individual=False, show_all=False, show_only=False):
    """
    Executes the process of calculation of indices for sentinel images

    :param prefix: Prefix to be added to the saved indices
    :type prefix: string
    :param show_individual: setting for showing individual images while calculating indices
    :type show_individual: bool
    :param show_all: setting to show all the indices one by one after calculation
    :type show_all: bool
    :param show_only: setting for only showing images of existing indices, if any
    :type show_only: bool
    """
    try:
        if show_only:
            image_display_sentinel()
            exit()
        ndmi_calc_sentinel(prefix=prefix, show_flag=show_individual)
        ndvi_calc_sentinel(prefix=prefix, show_flag=show_individual)
        savi_calc_sentinel(prefix=prefix, show_flag=show_individual)
        msavi_calc_sentinel(prefix=prefix, show_flag=show_individual)
        ndwi_calc_sentinel(prefix=prefix, show_flag=show_individual)
        if show_all:
            image_display_sentinel()
    except RuntimeError:
        print('Unable to show images')


def sentinel_test():
    """
    Test case for the index_calculator_sentinel.py file
    """
    execute_sentinel(show_individual=True)
    band_returner_sentinel(show_list=True)
