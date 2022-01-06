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
from .text import Text
from .text import TextComponentInfo
from .select import Select
from .select import SelectComponentInfo
from .display import Display
from .display import DisplayComponentInfo

# TODO add interface to inputs
GreppoCharts = Union[BarChart, LineChart]
GreppoChartNames = [i.proxy_name() for i in GreppoCharts.__args__]

GreppoInputs = Union[Display, Number, Text, Select, Multiselect, DrawFeature]
GreppoInputsNames = [i.proxy_name() for i in GreppoInputs.__args__]

ComponentInfo = Union[
    DisplayComponentInfo,
    NumberComponentInfo,
    TextComponentInfo,
    SelectComponentInfo,
    MultiselectComponentInfo,
    DrawFeatureComponentInfo,
    BarChartComponentInfo,
    LineChartComponentInfo,
]
