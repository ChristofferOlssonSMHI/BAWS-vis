# -*- coding: utf-8 -*-
"""
Created on 2020-09-17 17:21

@author: a002028

"""
import os

import numpy as np

from bawsvis.session import Session
from bawsvis.readers.text import np_txt_reader
from bawsvis.plotting import PlotMap, PlotIceMap
import matplotlib.pyplot as plt
import cmocean


if __name__ == "__main__":

    s = Session()

    lat = np_txt_reader('..\\proj\\havgem\\Johannes_Johansson\\N_FIX\\python_process_data\\lat_baws.txt')
    lon = np_txt_reader('..\\proj\\havgem\\Johannes_Johansson\\N_FIX\\python_process_data\\lon_baws.txt')

    # lat = np_txt_reader('E:\\Johannes_exjobb\\import_data\\lat_small.txt')
    # lon = np_txt_reader('E:\\Johannes_exjobb\\import_data\\lon_small.txt')

    # wd_data = 'E:\\Johannes_exjobb\\MODIS_data\\outdata\\monthly_seasonally_cummulative_and_FCA_data\\Cumulative\\annual\\Cumu_%s.txt'

    # for year in range(2019, 2021):
    #     year = str(year)
    #
    #     file = wd_data % year
    #     data = np_txt_reader(file)
    #
    #     map_frame = {'lat_min': 52., 'lat_max': 66.,
    #                  'lon_min': 7., 'lon_max': 37.5}
    #
    #     plot = PlotMap(data_mat=data.astype(float),
    #                    lat_mat=lat,
    #                    lon_mat=lon,
    #                    cbar_label='Number of bloom days',
    #                    cmap_step=5,
    #                    max_tick=20,
    #                    min_tick=0,
    #                    use_frame=True,
    #                    p_color=True,
    #                    map_frame=map_frame,
    #                    resolution='h',
    #                    fig_title='Cyanobacterial bloom %s' % year,
    #                    fig_name='aggregation_%s.png' % year,
    #                    save_fig=True,
    #                    clear_fig=True,
    #                    )
    #
    #     plot._draw_map()
    #     plot._draw_mesh(p_color=True)
    #     plot._save_figure(''.join((s.setting.export_directory, 'aggregation_baws_modis_%s.png' % year)))
    data = np_txt_reader('C:\\Utveckling\\BAWS-vis\\bawsvis\\export\\modis_aggregation_2002-2020.txt')
    data = np.where(data==0, np.nan, data)
    data = data/19.

    # mask = np_txt_reader('...N_FIX\\Result\\MASK_BP_GoF_GoB.txt')

    # map_frame = {'lat_min': 52., 'lat_max': 66.,
    #              'lon_min': 7., 'lon_max': 37.5}

    map_frame = {'lat_min': 52.5, 'lat_max': 66.,
                 'lon_min': 9., 'lon_max': 36.8}

    plot = PlotIceMap(data_mat=data.astype(float),
                   lat_mat=lat,
                   lon_mat=lon,
                   cbar_label='Average number of bloom days per year',
                   cmap=cmocean.cm.haline,
                   cmap_step=2,
                   max_tick=10,
                   min_tick=0,
                   use_frame=True,
                   p_color=True,
                   map_frame=map_frame,
                   resolution='f',
                   fig_title='Cyanobacterial bloom 2002-2020',
                   fig_name='aggregation_2002_2020_2.png',
                   save_fig=True,
                   clear_fig=True,
                   )

    plot._draw_map()
    plot._draw_mesh(p_color=True)

    save_dir = r'..\proj\havgem\Johannes_Johansson\coclime_figures\map'
    f_name = 'aggregation_2002_2020_v4'
    plt.savefig(os.path.join(save_dir, f_name) + '.png', format='png', dpi=500)
    # plt.savefig(os.path.join(save_dir, f_name) + '.eps', format='eps')
    plt.savefig(os.path.join(save_dir, f_name) + '.pdf', format='pdf')
    # plot._save_figure(''.join((s.setting.export_directory, 'aggregation_2002_2020_3.png')))
