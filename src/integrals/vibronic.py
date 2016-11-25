"""
Compute integrals over trajectories traveling on vibronic potentials
"""
import numpy as np


# Let propagator know if we need data at centroids to propagate
require_centroids = False

# Determines the basis set
basis = 'gaussian'

# Determines the Hamiltonian symmetry
hamsym = 'hermitian'

def v_integral(traj1, traj2=None, centroid=None):
    """Returns potential coupling matrix element between two trajectories.

    This will depend on how the operator is stored, and
    what type of coordinates are employed, etc.
    """
    pass


def prim_v_integral(n, p1, p2):
    """Returns the matrix element <cmplx_gaus(q,p)| q^N |cmplx_gaus(q,p)>

    Takes the arguments as particles.
    """
    n_2 = np.floor(0.5 * n)
    a   = p1.width + p2.width
    b   = np.fromiter((complex(2.*(p1.width*p1.x[i] + p2.width*p2.x[i]),
                               -(p1.p[i]-p2.p[i])) for i in range(p1.dim)),
                      dtype=complex)

    # generally these should be 1D harmonic oscillators. If
    # multi-dimensional, the final result is a direct product of
    # each dimension
    v_total  = complex(1.,0.)
    for d in range(p1.dim):
        v = complex(0.,0.)
        for i in range(n_2):
            v = (v + a**(i-N) * b**(N-2*i) /
                 (np.math.factorial(i) * np.math.factorial(N-2*i)))
        v_total = v_total * v

    # refer to appendix for derivation of these relations
    return v_total * np.math.factorial(N) / 2.**N


def ke_integral(traj1, traj2):
    """Returns kinetic energy integral over trajectories."""
    ke = complex(0.,0.)
    if traj1.state == traj2.state:
        for i in range(traj1.nparticles):
            ke = (ke - traj1.particles[i].deld2x(traj2.particles[i]) /
                  (2.*traj1.particles[i].mass))
        return ke * traj1.h_overlap(traj2)
    else:
        return ke


def sdot_integral(traj1, traj2):
    """Returns the matrix element <Psi_1 | d/dt | Psi_2>."""
    sdot = (-np.dot( traj2.velocity(), traj1.deldx(traj2) ) +
            np.dot( traj2.force(), traj1.deldp(traj2) ) +
            complex(0.,1.) * traj2.phase_dot() * traj1.h_overlap(traj2))
    return sdot
