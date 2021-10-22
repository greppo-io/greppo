from dataclasses import dataclass
from typing import Any


@dataclass
class Dataset:
    label: str
    backgroundColor: str
    data: list[Any]


@dataclass
class ChartData:
    labels: list[Any]
    datasets: list[Dataset]


# TODO doesn't handle multiple datasets.
@dataclass
class BarChart:
    def __init__(
        self,
        name: str,
        title: str,
        description: str,
        x: list,
        y: list,
        input_updates: dict[str, Any] = {},
    ):
        self.input_name = name
        self.title = title
        self.description = description
        self.input_updates = input_updates

        # background is defaulted
        dataset = Dataset(
            label=description, data=y, backgroundColor="#000000"
        )
        self.chartdata = ChartData(labels=x, datasets=[dataset])

    def get_value(self):
        return None

    def convert_to_component_info(self):
        _id, name = self.input_name.split("_")
        _type = BarChart.__name__
        title = self.title

        return BarChartComponentInfo(
            name=name,
            id=_id,
            type=_type,
            title=self.title,
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
    title: str
    description: str
    chartdata: ChartData
