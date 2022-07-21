#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 18 15:50:12 2022

@author: shunyang.wang
"""

import pandas as pd

c18pos = pd.read_csv('./data/C18_pos.inchi')['  InChIKey']

c18pos = set(pd.unique(c18pos))

c18neg = pd.read_csv('./data/C18_neg.inchi')['  InChIKey']

c18neg = set(pd.unique(c18neg))

pfpneg = pd.read_csv('./data/PFP_neg.inchi')['  InChIKey']

pfpneg = set(pd.unique(pfpneg))

pfppos = pd.read_csv('./data/PFP_pos.inchi')['  InChIKey']

pfppos = set(pd.unique(pfppos))
#%%

import matplotlib.pyplot as plt
from matplotlib_venn import venn2




pos = len(c18pos.intersection(pfppos))

neg = len(c18neg.intersection(pfpneg))


# Use the venn2 function
venn2(subsets = (len(c18pos)-pos, len(pfppos)-pos, pos), set_labels = ('C18', 'PFP'))

plt.show()


venn2(subsets = (len(c18neg)-neg, len(pfpneg)-neg, neg), set_labels = ('C18', 'PFP'))

plt.show()

#%%
from venn import venn

dataset_dict = {'c18pos':c18pos,'c18neg':c18neg,'pfppos':pfppos,'pfpneg':pfpneg}
venn(dataset_dict, fontsize=8, legend_loc="upper left")