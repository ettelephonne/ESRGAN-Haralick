import gdal
import numpy as np
from skimage.metrics import structural_similarity as ssim_ski
from math import log10, sqrt
import os
import pandas

epochs = 2400
def PSNR(original, compressed):
    psnr = np.zeros(3)
    for n in range(original.shape[0]):
        mse = np.mean((original[n, :, :] - compressed[n, :, :]) ** 2)
        if(mse == 0):  # MSE is zero means no noise is present in the signal .
                      # Therefore PSNR have no importance.
            return 100
        max_pixel = 255.0
        psnr[n] = 20 * log10(max_pixel / sqrt(mse))
        #print(psnr)
    psnr = np.mean(psnr)
    return psnr

def SSIM(original, compressed):
    ssim = np.zeros(3)
    for n in range(original.shape[0]):
        ssim[n] = ssim_ski(original[n, :, :], compressed[n, :, :])
        #print(ssim)
    ssim = np.mean(ssim)
    return ssim


#path_hr = r'E:\myriam\super_resolution\dataset\double_super\test_4\lr_2'
path_hr = r'E:\myriam\super_resolution\dataset\double_super\test_2\hr'
#path_fake = r'E:\myriam\super_resolution\dataset\double_super\test_4\fake_2_results'
path_fake = r'E:\myriam\super_resolution\dataset\double_super\test_2\fake_hr_results'
list_hr = os.listdir(path_hr)
list_fake = os.listdir(path_fake)

psnr_list = []
ssim_list = []
for image in enumerate(list_hr):

    img_name = os.path.splitext(os.path.basename(path_fake + '/' + image[1]))[0]
    img_ext = os.path.splitext(os.path.basename(path_fake + '/' + image[1]))[1]
    print(path_hr + '/' + image[1])
    hr = gdal.Open(path_hr + '/' + image[1])
    hr = hr.ReadAsArray()
    #print(hr.shape)
    print(path_fake + '/' + image[1].replace(img_ext, '') + '_fake_hr' + img_ext)
    fake = gdal.Open(path_fake + '/' + image[1].replace(img_ext, '') + '_fake_hr' + img_ext)
    fake = fake.ReadAsArray()
    #print(fake.shape)
    psnr = PSNR(hr, fake)
    #print(psnr)
    ssim = SSIM(hr, fake)

    psnr_list.append(psnr)
    ssim_list.append(ssim)

psnr_moy = np.mean(psnr_list)
ssim_moy = np.mean(ssim_list)
psnr_std = np.std(psnr_list)
ssim_std = np.std(ssim_list)

psnr_list.append(psnr_moy)
ssim_list.append(ssim_moy)
psnr_list.append(psnr_std)
ssim_list.append(ssim_std)

df = pandas.DataFrame(data={"PSNR": psnr_list, "SSIM": ssim_list})
#df.to_csv('E:\myriam\super_resolution\dataset\WV_MSI\indicateurs\indicateurs_WV_' + str(epochs) + '.csv', sep=';', index=False)
df.to_csv('E:\myriam\super_resolution\dataset\double_super/test_2/indicateurs_hr.csv', sep=';', index=False)
