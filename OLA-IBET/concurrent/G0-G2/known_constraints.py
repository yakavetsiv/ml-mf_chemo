#!/usr/bin/env python3
import numpy as np
from utils import norm_data_inverse, cell_viability

def known_constraints(param, thres=0.3):
    """
    Implementing a constraint on the CV space
    """

	# fitting parameters
    fit_params = {'drug': ['ola', 'ibet762'],
         'fit': [[0.34, 1.53, 123],
              [0.35, 3.42, 468]],
         'bounds': [[10, 1000], [0.01, 300]],
         'stock': [1000, 500]}

    param_inverse = norm_data_inverse(param, fit_params['bounds'])
    cv_exp = cell_viability(param_inverse['conc0'], param_inverse['conc1'], fit_params['fit'][0], fit_params['fit'][1])

    if cv_exp > thres:
        return True
    else:
        return False
