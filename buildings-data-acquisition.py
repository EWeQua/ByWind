import os
import xml.etree.ElementTree as ET

import geopandas as gpd
import requests
from shapely.geometry import Polygon


def parse_metalink(xml_string: str):
    # Parse the XML file
    root = ET.fromstring(xml_string)

    # Define the XML namespace to handle it properly
    namespace = {'': 'urn:ietf:params:xml:ns:metalink'}

    # List to store the result tuples
    result = []

    # Iterate over all 'file' elements in the XML
    for file_element in root.findall('file', namespace):
        # Extract the filename attribute
        filename = file_element.get('name')

        # Extract the first 'url' element
        first_url = file_element.find('url', namespace).text

        # Append the tuple (filename, first URL) to the result list
        result.append((filename, first_url))

    return result


def download_files(name_url_tuple, download_dir):
    """
    Downloads files from the provided tuple (filename, url)
    and saves them to the specified download directory.

    :param name_url_tuple: Tuple (filename, url)
    :param download_dir: The directory where files will be saved
    """
    # Ensure the download directory exists
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    filename, url = name_url_tuple
    # Define the full path to save the file
    file_path = os.path.join(download_dir, filename)

    # If the file already exists, skip downloading it
    if os.path.exists(file_path):
        print(f"Skip downloading: {file_path}")
        with open(file_path) as file:
            return file.read()

    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Write the content to a file
        # with open(file_path, 'wb') as file:
        #    file.write(response.content)

        print(f"Successfully downloaded: {filename}")

        return response.content.decode("utf-8")

    except requests.exceptions.RequestException as e:
        print(f"Failed to download {filename} from {url}. Error: {e}")


def extract_buildings(element: ET.Element, namespaces: dict) -> list[ET.Element]:
    extracted_buildings = []
    for building in element.findall('.//bldg:Building', namespaces):
        function_element = building.find('.//bldg:function', namespaces)
        if function_element is not None:
            extracted_buildings.append(building)
    return extracted_buildings


def extract_id_geometry_tuple(building: ET.Element, namespaces: dict) -> tuple[str, str, Polygon]:
    gml_id = building.attrib[f'{{{namespaces.get("gml")}}}id']
    building_function = building.find('.//bldg:function', namespaces).text
    for ground_surface in building.findall('.//bldg:GroundSurface', namespaces):
        for polygon in ground_surface.findall('.//gml:Polygon', namespaces):
            pos_list = polygon.find('.//gml:posList', namespaces)
            if pos_list is not None:
                coords = list(map(float, pos_list.text.split()))
                coords = [(coords[i], coords[i + 1], coords[i + 2]) for i in range(0, len(coords), 3)]
                poly = Polygon(coords)
                return gml_id, building_function, poly
    raise


# See https://repository.gdi-de.org/schemas/adv/citygml/Codelisten/BuildingFunctionTypeAdV.xml

residential_function_values = ['31001_1000',
                               '31001_1010',
                               '31001_1020',
                               '31001_1021',
                               '31001_1022',
                               '31001_1023',
                               '31001_1024',
                               '31001_1025',
                               '31001_1210',
                               '31001_3064',
                               '31001_3066',
                               '31001_2070',
                               '31001_2071',
                               '31001_2072',
                               '31001_2074']

health_function_values = ['31001_3240',
                          '31001_3241',
                          '31001_3242',
                          '31001_3051',
                          '31001_3052']

mixed_function_values = ['31001_1100',
                         '31001_1110',
                         '31001_1120',
                         '31001_1121',
                         '31001_1122',
                         '31001_1123',
                         '31001_1130',
                         '31001_1220',
                         '31001_1221',
                         '31001_1223']

gml_namespaces = {'bldg': 'http://www.opengis.net/citygml/building/1.0',
                  'gml': 'http://www.opengis.net/gml'}


download_link_metafile = 'https://geodaten.bayern.de/odd/a/lod2/citygml/meta/metalink/09.meta4'
print(download_link_metafile)
response = requests.get(download_link_metafile)
response.raise_for_status()  # Raise an exception for HTTP errors
file_names = parse_metalink(response.text)
failed_chunks = []

chunk_size = 100
for i in range(0, len(file_names), chunk_size):
    print(f'Downloading GML files: Chunk {i}')
    chunk = file_names[i:i + chunk_size]
    chunk_file = f'./downloads/intermediate/Chunk_{i}_{chunk_size}.gpkg'
    if os.path.exists(chunk_file):
        continue
    try:

        gml_ids = []
        building_functions = []
        ground_surfaces = []

        for filename, file_url in chunk:
            file = download_files((filename, file_url), './downloads/GML/')
            root = ET.fromstring(file)

            # Find all 'bldg:Building' elements in the XML
            buildings = extract_buildings(root, gml_namespaces)

            # Extract ids and GroundSurfaces
            for building in buildings:
                gml_id, building_function, geometry = extract_id_geometry_tuple(building, gml_namespaces)
                gml_ids.append(gml_id)
                building_functions.append(building_function)
                ground_surfaces.append(geometry)

        residential_buildings_gdf = gpd.GeoDataFrame(data={'id': gml_ids, 'GFK': building_functions},
                                                     geometry=ground_surfaces, crs='EPSG:25832')
        residential_buildings_gdf.to_file(chunk_file, driver='GPKG')

    except:
        failed_chunks.append(i)
        print(f'Failed to download {chunk_file}')

print(failed_chunks)
