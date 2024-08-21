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

def do_overlap(intervallo1, intervallo2):
    a, b = intervallo1
    c, d = intervallo2

    # Controlla se gli intervalli si sovrappongono
    return (a <= d and b >= c)


def conf_int_pval(pairs, metric, data, x, hue, conf_level=97.5):
    stats_res = {} # Cohen's D between all pairs
    conf_int = []
    for p in pairs:
        d1 = data.loc[data[hue]==p[0][1]].loc[data[x]==p[0][0]][metric].values
        d2 = data.loc[data[hue]==p[1][1]].loc[data[x]==p[1][0]][metric].values
        inter1 = [np.percentile(d1,100-conf_level), np.percentile(d1,conf_level)]
        inter2 = [np.percentile(d2,100-conf_level), np.percentile(d2,conf_level)]
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

def conf_int_pval_pair(d1, d2, conf_level=97.5):
    inter1 = [np.percentile(d1,100-conf_level), np.percentile(d1,conf_level)]
    inter2 = [np.percentile(d2,100-conf_level), np.percentile(d2,conf_level)]
    
    conf_int = do_overlap(inter1,inter2)
    if not conf_int:
        new_p = 0.05
    else:
        new_p = 1
    eff_size = cohen(d1,d2)

    return eff_size, new_p