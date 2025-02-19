def known_constraints(param, thres=11):
    if float(param["t0"]) + float(param["t1"]) > thres:
        return False
    else:
        return True
