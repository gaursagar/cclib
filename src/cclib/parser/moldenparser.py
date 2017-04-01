# -*- coding: utf-8 -*-
#
# Copyright (c) 2016, the cclib development team
#
# This file is part of cclib (http://cclib.github.io) and is distributed under
# the terms of the BSD 3-Clause License.

"""Parser for MOLDEN output files"""


import re

import numpy

from . import logfileparser
from . import utils


class MOLDEN(logfileparser.Logfile):
    """A GAMESS UK log file"""
    SCFRMS, SCFMAX, SCFENERGY = list(range(3))  # Used to index self.scftargets[]

    def __init__(self, *args, **kwargs):

        # Call the __init__ method of the superclass
        super(MOLDEN, self).__init__(logname="MOLDEN", *args, **kwargs)

    def __str__(self):
        """Return a string representation of the object."""
        return "MOLDEN format file %s" % (self.filename)

    def __repr__(self):
        """Return a representation of the object."""
        return 'MOLDEN("%s")' % (self.filename)

    def normalisesym(self, label):
        """TODO:Code for standard symmetry labels"""

    def before_parsing(self):
        #TODO

    def extract(self, inputfile, line):
        """Extract information from the file object inputfile."""

        if '[molden format]' in line.lower():
            self.logger.info("Found Molden Format. Initiating Parsing")

        
        #[Atoms] Angs
        #O     1    8         0.0000000000       -1.1362275006        0.0271298162
        #C     2    6         0.0000000000        0.0000000000       -0.0722772093
        #O     3    8         0.0000000000        1.1362275006        0.0271298162
        if '[atoms]' in line.lower():
            # Extract Atoms
            if not hasattr(self, "atomcoords"):
                self.atomcoords = []
            line = next(inputfile)
            atomcoords = []
            atomnos = []
            while len(line.strip().split()) > 1:
                temp = line.strip().split()
                atomcoords.append([utils.convertor(float(x), "bohr", "Angstrom") for x in temp[3:6]])
                atomnos.append(int(round(float(temp[2]))))  # Don't use the atom name as this is arbitary
                line = next(inputfile)
            self.set_attribute('atomnos', atomnos)
            self.set_attribute('natoms', len(atomnos))
            self.atomcoords.append(atomcoords)

        #[GTO]
        #atom_sequence_number1 0
        #shell_label number_of_primitives 1.00
        #exponent_primitive_1 contraction_coefficient_1 (contraction_coefficient_1)
        #...
        #empty line
        #atom_sequence__number2 0
        #shell_label number_of_primitives 1.00
        #exponent_primitive_1 contraction_coefficient_1 (contraction_coefficient_1)
        #...
        #empty line
        if '[gto]' in line.lower():
            # Extract gbasis
            gbasis = []
            line = next(inputfile)
            while line.strip().split():
                print "out",line
                line = next(inputfile)
                while line.strip() != '':
                    temp = line.split()
                    print "mid",line
                    label, nprim = temp[0].upper(), int(temp[1])
                    primitives = []
                    line = next(inputfile)
                    for i in xrange(nprim):
                        print "in", line
                        try:
                            line = line.replace('D','E')
                        except:
                            pass
                        coeff = [float(x) for x in line.strip().split()]
                        primitives.append(tuple(coeff))
                        line = next(inputfile)
                    gbasis.append((label, primitives))
            self.set_attribute('gbasis', gbasis)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
