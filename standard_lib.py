#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 14:09:48 2022

@author: shunyang.wang
"""

import os 
import sys 
import numpy as np
import pandas as pd
from function_mgf import *


files = ['C18Pos','C18Neg','PFPPos','PFPNeg']
dfs = pd.DataFrame()
for filename in files:
    path = '/Users/shunyang.wang/Dropbox (Brightseed)/Mac/Downloads/RESULTS/July/'+filename+'/'
    
    wf = []
    
    wf_duplicate = []
    rt = []
    mz = []
    add = []
    inchi = []
    name = []
    for file in os.listdir(path):
        wf_old = [0]
        if file.endswith('.msp'):
            with open(path + file,'r', encoding="ISO-8859-1") as f:
                tmp = f.readlines()
            f.close()
            for block in rdmsp(tmp):
                wf_tmp = []
                dup = False
                for line in block:    
                    if 'InChIKey' in line:
                        inchi.append(line.split(':')[1].strip())
                    if 'PRECURSORMZ' in line:
                        mz.append(line.split(':')[1].strip())
                    if 'Precursor_type' in line:
                        add.append(line.split(':')[1].strip())
                    if 'Name' in line:
                        name.append(line.split(':')[1].strip())    
                    if 'Comment' in line: 
                        # print('tmp',wf_tmp)
                        # print('old',wf_old)
                        if wf_old == wf_tmp:
                            print('found duplicates')
                            dup = True   
                        # print('tmp2',wf_tmp)
                        # print('old2',wf_old)
                        wf_old = wf_tmp.copy()# do not use =!!!
                        # print('old3',wf_old)
                        
                        # print(dup)
                        rttmp = line.split(';')[3].strip()
                        wf_tmp.append(rttmp+'\n')
                        rt.append(rttmp.split(' ')[1])
                        
                    wf_tmp.append(line)
                
               
                
                if dup:
                    wf_duplicate += wf_tmp
                    wf_duplicate += '\n'
                else:
                    wf += wf_tmp
                    wf += '\n'
    allist = []
    for i in range(len(add)):
        allist.append(name[2*i]+'_'+add[i]+'_'+inchi[i])
    # df = pd.DataFrame({'mz':mz,'rt':rt,'add':add,'inchikey':inchi})    
    df = pd.DataFrame({'Compound':allist,'mz':mz,'rt':rt})   
    df = df.drop_duplicates()
    dfs = pd.concat([dfs,df])
    df.to_csv(path[:-1]+'.csv',index=False)   
    
# with open(path[:-1]+'.inchi','w') as f:
#     f.writelines('  InChIKey\n')
#     f.writelines(inchi)

# with open(path[:-1]+'.msp','w') as f:
#     f.writelines(wf)
            
# with open(path[:-1]+'_dup.msp','w') as f:
#     f.writelines(wf_duplicate)