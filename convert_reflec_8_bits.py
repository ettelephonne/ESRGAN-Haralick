import gdal
import numpy as np
import os

# Reflectance images range from 0 to 1
# Multiply by 255 (integers type) to work on 8 bits
# The maximum spectral resolution loss is 0.4 %. It is acceptable.

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

in_path = r"E:\projet_myriam\super_resolution\images_reflec"
list_bloc = os.listdir(in_path)
out_path = r"E:\projet_myriam\super_resolution\images_8_bits"

for bloc in list_bloc:
    if 'tif' in bloc or 'TIF' in bloc:
        print(bloc)
        raster = gdal.Open(in_path+'/'+bloc)
        cols = raster.RasterXSize
        rows = raster.RasterYSize
        Nband = raster.RasterCount
        M = raster.ReadAsArray()
        S = M.shape
        print(S)

        M = np.where(M < 0, 0, M)
        M = np.where(M > 1, 1, M)

        M = M * 255

        save1 = creategeotiff(in_path+'/'+bloc, out_path+'/'+bloc.replace('.tif', '')+'_8_bits.tif', M)
