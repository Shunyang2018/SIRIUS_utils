# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os 
import sys 
import numpy as np
import pandas as pd
from function_mgf import *


    
sys.argv = ['./METASCI/']

if len(sys.argv) <1:
    print('ERROR \n Usage: python msp2mgf.py <directory containing msp> <mgf or ms>')
    raise Exception('Missing input option, stop...')
elif len(sys.argv)==1:
    sys.argv.append('mgf')
    
    
    
path = sys.argv[0]
    
    
for file in os.listdir(path):
    if file.endswith('.msp'):
        if sys.argv[1] == 'mgf':
            name, inchikey = wmgf(path, file)
        else:
            name, inchikey = wms(path, file)
        
        csv = path + '/' + file.replace('msp','csv')
        print(f'writing csv to safe the identifiers...\n for data safety, all identifiers are removeding from mgf files')     
        with open(csv,'w') as f:
            f.writelines('Index;Name;InChIKey\n')
            
            for i in range(len(name)):
                f.writelines(str(i+1)+';')
                f.writelines(name[i].strip() + ';')
                f.writelines(inchikey[i].strip() + '\n')
    
        break              
                

