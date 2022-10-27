#!/usr/bin/env python3
"""
Created on 2021-09-29 19:07

@author: johannes
"""
from bawsvis.session import Session
from bawsvis.plotting import PlotIceMap
import os
import numpy as np
import cmocean


if __name__ == "__main__":
    s = Session()
    lat = np.loadtxt(r'C:\Utveckling\TESTING\sst_products\data\latgrid.txt')
    lon = np.loadtxt(r'C:\Utveckling\TESTING\sst_products\data\longrid.txt')

    month_map = {
        5: 'maj',
        6: 'juni',
        7: 'juli',
        8: 'augusti',
    }

    # data = np.loadtxt(r'C:\Utveckling\TESTING\sst_products\data\mean_summer_temperature_2022.txt')
    for year in range(2022, 2023):
        for mon in [6,7,8]:
            data = np.loadtxt(r'C:\Utveckling\TESTING\sst_products\data\mean_summer_temperature_{}_{}.txt'.format(year, mon))
            map_frame = {'lat_min': 52.5, 'lat_max': 66.,
                         'lon_min': 9., 'lon_max': 36.8}

            plot = PlotIceMap(data_mat=data.astype(float),
                           lat_mat=lat,
                           lon_mat=lon,
                           cbar_label='Ytvattentemperatur °C',
                           cmap=cmocean.cm.thermal,
                           cmap_step=2,
                           # max_tick=20,
                           max_tick=22,
                           min_tick=12,
                           use_frame=True,
                           map_frame=map_frame,
                           resolution='i',
                           fig_title='Medeltemperatur {} {}'.format(month_map[mon], year),
                           fig_name='mean_temperature_{}.png'.format(year),
                           # fig_title='Medeltemperatur 2022',
                           # fig_name='mean_temperature_2022.png',
                           # fig_title='Mean summer temperature {}'.format(year),
                           # fig_name='mean_temperature_{}.png'.format(year),
                           # fig_title='Mean summer temperature 2003-2021',
                           # fig_name='mean_temperature_2003_2021.png',
                           save_fig=True,
                           clear_fig=True,
                           )

            plot._draw_map()
            plot._draw_mesh(p_color=True)
            # plot._save_figure(r'C:\Utveckling\TESTING\sst_products\mean_temperature_2022.png')
            plot._save_figure(r'C:\Utveckling\TESTING\sst_products\mean_temperature_{}_{}.png'.format(year, mon))
