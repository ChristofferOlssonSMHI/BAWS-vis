# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-08-31 11:27

@author: a002028

"""
from bawsvis.session import Session
from bawsvis.readers.raster import raster_reader
from bawsvis.plotting import PlotIceMap
import os


if __name__ == "__main__":
    s = Session()

    season = '2017_2018'

    file = r'C:\Utveckling\BAWS-vis\bawsvis\export\aggregation_{}.tiff'.format(season)
    # s.setting.set_export_directory(path=r'C:\Temp\baws_tempo\data_2021')

    data = raster_reader(file)

    map_frame = {'lat_min': 52.5, 'lat_max': 66.,
                 'lon_min': 9., 'lon_max': 36.8}

    plot = PlotIceMap(data_mat=data.astype(float),
                   lat_mat=s.setting.latitude_array,
                   lon_mat=s.setting.longitude_array,
                   cbar_label='Number of days with ice',
                   cmap_step=20,
                   max_tick=200,
                   min_tick=1,
                   use_frame=True,
                   map_frame=map_frame,
                   resolution='l',
                   fig_title='Ice Season {}'.format(season.replace('_', '-')),
                   fig_name='aggregation_ice_{}.png'.format(season),
                   # fig_title='BAWS - Intercalibration 2021',
                   # fig_name='intercalibration_2021.png',
                   save_fig=True,
                   clear_fig=True,
                   )

    plot._draw_map()
    # plot._draw_mesh(p_color=True)
    # plot._save_figure(os.path.join(s.setting.export_directory, 'aggregation_ice_{}.png'.format(season)))
