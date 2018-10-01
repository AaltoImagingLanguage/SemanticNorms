"""
This script extracts different sets of semantic norms (Aalto, CSLB, Vinson, 
Corpus, Questionnaire) and compares them.

@author: kivisas1 (sasa@neuro.hut.fi)
Last update: 30.5.2018
"""
#from scipy.io import loadmat
import pandas
from scipy.spatial.distance import squareform, pdist
from matplotlib import pyplot as plt
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage
from scipy.stats import spearmanr
#from sklearn.decomposition import PCA
#from run_zero_shot import run_zero_shot_leave1out

normpath = '/m/nbe/project/aaltonorms/data/'
#normpath = norms_path + 'data/norm_overlap/'

#Directory for the figures to be created
#figure_dir = norms_path + 'figures/'

#These are the files for different norm sets
#filenames = ['cslb_aaltoOverlap', 'vinson_aaltoOverlap', 'aalto85_aaltoOverlap',
#'ginter_aaltoOverlap', 'cmu_aaltoOverlap', 'aalto300', 'aalto300_cslbOverlap',
#'aalto300_vinsonOverlap','aalto300_aalto85Overlap', 'aalto300_cmuOverlap', 
#'vinson_ginterOverlap', 'cslb_ginterOverlap', 'ginter_vinsonOverlap', 'ginter_cslbOverlap']

def get_normdata(filename):   
    df = pandas.read_table(normpath + filename + '.csv', encoding='utf-8', 
    header=None, index_col=0)
    return df



cslb = pandas.read_table(normpath + 'cslb/' + 'vectors.csv', encoding='utf-8', 
                         header=None, index_col=None)

vinson = pandas.read_table(normpath + 'vinson/' + 'vectors.csv', encoding='utf-8', 
                         header=None, index_col=None)

cslb_vocab = pandas.read_table(normpath + 'cslb/' + 'vocab.csv', encoding='utf-8', 
                         header=None, index_col=None)

vinson_vocab = pandas.read_table(normpath + 'vinson/' + 'vocab.csv', encoding='utf-8', 
                         header=None, index_col=None)

cslb_corr = cslb_vocab = pandas.read_table(normpath + 'cslb/' + 'correspondence.csv', encoding='utf-8', 
                         header=0, index_col=0)

#Tässä pitäisi etsiä ne sanat, jotka löytyvät myös toisesta normisetistä. Käytä 
#correspondece.csv tiedostoa.
for name in cslb_corr['vinson']:
   # print(name)
    if isinstance(name, str):
        print(name)#print(name)


def get_distances(norms):
    distmat = squareform(pdist(norms, metric="cosine"))
    distmat_full = list(distmat)
    tri = np.tril_indices(norms.shape[0]) #For denoting lower triangular
    distmat[tri] = np.nan
    distvector = np.asarray(distmat.reshape(-1)) #Take upper triangular                                                     #and reshape
    distvector = distvector[~np.isnan(distvector)]
    return distmat_full, distvector





def remove_ticks(ax):
    ax.axes.get_xaxis().set_ticks([])
    ax.axes.get_xaxis().set_ticklabels([])
    ax.axes.get_yaxis().set_ticks([])
    ax.axes.get_yaxis().set_ticklabels([])
    return ax

def make_category_bar(cats):
    plt.figure(figsize=(1,3))    
    ax = plt.imshow(cats, cmap='Paired', interpolation='nearest', extent=[0,5,0,1], aspect=100)
    ax = remove_ticks(ax)
    return ax
    
def compare_norms(A,B, label_A, label_B, cats=None):
    plt.figure(figsize=(10,3))    
    ax1 = plt.subplot(1,2,1)
    plt.title(label_A)
    ax1 = remove_ticks(ax1)
    plt.imshow(get_distances(A)[0], cmap="plasma", interpolation='nearest')
    ax2 = plt.subplot(1,2,2)
    ax2 = remove_ticks(ax2)
    plt.title(label_B)
    plt.imshow(get_distances(B)[0], cmap="plasma", interpolation='nearest')
    plt.clim(0, 1);
    plt.colorbar(ax=[ax1, ax2])
    rho, pval = spearmanr(get_distances(A)[1], get_distances(B)[1])
   
    print(label_A + " vs. " + label_B + "  rho is: " + 
        str(round(rho,2)) + ", pvalue = " + str(round(pval,2)))
    plt.savefig(figure_dir + label_A + label_B + "_production_norm_comparison.pdf", 
                format='pdf', dpi=1000, bbox_inches='tight')
    plt.savefig(figure_dir + label_A + label_B + "_production_norm_comparison.pdf", 
                format='pdf', dpi=1000, bbox_inches='tight')
    plt.close()
   # make_category_bar(cats)
   # plt.savefig(figure_dir + label_A + label_B + "_catcolors.pdf", 
   #             format='pdf', dpi=1000, bbox_inches='tight')
        

def hierarchical_clustering(norms, truncate=True):
    mat = get_distances(norms)[0]
    labels = norms.index.values
    Z = linkage(mat, 'ward')
    plt.figure(figsize=(30, 10))
    if truncate:
        dendrogram(Z, labels=labels, p=5, truncate_mode='level', 
                   orientation='right', leaf_font_size=5)
    else: 
        dendrogram(Z, labels=labels, orientation='right', leaf_font_size=5)


#Make distance matrices
#compare_norms(aalto300_cslbOL, cslb_aaltoOL, "Aalto", "CSLB")
#compare_norms(aalto300_vinsonOL, vinson_aaltoOL, "Aalto", "Vinson")
#compare_norms(aalto300_aalto85OL, aalto85_aaltoOL, "Aalto", "Aalto85")
#compare_norms(aalto300, ginter_aaltoOL, "Aalto", "Ginter")
#compare_norms(aalto300_cmuOL, cmu_aaltoOL, "Aalto", "CMU")
#compare_norms(cslb_ginterOL, ginter_cslbOL, "CSLB", "Ginter")
#compare_norms(vinson_ginterOL, ginter_vinsonOL, "Vinson", "Ginter")

#pca = PCA(n_components=2)
#pca.fit(aalto300.transpose())
#print(pca.explained_variance_ratio_)
#print(pca.singular_values_)
#print(pca.components_)
#a = pca.components_.transpose()
#plt.figure()
#ax = plt.scatter(a[:,0], a[:,1], c=category.tolist())
#plt.colorbar()
#output='/m/nbe/project/aaltonorms/results/zero_shot/aaltoVsCslb.mat'
#run_zero_shot(aalto300_cslbOL, cslb_aaltoOL, output=output, distance_metric='cosine')

#output='/m/nbe/project/aaltonorms/results/zero_shot/aaltoProductionVsGinter.mat'
#run_zero_shot(aalto300, ginter_aaltoOL, output=output, distance_metric='cosine')
#
#output='/m/nbe/project/aaltonorms/results/zero_shot/aaltoProductionVsAalto85.mat'
#run_zero_shot(aalto300_aalto85OL,aalto85_aaltoOL, output=output, distance_metric='cosine')

#hierarchical_clustering(aalto300, truncate=False)