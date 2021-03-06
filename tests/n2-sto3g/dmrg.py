
# PYTHONPATH=../..:../../build python dmrg.py
# E(dmrg) = -107.64825089754916
# E(FCI) = -107.648250974014


from pyblock.qchem import *
from pyblock.dmrg import DMRG

bond_dim = 200

with BlockHamiltonian.get(fcidump='N2.STO3G.FCIDUMP', pg='d2h', su2=True, output_level=-1) as hamil:
    lcp = LineCoupling(hamil.n_sites, hamil.site_basis, hamil.empty, hamil.target)
    mps = MPS(lcp, center=0, dot=2)
    mps.randomize()
    mps.canonicalize()
    mpo = MPO(hamil)
    ctr = DMRGContractor(MPSInfo(lcp), MPOInfo(hamil))
    dmrg = DMRG(mpo, mps, bond_dim=[50, 80, 100, 200, 500], noise=[1E-3, 1E-4, 1E-5, 0], contractor=ctr)
    ener = dmrg.solve(10, 1E-6)
    print('final energy = ', ener)
