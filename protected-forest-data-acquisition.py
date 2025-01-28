import geopandas as gpd
from requests import Request

layer_names = ['Bodenschutzwald',
               'Erholungswald',
               'Lawinenschutzwald',
               'regionaler_Klimaschutzwald',
               'Schutzwald_fuer_Immissionen_Laerm_und_lokales_Klima',
               'Schutzwald_fuer_Lebensraum_Landschaftsbild_Genressourcen_und_historisch_wertvollen_Waldbestand',
               'Sichtschutzwald'
               ]
for name in layer_names:
    url = f"https://www.fovgis.bayern.de/arcgis/services/fov/waldfunktionskarte/MapServer/WFSServer?SERVICE=WFS&REQUEST=GetFeature&VERSION=2.0.0&TYPENAMES=fov_waldfunktionskarte:{name}&SRSNAME=urn:ogc:def:crs:EPSG::25832"

    q = Request('GET', url).prepare().url
    df = gpd.read_file(q, format='GML')

    df.to_file(f'./downloads/protected_forest/{name}.shp')
