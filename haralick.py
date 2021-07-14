import mahotas as mt
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import random
from math import log10, sqrt

# This code  computes some Haralick texture indices and builds the associated figure

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

def extract_features(image):
	# calculate haralick texture features for 4 types of adjacency
	textures = mt.features.haralick(image)

	# take the mean of it and return it
	ht_mean  = textures.mean(axis=0)
	return ht_mean
indices = ['Angular Second Moment', 'Contrast', 'Correlation', 'Variance', 'Inverse Difference Moment', 'Sum Average', 'Sum Variance', 'Sum Entropy', 'Entropy']
datasets = ['mars', 'WV_MSI', 'agricole', 'forets', 'urbain', 'general', 'mix']
names = ['Mars theme', 'Outcrops theme', 'Crops theme', 'Forest theme', 'Urban theme', 'Daily life theme', 'Mixed themes']
colors = ['coral', 'saddlebrown', 'darkgoldenrod', 'forestgreen', 'grey', 'dodgerblue', 'crimson']
nbr_img = 20
corr = np.zeros((7, nbr_img))
mean_corr = np.zeros(7)
err_corr = np.zeros(7)
ent = np.zeros((7, nbr_img))
err_ent = np.zeros(7)
mean_ent = np.zeros(7)
features_lr = np.zeros((7, nbr_img, 9))
features_hr = np.zeros((7, nbr_img, 9))

for i in range(len(datasets)):
    print('thématique en cours : ', datasets[i])
    input_path_lr = r'E:\myriam\super_resolution\dataset' + '/' + str(datasets[i] + '/test/lr')
    list_lr = os.listdir(input_path_lr)
    list_rand = random.sample(list_lr, k=nbr_img)
    input_path_hr = r'E:\myriam\super_resolution\dataset' + '/' + str(datasets[i] + '/test/hr')
    list_hr = os.listdir(input_path_hr)
    count = -1
    j = -1
    for img in enumerate(list_rand):
        count += 1
        if count < 30:
            j += 1
            image_lr = cv2.imread(input_path_lr + '/' + img[1])
            gray_lr = cv2.cvtColor(image_lr, cv2.COLOR_BGR2GRAY)
            h_lr = extract_features(gray_lr)[0:9]
            #h_lr = h_lr - np.min(h_lr)
            #h_lr = h_lr / np.max(h_lr)
            image_hr = cv2.imread(input_path_hr + '/' + img[1])
            gray_hr = cv2.cvtColor(image_hr, cv2.COLOR_BGR2GRAY)
            #plt.imshow(gray_hr)
            #plt.show()
            #cv2.imshow(datasets[i] + '_' + str(count), gray_hr)
            #cv2.waitKey()
            h_hr = extract_features(gray_hr)[0:9]
            #h_hr = h_hr - np.min(h_hr)
            #h_hr = h_hr / np.max(h_hr)
            r_h = h_lr / h_hr
            corr[i, j] = r_h[4]
            ent[i, j] = r_h[2]
            features_lr[i, j, :] = h_lr
            features_hr[i, j, :] = h_hr
    cv2.destroyAllWindows()
for k in range(features_hr.shape[2]):
    list_values = []
    list_std_values = []
    for l in range(features_hr.shape[0]-1):
        mean_lr = np.mean(features_lr[l, :, k])
        mean_hr = np.mean(features_hr[l, :, k])
        list_values.append(mean_hr)
        err_lr = np.std(features_lr[l, :, k])
        err_hr = np.std(features_hr[l, :, k])
        list_std_values.append(err_hr)
        plt.scatter(features_lr[l, :, k], features_hr[l, :, k], color=colors[l], s=4, label=names[l])
        plt.errorbar(mean_lr, mean_hr, xerr=err_lr, yerr=err_hr, fmt='*', color=colors[l],
                     ecolor=colors[l], ms=8,
                     elinewidth=1, capsize=5, capthick=1)

            #ax = plt.gca()
            #plt.scatter(h_hr, h_lr, color=colors[j])
    np.savetxt(r'E:\myriam\super_resolution\letter\figures/list_' + str(indices[k]) +  '.txt', np.asarray([list_values, list_std_values]))
    plt.xlabel("Values for the downscaled images", {'fontname': 'Times New Roman'}, fontsize=16)
    plt.ylabel("Values for the original images", {'fontname': 'Times New Roman'}, fontsize=16)
    plt.legend(loc='best', shadow=True, fontsize=10)
    plt.title(indices[k], {'fontname': 'Times New Roman'}, fontsize=16)
    plt.savefig(r'E:\myriam\super_resolution\letter\figures' + '/' + indices[k] + '.png')
    #plt.show()
    plt.close()
