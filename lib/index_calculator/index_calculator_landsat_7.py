from rasterio import open
from rasterio.plot import show
import numpy as np
import glob

np.seterr(divide='ignore', invalid='ignore')


def band_returner_landsat_7(show_list=False):
    """
    Returns the list of relevant bands as per the truth value of input parameters

    :param show_list: flag
    :type show_list: bool
    """
    _list = []
    _list = glob.glob('*')
    _list.sort()
    ret_dict = {}

    for band in _list:
        if '5.TIF' in band[-7:]:
            ret_dict['5'] = band  # swir
        if '4.TIF' in band[-7:]:
            ret_dict['4'] = band  # nir
        if '3.TIF' in band[-7:]:
            ret_dict['3'] = band  # red
        if '2.TIF' in band[-7:]:
            ret_dict['2'] = band  # green

    for band in _list:
        if '5.tif' in band[-7:]:
            ret_dict['5'] = band  # swir
        if '4.tif' in band[-7:]:
            ret_dict['4'] = band  # nir
        if '3.tif' in band[-7:]:
            ret_dict['3'] = band  # red
        if '2.tif' in band[-7:]:
            ret_dict['2'] = band  # green

    if show_list:
        # print(_list)
        print(ret_dict)
    if len(ret_dict) >= 3:
        return ret_dict
    else:
        return False


def ndmi_calc_landsat_7(prefix=None, show_flag=False):
    """
    Calculates and saves the Normalised Difference Moisture Index (NDMI) raster image
    :param prefix: Prefix to be added to the saved indices
    :type prefix: string
    :param show_flag: flag
    :type show_flag: bool
    """
    # get bands relevant to ndvi
    band_dict = band_returner_landsat_7()

    if band_dict:
        # read bands
        band4 = open(band_dict['4'])  # nir
        band5 = open(band_dict['5'])  # swir
        nir = band4.read(1).astype('float64')
        swir = band5.read(1).astype('float64')

        # calculate ndmi raster image
        ndmi = np.where(
            (swir + nir) == 0.,
            0,
            (nir - swir) / (nir + swir)
        )

        # save ndmi raster image
        ndmi_image = open('./{}_ndmi_landsat_7.tiff'.format(prefix), 'w', driver='GTiff',
                          width=band4.width, height=band4.height,
                          count=1,
                          crs=band4.crs,
                          transform=band4.transform,
                          dtype='float64')
        ndmi_image.write(ndmi, 1)
        ndmi_image.close()

        if show_flag:
            ndmi = open('{}_ndmi_landsat_7.tiff'.format(prefix))
            show(ndmi, cmap='Blues')


def ndvi_calc_landsat_7(prefix=None, show_flag=False):
    """
    Calculates and saves the Normalised Difference Vegetation Index (NDVI) raster image
    :param prefix: Prefix to be added to the saved indices
    :type prefix: string
    :param show_flag: flag
    :type show_flag: bool
    """
    # get bands relevant to ndvi
    band_dict = band_returner_landsat_7()

    if band_dict:
        # read bands
        band3 = open(band_dict['3'])  # red
        band4 = open(band_dict['4'])  # nir
        red = band3.read(1).astype('float64')
        nir = band4.read(1).astype('float64')

        # calculate ndvi raster image
        ndvi = np.where(
            (nir + red) == 0.,
            0,
            (nir - red) / (nir + red)
        )

        # save ndvi raster image
        ndvi_image = open('./{}_ndvi_landsat_7.tiff'.format(prefix), 'w', driver='GTiff',
                          width=band4.width, height=band4.height,
                          count=1,
                          crs=band4.crs,
                          transform=band4.transform,
                          dtype='float64')
        ndvi_image.write(ndvi, 1)
        ndvi_image.close()

        if show_flag:
            ndvi = open('{}_ndvi_landsat_7.tiff'.format(prefix))
            show(ndvi, cmap='Greens')


def savi_calc_landsat_7(prefix=None, show_flag=False):
    """
    Calculates and saves the Soil Adjusted Vegetation Index (SAVI) raster image
    :param prefix: Prefix to be added to the saved indices
    :type prefix: string
    :param show_flag: flag
    :type show_flag: bool
    """
    # get bands relevant to ndvi
    band_dict = band_returner_landsat_7()

    if band_dict:
        # read bands
        band3 = open(band_dict['3'])  # red
        band4 = open(band_dict['4'])  # nir
        red = band3.read(1).astype('float64')
        nir = band4.read(1).astype('float64')

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
        savi_image = open('./{}_savi_landsat_7.tiff'.format(prefix), 'w', driver='GTiff',
                          width=band4.width, height=band4.height,
                          count=1,
                          crs=band4.crs,
                          transform=band4.transform,
                          dtype='float64')
        savi_image.write(savi, 1)
        savi_image.close()

        if show_flag:
            savi = open('{}_savi_landsat_7.tiff'.format(prefix))
            show(savi, cmap='Greens')


