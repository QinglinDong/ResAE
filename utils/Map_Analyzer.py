import numpy as np

#Overlap rate between two maps 
#a, b are 1*N
def MapOverlap( a, b):
    Intersect = np.logical_and(a, b)
    Union=np.logical_or(a, b)
    I=np.count_nonzero(Intersect)
    U=np.count_nonzero(Union)
    return I/U

from sklearn import metrics
#A,B are k1 * N, k2*N
# D is k1*k2
def LayerOverlap(A,B):
    D=[]
    for i,a in enumerate(A):
        D.append([])
        for j,b in enumerate(B):
            score=MapOverlap(a,b)
            if score==1:
                score=0
            D[i].append(score)
    return D

def MapHierach( a, b):
    I = np.count_nonzero(np.logical_and(a, b))
    A=np.count_nonzero(a)
    B=np.count_nonzero(b)
    return I/A

def LayerHierach(A,B):
    D=[]
    for i,a in enumerate(A):
        D.append([])
        print(i)
        for j,b in enumerate(B):
            score=MapHierach(a,b)
            D[i].append(score)
    return D


from nilearn.datasets import load_mni152_brain_mask
from nilearn import image
from nilearn.input_data import NiftiMasker 
# mask_img = load_mni152_brain_mask()
# masker = NiftiMasker(mask_img=mask_img,standardize=True)
# masker.fit()

def load_maps(file):
    GLM=image.load_img(file)
    maps_GLM=masker.transform(GLM)
    maps_GLM[maps_GLM<0]=0
    return maps_GLM

def plot_maps(components_img,dir):        
    if not os.path.exists(dir):
        os.makedirs(dir)
    
    for i, cur_img in enumerate(iter_img(components_img)):
        outname=dir+str(i)+'.png'
        plot_stat_map(cur_img, display_mode="z", black_bg=True,cut_coords=10,
                     colorbar=True,output_file=outname,title="Cope %d" % int(i+1))   
        
import matplotlib.pyplot as plt
import seaborn as sns
def plot_clustermap(D,file):
    mask = np.zeros_like(D, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    plt.figure()
    sns_plot=sns.clustermap(D,cmap="Reds")
    plt.savefig(file, bbox_inches='tight')
    
def plot_GLM_Overlap(D):
    plt.figure(figsize=(15,3))
    plt.ylim(1, 7)
    plt.xlim(1, 101)
    sns_plot=sns.heatmap(D,cmap="Reds",vmax=1,xticklabels=5, yticklabels=1)
    plt.show()
#     plt.savefig(file, bbox_inches='tight')  
     
           