# Overlay layer
The Overlay Layer is used to render details on top of the Base Layer of the Map component on the UI.

## Parameters
`data` GeoPandas DataFrame representing the Overlay details. TODO What are the columns etc.

`title` Title string value rendered on the UI.

`description` Description string value rendered on the UI.

`style` Styling options for this layer.

`visible` Boolean toggle to turn this layer on or off.

## Usage
```python
import geopandas as gpd
import pandas as pd
import numpy as np

from greppo import app

data_gdf_1 = gpd.read_file("tests/data/communes.geojson")

data_gdf_1["Value"] = pd.Series(
    np.ones(len(data_gdf_1["code"])),
    index=data_gdf_1.index,
)

app.overlay_layer(
    data_gdf_1,
    title="Communes",
    description="Communes in Normandy, France",
    style={"fillColor": "#F87979"},
    visible=True,
)
```
