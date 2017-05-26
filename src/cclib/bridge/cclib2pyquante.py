# -*- coding: utf-8 -*-
#
# Copyright (c) 2016, the cclib development team
#
# This file is part of cclib (http://cclib.github.io) and is distributed under
# the terms of the BSD 3-Clause License.

"""Bridge for using cclib data in PyQuante (http://pyquante.sourceforge.net)."""

from __future__ import print_function

import sys

try:
    from PyQuante.Molecule import Molecule
except ImportError:
    # Fail silently for now.
    pass

try:
    from pyquante2 import molecule
except ImportError:
    # Fail silently for now.
    pass


def makepyquante(atomcoords, atomnos, charge=0, mult=1):
    """Create a PyQuante Molecule.

    >>> import numpy
    >>> from PyQuante.hartree_fock import hf
    >>> atomnos = numpy.array([1,8,1],"i")
    >>> a = numpy.array([[-1,1,0],[0,0,0],[1,1,0]],"f")
    >>> pyqmol = makepyquante(a,atomnos)
    >>> en,orbe,orbs = hf(pyqmol)
    >>> print int(en * 10) / 10. # Should be around -73.8
    -73.8
    """
    return Molecule("notitle", list(zip(atomnos, atomcoords)), units="Angstrom",
                    charge=charge, multiplicity=mult)

def makepyquante2(atomcoords, atomnos, charge=0, mult=1):
    """Create a pyquante2 Molecule.

    atomcoords : numpy.ndarray of shape (m,3)
    atomnos: numpy.ndarray of shape (m,)
    Note: in cclib atomcoords have shape (n,m,3)
    """
    geom = [np.append(i[0], i[1]) for i in list(zip(atomnos, atomcoords))]
    return molecule(geom, units="Angstrom", charge=charge, multiplicity=mult)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
