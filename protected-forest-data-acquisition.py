# Read all layers from forest functions mapping WFS and save the content of each layer in a single Shapefile
import os

import geopandas as gpd

results_file_path = "./input/Schutzwald"
os.makedirs(results_file_path, exist_ok=True)

wfs_url = "https://www.fovgis.bayern.de/arcgis/services/fov/waldfunktionskarte/MapServer/WFSServer"
wfs_parameters = (
    "SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&SRSNAME=urn:ogc:def:crs:EPSG::25832"
)

layer_names = [
    "Bodenschutzwald",
    "Erholungswald",
    "Lawinenschutzwald",
    "regionaler_Klimaschutzwald",
    "Schutzwald_fuer_Immissionen_Laerm_und_lokales_Klima",
    "Schutzwald_fuer_Lebensraum_Landschaftsbild_Genressourcen_und_historisch_wertvollen_Waldbestand",
    "Sichtschutzwald",
]

for name in layer_names:
    # Add parameters to wfs url and include the layer name to download
    url = f"{wfs_url}?{wfs_parameters}&TYPENAMES=fov_waldfunktionskarte:{name}"
    # Read wfs layer to GeoDataFrame and write it to Shapefile
    gdf = gpd.read_file(url)
    gdf.to_file(f"{results_file_path}/{name}.shp")
