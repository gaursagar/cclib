# This file is part of cclib (http://cclib.github.io), a library for parsing
# and interpreting the results of computational chemistry packages.
#
# Copyright (C) 2006,2007,2012,2014,2015, the cclib development team
#
# The library is free software, distributed under the terms of
# the GNU Lesser General Public version 2.1 or later. You should have
# received a copy of the license along with cclib. You can also access
# the full license online at http://www.gnu.org/copyleft/lgpl.html.

"""Test logfiles with hessian output in cclib"""

import os
import unittest

import numpy

__filedir__ = os.path.realpath(os.path.dirname(__file__))

class GenericHessianTest(unittest.TestCase):
    """Generic Hessian unittest."""

    def modes_from_hessian(self, flathessian, mass, units=5140.4872066):
        """ Calculate normal mode freqs (in 1/cm) and vectors from hessian.
        Default units=5140.4872066 assumes Hessian in Hartree/Bohr^2 and mass
        in amu (12C := 12 amu) """

        # get full Hessian as square matrix
        N = 3*len(mass);  # number of modes
        hessian = numpy.zeros((N,N))
        # trilidx = numpy.where(numpy.tril(numpy.ones((hdim,hdim),int),0) != 0)  # NumPy 1.3
        hessian[numpy.tril_indices(N)] = flathessian
        # fill in upper triangle
        hessian = hess.transpose()
        hessian[numpy.tril_indices(N)] = flathessian

        # create mass weighting matrix - repeat for x,y,z
        invrootmass = numpy.repeat(1/numpy.sqrt(numpy.array(mass)), 3)
        # for weighing hessian
        ivmassouter = numpy.outer(invrootmass, invrootmass)
        # we need a column vector for scaling normal modes all at once
        invrootmass = numpy.reshape(invrootmass, (-1,1))

        # Perform mass-weighting and diagonalize to get normal modes
        freq, modes = numpy.linalg.eigh(hess * ivmassouter)
        # convert freqs to 1/cm
        freq = numpy.sign(freq) * numpy.sqrt(numpy.abs(freq)) * units

        # scale and renormalize eigenvectors
        modes = modes * invrootmass
        modes = numpy.transpose(modes/numpy.sqrt(numpy.sum(modes**2, 0)))
        # after reshape, indicies are (<mode number>, <atom number>, X, Y, or Z)
        modes = numpy.reshape(modes, (N, int(N/3), 3))
        # The LAPACK routine used by numpy's eigh() always returns eigenvalues in
        #  ascending order, so we can safely assume the first 6 modes are the zero
        #  freq modes. This only works for a PES minimum, not a transition state
        return freq[6:], modes[6:]

    def testfreqval(self):
        """ Do the vibfreqs read directly match those calculated from the Hessian within +/-0.1/cm? """
        freqs, modes = self.modes_from_hessian(self.data.hessian, self.data.atommasses)
        self.assertEqual(len(self.data.vibfreqs), len(freqs))
        for delta in (self.data.vibfreqs - freqs):
            self.assertTrue(-0.1 <= delta <= 0.1)


class Gaussian03HessianTest(GenericHessianTest):
    """Gaussian 03 Hessian unittest."""

class Gaussian09HessianTest(GenericHessianTest):
    """Gaussian 09 Hessian unittest."""


if __name__=="__main__":

    import sys
    sys.path.append(os.path.join(__filedir__, ".."))

    from test_data import DataSuite
    suite = DataSuite(['hessian'])
    suite.testall()
