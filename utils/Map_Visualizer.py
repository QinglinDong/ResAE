#from nilearn.datasets import load_mni152_brain_mask
#mask_img = load_mni152_brain_mask()

from nilearn.input_data import NiftiMasker

mask_img ='utils/mask_152_4mm.nii.gz'
masker = NiftiMasker(mask_img=mask_img, standardize=True)
masker.fit()

import numpy as np

def flip(array):
    for row in array:
        if np.sum(row > 0) < np.sum(row < 0):
            row *= -1
    return array

from scipy.stats import scoreatpercentile        
def thresholding(array, T=35):        
#     array -= array.mean(axis=0)
#     array /= array.std(axis=0)
    for idx,component in enumerate(array):
        abs_maps = np.amax(component)
        threshold=T * abs_maps/100
#         threshold = scoreatpercentile(component,T)
        component[component < threshold] = 0
        array[idx,:]=component
    return array

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from scipy import stats
# X: T *N
# TimeCourse: K * T
# Maps: K * N
def gen_map(TC, X, alpha=0.0005):
    if alpha==0:
        clf = LinearRegression()
        clf.fit(TC,X)
    else:
        clf=Lasso(alpha,tol=0.1,max_iter=100)
        clf.fit(TC,X)
    components=clf.coef_.T
    return components

def gen_TC(maps,X):
    clf = LinearRegression()
    clf.fit(maps.T,X.T)
    TimeCourse=clf.coef_.T
#     TimeCourse=stats.zscore(TimeCourse)
    return TimeCourse
    
from nilearn.plotting import plot_stat_map, show
from nilearn.image import iter_img

def plot_map(components, output_file=None):  
    # input 1 * N
    components_img = masker.inverse_transform(components)
    plot_stat_map(components_img,bg_img='utils/MNI152_T1_1mm.nii.gz', output_file=output_file, display_mode="z", black_bg=True,annotate=False,
                         colorbar=1)

import os     
from nilearn.image import threshold_img
def plot_maps(components, dir):        
    # input k * N
    components_img = masker.inverse_transform(components)
#     components_img = threshold_img(components_img, threshold='97%')
    if not os.path.exists(dir):
        os.makedirs(dir)
    print("Dir created")
        
    for i, cur_img in enumerate(iter_img(components_img)):
        outname=dir+'/'+str(i)+'.png'
        plot_stat_map(cur_img, bg_img='utils/MNI152_T1_1mm.nii.gz',display_mode="z", black_bg=True,annotate=0,
                     colorbar=0,output_file=outname)
#         show()
        

        

    
   # Mosaic(dir,dir+'All.jpg')


import matplotlib.pyplot as plt
def plot_signal(signal):
    t = range(0, len(signal))
    plt.plot(t, signal)
    #plt.savefig(dir + ".png")    
