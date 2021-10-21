# Base Layer
The Base Layer used to render the Map component on the UI.

## Parameters
`name` Str value serving as a unique identifier.

`visible` Boolean toggle to turn on or off a Base Layer. A Greppo App can have multiple Base Layers.

`url` URL representing the resource.

`attributions` Usage attributions for the data.

## Usage
```python
from greppo import app

app.base_layer(
    name="CartoDB Light",
    visible=True,
    url="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}@2x.png",
    subdomains=None,
    attribution='&copy; <a target="_blank" href="http://osm.org/copyright">OpenStreetMap</a> contributors',
)
```