for i in range(features_hr.shape[0]-1):
    plt.scatter(features_hr[i, :, 4], features_hr[i, :, 8], color=colors[i], s=4, label=names[i])
    plt.errorbar(np.mean(features_hr[i, :, 4]), np.mean(features_hr[i, :, 8]),
                 xerr=np.std(features_hr[i, :, 4]), yerr=np.std(features_hr[i, :, 8]), fmt='*', color=colors[i],
                 ecolor=colors[i], ms=10,
                 elinewidth=1, capsize=5, capthick=1)
plt.xlabel("Inverse Difference values", {'fontname': 'Times New Roman'}, fontsize=16)
plt.ylabel("Entropy values", {'fontname': 'Times New Roman'}, fontsize=16)
plt.legend(loc='best', shadow=True, fontsize=10)
plt.title('Inverse Difference Vs Entropy (original images)', {'fontname': 'Times New Roman'}, fontsize=16)
plt.savefig(r'E:\myriam\super_resolution\letter\figures/Inverse Difference Vs Entropy.png')
#plt.show()
plt.close()
for i in range(features_lr.shape[0]-1):
    plt.scatter(features_lr[i, :, 4], features_lr[i, :, 8], color=colors[i], s=4, label=names[i])
    plt.errorbar(np.mean(features_lr[i, :, 4]), np.mean(features_lr[i, :, 8]),
                 xerr=np.std(features_lr[i, :, 4]), yerr=np.std(features_lr[i, :, 8]), fmt='*', color=colors[i],
                 ecolor=colors[i], ms=10,
                 elinewidth=1, capsize=5, capthick=1)
plt.xlabel("Inverse Difference values", {'fontname': 'Times New Roman'}, fontsize=16)
plt.ylabel("Entropy values", {'fontname': 'Times New Roman'}, fontsize=16)
plt.legend(loc='best', shadow=True, fontsize=10)
plt.title('Inverse Difference Vs Entropy (downscaled images)', {'fontname': 'Times New Roman'}, fontsize=16)
plt.savefig(r'E:\myriam\super_resolution\letter\figures/Inverse Difference Vs Entropy_lr.png')
plt.close()
for i in range(features_lr.shape[0]-1):
    plt.scatter(features_hr[i, :, 1], features_hr[i, :, 8], color=colors[i], s=4, label=names[i])
    plt.errorbar(np.mean(features_hr[i, :, 1]), np.mean(features_hr[i, :, 8]),
                 xerr=np.std(features_hr[i, :, 1]), yerr=np.std(features_hr[i, :, 8]), fmt='*', color=colors[i],
                 ecolor=colors[i], ms=10,
                 elinewidth=1, capsize=5, capthick=1)
plt.xlabel("Contrast values", {'fontname': 'Times New Roman'}, fontsize=16)
plt.ylabel("Entropy values", {'fontname': 'Times New Roman'}, fontsize=16)
plt.legend(loc='best', shadow=True, fontsize=10)
plt.title('Contrast Vs Entropy (original images)', {'fontname': 'Times New Roman'}, fontsize=16)
plt.savefig(r'E:\myriam\super_resolution\letter\figures/Contrast Vs Entropy_hr.png')
plt.close()
for i in range(features_lr.shape[0]-1):
    plt.scatter(features_hr[i, :, 3], features_hr[i, :, 4], color=colors[i], s=4, label=names[i])
    plt.errorbar(np.mean(features_hr[i, :, 3]), np.mean(features_hr[i, :, 4]),
                 xerr=np.std(features_hr[i, :, 3]), yerr=np.std(features_hr[i, :, 4]), fmt='*', color=colors[i],
                 ecolor=colors[i], ms=10,
                 elinewidth=1, capsize=5, capthick=1)
plt.xlabel("Variance values", {'fontname': 'Times New Roman'}, fontsize=16)
#plt.semilogx()
plt.ylabel("Inverse difference values", {'fontname': 'Times New Roman'}, fontsize=16)
plt.legend(loc='best', shadow=True, fontsize=10)
plt.title('Variance Vs Inverse Difference (original images)', {'fontname': 'Times New Roman'}, fontsize=16)
plt.savefig(r'E:\myriam\super_resolution\letter\figures/Variance Vs Inverse_hr.png')
#plt.show()

