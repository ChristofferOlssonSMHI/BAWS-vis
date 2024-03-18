# Visualize BAWS data

## Work-in-progress README
The purpose of the current iteration of BAWS-vis is to produce the visualizations for the 2023 Baltic sea cyanobacteria season report. The numbered files in the root folder (1_15) need to be run in approximately that order to prepare the data for the visualization files in 0_1-0_3 plus baws_box_plot/boxes and get_history_bloom_start_end. File paths in the scripts currently need to be adjusted.

TODO (incomplete):
- Remove unnecessary code in all files
- Merge baws_box_plot with the rest of BAWS-vis 
- Refactor code to better integrate existing SMHI tools and data workflow
    - Implement FAIR principles
- Remove unnecessary hardcoding and parameterize
- Annotate code and improve readability (PEP 8 compliance)

## Original README
Post season processing pinpoints
--------------------------------
Products we want to produce:
1. Quality controlled data (daily/weekly - shp/raster)
2. Daily areas (subsurface, surface, weekly-composition, clouds over area of interest) for each date (json)
3. Aggregated data (seasonal matrix - raster)
4. Figures based on the data above (png)


Different data formats for different purposes. 
Shapefiles for:
- manual adjustment in QGIS
- Calculating areas

Geotiff for:
- aggregations
- masking (coastal, basin areas)

JSON/Excel for:
- areas
- statistics

Workflow - Data processing
----------
Step 1: Copy all the shp/raster files from the server to the local machine.

Step 2: Manually quality control data for each date. This includes:
- Start with going through "Algarkivet" on smhi.se to spot false positives. Compare to RGB-images form the file server.
- Open any suspicious files in QGIS and adjust if needed.

Step 3: Adjust paths in, and then run the script `baws_correct_geoms.py` -> This will correct geometries (eg. bowtie geometries) and remove duplicates.

Step 4: Rasterize the shapefiles using `baws_rasterize_daily_shapefiles.py` -> This will create a raster for each date.

Step 5: Create weekly composites using `baws_create_weekly_aggregations.py` -> This will create a weekly composite for each date using the past 7 days.

Step 6: Shapeify the weekly composites using `baws_shapeify_raster_data.py` -> This will create a shapefile for each weekly composite.

Step 7: Create daily cloud data using `baws_shapeify_masked_cloud_data.py` -> This will create a raster for each date with cloud data.

Step 8: Create a seasonal bloom aggregation 2D array using `baws_aggregate_daily_data.py` -> This will create a 2D array for the given season.

Step 9: Calculate seasonal stats using the datafile above and `baws_get_annual_stats.py` -> This will create an excel file with stats for the given season. 

Step 10: Calculate areas for each date using `baws_get_statistics.py` -> This will create a json file with areas for each date.

Create figures
--------------
Fig 1: Seasonal bloom aggregation 2D array (heatmap) -> `baws_plot_single_map.py`

Fig 2: Season diagram (line plot) -> `baws_season_diagram.py`

Fig 3: Plot TA / FCA (bar plot) -> `baws_plot_bars_TA_FCA.py`