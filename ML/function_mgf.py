#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  1 12:51:09 2022

@author: shunyang.wang
"""

def rdmsp(lines):
    block = []
    for line in lines:
        if len(line)==1:
            yield block
            block = []
        else:
            block.append(line)
            
def wmgf(path,file):
    msp = path+'/'+file
    mgf = path + '/' + file.replace('msp','mgf')
    print(f'reading msp: {file} ...' )
    with open(msp,'r') as f:
        tmp = f.readlines()
        f.close()
    
    print(f'writing mgf: {mgf} ...')
    with open(mgf, 'w') as f:
        i = 0
        name = []
        inchikey = []
        for block in rdmsp(tmp):
            f.writelines('BEGIN IONS\n')
            MS = False
            
            
            for line in block:
                if not MS:
                    if 'Comment' in line:
                        pass
                    else:
                        linea, lineb = line.split(':')
                        if linea == 'PRECURSORMZ':
                            f.writelines('PEPMASS='+lineb)
                        elif linea == 'Precursor_type':
                            f.writelines('Ionization='+lineb)
                        elif linea == 'Name':
                            i +=1
                            name.append(lineb)
                            f.writelines('NAME='+str(i)+'\n')
                        elif linea == 'InChIKey':
                            inchikey.append(lineb)
                        elif linea =='Ion_mode':
                            if 'P' in lineb:
                                f.writelines('CHARGE=1+\n')
                            else:
                                f.writelines('CHARGE=1-\n')        
                        elif linea == 'Num Peaks':
                            MS = True
                        # else:
                        #     f.writelines(linea+'='+lineb)
                else:
                    f.writelines(line)
            f.writelines('END IONS \n\n')
            
    return name, inchikey      
  
def wms(path, file):
    msp = path+'/'+file
    ms = path + '/' + file.replace('msp','ms')
    print(f'reading msp: {file} ...' )
    with open(msp,'r') as f:
        tmp = f.readlines()
        f.close()
    
    print(f'writing ms: {ms} ...')
    with open(ms, 'w') as f:
        name = []
        inchikey = []
        i=0
        for block in rdmsp(tmp):

            MS = False

            for line in block:
                if not MS:
                    if 'Comment' in line:
                        pass
                    else:
                        linea, lineb = line.split(':')
                        if linea == 'PRECURSORMZ':
                            f.writelines('>parentmass'+lineb)
                        elif linea == 'Name':
                            i +=1
                            name.append(lineb)
                            f.writelines('>compound'+str(i)+'\n')
                        elif linea == 'InChIKey':
                            inchikey.append(lineb)
                        elif linea == 'Formula':
                            f.writelines('>formula'+ lineb)
                        elif linea == 'Precursor_type':
                            f.writelines('>ionization' + lineb)
                        elif linea == 'Num Peaks':
                            MS = True
                            f.writelines('\n>ms2\n')
                        
                else:
                    f.writelines(line)

    return name, inchikey     
        
