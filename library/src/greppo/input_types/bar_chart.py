from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import List


@dataclass
class Dataset:
    label: str
    backgroundColor: str
    data: List[Any]


@dataclass
class ChartData:
    labels: List[Any]
    datasets: List[Dataset]


# TODO doesn't handle multiple datasets.
@dataclass
class BarChart:
    def __init__(
        self,
        name: str,
        description: str,
        x: List,
        y: List,
        color: str = "#000000",
        input_updates: Dict[str, Any] = {},
    ):
        self.input_name = name
        self.description = description
        self.input_updates = input_updates

        _, label = name.split("_")
        dataset = Dataset(label=label, data=y, backgroundColor=color)
        self.chartdata = ChartData(labels=x, datasets=[dataset])

    def get_value(self):
        return None

    def convert_to_component_info(self):
        _id, name = self.input_name.split("_")
        _type = BarChart.__name__

        return BarChartComponentInfo(
            name=name,
            id=_id,
            type=_type,
            description=self.description,
            chartdata=self.chartdata,
        )

    @classmethod
    def proxy_name(cls):
        return "bar_chart"

    def __repr__(self):
        return str(self.get_value())

    def __str__(self):
        return self.__repr__()


@dataclass
class BarChartComponentInfo:
    name: str
    id: str
    type: str
    description: str
    chartdata: ChartData
