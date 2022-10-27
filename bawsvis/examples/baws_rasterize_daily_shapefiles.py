"""
Created on 2021-09-02 13:59
@author: johannes
"""
from bawsvis.utils import generate_filepaths
from bawsvis.session import Session
from bawsvis.data_handler import rasterize_daily_shp


if __name__ == "__main__":
    # Set path to data directory
    # data_path = r'C:\Temp\baws_tempo\data_2021\corrected_geometries'
    # data_path = r'C:\Temp\baws_reanalys\clipped_archive\corrected_geoms'
    data_path = r'C:\Temp\baws_reanalys\clipped_archive'
    # data_path = r'C:\Temp\baws_reanalys\2022\corrected_geoms'

    # Create the Session object
    s = Session(data_path=data_path)

    # If we want to save data to a specific location, we set the export path here.
    s.setting.set_export_directory(
        path=r'C:\Temp\baws_reanalys\clipped_archive\corrected_geoms')

    # Generate filepaths
    generator = generate_filepaths(s.data_path, pattern='cyano_daymap_200',
                                   endswith='.shp')

    for f in generator:
        if not any((d in f for d in ('cyano_daymap_20080702',
                                     'cyano_daymap_20040705',
                                     'cyano_daymap_20040702',
                                     'cyano_daymap_20040630',
                                     'cyano_daymap_20040629',
                                     'cyano_daymap_20040626',
                                     'cyano_daymap_20030705',
                                     'cyano_daymap_20030615'))):
            continue
        print(f)
        # if 'cyano_daymap_200' in f:
        #     continue
        rasterize_daily_shp(f, meta=s.setting.raster_template_meta)
        # break
