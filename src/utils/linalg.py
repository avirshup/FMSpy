"""
Linear algebra library routines.
"""

import sys
import numpy as np
import src.dynamics.timings as timings
import src.fmsio.glbl as glbl

def pseudo_inverse(mat):
    """ Modified version of the scipy pinv function. Altered such that
    the the cutoff for singular values can be set to a hard
    value. Note that by default the scipy cutoff of 1e-15*sigma_max is
    taken."""

    dim1, dim2 = mat.shape
    
    invmat = np.zeros((dim1, dim2), dtype=complex)
    cmat=np.conjugate(mat)
    
    # SVD of the overlap matrix
    u, s, vt = np.linalg.svd(cmat, full_matrices=True)

    #print("\n",s,"\n")

    # Condition number
    ns = min(dim1, dim2)
    if s[ns-1] < 1e-90:
        cond = 1e+90
    else:
        cond = s[0]/s[ns-1]

    # Moore-Penrose pseudo-inverse
    if glbl.fms['sinv_thrsh'] == -1.0:
        # set cutoff to machine epsilon * sigma_max
        cutoff = np.finfo(float).eps * np.maximum.reduce(s)
    else:
        cutoff = glbl.fms['sinv_thrsh']
    for i in range(min(dim1, dim2)):
        if s[i] > cutoff:
            s[i] = 1./s[i]
        else:
            s[i] = 0.
    invmat = np.dot(np.transpose(vt), np.multiply(s[:, np.newaxis],
                                                  np.transpose(u)))    

    return invmat, cond
