# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
import sys
import os

name = "bawsvis"

package_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(package_path)

from bawsvis import plotting
from bawsvis import readers
from bawsvis import writers
