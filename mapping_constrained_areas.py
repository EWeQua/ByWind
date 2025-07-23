import pandas as pd
from glaes import ExclusionCalculator

from main import (
    base_path,
    conservation_constraints,
    physical_constraints,
    raster_size,
    social_political_constraints,
    technical_economic_constraints,
)

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
        print(f"Excluding {constraint}")
        if constraint["source"].endswith(".shp"):
            ec.excludeVectorType(**constraint)
        elif constraint["source"].endswith(".tif"):
            ec.excludeRasterType(**constraint)
        else:
            print(f"Unknown exclude type ignored: {constraint['source']}")
    ec.save(f"./output/ByWind_{raster_size}_{name}.tif")
    result_df.at[name, "constrained_area"] = 100 - ec.percentAvailable

result_df.to_csv(f"./output/ByWind_constrained_areas.csv")
