import pandas as pd
from glaes import ExclusionCalculator

base_path = "./input/"
hub_height = 120
diameter = 155
radius = diameter / 2
height = hub_height + radius

raster_size = 10

vector_excludes = [
    {
        # Buildings health treatment
        "source": f"{base_path}/Gebäude/health.shp",
        "buffer": 3 * height,
    },
    {
        # Airports
        "source": f"{base_path}/Basis-DLM/ver04_f.shp",
        "where": "ART in ('5510','5511','5512') OR NTZ in ('2000','3000') AND ZUS IS NULL",
        "buffer": 6000,
    },
    {
        # Airfields
        "source": f"{base_path}/Basis-DLM/ver04_f.shp",
        "where": "ART in ('5520', '5540', '5550') AND (ZUS IS NULL or ZUS = 'None')",
        "buffer": 1750,
    },
    {
        # Camping
        "source": f"{base_path}/Basis-DLM/sie02_f.shp",
        "where": "FKT = '4330'",
        "buffer": 3 * height,
    },
    {
        # Cemetery
        "source": f"{base_path}/Basis-DLM/sie02_f.shp",
        "where": "OBJART = '41009'",
    },
    {
        # Industrial/Commercial
        "source": f"{base_path}/Basis-DLM/sie02_f.shp",
        "where": "OBJART ='41002'",
        "buffer": 2 * height,
    },
    {
        # Lakes
        # Use gew01_f instead of ver04_f as suggested in the supplementary material
        "source": f"{base_path}/Basis-DLM/gew01_f.shp",
        "where": "OBJART_TXT='AX_Hafenbecken' OR OBJART_TXT='AX_StehendesGewaesser'",
        "buffer": 50,
    },
    {
        # Military
        "source": f"{base_path}/Basis-DLM/geb03_f.shp",
        "where": "ADF = '4720'",
    },
    {
        # Mineral extraction
        "source": f"{base_path}/Basis-DLM/sie02_f.shp",
        "where": "OBJART ='41005' OR OBJART ='41004'",
    },
    {
        # Motorways 1
        "source": f"{base_path}/Basis-DLM/ver01_l.shp",
        "where": "WDM = '1301'",
        "buffer": 40 + radius,
    },
    {
        # Motorways 2
        "source": f"{base_path}/Basis-DLM/ver01_f.shp",
        "where": "OBJART_TXT = 'AX_Platz' and FKT != '5310'",
        "buffer": 40 + radius,
    },
    {
        # Outer areas
        "source": f"{base_path}/Basis-DLM/sie02_f.shp",
        "where": "OBJART = '41001' OR (OBJART='41007' AND FKT in ('1110', '1120', '1130', '1150', '1160', '1170'))",
        "buffer": 3 * height,
    },
    {
        # Power lines
        "source": f"{base_path}/Basis-DLM/sie03_l.shp",
        "where": "OBJART_TXT = 'AX_Leitung'",
        "buffer": 2 * radius,
    },
    {
        # Primary roads
        "source": f"{base_path}/Basis-DLM/ver01_l.shp",
        "where": "WDM = '1303'",
        "buffer": 20 + radius,
    },
    {
        # Railways 1
        "source": f"{base_path}/Basis-DLM/ver03_l.shp",
        "where": "OBJART_TXT = 'AX_Bahnstrecke'",
        "buffer": 2 * radius,
    },
    {
        # Railways 2
        "source": f"{base_path}/Basis-DLM/ver03_f.shp",
        "buffer": 2 * radius,
    },
    {
        # Railways 3
        "source": f"{base_path}/Basis-DLM/ver06_f.shp",
        "where": "OBJART_TXT ='AX_Bahnverkehrsanlage'",
        "buffer": 2 * radius,
    },
    {
        # Recreational
        "source": f"{base_path}/Basis-DLM/sie02_f.shp",
        "where": "OBJART = '41008'",
    },
    {
        # Regional roads
        "source": f"{base_path}/Basis-DLM/ver01_l.shp",
        "where": "WDM != '1301' AND WDM != '1303' AND WDM != '1305'",
        "buffer": radius,
    },
    {
        # Rivers
        "source": f"{base_path}/Basis-DLM/gew01_f.shp",
        "where": "OBJART_TXT='AX_Fliessgewaesser' OR OBJART_TXT='AX_Kanal' OR OBJART_TXT='AX_Wasserlauf' OR OBJART_TXT='AX_Gewaesserachse'",
        "buffer": 50,
    },
    {
        # Secondary roads
        "source": f"{base_path}/Basis-DLM/ver01_l.shp",
        "where": "WDM = '1305'",
        "buffer": radius,
    },
    {
        # National park
        "source": f"{base_path}/nlp_epsg25832_shp/nlp_epsg25832_shp.shp",
    },
    {
        # Nature reserve (NSG)
        "source": f"{base_path}/nsg_epsg25832_shp/nsg_epsg25832_shp.shp",
    },
    {
        # Birds protected areas (SPA)
        "source": f"{base_path}/vogelschutz_epsg25832_shp/vogelschutz_epsg25832_shp.shp",
        "buffer": 10 * height,
    },
    {
        # Alpenplan
        "source": f"{base_path}/Alpenplan/Alpenplan.shp",
        "where": "zone = 'C'",
    },
    {
        # Water protection
        "source": f"{base_path}/Wasserschutz/Wasserschutz.shp",
        "buffer": 50,
    },
    {
        # Biosphere (core zones)
        # Acquired from https://geodienste.bfn.de/ogc/wfs/schutzgebiet
        "source": f"{base_path}/Biosphäre/Kernzone.shp",
    },
    {
        # DVOR
        # Acquired from OSM (see osm-data-acquisition.py)
        "source": f"{base_path}/DVOR/DVOR.shp",
        "buffer": 10000,
    },
    {
        # VOR
        # Acquired from OSM (see osm-data-acquisition.py)
        "source": f"{base_path}/DVOR/VOR.shp",
        "buffer": 15000,
    },
    {
        # Historical
        # Acquired from OSM (see geofabrik-preprocessing.py)
        "source": f"{base_path}/OSM/gis_osm_pois_a_free_1.shp",
    },
    {
        # Stream
        # Acquired from OSM (see geofabrik-preprocessing.py)
        "source": f"{base_path}/OSM/gis_osm_waterways_free_1.shp",
    },
    {
        # Borders
        # Preprocessed with QGIS: Vector > Geometry Tools > Polygons to Lines
        "source": f"{base_path}/Grenzen/VG250_STA.shp",
        "buffer": 100,
    },
]
raster_excludes = [
    {
        # EU-DEM Slope
        # Preprocessed with QGIS: Crop raster to extent of Bavaria, calculate slope
        "source": f"{base_path}/EU-DEM/EU-DEM-Slope-BY.tif",
        "value": "(17-]",
    },
]

