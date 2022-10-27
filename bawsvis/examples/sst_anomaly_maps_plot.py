#!/usr/bin/env python3
"""
Created on 2021-10-01 12:21

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

    for year in range(2021, 2022):
        data = np.loadtxt(r'C:\Utveckling\TESTING\sst_products\data\mean_summer_temperature_anomaly_{}.txt'.format(year))

        map_frame = {'lat_min': 52.5, 'lat_max': 66.,
                     'lon_min': 9., 'lon_max': 36.8}

        plot = PlotIceMap(data_mat=data.astype(float),
                       lat_mat=lat,
                       lon_mat=lon,
                       cbar_label='Ytvattentemperatur °C',
                       cmap=cmocean.cm.balance,
                       cmap_step=1,
                       max_tick=5,
                       min_tick=-5,
                       use_frame=True,
                       map_frame=map_frame,
                       resolution='i',
                       fig_title='Temperaturanomali {}'.format(year),
                       fig_name='mean_temperature_anomaly_{}.png'.format(year),
                       save_fig=True,
                       clear_fig=True,
                       )

        plot._draw_map()
        plot._draw_mesh(p_color=True)
        plot._save_figure(r'C:\Utveckling\TESTING\sst_products\mean_temperature_anomaly_{}.png'.format(year))
