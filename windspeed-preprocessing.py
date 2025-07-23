# Convert WMS image from the Bavarian Windatlas to binary GeoTIFFs indicating whether wind speed is above a given
# threshold, e.g., 4.5 or 4.8 m/s
# For further info on the Bavarian Windatlas WMS see:
# https://www.lfu.bayern.de/umweltdaten/geodatendienste/index_detail.htm?id=0cdaec03-b7ce-4333-8288-53663eb1da35&profil=WMS
import numpy as np
import rasterio

# Before running this script, download the whole WMS content (layer "windgeschwindigkeit_120m") from
# https://www.lfu.bayern.de/gdi/wms/energieatlas/windatlas2021? as a GEOTIFF (resolution 10x10 meters), e.g., via QGIS
# using the filename below and move it to the input path below
input_path = "./downloads/windspeed/windspeed_120.tif"
output_path = "./downloads/windspeed/"

# Create a blocklist for wind speeds up to 4.5 m/s
# See the legend for further details
# https://www.lfu.bayern.de/gdi/legende/energieatlas/windatlas2021/windgeschwindigkeit_120m.png
blocklist_45 = [
    (0, 15, 135),  # bis 3.5 m/s
    (3, 42, 149),  # > 3.5 - 3.6 m/s
    (7, 70, 164),  # > 3.6 - 3.7 m/s
    (10, 97, 179),  # > 3.7 - 3.8 m/s
    (14, 125, 194),  # > 3.8 - 3.9 m/s
    (8, 156, 208),  # > 3.9 - 4.0 m/s
    (0, 187, 238),  # > 4.0 - 4.1 m/s
    (82, 232, 221),  # > 4.1 - 4.2 m/s
    (36, 210, 161),  # > 4.2 - 4.3 m/s
    (45, 195, 137),  # > 4.3 - 4.4 m/s
    (54, 180, 115),  # > 4.4 - 4.5 m/s
]
# Create a blocklist for wind speeds up to 4.8 m/s by extending blocklist for wind speeds up to 4.5 m/s
blocklist_48 = blocklist_45 + [
    (110, 195, 53),  # > 4.5 - 4.6 m/s
    (150, 205, 15),  # > 4.6 - 4.7 m/s
    (180, 215, 0),  # > 4.7 - 4.8 m/s
]

blocklists = [("4.5m", blocklist_45), ("4.8m", blocklist_48)]


with rasterio.Env():
    with rasterio.open(input_path) as src:
        r = src.read(1)
        g = src.read(2)
        b = src.read(3)

        height, width = r.shape

        for name, blocklist in blocklists:
            # Initially create a mask of ones
            mask = np.ones((height, width), dtype=np.uint8)

            # Apply blocklist
            for color in blocklist:
                r_val, g_val, b_val = color
                match = (r == r_val) & (g == g_val) & (b == b_val)
                mask[match] = 0  # Set mask to 0 where blocklist matches

            # show(mask)

            # Prepare output profile
            profile = src.profile.copy()
            # Only one band is required
            profile.update({"count": 1})

            # Write the output to GeoTIFF
            # Set nbits=1 to reduce file size, see https://gis.stackexchange.com/a/338424
            with rasterio.open(
                f"{output_path}windspeed_120_{name}.tif", "w", nbits=1, **profile
            ) as dst:
                dst.write(mask, 1)
