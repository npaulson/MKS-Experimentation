import gsh_cub_tri_L0_16 as gsh
import numpy as np


def const():

    """define variables related to the angles"""
    thetamax = 60  # theoretical max theta in degrees
    phi1max = 360  # theoretical max phi1 in degrees
    phimax = 90  # theoretical max Phi in degrees
    phi2max = 60  # theoretical max phi2 in degrees

    inc_eul = 5.0  # degree increment for euler angles
    inc_th = 1.5  # degree increment for deformation mode angle
    n_th = np.int64(thetamax/inc_th)  # number of theta samples for FZ
    n_p1 = np.int64(phi1max/inc_eul)  # number of phi1 samples for FZ
    n_P = np.int64(phimax/inc_eul)  # number of Phi samples for FZ
    n_p2 = np.int64(phi2max/inc_eul)  # number of phi2 samples for FZ

    n_eul = n_p1 * n_P * n_p2  # total number of orientations
    L_th = np.pi/3.  # range of theta in radians

    # domain_eul_sz is the integration domain in radians
    domain_eul_sz = phi1max*phimax*phi2max*(np.pi/180.)**3
    # full_eul_sz is the size of euler space in radians
    full_eul_sz = (2*np.pi)*(np.pi)*(2*np.pi)
    eul_frac = domain_eul_sz/full_eul_sz
    fzsz_eul = 1./(eul_frac*8.*np.pi**2)
    bsz_eul = domain_eul_sz/n_eul
    bsz_th = L_th/n_th

    """define variables related to the total strain"""
    a = 0.00485  # start for en range
    b = 0.00905  # end for en range
    n_en = 14
    L_en = b-a
    bsz_en = L_en/n_en

    """define variables required for integration"""
    n_jobs_Xcalc = 40  # number of jobs submitted for Xcalc
    n_jobs_integrate = 400.  # number of jobs submitted for integration

    LL_p = 16  # gsh truncation level
    indxvec = gsh.gsh_basis_info()
    N_p = np.sum(indxvec[:, 0] <= LL_p)  # number of GSH bases to evaluate
    N_q = 40  # number of cosine bases to evaluate for theta
    N_r = 14  # number of cosine bases to evaluate for en
    N_tuple = [N_p, N_q, N_r]
    cmax = N_p*N_q*N_r

    cdict = {'inc_eul': inc_eul,
             'inc_th': inc_th,
             'n_th': n_th,
             'n_p1': n_p1,
             'n_P': n_P,
             'n_p2': n_p2,
             'n_eul': n_eul,
             'L_th': L_th,
             'fzsz_eul': fzsz_eul,
             'bsz_eul': bsz_eul,
             'bsz_th': bsz_th,
             'a': a,
             'b': b,
             'n_en': n_en,
             'L_en': L_en,
             'bsz_en': bsz_en,
             'n_jobs_Xcalc': n_jobs_Xcalc,
             'n_jobs_integrate': n_jobs_integrate,
             'N_p': N_p,
             'N_q': N_q,
             'N_r': N_r,
             'N_tuple': N_tuple,
             'cmax': cmax}

    return cdict
