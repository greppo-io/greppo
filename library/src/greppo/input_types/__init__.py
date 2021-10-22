from typing import Union

from .bar_chart import BarChart
from .bar_chart import BarChartComponentInfo
from .draw_feature import DrawFeature
from .draw_feature import DrawFeatureComponentInfo
from .line_chart import LineChart
from .line_chart import LineChartComponentInfo
from .multiselect import Multiselect
from .multiselect import MultiselectComponentInfo
from .number import Number
from .number import NumberComponentInfo
from .select import Select
from .select import SelectComponentInfo

# TODO add interface to inputs
GreppoInputs = Union[
    Number, Select, Multiselect, DrawFeature, BarChart, LineChart
]
GreppoInputsNames = [i.proxy_name() for i in GreppoInputs.__args__]

ComponentInfo = Union[
    NumberComponentInfo,
    SelectComponentInfo,
    MultiselectComponentInfo,
    DrawFeatureComponentInfo,
    BarChartComponentInfo,
    LineChartComponentInfo,
]
