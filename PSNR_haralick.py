import numpy as np
import matplotlib.pyplot as plt

# This code makes the figures "Haralick indices Vs PSNR"

title = ['Mars theme', 'Outcrops theme', 'Crops theme', 'Forest theme', 'Urban theme', 'Daily life theme', 'Mixed themes']
folder = ['mars', 'WV_MSI', 'agricole', 'forets', 'urbain', 'general', 'mix']
indices = ['Angular Second Moment', 'Contrast', 'Correlation', 'Variance', 'Inverse Difference Moment', 'Sum Average', 'Sum Variance', 'Sum Entropy', 'Entropy']
colors = ['coral', 'saddlebrown', 'darkgoldenrod', 'forestgreen', 'grey', 'dodgerblue', 'crimson']
psnr = np.loadtxt(r'E:\myriam\super_resolution\letter\figures/psnr_moy.txt')
for i in range(len(indices)):
    har = np.loadtxt(r'E:\myriam\super_resolution\letter\figures/list_' + str(indices[i]) + '.txt')
    print(har.shape)
    counter = 0
    for j in range(6):
        plt.scatter(har[0, j], psnr[0, j], color=colors[j], label=title[j])
        plt.errorbar(har[0, j], psnr[0, j], xerr=har[1, j], yerr=psnr[1, j], fmt='*', color=colors[j],
                     ecolor=colors[j], ms=8,
                     elinewidth=1, capsize=5, capthick=1)
        if counter == 0:
            plt.legend(loc='best', shadow=True, fontsize=10)
    plt.title('PSNR Vs '+ str(indices[i]), {'fontname': 'Times New Roman'}, fontsize=22)
    plt.xlabel(str(indices[i]), {'fontname': 'Times New Roman'}, fontsize=16)
    plt.ylabel("PSNR values", {'fontname': 'Times New Roman'}, fontsize=16)
    plt.savefig(r'E:\myriam\super_resolution\letter\figures/psnr_vs_' + str(indices[i]) + '.png')
    plt.close()
    #plt.show()