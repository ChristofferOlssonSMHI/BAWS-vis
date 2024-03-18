#!/usr/bin/env python3
"""
Created on 2021-10-16 17:09

@author: johannes
"""
import os
from bawsvis.readers.dictionary import pandas_reader
from bawsvis.utils import generate_filepaths
import geopandas as gp
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_areas_index(areas, cyano_shp, value=None, not_index=None):

    not_index = not_index or []

    if isinstance(value, int):
        boolean_bloom = cyano_shp['class'] == value
    else:
        boolean_bloom = cyano_shp['class'].isin(value)

    if value == 1:
        # Clouds. We check if clouds cover an area >= threshold area for each basin.
        # Threshold area = 80% of total basin area.
        res = []
        for i in range(areas.shape[0]):
            if i not in not_index:
                cloud_cover = cyano_shp[boolean_bloom].clip(areas.iloc[i:i+1]).area.sum()
                if cloud_cover >= areas['area_threshold'][i]:
                    res.append(i)
    else:
        inp, res = areas.sindex.query_bulk(
            cyano_shp[boolean_bloom].geometry,
            predicate='intersects'
        )
    return np.unique(res)


if __name__ == "__main__":
    # "POLY_NAMN"
    areas = gp.read_file(
        r'c:\Arbetsmapp\Shapefiler\Sub-basins_Baltic_Sea\Havsomr_SVAR_2016_3b.shp'
        # r'C:\Utveckling\w_sharktoolbox\SharkToolbox\data\shapefiles\SVAR 2016_3b_for_statistic_plotting\statistic_areas.shp'
    )
    areas = areas.to_crs(epsg=3006)
    areas_geometries = areas[['BASIN_NR', 'geometry']]
    areas = areas_geometries.dissolve(by='BASIN_NR', as_index=False)
    # selected_basins = [f'BASIN_NR_{n}' for n in
    #                    (3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)]
    selected_basins = (3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15)
    boolean_filter = areas['BASIN_NR'].isin(selected_basins)
    areas = areas.loc[boolean_filter, :].reset_index(drop=True)
    areas['area'] = areas['geometry'].apply(lambda geom: int(geom.area))
    areas['area_threshold'] = areas['area'].apply(lambda a: int(a * .8))
    # YEAR = 2002
    for YEAR in range(2004, 2024):
    # directory = r'C:\Temp\baws_reanalys\tiff_archive'
        directory = r'C:\Arbetsmapp\BAWS\Årsrapport 2023\Data_test\baws_rasterize' \
            if YEAR == 2023 else r'C:\Arbetsmapp\BAWS\Årsrapport 2023\Data_test\baws_rasterize\prior_years'
        # directory = r'C:\Temp\baws_reanalys\clipped_archive\corrected_geoms'
        files = generate_filepaths(directory, pattern=f'cyano_daymap_{YEAR}', endswith='.shp')
        files = list(files)

        df = pd.DataFrame(
            columns=[d.split('_')[-1].split('.')[0] for d in files],
            index=selected_basins
        )
        for cyano_fid in files:
            date = os.path.basename(cyano_fid).split('_')[-1].split('.')[0]
            print(date)
            cyano_shp = gp.read_file(cyano_fid)
            if not cyano_shp['class'].isin((1, 2, 3)).any():
                continue

            if not cyano_shp.is_valid.all():
                cyano_shp.geometry = cyano_shp.buffer(0)

            bloom_indices = set()
            for v in (2, 3, 1):
                indices = get_areas_index(
                    areas,
                    cyano_shp,
                    value=v,
                    not_index=bloom_indices if v == 1 else []
                )
                touched_areas = areas['BASIN_NR'].iloc[indices]
                df.loc[touched_areas, date] = v
                if v in (2, 3):
                    for iii in indices:
                        bloom_indices.add(iii)

        df['BASIN'] = df.index
        df.to_excel(f'area_season_bloom_{YEAR}_incl_cloud.xlsx', index=False)
