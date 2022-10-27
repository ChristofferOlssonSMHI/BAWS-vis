# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-05-12 08:32
@author: johannes
"""
from bawsvis.utils import generate_filepaths
from bawsvis.session import Session
import rasterio as rio
from rasterio import features
from rasterio import warp
import pandas as pd
import geopandas as gp
import numpy as np
import matplotlib.pyplot as plt
import folium
from folium import plugins


if __name__ == "__main__":
    lat = np.loadtxt(r'C:\Utveckling\Github\satpy_johannes\latitude_20190415_baws1000_sweref99tm_.txt')
    lon = np.loadtxt(r'C:\Utveckling\Github\satpy_johannes\longitude_20190415_baws1000_sweref99tm_.txt')

    # rst = rio.open(r'C:\Utveckling\TESTING\cyano_weekmap_20200718.tiff')
    # image = rst.read(1, masked=True)
    rst = rio.open(r'C:\Temp\baws_tempo\data_2021\cyano_weekmap_20210702.tiff')
    image = rst.read()[0]
    mask = image != 0

    heat_data = [
        lat[mask],
        lon[mask],
        image[mask] / 1.
    ]

    m = folium.Map(location=[60.55, 18.0],
                   zoom_start=5,
                   tiles='cartodbdark_matter')

    # df = pd.DataFrame({'lat': [57, 57, 57, 58., 60.01, 60.02, 60.03], 'lon': [18, 21, 22, 17, 18,18,18], 'weight': [.1, .1, .1, .3, .3, .4, .5]})
    #
    plugins.HeatMap(
        heat_data,
        radius=5,
        max_val=0.0005,
        blur=5,
        min_opacity=0,
    ).add_to(m)

    # folium.raster_layers.ImageOverlay(
    #     image=np.flipud(image.data),
    #     bounds=[[53.057164270796875, 2.9077976800228247], [66.30693869687342, 33.35845793927669]],
    #     colormap=lambda x: (1, 0, 0, x),
    #     origin="lower",
    # ).add_to(m)

    m.save('testheatmap.html')

