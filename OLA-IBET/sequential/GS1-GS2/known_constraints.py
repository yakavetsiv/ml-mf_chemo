#!/usr/bin/env python3
import numpy as np

def known_constraints_chrono(param, thres=12):
    """
    Implementing a constraint on the CV space
    """

    if (int(param['t0']) >= thres) & (int(param['t0']) <= 48-thres) :
        return True
    else:
        return False
