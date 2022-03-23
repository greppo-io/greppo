from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import List, Union

num = Union[int, float]
num_list = List[num]
num_num_list = Union[num, num_list]
str_list = List[str]
str_str_list = Union[str, str_list]
x_type = Union[int, float, str]

@dataclass
class Dataset:
    data: List[num_num_list]
    label: str
    backgroundColor: str
    borderColor: str
    fill: bool = False
    pointRadius = 10


@dataclass
class ChartData:
    labels: List[Any]
    datasets: List[Dataset]


# TODO handle multiple datasets.
@dataclass
class LineChart:
    def __init__(
        self,
        name: str,
        x: List[x_type],
        y: List[num_num_list],
        color: str_str_list = "#CCCCCC",
        label: str_str_list = '',
        description: str = '',
        input_updates: Dict[str, Any] = {},
    ):
        self.input_name = name
        self.description = description
        self.input_updates = input_updates

        if isinstance(y[0], list):
            dataset = []
            for idx in range(len(y)):              
                if isinstance(label, list) and (len(label) == len(y)): this_label = label[idx]
                else: raise ValueError('`label` passed in to the line_chart must be of same length as `y`')
                if isinstance(color, list) and (len(color) == len(y)): this_color = color[idx]
                else: raise ValueError('`color` passed in to the line_chart must be of same length as `y`')
                dataset.append(Dataset(label=this_label, data=y[idx],backgroundColor=this_color, borderColor=this_color))
            self.chartdata = ChartData(labels=x, datasets=dataset)
        else:
            if not bool(label):
                _, label = name.split("_")
            dataset = Dataset(label=label, data=y,backgroundColor=color, borderColor=color)
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
    description: str
    chartdata: ChartData