def msavi_calc_landsat_7(prefix=None, show_flag=False):
    """
    Calculates and saves the Modified Soil Adjusted Vegetation Index (MSAVI) raster image
    :param prefix: Prefix to be added to the saved indices
    :type prefix: string
    :param show_flag: flag
    :type show_flag: bool
    """
    # get bands relevant to ndvi
    band_dict = band_returner_landsat_7()

    if band_dict:
        # read bands
        band3 = open(band_dict['4'])  # red
        band4 = open(band_dict['5'])  # nir
        red = band3.read(1).astype('float64')
        nir = band4.read(1).astype('float64')

        # calculate msavi raster image
        msavi = np.where(
            (nir + red) == 0.,
            0,
            (2 * nir + 1 - np.sqrt((2 * nir + 1) ** 2 - 7 * (nir - red))) / 2
        )

        # INSERT CHECKING CONDITION
        msavi[msavi > 1] = 1
        msavi[msavi < -1] = -1

        # save msavi raster image
        msavi_image = open('./{}_msavi_landsat_7.tiff'.format(prefix), 'w', driver='GTiff',
                           width=band4.width, height=band4.height,
                           count=1,
                           crs=band4.crs,
                           transform=band4.transform,
                           dtype='float64')
        msavi_image.write(msavi, 1)
        msavi_image.close()

        if show_flag:
            msavi = open('{}_msavi_landsat_7.tiff'.format(prefix))
            show(msavi, cmap='Greens')


def ndwi_calc_landsat_7(prefix=None, show_flag=False):
    """
    Calculates and saves the Normalised Difference Water Index (NDWI) raster image
    :param prefix: Prefix to be added to the saved indices
    :type prefix: string
    :param show_flag: flag
    :type show_flag: bool
    """
    # get bands relevant to ndvi
    band_dict = band_returner_landsat_7()

    if band_dict:
        # read bands
        band2 = open(band_dict['2'])  # green
        band4 = open(band_dict['4'])  # nir
        green = band2.read(1).astype('float64')
        nir = band4.read(1).astype('float64')

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
        ndwi_image = open('./{}_ndwi_landsat_7.tiff'.format(prefix), 'w', driver='GTiff',
                          width=band4.width, height=band4.height,
                          count=1,
                          crs=band4.crs,
                          transform=band4.transform,
                          dtype='float64')
        ndwi_image.write(ndwi, 1)
        ndwi_image.close()

        if show_flag:
            ndwi = open('{}_ndwi_landsat_7.tiff'.format(prefix))
            show(ndwi, cmap='Greens')


def image_display_landsat_7():
    """
    Displays the images of landsat indices in a folder one at a time
    """
    ndmi = open('ndmi_landsat_7.tiff')
    ndvi = open('ndvi_landsat_7.tiff')
    savi = open('savi_landsat_7.tiff')
    msavi = open('msavi_landsat_7.tiff')
    ndwi = open('ndwi_landsat_7.tiff')
    show(ndmi, cmap='Blues')
    show(ndvi, cmap='Greens')
    show(savi, cmap='Greens')
    show(msavi, cmap='Greens')
    show(ndwi, cmap='BrBG')


def execute_landsat_7(prefix=None, show_individual=False, show_all=False, show_only=False, indices_requested=[False, False, False, True, False]):
    """
    Executes the process of calculation of indices for landsat images

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
            image_display_landsat_7()
            exit()
        if indices_requested[0]==True:
            ndmi_calc_landsat_7(prefix=prefix, show_flag=show_individual)
        if indices_requested[1]==True:
            ndvi_calc_landsat_7(prefix=prefix, show_flag=show_individual)
        if indices_requested[2] == True:
            savi_calc_landsat_7(prefix=prefix, show_flag=show_individual)
        if indices_requested[3] == True:
            msavi_calc_landsat_7(prefix=prefix, show_flag=show_individual)
        if indices_requested[4] == True:
            ndwi_calc_landsat_7(prefix=prefix, show_flag=show_individual)
        if show_all:
            image_display_landsat_7()
    except RuntimeError:
        print('Unable to show images')


def landsat_7_test():
    """
    Test case for the index_calculator_landsat_7.py file
    """
    execute_landsat_7(show_individual=True)
    band_returner_landsat_7(show_list=True)
