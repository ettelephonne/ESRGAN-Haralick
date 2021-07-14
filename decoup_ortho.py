import os
import gdal
import numpy as np

# Cut the whole image in smaller tiles that will feed the networks

path_hr = r'E:\myriam\super_resolution\WV'
list_hr = os.listdir(path_hr)
path_lr = r'E:\XEOS\foret_inf\hr'
list_lr = os.listdir(path_lr)

out_path_hr = r'E:\myriam\super_resolution\dataset\axel_heiberg\hr_2'
bands = [1, 3, 4]
# recherche du maximum dans toutes les images
maximum = 0
for bloc in enumerate(list_hr):
    if 'tif' in bloc[1]:
        print(bloc[1])
        try:
            raster = gdal.Open(path_hr + '/' + bloc[1])
            projection = raster.GetProjection()
            img = raster.ReadAsArray()
            max = np.max(img)
            print('max : ', max)
            if max > maximum:
                maximum = max
                print('le maximum est : ', maximum)
        except:
            continue
n = 0
for bloc in enumerate(list_hr):
    if 'tif' in bloc[1]:
        n += 1
        print(bloc[1])
        if n/2 == float(int(n/2)):
            try:
                raster = gdal.Open(path_hr + '/' + bloc[1])
                projection = raster.GetProjection()
                img = raster.ReadAsArray()
                img = img[bands, :, :]
                print(img.shape)
                driver = gdal.GetDriverByName('GTiff')
                cols = raster.RasterXSize
                rows = raster.RasterYSize
                Nband = raster.RasterCount
                tile_size_x = 1024
                tile_size_y = 1024

                for i in range(0, rows, int(tile_size_y)):
                    for j in range(0, cols, int(tile_size_x)):
                        print(i, j)
                        tile = img[:, i:i+tile_size_y, j:j+tile_size_x]
                        occurences = np.count_nonzero(tile == 0)
                        nbr_elts = tile.shape[0] * tile.shape[1] * tile.shape[2]
                        ratio = occurences / nbr_elts
                        print('ratio', ratio)
                        if ratio < 0.2:
                            DataSet = driver.Create(
                                out_path_hr + '/tile_' + str(i) + '_' + str(j) + str(bloc[1]),
                                tile_size_y, tile_size_x, 3, gdal.GDT_Byte)
                            for z, image in enumerate(tile, 1):
                                DataSet.GetRasterBand(z).WriteArray(image)
                                print('jecris')
                            DataSet = None
                            raster = None
            except:
                continue
