# Read all geofabrik shape files for each category and area
import os

import geopandas as gpd
import pandas as pd

# Download .shp.zip for all Bavarian subregions from https://download.geofabrik.de/europe/germany/bayern.html
# Extract them to base_dir
base_dir = './downloads/geofabrik'

# File names and adapted queries from Supplementary material
files_to_read = [('gis_osm_waterways_free_1', "fclass=='stream' | fclass=='ditch'"),
                 ('gis_osm_pois_a_free_1', "fclass in ['archaeological','monument','memorial','castle']")]

# Read, query and concat the files from every folder to a single gdf and save it to the input directory
for file, query in files_to_read:
    gdfs = []
    for folder in os.listdir(base_dir):
        single_gdf = gpd.read_file(f'{base_dir}/{folder}/{file}.shp').query(query)
        gdfs.append(single_gdf)
    gdf = pd.concat(gdfs)
    gdf.to_file(f'./input/OSM/{file}.shp')
