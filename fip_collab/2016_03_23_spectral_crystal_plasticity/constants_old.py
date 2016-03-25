import gsh_cub_tri_L0_16 as gsh
import numpy as np


def const():

    C = {}

    """general constants"""
    C['path'] = '/gpfs/pace1/project/me-kalidindi/shared/dir_nhp_test'

    """for read_input_data"""
    C['read_njobs'] = 60
    C['read_mem'] = 8
    C['read_walltime'] = 4
    C['read_scriptname'] = 'read_input_data.py'
    C['read_output'] = 'var_extract_%s.hdf5'

    """for combine_input_data.py"""
    C['combineread_scriptname'] = 'combine_input_data.py'
    C['combineread_output'] = 'var_extract_total.hdf5'

    """for Xcalc_GSH_parallel"""
    C['XcalcGSH_njobs'] = 1
    C['XcalcGSH_nchunks'] = 1
    C['XcalcGSH_mem'] = 4
    C['XcalcGSH_walltime'] = 1
    C['XcalcGSH_scriptname'] = 'Xcalc_GSH_parallel.py'
    C['XcalcGSH_output'] = 'X_parts_GSH_%s.hdf5'

    """for Xcalc_cos"""
    C['Xcalccos_scriptname'] = 'Xcalc_cos.py'
    C['Xcalccos_output'] = 'X_parts_cos.hdf5'

    """for combine_input_data.py"""
    C['combineXcalc_scriptname'] = 'combine_Xcalc.py'
    C['combineXcalc_output'] = 'X_parts.hdf5'

    """for integrate_parallel"""
    C['integrate_njobs'] = 1
    C['integrate_mem'] = 4
    C['integrate_walltime'] = 1
    C['integrate_scriptname'] = 'integrate_parallel.py'
    C['integrate_output'] = 'coef_prt_%s.hdf5'

    """for combine_coef.py"""
    C['combinecoef_scriptname'] = 'combine_coef.py'
    C['combinecoef_coef'] = 'coef.hdf5'
    C['combinecoef_results'] = 'final_results.hdf5'

    """define variables related to the angles"""
    C['thetamax'] = 60  # theoretical max theta in degrees
    C['phi1max'] = 360  # theoretical max phi1 in degrees
    C['phimax'] = 90  # theoretical max Phi in degrees
    C['phi2max'] = 90  # theoretical max phi2 in degrees

    C['inc'] = 10.0  # degree increment for euler angles

    # n_th: number of theta samples for FZ
    C['n_th'] = np.int64(C['thetamax']/C['inc'])
    # n_p1 number of phi1 samples for FZ
    C['n_p1'] = np.int64(C['phi1max']/C['inc'])
    # n_P: number of Phi sample for FZ
    C['n_P'] = np.int64(C['phimax']/C['inc'])
    # n_p2: number of phi2 sample for FZ
    C['n_p2'] = np.int64(C['phi2max']/C['inc'])

    # n_eul: total number of orientations
    C['n_eul'] = C['n_p1'] * C['n_P'] * C['n_p2']
    C['L_th'] = C['thetamax']*(np.pi/180.)  # range of theta in radians
    C['bsz_th'] = C['L_th']/C['n_th']

    # domain_eul_sz is the integration domain in radians
    C['domain_eul_sz'] = C['phi1max']*C['phimax']*C['phi2max']*(np.pi/180.)**3
    # full_eul_sz is the size of euler space in radians
    C['full_eul_sz'] = (2*np.pi)*(np.pi)*(2*np.pi)
    C['eul_frac'] = C['domain_eul_sz']/C['full_eul_sz']
    C['fzsz_eul'] = 1./(C['eul_frac']*8.*np.pi**2)
    C['bsz_eul'] = C['domain_eul_sz']/C['n_eul']

    """define variables required for integration"""
    LL_p = 4  # gsh truncation level
    indxvec = gsh.gsh_basis_info()
    C['N_p'] = np.sum(indxvec[:, 0] <= LL_p)  # number of GSH bases to evaluate
    C['N_q'] = C['n_th']  # number of cosine bases to evaluate for theta
    C['N_tuple'] = [C['N_p'], C['N_q']]
    C['cmax'] = C['N_p']*C['N_q']

    return C
