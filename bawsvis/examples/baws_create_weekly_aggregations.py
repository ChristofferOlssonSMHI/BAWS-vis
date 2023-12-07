"""
Created on 2021-09-02 14:57
@author: johannes
"""
from bawsvis.utils import generate_filepaths
from bawsvis.session import Session
from bawsvis.data_handler import create_7day_composite


if __name__ == "__main__":
    # Set path to data directory
    # data_path = r'C:\Temp\baws_tempo\data_2021'
    data_path = r'C:\Temp\baws_reanalys\tiff_archive\corrected'
    # data_path = r'C:\Temp\baws_reanalys\2022\corrected_geoms'

    # Create the Session object
    s = Session(data_path=data_path)

    # If we want to save data to a specific location,
    # we set the export path here.
    s.setting.set_export_directory(path=data_path)

    # Generate filepaths
    generator = generate_filepaths(
        s.data_path,
        pattern='cyano_daymap_',
        endswith='.tiff'
    )

    for f in generator:
        print(f)
        create_7day_composite(s.data_path, f)
