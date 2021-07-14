import gdal
import numpy as np
import os

# Corrections for WV images

def creategeotiff(path, path_2, data):
    raster = gdal.Open(path)
    geotransform = raster.GetGeoTransform()
    projection = raster.GetProjection()
    driver = gdal.GetDriverByName('GTiff')
    no_bands, rows, cols, = data.shape
    DataSet = driver.Create(path_2, cols, rows, no_bands, gdal.GDT_Float32)
    DataSet.SetGeoTransform(geotransform)
    DataSet.SetProjection(projection)
    for i, image in enumerate(data, 1):
        DataSet.GetRasterBand(i).WriteArray(image)
    DataSet.FlushCache()

in_path = r"E:\projet_myriam\super_resolution/WV_brute"
list_bloc = os.listdir(in_path)
out_path = r"E:\projet_myriam\super_resolution\images"

gain = [0.863, 0.905, 0.907, 0.938, 0.945, 0.98, 0.982, 0.954]
offset = [-7.154, -4.189, -3.287, -1.816, -1.35, -2.617, -3.752, -1.507]
abscal1 = [1.434360e-02, 1.165330e-02, 8.873020e-03, 6.901951e-03, 1.025700e-02, 6.231750e-03, 1.184670e-02, 1.065140e-02]
abscal2 = [1.432870e-02, 1.762010e-02, 1.331870e-02, 6.843070e-03, 1.020000e-02, 6.219960e-03, 1.179710e-02, 1.063780e-02]
effective = [4.050000e-02, 5.400000e-02, 6.180000e-02, 3.810000e-02, 5.850000e-02, 3.870000e-02, 1.004000e-01, 8.890000e-02]
E = [1757.89, 2004.61, 1830.18, 1712.07, 1535.33, 1348.08, 1055.94, 858.77]
teta1 = 90-43.8
teta2 = 90-58.6

for bloc in list_bloc:
    if 'tif' in bloc or 'TIF' in bloc:
        print(bloc)
        raster = gdal.Open(in_path+'/'+bloc)
        cols = raster.RasterXSize
        rows = raster.RasterYSize
        Nband = raster.RasterCount
        M = np.float32(raster.ReadAsArray())
        for i in range(8):
            if 'malartic' in bloc:
                M[i, :, :] = offset[i] + gain[i] * M[i, :, :] * (abscal2[i] / effective[i])
                M[i, :, :] = (M[i, :, :] * np.pi) / (E[i] * np.cos(np.deg2rad(teta2)))
            else:
                M[i, :, :] = offset[i] + gain[i] * M[i, :, :] * (abscal1[i] / effective[i])
                M[i, :, :] = (M[i, :, :] * np.pi) / (E[i] * np.cos(np.deg2rad(teta1)))
        M = np.where(M < 0, 0, M)
        M = np.where(M > 1, 1, M)
        print('minimun = ', np.min(M), 'moyenne = ', np.mean(M), 'maximum = ', np.max(M))

        save_raster = creategeotiff(in_path + '/' + bloc, out_path + '/' + bloc, M)