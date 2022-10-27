#!/usr/bin/env python3
# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-12-09 12:38

@author: johannes
"""
from bawsvis.session import Session
from bawsvis.readers.raster import raster_reader
from bawsvis.plotting import PlotBasinPatchesMap
import os
import numpy as np


def get_random_color():
    return (np.random.rand(), np.random.rand(), np.random.rand())


if __name__ == "__main__":

    s = Session()

    map_frame = {'lat_min': 53.5, 'lat_max': 65.,
                 'lon_min': 8.2, 'lon_max': 33.4}

    mapping_basin = {
        'BASIN_NR_3': {'color': '#F44F7A',  # get_random_color(),
                       'label': 'Bottenhavet'},
        'BASIN_NR_4': {'color': '#764FF4',  # get_random_color(),
                       'label': 'Ålands hav'},
        'BASIN_NR_6': {'color': '#4FF4B2',  # get_random_color(),
                       'label': 'Finska viken'},
        'BASIN_NR_7': {'color': '#E8F927',  # get_random_color(),
                       'label': 'Norra Egentliga Östersjön'},
        'BASIN_NR_8': {'color': '#F96927',  # get_random_color(),
                       'label': 'Västra Gotlandshavet'},
        'BASIN_NR_9': {'color': '#01B22D',  # get_random_color(),
                       'label': 'Östra Gotlandshavet'},
        'BASIN_NR_10': {'color': '#070089',  # get_random_color(),
                       'label': 'Rigabukten'},
        'BASIN_NR_11': {'color': '#A30404',  # get_random_color(),
                       'label': 'Gdanskbukten'},
        'BASIN_NR_12': {'color': '#7E7979',  # get_random_color(),
                       'label': 'Bornholmshavet'},
        'BASIN_NR_13': {'color': '#F26EE6',  # get_random_color(),
                       'label': 'Arkonahavet'},
        'BASIN_NR_14': {'color': '#fcba03',  # get_random_color(),
                       'label': 'Bälthavet'},
        'BASIN_NR_15': {'color': '#03fc07',  # get_random_color(),
                       'label': 'Öresund'},
    }

    plot = PlotBasinPatchesMap(
        basin_file_path=r'C:\Temp\shapes\helcom_coclime\HELCOM_subbasins_2018_baws_use.shp',
        basin_color_mapper=mapping_basin,
        map_frame=map_frame,
        resolution='f',
    )

    plot._draw_map()
    plot._save_figure(name='HELCOM_subbasins_basin_map.png')
