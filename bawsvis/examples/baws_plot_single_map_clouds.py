# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-08-31 11:27

@author: a002028

"""
from bawsvis.session import Session
from bawsvis.readers.raster import raster_reader
from bawsvis.plotting import PlotMap
import os
import cmocean
import numpy as np
from matplotlib.colors import LinearSegmentedColormap


if __name__ == "__main__":
    s = Session()
    file = r'C:\Utveckling\BAWS-vis\bawsvis\export\cloud_aggregation_2021.tiff'

    data, meta = raster_reader(file, include_meta=True)

    map_frame = {'lat_min': 52., 'lat_max': 66.,
                 'lon_min': 7., 'lon_max': 37.5}

    color = cmocean.cm.gray(np.linspace(0.9, 0., 256))
    cmappen = LinearSegmentedColormap.from_list('cm_smhi_gray', color)

    plot = PlotMap(data_mat=data.astype(float),
                   lat_mat=s.setting.latitude_array,
                   lon_mat=s.setting.longitude_array,
                   cbar_label='Number of cloudy days',
                   cmap_step=10,
                   max_tick=60,
                   min_tick=20,
                   # cmap_step=5,
                   # max_tick=20,
                   # min_tick=0,
                   # cmap=cmocean.cm.turbid,
                   # cmap=cmocean.cm.gray,
                   cmap=cmappen,
                   use_frame=True,
                   map_frame=map_frame,
                   resolution='h',
                   fig_title='Clouds 2021',
                   fig_name='clouds_aggregation_2021.png',
                   save_fig=True,
                   clear_fig=True,
                   )

    plot._draw_map()
    plot._draw_mesh(p_color=True)
    plot._save_figure(os.path.join(s.setting.export_directory, 'clouds_aggregation_2021.png'))
