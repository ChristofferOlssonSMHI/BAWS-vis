"""
Created on 2021-09-02 15:58
@author: johannes
"""
from bawsvis.utils import generate_filepaths
from bawsvis.session import Session
from bawsvis.writers.dictionary import json_writer
from bawsvis.readers.dictionary import json_reader
from bawsvis.data_handler import get_area
import geopandas as gp
import os
from pathlib import Path


if __name__ == "__main__":
    # Set path to data directory
    # data_path = r'C:\Temp\baws_tempo\data_2021\daily_from_raster'
    # data_path = r'C:\Temp\baws_reanalys\clipped_archive\corrected_geoms'
    # original
    # data_path = r'C:\Temp\baws_reanalys\2022\corrected_geoms\clipped_archive'

    data_path = r'C:\Arbetsmapp\BAWS\Årsrapport 2023\Data_test\baws_rasterize\prior_years'
    # data_path = r'C:\Arbetsmapp\BAWS\Årsrapport 2023\Data_prior_years\reanalyzed_data'
    # Create the Session object
    s = Session(data_path=data_path)

    # If we want to save data to a specific location, we set the export path here.
    # s.setting.set_export_directory(path=data_path)

    # year = 2023
    for year in range(2002, 2023):

        # Generate filepaths
        generator = generate_filepaths(s.data_path,
                                    pattern=f'cyano_daymap_{year}',
                                    endswith='.shp')
        # generator = generate_filepaths(s.data_path, pattern='cyano_weekmap_', endswith='.shp')

        stat = json_reader(os.path.join(
            s.setting.export_directory, f'stats_{year}.json'))

        # Loop through the file-generator extract statistics..
        for day_path in generator:
            print(day_path)
            # if 'cyano_daymap' in day_path:
            #     continue
            day_frame = gp.read_file(day_path)
            # week_path = Path(day_path).parent.joinpath(
            #     Path(day_path).name.replace('_daymap_', '_weekmap_')
            # )
            # week_frame = gp.read_file(week_path)
            date_tag = os.path.basename(day_path).split('.')[0].split('_')[-1]
            stat[date_tag]["daily_bloom_area"] = get_area(day_frame.loc[day_frame['class'].isin([2, 3]), :])
            stat[date_tag]["surface_area"] = get_area(day_frame.loc[day_frame['class'] == 3, :])
            stat[date_tag]["subsurface_area"] = get_area(day_frame.loc[day_frame['class'] == 2, :])
            # stat[date_tag]["weekly_bloom_area"] = get_area(week_frame)

            # stat[date_tag] = {
            #     "daily_bloom_area": get_area(day_frame.loc[day_frame['class'].isin([2, 3]), :]),
            #     "surface_area": get_area(day_frame.loc[day_frame['class'] == 3, :]),
            #     "subsurface_area": get_area(day_frame.loc[day_frame['class'] == 2, :]),
            #     "weekly_bloom_area": get_area(week_frame)
            # }

        out_file_path = os.path.join(s.setting.export_directory,
                                    f'stats_{year}_2.json')
        json_writer(out_file_path, stat)
