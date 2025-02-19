#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 12 20:33:41 2021

@author: viprorok
"""

import numpy as np


def hill(c, e1, h, ec):
    return 1+np.divide(e1-1,np.power(np.divide(ec,c),h)+1) 


def norm_conc_inverse(x, norm_bounds):
    norm_bounds_log = np.log10(norm_bounds)
    x_inverse = (x*(max(norm_bounds_log) - min(norm_bounds_log)))+min(norm_bounds_log)
    x_scaled = np.power(10,x_inverse)
    return x_scaled

#Calculation of CVtheor (concentrations )
def cell_viability(x, y, fit_x, fit_y):
        
    cv_x = hill(x, fit_x[0], fit_x[1], fit_x[2])
    cv_y = hill(y, fit_y[0], fit_y[1], fit_y[2])
   
    cv = cv_x*cv_y
    return cv 

def norm_data_inverse(data_raw,bounds):
    data_inv = data_raw.copy()
    data_inv['conc0'] = norm_conc_inverse(data_raw['conc0'],bounds[0])
    data_inv['conc1'] = norm_conc_inverse(data_raw['conc1'],bounds[1])
    return data_inv
 