# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-08-31 11:27

@author: a002028

"""
from bawsvis.session import Session
from bawsvis.readers.raster import raster_reader
from bawsvis.plotting import PlotMap


if __name__ == "__main__":

    s = Session()

    # for year in range(2002, 2010):
    for year in range(2022, 2023):
        year = str(year)

        # file = 'C:/Utveckling/BAWS-vis/bawsvis/export/aggregation_%s.tiff' % year
        file = r'C:\Temp\baws_reanalys\aggragated_archive\not_corrected_aggregation_2022.tiff'
        data, meta = raster_reader(file, include_meta=True)

        map_frame = {'lat_min': 52., 'lat_max': 66.,
                     'lon_min': 7., 'lon_max': 37.5}

        plot = PlotMap(data_mat=data.astype(float),
                       lat_mat=s.setting.latitude_array,
                       lon_mat=s.setting.longitude_array,
                       cbar_label='Number of bloom days',
                       cmap_step=5,
                       max_tick=30,
                       min_tick=0,
                       use_frame=True,
                       p_color=True,
                       map_frame=map_frame,
                       resolution='l',
                       fig_title='Cyanobacterial bloom %s' % year,
                       fig_name='aggregation_%s.png' % year,
                       save_fig=True,
                       clear_fig=True,
                       )

        plot._draw_map()
        plot._draw_mesh(p_color=True)
        plot._save_figure(
            ''.join((s.setting.export_directory, 'not_corrected_aggregation_%s.png' % year))
        )
