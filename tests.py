import pandas as pd
import geopandas as gp
import glob

from bawsvis.data_handler import get_area, rasterize_daily_shp, filter_shapes

def sum_area_from_json():
    df = pd.read_json(r'C:\Kodning\BAWS-vis\bawsvis\export\stats_2022_2.json')

    # sum = df.daily_bloom_area.sum()

    print(df.loc['daily_bloom_area', :].sum())
    print(df.loc['surface_area', :].sum())
    print(df.loc['subsurface_area', :].sum())

def get_columns_from_shp():
    gf = gp.read_file(r'C:\Arbetsmapp\BAWS\Årsrapport 2023\Data_test\corrected_geoms\cyano_daymap_20230918.shp')

    gf_clouds = gf.loc[gf['class'].isin([1]), :]
    gf_blooms = gf.loc[gf['class'].isin([2, 3]), :]
    clouds_area = get_area(gf_clouds)
    blooms_area = get_area(gf_blooms)

    print(clouds_area)
    print(blooms_area)

def test_filtering(file):
    gf = gp.read_file(file)
    a = filter_shapes(gf)
    print(a)

def merge_json():
    data_path = r'C:\Kodning\BAWS-vis\bawsvis\export'

    files = glob.glob(f'{data_path}/*_.xlsx')
    df = pd.DataFrame()

    for f in files:
        data = pd.read_excel(f, 'data')
        # df = pd.append([df, data])
        df = pd.concat([df, data])
    
    df.to_excel(
        f'fca_means_aggregate.xlsx',
        sheet_name='data',
        index=None,
    )

def sub_basin_shp_info():
    areas = gp.read_file(
        r'c:\Arbetsmapp\Shapefiler\Sub-basins_Baltic_Sea\Havsomr_SVAR_2016_3b.shp'
        # r'C:\Utveckling\w_sharktoolbox\SharkToolbox\data\shapefiles\SVAR 2016_3b_for_statistic_plotting\statistic_areas.shp'
    )
    pd.set_option('display.max_columns',None)
    pd.set_option('display.max_rows',None)
    basin_geometries = areas[['BASIN_NR', 'geometry']]
    basins = basin_geometries.dissolve(by='BASIN_NR')
    basins.plot()

sub_basin_shp_info()

# import geopandas as gpd
# import numpy as np
# import matplotlib.pyplot as plt
# from shapely.geometry import Polygon, LineString, MultiLineString, MultiPolygon, mapping

# from bawsvis.data_handler import get_valid_interiors

# # Create a sample geodataframe

# a = LineString([(0, 0), (0, 0.4), (1, 0.4), (1, 0)])
# b = MultiLineString([[(0, 1.6), (0.5, 2.4), (1.2, 2.6), (1.3, 1.7)], [(0, 1.5), (1, 1.3), (1.5, 1.6)]])
# c = MultiPolygon([ [ 18.8053638, 55.6800324 ], [ 18.8052141, 55.6784925 ], [ 18.8053638, 55.6800324 ], [ 18.8056633, 55.6831122 ], [ 18.8086886, 55.6861074 ], [ 18.8097381, 55.6968865 ], [ 18.8070116, 55.6969712 ], [ 18.8014088, 55.6956005 ], [ 18.7877763, 55.6960223 ], [ 18.7856901, 55.6744634 ], [ 18.7882661, 55.6728393 ], [ 18.7881171, 55.6712994 ], [ 18.801741, 55.6708776 ], [ 18.8053638, 55.6800324 ] ])
# # gf = gpd.GeoDataFrame({"ID": ["a", "b", "c"], "geometry": [a, b, c]})

# d = c.buffer(0)
# df = gpd.GeoDataFrame({"ID": ["a", "b", "d"], "geometry": [a, b, d]})

# shapes = []
# for i, shape in enumerate(gf._to_geo()['features']):

#     row_gf = gf.iloc[i: i + 1].explode(index_parts=False).reset_index(drop=True)

#     if row_gf.shape[0] > 1:
#         exp_gf = row_gf.buffer(0)
#         invalid_exteriors = []
#         for ii, geom in enumerate(exp_gf):
#             indices = [j for j in range(exp_gf.shape[0]) if j != ii]
#             invalid_exteriors.append(exp_gf[indices].contains(geom).any())

#         interiors = get_valid_interiors(
#             [p.exterior for p in row_gf.loc[invalid_exteriors, :].geometry]
#         )
#         polys = row_gf.loc[np.logical_not(invalid_exteriors), :].geometry
#     else:
#         polys = row_gf.geometry
#         interiors = []

#     for poly in polys:
#         if not poly.is_valid:
#             # TODO Testa med överdrivet skum polygon
#             print('Found invalid polygon. Cleaning...')
#             clean = poly.buffer(0)
#             # gf = gpd.GeoDataFrame({"geometry": poly})
#             # gf.plot()
#             # plt.show()
            
#             if clean.is_valid == True:
#                 print('Cleaned!')
#                 new_shape = shape.copy()
#                 new_shape['geometry'] = mapping(clean)
#                 shapes.append(new_shape)
#             else:
#                 print('Unable to clean.')

# gf.plot()
# df.plot()
# plt.show()