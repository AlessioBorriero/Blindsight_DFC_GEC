import numpy as np

# Reconstruct full matrix from flattened upper triangle
def utri2mat(utri):
    n = int(-1 + np.sqrt(1 + 8*len(utri))) // 2
    iu1 = np.triu_indices(n)
    ret = np.empty((n, n))
    ret[iu1] = utri
    ret.T[iu1] = utri
    return ret

def mov_av_smooth(x,y,win):
    x_=win
    y_=[]
    while(x_<np.asarray(x).shape[0]):
        y_.append(np.mean(y[x_-win:x_]))
        x_+=1
    return x[win:][::-1], y_[::-1]

def find_the_min(x_,y_, tol):
    y_prev = y_[0]
    y_min = y_prev
    x_min = x_[0]
    for i,y__ in enumerate(y_[1:]):
        if y__+tol<y_prev:
            # print(x_[i])
            y_min = y__
            x_min = x_[i]
        y_prev = y__
    return x_min, y_min

def boool(n, base=4):
    if n-base<=0:
        piera=0
    elif n-base>0:
        piera=1
    return piera