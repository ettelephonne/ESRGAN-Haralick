import os
import cv2
import numpy as np

# Computes the difference between the original image and the faked one. Good for the reconstruction error visualization

datasets = ['mars', 'WV_MSI', 'agricole', 'urbain', 'forets']
moy = np.zeros(65)
min = 255

for i in range(len(datasets)):
    print('thématique en cours : ', datasets[i])
    input_path_hr = r'E:\myriam\super_resolution\dataset' + '/' + datasets[i] + '/test/hr'
    list_hr = os.listdir(input_path_hr)
    input_path_fake = r'E:\myriam\super_resolution\dataset' + '/' + datasets[i] + '/' + datasets[i] + '_results' + '/' + datasets[i] + '_results_4800'
    list_fake = os.listdir(input_path_fake)
    count = -1
    for img in enumerate(list_hr):
        count += 1
        #print(count)
        image_hr = cv2.imread(input_path_hr + '/' + img[1])
        gray_hr = cv2.cvtColor(image_hr, cv2.COLOR_BGR2GRAY).astype(float)
        #gray_hr = (gray_hr - np.min(gray_hr)) / np.max(gray_hr)
        image_fake = cv2.imread(input_path_fake + '/' + img[1].replace('.tif', '') + '_' + datasets[i] + '_4800.tif')
        gray_fake = cv2.cvtColor(image_fake, cv2.COLOR_BGR2GRAY).astype(float)
        #gray_fake = gray_fake / np.max(gray_fake)
        #diff = ((gray_hr - gray_fake) * 255).astype(int)
        diff = abs(gray_hr - gray_fake)
        #diff = image_hr[:, :, 0] - image_fake[:, :, 0]
        #diff = diff - np.min(diff)
        #print(np.min(diff))
        moy[count] = np.mean(diff)
        #if np.min(diff) < min:
        #    min = np.min(diff)
        #plt.imshow(diff)
        #plt.colorbar()
        #cv2.imwrite(r'E:\myriam\super_resolution\dataset' + '/' + datasets[i] + '/difference' + '/' + img[1], diff)
        #plt.savefig(r'E:\myriam\super_resolution\dataset' + '/' + datasets[i] + '/difference' + '/' + img[1].replace('.tif', '.png'))
        #plt.close()
    print('Moyenne des erreurs absolues dans le dataset : ', np.mean(moy))
    #plt.show()

'''for i in range(len(datasets)):
    print('thématique en cours : ', datasets[i])
    input_path_hr = r'E:\myriam\super_resolution\dataset' + '/' + datasets[i] + '/test/hr'
    list_hr = os.listdir(input_path_hr)
    input_path_fake = r'E:\myriam\super_resolution\dataset' + '/' + datasets[i] + '/' + datasets[i] + '_results' + '/' + datasets[i] + '_results_4800'
    list_fake = os.listdir(input_path_fake)
    count = -1
    for img in enumerate(list_hr):
        count += 1
        #print(count)
        image_hr = cv2.imread(input_path_hr + '/' + img[1])
        gray_hr = cv2.cvtColor(image_hr, cv2.COLOR_BGR2GRAY)
        image_fake = cv2.imread(input_path_fake + '/' + img[1].replace('.tif', '') + '_' + datasets[i] + '_4800.tif')
        gray_fake = cv2.cvtColor(image_fake, cv2.COLOR_BGR2GRAY)
        diff = gray_fake - gray_hr
        #diff = image_hr[:, :, 0] - image_fake[:, :, 0]
        diff = diff - np.min(diff)
        #diff = diff / max
        print(np.max(diff))
        plt.imshow(diff)
    plt.colorbar()
    plt.show()'''