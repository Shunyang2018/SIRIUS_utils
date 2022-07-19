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



path = '/Users/shunyang.wang/Dropbox (Brightseed)/Mac/Downloads/June/C18_Pos/'

wf = []

wf_duplicate = []

inchi = []
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
                    inchi.append(line.split(':')[1])
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
                    
                    wf_tmp.append(line.split(';')[3].strip()+'\n')
                wf_tmp.append(line)
            
           
            
            if dup:
                wf_duplicate += wf_tmp
                wf_duplicate += '\n'
            else:
                wf += wf_tmp
                wf += '\n'
      
with open(path[:-1]+'.inchi','w') as f:
    f.writelines('  InChIKey\n')
    f.writelines(inchi)

with open(path[:-1]+'.msp','w') as f:
    f.writelines(wf)
            
with open(path[:-1]+'_dup.msp','w') as f:
    f.writelines(wf_duplicate)