forest_functions = [
    "Bodenschutzwald",
    "Erholungswald",
    "Lawinenschutzwald",
    "regionaler_Klimaschutzwald",
    "Schutzwald_fuer_Immissionen_Laerm_und_lokales_Klima",
    "Schutzwald_fuer_Lebensraum_Landschaftsbild_Genressourcen_und_historisch_wertvollen_Waldbestand",
    "Sichtschutzwald",
]

restricted_forest_use = [
    {"source": f"{base_path}/Schutzwald/{function}.shp"}
    for function in forest_functions
]
forest_use = [
    {
        # Forest
        "source": f"{base_path}/Basis-DLM/veg02_f.shp"
    }
]
variable_excludes = [
    {
        # Buildings residential
        "source": f"{base_path}/Gebäude/residential.shp"
    },
    {
        # Inner areas
        "source": f"{base_path}/Basis-DLM/sie01_f.shp"
    },
]

# Specify what to exclude and in what order
exclude_configurations = [
    ("forest_use", variable_excludes),
    ("restricted_forest_use", restricted_forest_use),
    ("no_forest_use", forest_use),
]

variable_exclude_buffers = range(0, 2000, 100)
result_df = pd.DataFrame(
    index=variable_exclude_buffers, columns=[name for name, _ in exclude_configurations]
)

ec = ExclusionCalculator(
    f"{base_path}/ALKIS-Vereinfacht/VerwaltungsEinheit.shp",
    srs=25832,
    pixelSize=raster_size,
    where="art = 'Bundesland'",
)
for exclude in vector_excludes:
    print(exclude)
    ec.excludeVectorType(**exclude)
for exclude in raster_excludes:
    print(exclude)
    ec.excludeRasterType(**exclude)

# ec.draw()
# plt.show()
print(ec.percentAvailable)
ec.save(f"./output/ByWind_{raster_size}.tif")

for variable_buffer in variable_exclude_buffers:
    new_ec = ExclusionCalculator(
        f"{base_path}/ALKIS-Vereinfacht/VerwaltungsEinheit.shp",
        srs=25832,
        pixelSize=raster_size,
        where="art = 'Bundesland'",
        initialValue=f"./output/ByWind_{raster_size}.tif",
    )
    for name, excludes in exclude_configurations:
        for exclude in excludes:
            # Update buffer
            if name == "forest_use":
                exclude.update({"buffer": variable_buffer})
            print(exclude)
            new_ec.excludeVectorType(**exclude)
        print(new_ec.percentAvailable)
        result_df.at[variable_buffer, name] = new_ec.percentAvailable

        # new_ec.draw()
        # plt.show()
        new_ec.save(f"./output/ByWind_{raster_size}_{variable_buffer}_{name}.tif")
    result_df.to_csv(f"./output/ByWind_results.csv")
