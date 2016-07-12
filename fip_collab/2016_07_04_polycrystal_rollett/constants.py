import time


def const():

    C = {}

    """general constants"""
    C['path'] = '/gpfs/scratch1/3/nhpnp3/4_28_neig'
    C['wrt_file'] = 'log_%s.txt' % (time.strftime("%Y-%m-%d_h%H"))

    # C['names'] = ['equiaxed, 15%% $\alpha$',
    #               'equiaxed, 30%% $\alpha$',
    #               'equiaxed, 40%% $\alpha$',
    #               'equiaxed, 50%% $\alpha$',
    #               'equiaxed, 60%% $\alpha$',
    #               'equiaxed, 65%% $\alpha$',
    #               'rolled, 15%% $\alpha$',
    #               'rolled, 30%% $\alpha$',
    #               'rolled, 40%% $\alpha$',
    #               'rolled, 50%% $\alpha$',
    #               'rolled, 60%% $\alpha$',
    #               'rolled, 65%% $\alpha$']

    C['names'] = [r'equiaxed, 15% $\alpha$',
                  r'equiaxed, 30% $\alpha$',
                  r'equiaxed, 40% $\alpha$',
                  r'equiaxed, 50% $\alpha$',
                  r'equiaxed, 60% $\alpha$',
                  r'equiaxed, 65% $\alpha$',
                  r'rolled, 15% $\alpha$',
                  r'rolled, 30% $\alpha$',
                  r'rolled, 40% $\alpha$',
                  r'rolled, 50% $\alpha$',
                  r'rolled, 60% $\alpha$',
                  r'rolled, 65% $\alpha$']

    C['set_id'] = ['equi15', 'equi30', 'equi40',
                   'equi50', 'equi60', 'equi65',
                   'roll15', 'roll30', 'roll40',
                   'roll50', 'roll60', 'roll65']

    C['dir_micr'] = "microstructure"
    C['dir_resp'] = "response"

    C['H_cub'] = 6
    C['H_hex'] = 9
    C['H'] = C['H_cub'] + C['H_hex']

    C['el'] = 225
    C['vmax'] = 81
    C['n_pc_tot'] = 11

    C['n_pc_max'] = 11
    C['n_poly_max'] = 1

    return C
