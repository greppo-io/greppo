# Draw Feature
Draw a Feature on the interactive map. The feature can then be accessed on update and consumed by the user script.

## Parameters
`name` Str value serving as a unique identifier.

`feature` - A GeoPandas DataFrame representing the feature.

## Usage
```python
import geopandas as gpd

from greppo import app

random_draw_features = gpd.read_file("tests/data/features.geojson")
draw_feature_input = app.draw_feature(
    name="Draw random features", features=random_draw_features
)

# Consume draw_feature_input as a gdf, for example read value and plot a Chart.
# ...
```
