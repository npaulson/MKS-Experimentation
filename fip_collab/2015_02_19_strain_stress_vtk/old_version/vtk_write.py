import os
import time
import numpy as np
import functions as rr


def vtk_write(el, ns, set_id, step, newdir, wrt_file):

    st = time.time()

    nx_el, ny_el, nz_el = el, el, el
    nx_pt, ny_pt, nz_pt = el + 1, el + 1, el + 1

    no_el = nx_el * ny_el * nz_el
    dx, dy, dz = 0.02, 0.02, 0.02
    lx, ly, lz = dx*nx_el, dy*ny_el, dz*nz_el

    # Coordinates
    X = np.arange(0, lx+dx, dx)
    Y = np.arange(0, ly+dx, dy)
    Z = np.arange(0, lz+dx, dz)

    grain = np.load('gID_%s%s_s%s.npy' % (ns, set_id, step))
    euler = np.load('euler_%s%s_s%s.npy' % (ns, set_id, step))

    e11 = np.load('mksR%s_%s%s_s%s.npy' % (11, ns, set_id,
                                           step)).reshape([ns, el**3])
    e22 = np.load('mksR%s_%s%s_s%s.npy' % (22, ns, set_id,
                                           step)).reshape([ns, el**3])
    e33 = np.load('mksR%s_%s%s_s%s.npy' % (33, ns, set_id,
                                           step)).reshape([ns, el**3])
    e12 = np.load('mksR%s_%s%s_s%s.npy' % (12, ns, set_id,
                                           step)).reshape([ns, el**3])
    e13 = np.load('mksR%s_%s%s_s%s.npy' % (31, ns, set_id,
                                           step)).reshape([ns, el**3])
    e23 = np.load('mksR%s_%s%s_s%s.npy' % (23, ns, set_id,
                                           step)).reshape([ns, el**3])

    s11 = np.load('stress%s_%s%s_s%s.npy' % (11, ns, set_id, step))
    s22 = np.load('stress%s_%s%s_s%s.npy' % (22, ns, set_id, step))
    s33 = np.load('stress%s_%s%s_s%s.npy' % (33, ns, set_id, step))
    s12 = np.load('stress%s_%s%s_s%s.npy' % (12, ns, set_id, step))
    s13 = np.load('stress%s_%s%s_s%s.npy' % (31, ns, set_id, step))
    s23 = np.load('stress%s_%s%s_s%s.npy' % (23, ns, set_id, step))

#    nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir  # for unix
    os.chdir(nwd)

    for sn in xrange(ns):

        filename = 'mks_alphaTi_Xdir_ID%s_sn%s_step%s.vtk' % (set_id, sn, step)

        file_vtk = open(filename, 'w')

        rr.VTK_Header(file_vtk, 'MKS_results', nx_pt, ny_pt, nz_pt, X, Y,
                      Z, no_el)

        rr.VTK_Scalar_Int(file_vtk, 'GrainID', grain[sn, :], nx_el)

        rr.VTK_Vector(file_vtk, 'Euler_phi1Phi0phi2', euler[sn, :, :], nx_el)

        rr.VTK_Tensor(file_vtk, 'Stress', s11[sn, :], s12[sn, :], s13[sn, :],
                      s22[sn, :], s23[sn, :], s33[sn, :], nx_el)

        rr.VTK_Tensor(file_vtk, 'Strain', e11[sn, :], e12[sn, :], e13[sn, :],
                      e22[sn, :], e23[sn, :], e33[sn, :], nx_el)

        file_vtk.close()

    # return to the original directory
    os.chdir('..')

    msg = 'write .vtk files: %ss' % (time.time()-st)
    rr.WP(msg, wrt_file)
