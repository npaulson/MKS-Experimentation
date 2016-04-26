import numpy as np
from numpy import linalg as LA
import h5py


def tensnorm(tensvec):
    return np.sqrt(np.sum(tensvec[:, 0:3]**2+2*tensvec[:, 3:]**2, 1))

if __name__ == '__main__':

    el = 21
    nsteps = 100

    f = h5py.File("theta_fields.hdf5", 'w')
    alltheta = f.create_dataset("alltheta", (nsteps-1, el, el, el))
    envec = f.create_dataset("envec", (nsteps-1,))

    for ii in xrange(nsteps-1):
        filename = "Results_Ti64_Dream3D_XdirLoad_210microns_9261el_AbqInp" +\
                  "_PowerLaw_LCF_10cycles_3_data_strain_step0_frame%s.txt" % str(ii+1)
        rawdata = np.loadtxt(filename, skiprows=2)

        """sort the data by element"""
        indxlist = np.argsort(rawdata[:, 7])
        etsort = rawdata[indxlist, 1:7]

        # print rawdata.shape
        # print rawdata.shape[0]/8.

        etvec = np.zeros((el**3, 6))

        etvec = (etsort[0::8, :]+etsort[1::8, :]+etsort[2::8, :] +
                 etsort[3::8, :]+etsort[4::8, :]+etsort[5::8, :] +
                 etsort[6::8, :]+etsort[7::8, :])/8.

        # c = 0
        # for jj in xrange(el**3):
        #     tmp = np.zeros((6))
        #     for kk in xrange(8):
        #         tmp += rawdata[c, 1:7]
        #         c += 1
        #     etvec[jj, :] = tmp/8

        # c = 0
        # for jj in xrange(8*el**3):
        #     if np.mod(jj, 8) == 0:
        #         etvec[c, :] = etsort[jj, :]
        #         c += 1

        """find the deviatoric strain tensor"""

        et_dev = np.zeros(etvec.shape)
        et_dev[:, 0:3] = etvec[:, 0:3] - (1./3.)*np.expand_dims(np.sum(etvec[:, 0:3], 1), 1)
        et_dev[:, 3:] = etvec[:, 3:]

        # print np.all(np.isclose(np.sum(et_dev[:, 0:3]), np.zeros(el**3)))

        """find the norm of the tensors"""
        en = tensnorm(et_dev)

        # print "min(en): %s" % en.min()
        print "mean(en): %s" % en.mean()
        # print "max(en): %s" % en.max()

        """normalize the deviatoric strain tensor"""
        et_n = et_dev/np.expand_dims(en, 1)

        # print np.all(np.isclose(tensnorm(et_n), np.ones(el**3)))

        """write the normalized deviatioric total strain and plastic strains
        in matrix form"""
        et_m = np.zeros((el**3, 3, 3))
        et_m[:, 0, 0] = et_n[:, 0]
        et_m[:, 1, 1] = et_n[:, 1]
        et_m[:, 2, 2] = et_n[:, 2]
        et_m[:, 0, 1] = et_n[:, 3]
        et_m[:, 1, 0] = et_n[:, 3]
        et_m[:, 0, 2] = et_n[:, 4]
        et_m[:, 2, 0] = et_n[:, 4]
        et_m[:, 1, 2] = et_n[:, 5]
        et_m[:, 2, 1] = et_n[:, 5]

        """find the eigenvalues of the normalized tensor"""
        eigval, g_p2s = LA.eigh(et_m)
        del et_m
        # print eigval[:5, :]

        """find the deformation mode"""
        theta = np.arccos(-np.sqrt(3./2.)*eigval[:, 0])

        # print "min(theta): %s" % np.str(theta.min()*180./np.pi)
        print "mean(theta): %s" % np.str(theta.mean()*180./np.pi)
        # print "max(theta): %s" % np.str(theta.max()*180./np.pi)

        # alltheta[ii, ...] = theta.reshape(el, el, el)
        alltheta[ii, ...] = theta.reshape(el, el, el)

        envec[ii] = en.mean()

    f.close()
