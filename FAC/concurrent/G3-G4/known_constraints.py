#!/usr/bin/env python3
import numpy as np
from utils import norm_data_inverse, cell_viability, conc_total

def known_constraints(param, thres1=0.5, thres2=0.33):
    """
    Implementing a constraint on the CV space
    """

	# fitting parameters
    fit_params = {'drug': ['dox', 'cpa', '5-fu'],
         'fit': [[0.32, 1.38, 2.365536973],
              [0.020, 1.846, 13834.082806413],
              [0.3, 0.842, 2732.790887234]],
         'bounds': [[0.1, 100], [10, 200000], [10, 10000]],
         'stock': [10, 20000, 3000]}

    param_inverse = norm_data_inverse(param, fit_params['bounds'])
    cv_exp = cell_viability(param_inverse['conc0'], param_inverse['conc1'], param_inverse['conc2'], fit_params['fit'][0], fit_params['fit'][1], fit_params['fit'][2])

    conc = conc_total(param['conc0'], param['conc1'], param['conc2'])/1.73


    if (conc < thres2):
        return True
    else:
        return False

