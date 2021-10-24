# Bar Chart
2-D Bar Chart is a UI component for rendering data.

## Parameters
`name` Str value serving as a unique identifier for this UI component.

`title` - Title string rendered on the UI.

`description` - Description string rendered on the UI. 

`x` - x-axis values.

`y` - y-axis values.

## Usage
```python
from greppo import app

app.bar_chart(
    name="A bar chart",
    title="Test title",
    description="A simple bar chart",
    x = ['1', '2', '3', '4'],
    y=[1, 2, 3, 4,],
)
```
