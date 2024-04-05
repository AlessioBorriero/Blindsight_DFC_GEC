import numpy as np
import pandas as pd

# check values for stats in Cohen's d

def cohen(x,y):
    d = (np.mean(x) - np.mean(y))/(np.sqrt((np.std(x)**2 + np.std(y)**2)/2))
    return d

def annotate_D(pairs, metric, data):
    thr_low = 1.5
    thr_high = 2
    stats_res = {} # Cohen's D between all pairs
    cohen_vals = []
    for p in pairs:
        n1 = data[data['state']==p[0][0]][data['groups']==p[0][1]][metric].values
        n2 = data[data['state']==p[1][0]][data['groups']==p[1][1]][metric].values
        cohen_vals.append(cohen(n1,n2))

    stats_res['Effect Size'] = cohen_vals

    new_p = []
    
    for es in enumerate(stats_res['Effect Size']):
        if abs(es[1]) >= thr_high:
            new_p.append(0.01)
        elif abs(es[1]) >= thr_low:
            new_p.append(0.05)
        else:
            new_p.append(1)

    stats_res['p_val'] = new_p
    
    return stats_res['p_val']



def conf_int_pval(pairs, metric, data):
    stats_res = {} # Cohen's D between all pairs
    conf_int = []
    for p in pairs:
        d1 = data.loc[data['groups']==p[0][1]].loc[data['state']==p[0][0]][metric].values
        d2 = data.loc[data['groups']==p[1][1]].loc[data['state']==p[1][0]][metric].values
        inter1 = [np.percentile(d1,2.5), np.percentile(d1,97.5)]
        inter2 = [np.percentile(d2,2.5), np.percentile(d2,97.5)]
        conf_int.append(do_overlap(inter1,inter2))

    stats_res['Effect Size'] = conf_int

    new_p = []
    
    for es in enumerate(stats_res['Effect Size']):
        if not es[1]:
            new_p.append(0.05)
        else:
            new_p.append(1)

    stats_res['p_val'] = new_p
    
    return stats_res['p_val']