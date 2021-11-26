from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import List
from typing import Optional


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
class LineChart:
    def __init__(
        self,
        name: str,  # title and name should be the same
        title: str,
        description: Optional[str],
        x,  # TODO needs typing
        y,
        backgroundColor: str = "#000000",
        input_updates: Dict[str, Any] = {},
    ):
        self.input_name = name
        self.title = title
        self.description = description
        self.input_updates = input_updates

        # background is defaulted
        dataset = Dataset(label=description, data=y, backgroundColor=backgroundColor)
        self.chartdata = ChartData(labels=x, datasets=[dataset])

    def get_value(self):
        return None

    def convert_to_component_info(self):
        _id, name = self.input_name.split("_")
        _type = LineChart.__name__

        return LineChartComponentInfo(
            name=name,
            id=_id,
            type=_type,
            title=self.title,
            description=self.description,
            chartdata=self.chartdata,
        )

    @classmethod
    def proxy_name(cls):
        return "line_chart"

    def __repr__(self):
        return str(self.get_value())

    def __str__(self):
        return self.__repr__()


@dataclass
class LineChartComponentInfo:
    name: str
    id: str
    type: str
    title: str
    description: str
    chartdata: ChartData
