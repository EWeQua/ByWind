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
        "buffer": 7000,
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

forest_functions = [
    "Bodenschutzwald",
    "Erholungswald",
    "Lawinenschutzwald",
    "regionaler_Klimaschutzwald",
    "Schutzwald_fuer_Immissionen_Laerm_und_lokales_Klima",
    "Schutzwald_fuer_Lebensraum_Landschaftsbild_Genressourcen_und_historisch_wertvollen_Waldbestand",
    "Sichtschutzwald",
]

protected_forests = [
    {"source": f"{base_path}/Schutzwald/{function}.shp"}
    for function in forest_functions
]
all_forests = [
    {
        # Forest
        "source": f"{base_path}/Basis-DLM/veg02_f.shp"
    }
]
residential_areas = [
    {
        # Buildings residential
        "source": f"{base_path}/Gebäude/residential.shp",
        # Custom flag to indicate that a buffer should be added / updated later on
        "update_buffer": True,
    },
    {
        # Inner areas
        "source": f"{base_path}/Basis-DLM/sie01_f.shp",
        # Custom flag to indicate that a buffer should be added / updated later on
        "update_buffer": True,
    },
]

# The order of scenarios matters: For performance reasons, the unrestricted_forest_use scenario is calculated first and
# forms the basis for all other scenarios. All other scenarios load the results from unrestricted_forest_use and only
# exclude further constrained areas.
scenarios = [
    (
        # In the unrestricted forest use scenario, only residential buildings are excluded implicitly
        "unrestricted_forest_use",
        None,
    ),
    (
        # In the restricted forest use scenario, additionally protected forests have to be excluded
        "restricted_forest_use",
        protected_forests,
    ),
    (
        # In the no_forest_use scenario, protected forests and all forests have to be excluded
        "no_forest_use",
        [*protected_forests, *all_forests],
    ),
    (
        # In the unrestricted forest use scenario, technical economic constraints are excluded
        "unrestricted_forest_use_economic",
        technical_economic_constraints,
    ),
    (
        # In the restricted forest use scenario, technical economic constraints and protected forests have to be excluded
        "restricted_forest_use_economic",
        [*protected_forests, *technical_economic_constraints],
    ),
    (
        # In the no_forest_use scenario, technical economic constraints, protected forests and all forests have to be excluded
        "no_forest_use_economic",
        [*protected_forests, *all_forests, *technical_economic_constraints],
    ),
]

if __name__ == "__main__":
    # First run with fixed excludes
    print(f"Running ExclusionCalculator with fixed excludes")
    ec = ExclusionCalculator(
        f"{base_path}/ALKIS-Vereinfacht/VerwaltungsEinheit.shp",
        srs=25832,
        pixelRes=raster_size,
        where="art = 'Bundesland'",
    )
    for exclude in [
        *social_political_constraints,
        *physical_constraints,
        *conservation_constraints,
    ]:
        print(f"Excluding {exclude}")
        if "source" in exclude and exclude["source"].endswith(".shp"):
            ec.excludeVectorType(**exclude)
        elif "source" in exclude and exclude["source"].endswith(".tif"):
            ec.excludeRasterType(**exclude)
        else:
            print(f"Unknown exclude type ignored: {exclude.source}")

    print(ec.percentAvailable)
    initial_result_path = f"./output/ByWind_{raster_size}.tif"
    ec.save(initial_result_path)

    variable_exclude_buffers = range(0, 2100, 100)
    result_df = pd.DataFrame(
        index=variable_exclude_buffers, columns=[name for name, _ in scenarios]
    )

    for name, excludes in scenarios:
        for variable_buffer in variable_exclude_buffers:
            print(
                f"Running scenario {name} with distance to residential buildings of {variable_buffer}m"
            )
            # Unrestricted forest use scenario is computed explicitly and at first for performance reasons
            if name == "unrestricted_forest_use":
                new_ec = ExclusionCalculator(
                    f"{base_path}/ALKIS-Vereinfacht/VerwaltungsEinheit.shp",
                    srs=25832,
                    pixelRes=raster_size,
                    where="art = 'Bundesland'",
                    initialValue=initial_result_path,
                )
                for residential_exclude in residential_areas:
                    # Update buffer
                    residential_exclude.update({"buffer": variable_buffer})
                    print(f"Excluding {residential_exclude}")
                    new_ec.excludeVectorType(**residential_exclude)
                result_df.at[variable_buffer, name] = new_ec.percentAvailable
                new_ec.save(
                    f"./output/ByWind_{raster_size}_{variable_buffer}_{name}.tif"
                )

            else:
                # All scenarios are based on unrestricted forest use results and only exclude additional areas
                unrestricted_forest_use_result_path = f"./output/ByWind_{raster_size}_{variable_buffer}_unrestricted_forest_use.tif"
                new_ec = ExclusionCalculator(
                    f"{base_path}/ALKIS-Vereinfacht/VerwaltungsEinheit.shp",
                    srs=25832,
                    pixelRes=raster_size,
                    where="art = 'Bundesland'",
                    initialValue=unrestricted_forest_use_result_path,
                )
                for exclude in excludes:
                    print(f"Excluding {exclude}")
                    if "source" in exclude and exclude["source"].endswith(".shp"):
                        new_ec.excludeVectorType(**exclude)
                    elif "source" in exclude and exclude["source"].endswith(".tif"):
                        new_ec.excludeRasterType(**exclude)
                    else:
                        print(f"Unknown exclude type ignored: {exclude.source}")
                result_df.at[variable_buffer, name] = new_ec.percentAvailable
                new_ec.save(
                    f"./output/ByWind_{raster_size}_{variable_buffer}_{name}.tif"
                )

    result_df.to_csv(f"./output/ByWind_results.csv")
