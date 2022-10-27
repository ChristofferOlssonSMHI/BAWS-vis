#!/usr/bin/env python
# Copyright (c) 2022 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2022-06-27 11:02

@author: johannes
"""
from bawsvis.utils import generate_filepaths
from bawsvis.session import Session
import geopandas as gp
import os
from pathlib import Path
import shapely
import pickle
import descartes
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
import matplotlib.cbook as cbook

from mpl_toolkits.basemap import Basemap


class MapHandler:
    """"""

    def __init__(self, path_figure=None, path_basemap=None):
        """Initialize.

        self.map_obj is used to transform polygon coordinates to the
        map projection.
        """
        self.path_figure = path_figure
        with open(path_basemap, 'rb') as f:
            self.map_obj = pickle.load(f)
        self.day_map = None
        self.day_axes = None
        self.day_figure = None

        self.day_colormap_properties = {
            0: '#000000', 1: '#7a7a7a', 2: '#Ffff00', 3: '#Ff9900', 4: '#000000'
        }

    def initialize_maps(self):
        """Initiate maps.

        Takes around 15 seconds per map,
        hence the threading might be a good idea.
        """
        with open(self.path_figure, 'rb') as openfile:
            self.day_figure = pickle.load(openfile)
        self.day_axes = self.day_figure.axes[0]

    @staticmethod
    def add_picture_to_figure(figure, path_picture='',
                              axes_settings=None):
        """Add logo and legend."""
        axes_settings = axes_settings or [0, 1, 2, 3]
        img = plt.imread(cbook.get_sample_data(path_picture))
        new_ax = figure.add_axes(axes_settings, zorder=3)
        new_ax.imshow(img)

        if 'smhi-logo' in path_picture:
            labels = [item.get_text() for item in new_ax.get_xticklabels()]
            labels[3] = '1'
            new_ax.set_xticklabels(labels)

        elif 'legend' in path_picture:
            new_ax.tick_params(axis="x", direction="in", pad=-22)
            new_ax.tick_params(axis="y", direction="in", pad=-22)

        new_ax.axis('off')

    @staticmethod
    def plot_patches(patches, map_axes=None):
        """Add color patches to map."""
        if any(patches):
            map_axes.add_collection(
                PatchCollection(patches, match_original=True)
            )


def get_matplotlib_patches(gf, map_obj, color_mapper):
    """"""
    prioritized_values = [4, 2, 3, 1]
    patches_dict = {value: [] for value in prioritized_values}

    for poly, value in zip(gf['geometry'], gf['class']):
        if int(value) == 0:
            continue

        if poly.geom_type == 'Polygon':
            mpoly = shapely.ops.transform(map_obj, poly)
            patches_dict[value].append(descartes.PolygonPatch(
                mpoly,
                lw=0.15,
                ec=color_mapper[value],
                color=color_mapper[value])
            )
        elif poly.geom_type == 'MultiPolygon':
            for subpoly in poly:
                mpoly = shapely.ops.transform(map_obj, subpoly)
                patches_dict[value].append(descartes.PolygonPatch(
                    mpoly,
                    lw=0.15,
                    ec=color_mapper[value],
                    color=color_mapper[value])
                )
        else:
            print('Not working......')

    patches_list = []
    for i in prioritized_values:
        patches_list.extend(patches_dict[i])

    return patches_list


if __name__ == "__main__":
    # Set path to data directory
    data_path = r'C:\Temp\baws_reanalys\clipped_archive\corrected_geoms'
    export_directory = Path(r'C:\Utveckling\BAWS-vis\bawsvis\export\daymaps_png')
    path_bmap_obj = r'C:\Utveckling\BAWS-vis\bawsvis\etc\baws_basemap.pickle'
    path_fig_obj = r'C:\Utveckling\BAWS-vis\bawsvis\etc\baws_cyano_figure.pickle'
    # Create the Session object
    s = Session(data_path=data_path)

    data = {}
    for year in range(2002, 2022):
        # Generate filepaths
        generator = generate_filepaths(s.data_path,
                                       pattern=f'cyano_daymap_{year}',
                                       endswith='.shp')

        # Loop through the file-generator extract statistics..
        for day_path in generator:
            file_name = Path(day_path).name.replace('.shp', '.png')
            print(file_name)

            gf = gp.read_file(day_path)
            gf['geometry'] = gf['geometry'].to_crs(epsg=4326)

            plot_handler = MapHandler(path_figure=path_fig_obj,
                                      path_basemap=path_bmap_obj)
            plot_handler.initialize_maps()

            patches = get_matplotlib_patches(
                gf,
                plot_handler.map_obj,
                plot_handler.day_colormap_properties
            )
            plot_handler.plot_patches(
                patches,
                map_axes=plot_handler.day_axes
            )
            plot_handler.day_figure.savefig(
                export_directory.joinpath(file_name), dpi=287
            )

            plt.close(plot_handler.day_figure)
