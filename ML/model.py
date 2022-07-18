# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 09:26:02 2022

@author: Study
"""

import pandas as pd
import numpy as np
import random

SEED = 999
np.random.seed(SEED)
random.seed(SEED)

clean = pd.read_excel('./June_rt.xlsx',sheet_name='clean')

clean2 = clean[clean['CanonicalSMILES'].notnull()]

smiles = clean2['CanonicalSMILES']


# calculate infomax fingerprint
from infofunction import smi2infomax,train,split
df = smi2infomax(smiles)

clean_info = pd.concat([clean2, df], axis=1).drop(['order','Source','InChIKey','short'],axis=1)

ratio = 0.8#train ratio

#%% C18 RT

c18 = clean_info.drop(['PFPRT'],axis=1)
c18 = c18[c18['C18RT'].notnull()]
# fingerprint only
c18_info = c18.drop(['XLogP','Fingerprint2D','CanonicalSMILES'],axis=1).reset_index()


length = c18_info.shape[0]


train_index, test_index = split(length,ratio)

y, X = c18_info['C18RT'], c18_info.iloc[:,2:]
name = 'C18RT'
perf = train(y, X, train_index, test_index, name, 'C18')


# XlogP
c18_p = c18.drop(['Fingerprint2D','CanonicalSMILES'],axis=1).reset_index()
y, X = c18_p['C18RT'], c18_p.iloc[:,2:]
perf = train(y, X, train_index, test_index, name, 'C18_p')


#%% PFP RT
pfp = clean_info.drop(['C18RT'],axis=1)
pfp = pfp[pfp['PFPRT'].notnull()]
pfp_info = pfp.drop(['XLogP','Fingerprint2D','CanonicalSMILES'],axis=1).reset_index()
length = pfp_info.shape[0]
train_index, test_index = split(length,ratio)
y, X = pfp_info['PFPRT'], pfp_info.iloc[:,2:]
name = 'PFPRT'
perf = train(y, X, train_index, test_index, name, 'PFP')


#%% descriptors

from rdkit import Chem
from mordred import Calculator, descriptors

def make_descriptors(data, ignore_3D_label = True):
    calc = Calculator(descriptors, ignore_3D = ignore_3D_label)
    mols = [Chem.MolFromSmiles(smi) for smi in data['CanonicalSMILES']]
    df = calc.pandas(mols, quiet = True)
    return(df)
# feature imputing

clean_des = make_descriptors(clean)
# clean_des.to_csv('./descriptors.csv')
clean_des = pd.concat([clean2, clean_des], axis=1).drop(['order','Source','InChIKey','short'],axis=1)

c18 = clean_des.drop(['PFPRT'],axis=1)
c18 = c18[c18['C18RT'].notnull()]
# fingerprint only
c18_des = c18.drop(['XLogP','Fingerprint2D','CanonicalSMILES'],axis=1).reset_index()

length = c18_des.shape[0]

train_index, test_index = split(length,ratio)

y, X = c18_des['C18RT'], c18_des.iloc[:,2:]
name = 'C18RT'
perf = train(y, X, train_index, test_index, name, 'C18_des')


#%%
length = clean.shape[0]
train_index, test_index = split(length,ratio)
clean = clean2.loc[test_index]
c18 = clean.drop(['PFPRT'],axis=1)
c18 = c18[c18['C18RT'].notnull()].iloc[0:100]
c18 = c18.reset_index(drop=True)
clean_des = make_descriptors(c18)
des = pd.concat([c18, clean_des], axis=1).drop(['order','Source','InChIKey','short'],axis=1)

des = des.copy()
from autogluon.tabular import  TabularPredictor
predictor = TabularPredictor.load('C18_des')

imp = predictor.feature_importance(des)

imp.to_csv('imp.csv')

# part des

clean_des = pd.read_csv('./descriptors.csv')
clean_des = clean_des[imp.iloc[0:525].index.tolist()]
clean_des = pd.concat([clean2, clean_des], axis=1).drop(['order','Source','InChIKey','short'],axis=1)

c18 = clean_des.drop(['PFPRT'],axis=1)
c18 = c18[c18['C18RT'].notnull()]
# fingerprint only
c18_des = c18.drop(['XLogP','Fingerprint2D','CanonicalSMILES'],axis=1).reset_index()

length = c18_des.shape[0]

train_index, test_index = split(length,ratio)

y = c18_des['C18RT']
X = c18_des.iloc[:,2:]

name = 'C18RT'
perf = train(y, X, train_index, test_index, name, 'C18_des_part')

#%% GNN + part des

clean_combine = pd.concat([c18_des, c18_info],axis=1)
y = clean_combine['C18RT'].iloc[:,0]
X = clean_combine.iloc[:,2:].drop(['index','C18RT'],axis=1)

name = 'C18RT'
perf = train(y, X, train_index, test_index, name, 'C18_combine')









