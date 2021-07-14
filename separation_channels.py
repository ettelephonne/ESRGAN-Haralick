import gdal
import numpy as np
import os

# This code separates the channels by group of three bands

def creategeotiff(path, path_2, data):
    raster = gdal.Open(path)
    geotransform = raster.GetGeoTransform()
    projection = raster.GetProjection()
    driver = gdal.GetDriverByName('GTiff')
    no_bands, rows, cols, = data.shape
    DataSet = driver.Create(path_2, cols, rows, no_bands, gdal.GDT_Byte)
    DataSet.SetGeoTransform(geotransform)
    DataSet.SetProjection(projection)
    for i, image in enumerate(data, 1):
        DataSet.GetRasterBand(i).WriteArray(image)
    DataSet.FlushCache()

in_path = r"E:\projet_myriam\super_resolution\images_8_bits"
list_bloc = os.listdir(in_path)

out_path_VIS = r"E:\projet_myriam\super_resolution\VIS"
out_path_VIS_NIR = r"E:\projet_myriam\super_resolution\VIS_NIR"
out_path_NIR = r"E:\projet_myriam\super_resolution\NIR"
out_path_MIX = r"E:\projet_myriam\super_resolution\MIX"

for bloc in list_bloc:
    if 'tif' in bloc:
        print(bloc)
        raster = gdal.Open(in_path+'/'+bloc)
        cols = raster.RasterXSize
        rows = raster.RasterYSize
        Nband = raster.RasterCount
        M = raster.ReadAsArray()
        MIX = np.zeros((3, rows, cols))
        VIS = M[0:3, :, :]
        VIS_NIR = M[3:6, :, :]
        NIR = M[5:8, :, :]
        MIX[0, :, :] = M[6, :, :]
        MIX[1, :, :] = M[4, :, :]
        MIX[2, :, :] = M[1, :, :]
        print(VIS.shape, VIS_NIR.shape, NIR.shape)

        save_VIS = creategeotiff(in_path+'/'+bloc, out_path_VIS+'/'+bloc, VIS)
        save_VIS_NIR = creategeotiff(in_path + '/' + bloc, out_path_VIS_NIR + '/' + bloc, VIS_NIR)
        save_NIR = creategeotiff(in_path + '/' + bloc, out_path_NIR + '/' + bloc, NIR)
        save_MIX = creategeotiff(in_path + '/' + bloc, out_path_MIX + '/' + bloc, MIX)

