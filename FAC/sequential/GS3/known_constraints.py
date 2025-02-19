def known_constraints(param, thres=23):
    if float(param["t0"]) + float(param["t1"]) > thres:
        return False
    else:
        return True
