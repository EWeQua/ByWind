# Read and join all the chunk geopackage files to a single GeoDataFrame and filter and save them by building function
import os

import geopandas as gpd
import pandas as pd

chunk_file_path = "./downloads/intermediate/"
results_file_path = "./input/Gebäude/"
os.makedirs(results_file_path, exist_ok=True)

# Building functions to filter for according to the supplementary material of Risch et al.
# See https://repository.gdi-de.org/schemas/adv/citygml/Codelisten/BuildingFunctionTypeAdV.xml for the complete list of
# building functions
residential_function_values = [
    "31001_1000",
    "31001_1010",
    "31001_1020",
    "31001_1021",
    "31001_1022",
    "31001_1023",
    "31001_1024",
    "31001_1025",
    "31001_1210",
    "31001_3064",
    "31001_3066",
    "31001_2070",
    "31001_2071",
    "31001_2072",
    "31001_2074",
]

health_function_values = [
    "31001_3240",
    "31001_3241",
    "31001_3242",
    "31001_3051",
    "31001_3052",
]

mixed_function_values = [
    "31001_1100",
    "31001_1110",
    "31001_1120",
    "31001_1121",
    "31001_1122",
    "31001_1123",
    "31001_1130",
    "31001_1220",
    "31001_1221",
    "31001_1223",
]

all_function_values = (
    residential_function_values + health_function_values + mixed_function_values
)

# Read and join all the chunk geopackage files to a single GeoDataFrame and drop eventual duplicates
gpkg_files = [
    f"{chunk_file_path}{f}" for f in os.listdir(chunk_file_path) if f.endswith(".gpkg")
]
gdfs = [gpd.read_file(file) for file in gpkg_files]
combined_gdf = gpd.GeoDataFrame(pd.concat(gdfs, ignore_index=True)).drop_duplicates()

# Filter for building functions specified in supplementary material of Risch et al.
residential_buildings = combined_gdf.query("GFK in @residential_function_values")
health_buildings = combined_gdf.query("GFK in @health_function_values")
mixed_buildings = combined_gdf.query("GFK in @mixed_function_values")
other_buildings = combined_gdf.query("GFK not in @all_function_values")

# Save the filtered data to single Shapefiles in results_file_path
residential_buildings.to_file(
    f"{results_file_path}residential.shp", driver="ESRI Shapefile"
)
health_buildings.to_file(f"{results_file_path}health.shp", driver="ESRI Shapefile")
mixed_buildings.to_file(f"{results_file_path}mixed.shp", driver="ESRI Shapefile")
other_buildings.to_file(f"{results_file_path}other.shp", driver="ESRI Shapefile")
