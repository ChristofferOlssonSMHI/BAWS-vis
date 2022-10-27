#!/usr/bin/env python3
"""
Created on 2021-10-01 12:21

@author: johannes
"""
from bawsvis.session import Session
from bawsvis.plotting import PlotIceMap
import os
import xarray as xr
import numpy as np
import pandas as pd
import cmocean


if __name__ == "__main__":
    s = Session()
    lat = np.loadtxt(r'C:\Utveckling\TESTING\sst_products\data\OLD_latgrid.txt')
    lon = np.loadtxt(r'C:\Utveckling\TESTING\sst_products\data\OLD_longrid.txt')
    fid_template = r'C:\Temp\Satellit\modis_data\sst4\anomaly\AQUA_MODIS.{}.L3m.ANOMALY.SST4.x_sst4.nc'
    date_sets = set(os.listdir(r'C:\Temp\Satellit\modis_data\sst4\anomaly'))
    for date in pd.date_range(start=pd.Timestamp('2021-06-01'), end=pd.Timestamp('2021-08-31')):
        print(date)
        fid = fid_template.format(date.strftime('%Y%m%d'))
        if os.path.basename(fid) in date_sets:
            ds = xr.open_dataset(fid)
            data = ds['sst4_anomaly'].data

            map_frame = {'lat_min': 52.5, 'lat_max': 66.,
                         'lon_min': 9., 'lon_max': 36.8}

            plot = PlotIceMap(
                data_mat=data,
                lat_mat=lat,
                lon_mat=lon,
                # cbar_label='SST °C',
                cbar_label='Ytvattentemperatur °C',
                cmap=cmocean.cm.balance,
                cmap_step=1,
                max_tick=5,
                min_tick=-5,
                use_frame=True,
                map_frame=map_frame,
                resolution='f',
                fig_title='Temperaturavvikelse {}'.format(date.strftime('%Y-%m-%d')),
                fig_name='temperature_anomaly_{}.png'.format(date.strftime('%Y%m%d')),
                save_fig=True,
                clear_fig=True,
            )

            plot._draw_map()
            plot._draw_mesh(p_color=True)
            plot._save_figure(
                r'C:\Utveckling\TESTING\sst_products\figures\anomalies\temperature_anomaly_{}.png'
                r''.format(date.strftime('%Y%m%d'))
            )
