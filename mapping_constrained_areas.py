import pandas as pd
from glaes import ExclusionCalculator

base_path = "./input"
hub_height = 120
diameter = 155
radius = diameter / 2
height = hub_height + radius

raster_size = 10

social_political_constraints = [
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
        # Secondary roads
        "source": f"{base_path}/Basis-DLM/ver01_l.shp",
        "where": "WDM = '1305'",
        "buffer": radius,
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
        # Borders
        # Preprocessed with QGIS: Vector > Geometry Tools > Polygons to Lines
        "source": f"{base_path}/Grenzen/VG250_STA.shp",
        "buffer": 100,
    },
]

physical_constraints = [
    {
        # Lakes
        # Use gew01_f instead of ver04_f as suggested in the supplementary material
        "source": f"{base_path}/Basis-DLM/gew01_f.shp",
        "where": "OBJART_TXT='AX_Hafenbecken' OR OBJART_TXT='AX_StehendesGewaesser'",
        "buffer": 50,
    },
    {
        # Rivers
        "source": f"{base_path}/Basis-DLM/gew01_f.shp",
        "where": "OBJART_TXT='AX_Fliessgewaesser' OR OBJART_TXT='AX_Kanal' OR OBJART_TXT='AX_Wasserlauf' OR OBJART_TXT='AX_Gewaesserachse'",
        "buffer": 50,
    },
    {
        # Stream
        # Acquired from OSM (see geofabrik-preprocessing.py)
        "source": f"{base_path}/OSM/gis_osm_waterways_free_1.shp",
    },
    {
        # EU-DEM Slope
        # Preprocessed with QGIS: Crop raster to extent of Bavaria, calculate slope
        "source": f"{base_path}/EU-DEM/EU-DEM-Slope-BY.tif",
        "value": "(17-]",
    },
]

conservation_constraints = [
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
]

technical_economic_constraints = [
    {
        # Wind speeds
        # Preprocessed with QGIS (export to GeoTIFF) and windspeed-preprocessing.py (create a mask of zeros, indicating
        # areas below the wind speed threshold)
        "source": f"{base_path}/Windgeschwindigkeit/windspeed_120_4.5m.tif",
        "value": 0,
    },
]


all_constraint_sets = {
    "social_political": social_political_constraints,
    "physical": physical_constraints,
    "conservation": conservation_constraints,
    "technical_economic": technical_economic_constraints,
}

result_df = pd.DataFrame(
    index=list(all_constraint_sets.keys()), columns=["constrained_area"]
)


for name, constraint_set in all_constraint_sets.items():
    print(f"Calculating constrained area ({name})")
    ec = ExclusionCalculator(
        f"{base_path}/ALKIS-Vereinfacht/VerwaltungsEinheit.shp",
        srs=25832,
        pixelRes=raster_size,
        where="art = 'Bundesland'",
    )
    for constraint in constraint_set:
        if constraint["source"].endswith(".shp"):
            ec.excludeVectorType(**constraint)
        elif constraint["source"].endswith(".tif"):
            ec.excludeRasterType(**constraint)
        else:
            print(f"Unknown exclude type ignored: {constraint['source']}")
    ec.save(f"./output/ByWind_{raster_size}_{name}.tif")
    result_df.at[name, "constrained_area"] = 100 - ec.percentAvailable

result_df.to_csv(f"./output/ByWind_constrained_areas.csv")
