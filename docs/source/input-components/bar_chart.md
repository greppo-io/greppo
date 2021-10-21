# Bar Chart
2-D Bar Chart is a UI component for rendering data.

## Parameters
`input_name` Str value serving as a unique identifier.

`title` - Title string rendered on the UI.

`description` - Description string rendered on the UI. 

`chardata` - Class representing data for the chart. The shape is similar to `chart.js`,
    `labels` - List of values rendered on the x-axis.
    `datasets` - List of Dataset objects that represent the y-axis values,
        `label` - Label for the dataset (ie. the legend on the chart).
        `backgroundColor` - Chart color.
        `data` - List of y-axis data points

## Usage
```python
from greppo import app
from input_types import Dataset
from input_types import ChartData

app.bar_chart(
    input_name="A bar chart",
    title="Test title",
    description="A simple bar chart",
    chartdata=[
        ChartData(
            labels=['1', '2', '3', '4'],
            datasets=[
                Dataset(
                    label="First Data",
                    backgroundColor="#FFFFFF",
                    data=[1, 2, 3, 4,],
                ),
            ]
        )
    ]
)
```
