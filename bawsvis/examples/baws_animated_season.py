# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-05-11 16:35
@author: johannes
"""
from bawsvis.utils import generate_filepaths
from bawsvis.session import Session
import rasterio as rio
from rasterio import features
from rasterio import warp
import geopandas as gp
import numpy as np
import folium
from folium import plugins


if __name__ == "__main__":

    rst = rio.open(r'C:\Utveckling\TESTING\cyano_weekmap_20200718.tiff')
    image = rst.read(1, masked=True)

    m = folium.Map(location=[60.55, 18.0],
                   zoom_start=5,
                   tiles='cartodbdark_matter')

    # folium.raster_layers.ImageOverlay(
    #     image=np.flipud(image.data),
    #     bounds=[[53.057164270796875, 2.9077976800228247], [66.30693869687342, 33.35845793927669]],
    #     colormap=lambda x: (1, 0, 0, x),
    #     origin="lower",
    # ).add_to(m)
    #
    # m.save('test.html')

    gdf = gp.GeoDataFrame(columns=['class', 'geometry'], index=[])
    # Extract feature shapes and values from the array.
    polys = []
    for geom, val in rio.features.shapes(image, transform=rst.transform):
        # Print GeoJSON shapes to stdout.
        # print(geom)
        polys.append(
            {
                'time': '2020-07-18',
                'value': val,
                'coordinates': geom['coordinates'],
            }
        )

    features = {
        'type': 'FeatureCollection',
        'features': [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": poly["coordinates"],
                },
                "properties": {
                    "times": poly["time"],
                    "value": poly["value"],
                },
            }
            for poly in polys
        ]
    }
    plugins.TimestampedGeoJson(
        features,
        auto_play=False,
        # date_options='YYY'
    ).add_to(m)
