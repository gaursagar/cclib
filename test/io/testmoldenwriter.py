# -*- coding: utf-8 -*-
#
# Copyright (c) 2017, the cclib development team
#
# This file is part of cclib (http://cclib.github.io) and is distributed under
# the terms of the BSD 3-Clause License.

"""Unit tests for writer moldenwriter module."""

import os
import unittest

import cclib
from cclib.io.filewriter import MissingAttributeError
from cclib.parser.utils import MoldenReformatter

from difflib import ndiff

__filedir__ = os.path.dirname(__file__)
__filepath__ = os.path.realpath(__filedir__)
__datadir__ = os.path.join(__filepath__, "..", "..")


class MOLDENTest(unittest.TestCase):

    def test_missing_attributes(self):
        """Check if MissingAttributeError is raised as expected."""
        fpath = os.path.join(__datadir__,
                             "data/ADF/basicADF2007.01/dvb_gopt.adfout")
        data = cclib.io.ccopen(fpath).parse()
        del data.atomcoords

        # Molden files cannot be wriiten if atomcoords are missing.
        with self.assertRaises(MissingAttributeError):
            cclib.io.moldenwriter.MOLDEN(data)

    def test_molden_cclib_diff(self):
        """Check if file written by cclib matched file written by Molden."""
        fpath = os.path.join(__datadir__,
                             "data/GAMESS/basicGAMESS-US2014/C_bigbasis.out")
        data = cclib.io.ccopen(fpath).parse()
        cclib_out = cclib.io.moldenwriter.MOLDEN(data).generate_repr()
        cclib_out = MoldenReformatter(cclib_out).reformat()
        fpath = os.path.join(__datadir__,
                             "data/GAMESS/basicGAMESS-US2014/molden_ref/C_bigbasis.molden")
        molden_out = open(fpath).read()
        molden_out = MoldenReformatter(molden_out).reformat()
        # Molden files cannot be wriiten if atomcoords are missing.
        for i in ndiff(cclib_out, molden_out):
            print(i)

if __name__ == "__main__":
    unittest.main()
