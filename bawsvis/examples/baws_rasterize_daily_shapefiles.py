"""
Created on 2021-09-02 13:59
@author: johannes
"""
import pandas as pd

from bawsvis.utils import generate_filepaths
from bawsvis.session import Session
from bawsvis.data_handler import rasterize_daily_shp
from pathlib import Path


if __name__ == "__main__":
    # Set path to data directory
    # data_path = r'C:\Temp\baws_tempo\data_2021\corrected_geometries'
    # data_path = r'C:\Temp\baws_reanalys\clipped_archive\corrected_geoms'
    data_path = r'C:\Temp\baws_reanalys\tiff_archive\corrected'
    # data_path = r'C:\Temp\baws_reanalys\2022\corrected_geoms'

    # Create the Session object
    s = Session(data_path=data_path)

    # If we want to save data to a specific location, we set the export path here.
    s.setting.set_export_directory(path=data_path)

    # Generate filepaths
    generator = generate_filepaths(s.data_path, pattern='cyano_daymap_',
                                   endswith='.shp')

    for f in generator:
        f = Path(f)
        ts = pd.Timestamp(f.stem.split('_')[-1])
        if ts.year > 2012:
            continue
        print(f)
        rasterize_daily_shp(str(f), meta=s.setting.raster_template_meta)
        # break
