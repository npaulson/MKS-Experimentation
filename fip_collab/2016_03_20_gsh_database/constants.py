import gsh_hex_tri_L0_16 as gsh
import numpy as np


def const():

    C = {}

    """general constants"""
    C['path'] = '/gpfs/scratch1/3/nhpnp3/1_31_5deg'

    """for read_input_data"""
    C['read_njobs'] = 40
    C['read_mem'] = 8
    C['read_walltime'] = 1
    C['read_scriptname'] = 'read_input_data.py'
    C['read_output'] = 'var_extract_%s.hdf5'

    """for combine_input_data.py"""
    C['combineread_scriptname'] = 'combine_input_data.py'
    C['combineread_output'] = 'var_extract_total.hdf5'

    """for Xcalc_GSH_parallel"""
    C['XcalcGSH_njobs'] = 40
    C['XcalcGSH_mem'] = 12
    C['XcalcGSH_walltime'] = 5
    C['XcalcGSH_scriptname'] = 'Xcalc_GSH_parallel.py'
    C['XcalcGSH_output'] = 'X_parts_GSH_%s.hdf5'

    """for Xcalc_cos"""
    C['Xcalccos_scriptname'] = 'Xcalc_cos.py'
    C['Xcalccos_output'] = 'X_parts_cos.hdf5'

    """for combine_input_data.py"""
    C['combineXcalc_scriptname'] = 'combine_Xcalc.py'
    C['combineXcalc_output'] = 'X_parts.hdf5'

    """for integrate_parallel"""
    C['integrate_njobs'] = 200
    C['integrate_mem'] = 12
    C['integrate_walltime'] = 24
    C['integrate_scriptname'] = 'integrate_parallel.py'
    C['integrate_output'] = 'coeff_prt_%s.hdf5'

    """for combine_coef.py"""
    C['combinecoef_scriptname'] = 'combine_coef.py'
    C['combinecoef_coef'] = 'coef.hdf5'
    C['combinecoef_results'] = 'results.hdf5'

    """define variables related to the angles"""
    C['thetamax'] = 60  # theoretical max theta in degrees
    C['phi1max'] = 360  # theoretical max phi1 in degrees
    C['phimax'] = 90  # theoretical max Phi in degrees
    C['phi2max'] = 60  # theoretical max phi2 in degrees

    C['inc_eul'] = 5.0  # degree increment for euler angles
    C['inc_th'] = 1.5  # degree increment for deformation mode angles

    # n_th: number of theta samples for FZ
    C['n_th'] = np.int64(C['thetamax']/C['inc_th'])
    # n_p1 number of phi1 samples for FZ
    C['n_p1'] = np.int64(C['phi1max']/C['inc_eul'])
    # n_P: number of Phi sample for FZ
    C['n_P'] = np.int64(C['phimax']/C['inc_eul'])
    # n_p2: number of phi2 sample for FZ
    C['n_p2'] = np.int64(C['phi2max']/C['inc_eul'])

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

    """define variables related to the total strain"""
    C['a'] = 0.00485  # start for en range
    C['b'] = 0.00905  # end for en range
    C['n_en'] = 14
    C['L_en'] = C['b']-C['a']
    C['bsz_en'] = C['L_en']/C['n_en']

    """define variables required for integration"""
    LL_p = 16  # gsh truncation level
    indxvec = gsh.gsh_basis_info()
    C['N_p'] = np.sum(indxvec[:, 0] <= LL_p)  # number of GSH bases to evaluate
    C['N_q'] = C['n_th']  # number of cosine bases to evaluate for theta
    C['N_r'] = C['n_en']  # number of cosine bases to evaluate for en
    C['N_tuple'] = [C['N_p'], C['N_q'], C['N_r']]
    C['cmax'] = C['N_p']*C['N_q']*C['N_r']

    return C
