# Read all geofabrik shape files for each category and area
import os

import geopandas as gpd
import pandas as pd

# Before running this script, download .shp.zip for all Bavarian subregions from
# https://download.geofabrik.de/europe/germany/bayern.html and extract them to base_dir first
base_dir = "./downloads/geofabrik"
results_file_path = "./input/OSM"
os.makedirs(results_file_path, exist_ok=True)

# File names and adapted queries from Supplementary material
files_to_read = [
    ("gis_osm_waterways_free_1", "fclass=='stream' | fclass=='ditch'"),
    (
        "gis_osm_pois_a_free_1",
        "fclass in ['archaeological','monument','memorial','castle']",
    ),
]

# Read, query and concat the files from every region to a single gdf and save it to the input directory
for file, query in files_to_read:
    gdfs = []
    for region_folder in os.listdir(base_dir):
        region_gdf = gpd.read_file(f"{base_dir}/{region_folder}/{file}.shp").query(
            query
        )
        gdfs.append(region_gdf)
    gdf = pd.concat(gdfs)
    gdf.to_file(f"{results_file_path}/{file}.shp")
