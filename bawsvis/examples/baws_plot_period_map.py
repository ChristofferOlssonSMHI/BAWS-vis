# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-08-31 11:27

@author: a002028
"""
from bawsvis.session import Session
from bawsvis.plotting import PlotWhiteMap
import os
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":

    s = Session()
    file = r'C:\Temp\baws_reanalys\aggragated_archive\aggregation_2002-2022.txt'

    # data, meta = raster_reader(file, include_meta=True)
    data = np.loadtxt(file)

    map_frame = {'lat_min': 53.5, 'lat_max': 65.,
                 'lon_min': 9.2, 'lon_max': 35.}

    plot = PlotWhiteMap(data_mat=data.astype(float),
                        lat_mat=s.setting.latitude_array,
                        lon_mat=s.setting.longitude_array,
                        cbar_label='Antal dagar med blomning',
                        cmap_step=50,
                        max_tick=300,
                        min_tick=0,
                        map_frame=map_frame,
                        resolution='f',
                        # text=str(year),
                        )
    plot._draw_map()
    plot._draw_mesh(p_color=True)
    plot.hide_axis()
    plot._save_figure(
        os.path.join(
            s.setting.export_directory,
            'aggregation_2002-2022.png'
        )
    )
