# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 11:33:17 2022

@author: Study
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib_venn import venn2

import seaborn as sn

clean = pd.read_excel('./June_rt.xlsx',sheet_name='clean')


c18 = set(clean[clean['C18RT'].notnull()].index)
pfp = set(clean[clean['PFPRT'].notnull()].index)

overlap = len(c18.intersection(pfp))

# Use the venn2 function
venn2(subsets = (len(c18)-overlap-2664, len(pfp)-overlap, overlap), set_labels = ('C18', 'PFP'))
plt.show()



for column in ['C18RT','PFPRT']:
    clean2 = clean[clean[column].notnull()]
    dup = clean2['InChIKey'][clean2.duplicated(['InChIKey'],keep=False)]
    dup = dup.unique()
    diff = []
    for key in dup:
        value = clean[column][clean['InChIKey']==key]
        diff.append(value.max() - value.min())
    
    hist = sn.displot(diff,binwidth=0.1)
    hist.set(xlabel=column)
    
    df = pd.DataFrame({'inchikey':dup, 'diff':diff})
    mean = df['diff'].mean()
    break


