"""
Created on 2021-09-02 13:59
@author: johannes
"""
from bawsvis.utils import generate_filepaths
from bawsvis.session import Session
from bawsvis.data_handler import rasterize_daily_iceshp
import rasterio as rio
import geopandas as gp


class AreaTransformer:
    """
    """
    def __init__(self, *args, epsg=None, shape=None, bounds=None, **kwargs):
        self.epsg = epsg
        if shape:
            self.height, self.width = shape
        if bounds:
            self.west, self.south, self.east, self.north = bounds

    @property
    def crs(self):
        return rio.crs.CRS.from_string(f'epsg:{self.epsg}')

    @property
    def transform(self):
        """
        Return an Affine transformation for a georeferenced raster given
        its bounds `west`, `south`, `east`, `north` and its `width` and
        `height` in number of pixels.
        """
        return rio.transform.from_bounds(
            self.west, self.south,
            self.east, self.north,
            self.width, self.height
        )

    def update_area_attributes(self, epsg=None, shape=None, bounds=None):
        if epsg:
            self.epsg = epsg
        if shape:
            self.height, self.width = shape
        if bounds:
            self.west, self.south, self.east, self.north = bounds

    @property
    def raster_meta(self):
        return {
            'driver': 'GTiff',
            'dtype': 'uint8',
            'nodata': None,
            'width': self.width,
            'height': self.height,
            'count': 2,
            'crs': self.crs,
            'transform': self.transform,
            'compress': 'lzw'
        }


if __name__ == "__main__":
    # Set path to data directory
    data_path = r'C:\Temp\ice_data'
    # data_path = r'C:\Utveckling\TESTING\ice\data'

    # Create the Session object
    s = Session(data_path=data_path)

    # If we want to save data to a specific location, we set the export path here.
    s.setting.set_export_directory(path=data_path)

    # Generate filepaths
    generator = generate_filepaths(s.data_path,
                                   pattern='seaice_',
                                   endswith='.shp',
                                   only_from_dir=True)

    # a = AreaTransformer(
    #     epsg=4326,
    #     shape=(1400, 1400),
    #     bounds=(8.1968, 53.6010, 30.2260, 65.9031),
    # )
    gf = gp.read_file(r'C:\Temp\baws_tempo\data_2021\cyano_daymap_20210601.shp')
    crs_meta = (gf.crs, 3006)

    for f in generator:
        print(f)
        rasterize_daily_iceshp(f, meta=s.setting.raster_template_meta, crs=crs_meta)
