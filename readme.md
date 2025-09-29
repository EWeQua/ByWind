# The Impact of Forest Use and Distance to Residential Buildings on Wind Potential Areas in Bavaria, Germany

## Description

This is the evaluation repo for The Impact of Forest Use and Distance to Residential Buildings on Wind Potential Areas 
in Bavaria, Germany.
See the [paper](https://eplus.uni-salzburg.at/agit/periodical/titleinfo/12103771) for further information.
This repo recreates the wind potential area analysis from [Risch et al.](https://www.mdpi.com/1996-1073/15/15/5536) for 
Bavaria and on this basis explores the impact of forest use, distance to residential buildings and economic constraints
on eligible areas for wind turbines in Bavaria through [GLAES](https://github.com/FZJ-IEK3-VSA/glaes)-based eligibility analyses.
In detail, the distance to residential buildings is increased from 0 to 2000 metres in three scenarios: Unrestricted 
forest use, restricted forest use according to the [forest function mapping](https://www.stmelf.bayern.de/wald/wald_mensch/waldfunktionsplanung-in-bayern/index.html) 
and without the use of forests.
As an extension, every scenario is considered with and without economic constraints, i.e. low wind speeds.
In the paper, the results in terms of eligible areas are visualised and discussed within the context of the current 
legal framework.

## Preparation

This repo requires the use of the [conda](https://docs.conda.io/en/latest/) package manager. conda can be obtained by
installing the
[Anaconda Distribution](https://www.anaconda.com/distribution/), or [miniconda](https://docs.anaconda.com/miniconda/).
See the [Conda installation docs](https://conda.io/docs/user-guide/install/download.html>) for more information.

### Installing dependencies

Due to incompatibility of GLAES with newer Python versions, we decided to create two separate conda environments,
one for running GLAES (`by-wind`) and one for running the data acquisition scripts (`by-wind-da`).
If you're only interested in running GLAES, e.g., for reproducing the results in the paper, you can skip the creation 
of the `by-wind-da` environment.

To create the `by-wind` environment run:

    cd ByWind
    conda env create --file=environment.yml

To create the `by-wind-da` environment run:

    conda env create --file=environment-da.yml

### Acquire geodata from Zenodo

Download the required [geodata from Zenodo](https://zenodo.org/records/16940499) and unpack it into the input directory.
Afterward, your directory structure should look like this:

```
ByWind
└───input
│   └───ALKIS-Vereinfacht
│   └───Alpenplan
│   └───Basis-DLM
│   └───...
│   
└───output
└───readme.md
└───...
```

Note that the data remains under the original license, see [Used data sources](#used-data-sources) and the next sections
for further information on the used data and data acquisition process.

### Alternative: Acquire and preprocess geodata via scripts and manually

Alternatively to downloading the required geodata from Zenodo, you can also acquire and preprocess some of the data 
using the provided Python scripts.
Note that some data has to be acquired manually, see [Used data sources](#used-data-sources).
Also note that acquiring data on your own might result in different results than in the paper as the data sources might 
have changed in the meantime.

Activate the `by-wind-da` environment and run the corresponding script, e.g., `protected-forest-data-acquisition.py`:

    conda activate by-wind-da
    python protected-forest-data-acquisition.py

The scripts will typically try to download the corresponding data and write the results directly to the corresponding 
input directory, e.g., `/input/Schutzwald/`.

## Running
Once the required geodata is downloaded, you can create maps of the constrained areas or run the eligibility analyses.
The mapping of constrained areas is optional and not required for running the eligibility analyses.


### Optional: Mapping constrained areas

Activate the `by-wind` environment and run `mapping_constrained_areas.py`:

    conda activate by-wind
    python mapping_constrained_areas.py

To understand the spatial distribution of constraints and their interaction, constraints are classified into four 
categories (social political, physical, conservation and technical economic) according to 
[Ryberg et al.](https://www.mdpi.com/1996-1073/11/5/1246) before mapping.
The results, 4 .tif files, one for each constraint category, and a CSV, will be written to the output directory.

Note that residential areas and forests are not included in the maps as their influence is analysed in greater detail in 
the eligibility analyses.

### Eligibility analyses

To run the eligibility analyses, activate the `by-wind` environment and run `main.py`:

    conda activate by-wind
    python main.py

The results (.tif files and a CSV) will be written to the output directory.


## Used data sources
Most of the data sources used are based on the 
[supplementary materials of Risch et al.](https://www.mdpi.com/1996-1073/15/15/5536/s1?version=1659166850):
See the section on Onshore wind potential (referring to Section 2.3 in the paper) and especially Table S4 for Bavaria 
(in short: BY) on pages 12-13.

Additionally, data regarding the Alpine Plan, forest function mapping and wind speeds are used.

|                                                         | Data source                                                                                                   | License / Terms of use                                                                                                                                 |
|---------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------|
| Administrative boundaries                               | https://geodaten.bayern.de/opengeodata/OpenDataDetail.html?pn=verwaltung                                      | https://creativecommons.org/licenses/by/4.0/deed.de                                                                                                    |
| Buildings                                               | https://geodaten.bayern.de/opengeodata/OpenDataDetail.html?pn=lod2                                            | https://creativecommons.org/licenses/by/4.0/deed.de                                                                                                    |
| Land use                                                | https://geodaten.bayern.de/opengeodata/OpenDataDetail.html?pn=atkis_basis_dlm                                 | https://creativecommons.org/licenses/by/4.0/deed.de                                                                                                    |
| Forest function mapping                                 | https://geoportal.bayern.de/geoportalbayern/details-suche?5&resId=81716c2d-4fd8-4a48-a52f-16826a7728de        | https://creativecommons.org/licenses/by/4.0/deed.de                                                                                                    |
| Nature conservation                                     | https://gdk.gdi-de.org/geonetwork/srv/api/records/bec888f9-ba0c-42dc-846e-177b8265dafa                        | http://www.gesetze-im-internet.de/bundesrecht/geonutzv/gesamt.pdf                                                                                      |
| Water protection                                        | https://geoportal.bafg.de/inspire/download/AM/waterProtectionArea/datasetfeed.xml                             | Copyright: "WasserBLIcK/BfG & Zuständige Behörden der Länder, 2024-10-02."                                                                             |
| Biosphere                                               | https://geodienste.bfn.de/ogc/wfs/schutzgebiet                                                                | http://www.gesetze-im-internet.de/bundesrecht/geonutzv/gesamt.pdf                                                                                      |
| Alpine plan                                             | https://geoportal.bayern.de/geoportalbayern/suche/suche?0&q=alpenplan                                         | https://creativecommons.org/licenses/by-nd/4.0/deed.de                                                                                                 |
| EU-DEM                                                  | https://ec.europa.eu/eurostat/de/web/gisco/geodata/digital-elevation-model/eu-dem#Steigung                    | https://sdi.eea.europa.eu/catalogue/datahub/api/records/3473589f-0854-4601-919e-2e7dd172ff50/formatters/xsl-view?output=pdf&language=eng&approved=true |
| Historical areas and streams                            | https://download.geofabrik.de/europe/germany/bayern.html                                                      | https://opendatacommons.org/licenses/odbl/                                                                                                             |
| Very High Frequency Omnidirectional Range Station (VOR) | OpenStreetMap, see [osm-data-acquisition.py ](osm-data-acquisition.py)                                        | https://opendatacommons.org/licenses/odbl/                                                                                                             |
| Borders                                                 | https://gdz.bkg.bund.de/index.php/default/open-data/verwaltungsgebiete-1-250-000-stand-01-01-vg250-01-01.html | https://www.govdata.de/dl-de/by-2-0                                                                                                                    |
| Wind speeds                                             | https://geoportal.bayern.de/geoportalbayern/anwendungen/details?&resId=9d547b92-13bc-4d73-910f-c2dc2ffc4622 | https://creativecommons.org/licenses/by/4.0/deed.de                                                                                                                   |

## Citation

````
 @article{Neumayer_Mitterhofer_2025, 
    title={Mapping Wind Potential Areas in Bavaria, Germany: The Impact of Forest Use and Distance to Residential Buildings}, 
    volume={1}, 
    url={https://eplus.uni-salzburg.at/doi/10.25598/agit/2025-8}, 
    DOI={10.25598/AGIT/2025-8}, 
    journal={AGIT Conference}, 
    publisher={Universitätsbibliothek Salzburg}, 
    author={Neumayer, Martin and Mitterhofer, Matthias}, 
    year={2025}
 }
````

## Acknowledgment

This work was funded by the Bavarian State Ministry of Science and the Arts to promote applied research and development
at universities of applied sciences and technical universities.
