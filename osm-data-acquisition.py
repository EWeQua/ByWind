# Download and filter airmark beacons from OSM via Overpass
import os

import overpy
from geopandas import GeoDataFrame
from shapely import Point

results_file_path = "./input/DVOR"
os.makedirs(results_file_path, exist_ok=True)

api = overpy.Overpass()

# Query adapted from Supplementary Material of Risch et al.
# We choose an area larger than Germany to include airmark beacons that are outside Germany but close enough to affect
# eligible areas due to the large buffers applied
dvor = api.query(
    """
    [out:json][timeout:250];
    nwr["airmark"="beacon"](44.653024159812,-0.21972656250000003,56.65622649350222,22.96142578125);
    out geom;
    """
)

# Structure the results into a list of dicts, inspired by https://stackoverflow.com/a/72677231
results = [{"id": x.id, "geometry": Point(x.lon, x.lat), **x.tags} for x in dvor.nodes]

# Split beacons into VOR and DVOR
# Filters adapted from Supplementary Material of Risch et al.
filtered_results_vor = [
    x
    for x in results
    if (
        "beacon:type" in x
        and x["beacon:type"] in ["VOR", "VOR-DME", "VOR/DME", "VOR;DME", "VOR;TACAN"]
    )
    or ("type" in x and x["type"] in ["VOR/DME"])
    or ("beacon_t_1" in x and x["beacon_t_1"] in ["VOR", "VOR;TACAN"])
]

filtered_results_dvor = [
    x
    for x in results
    if (
        "beacon:type" in x
        and x["beacon:type"]
        in ["DVOR", "DVOR/DME", "DVOR;DME", "DVOR;TACAN", "DVORTAC"]
    )
    or (
        "beacon_t_1" in x
        and x["beacon_t_1"] in ["DVOR", "DVOR-DME", "DVOR/DME", "DVOR;DME"]
    )
]

# Save filtered results to ShapeFiles
GeoDataFrame(filtered_results_vor, crs="epsg:4326").to_file(
    f"{results_file_path}/VOR.shp"
)
GeoDataFrame(filtered_results_dvor, crs="epsg:4326").to_file(
    f"{results_file_path}/DVOR.shp"
)
