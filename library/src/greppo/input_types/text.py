from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import Union

import numpy as np
import pandas as pd

@dataclass
class Text:
    def __init__(self, name: str, value: str, input_updates: Dict[str, Any] = {}):
        self.input_name = name
        self.value = value

        self.input_updates = input_updates

    def get_value(self):
        id, name = self.input_name.split("_")
        return self.input_updates.get(name, self.value)

    def convert_to_component_info(self):
        _id, name = self.input_name.split("_")
        _type = Text.__name__
        value = str(self.get_value())

        return TextComponentInfo(id=_id, name=name, type=_type, value=value)

    @classmethod
    def proxy_name(cls):
        return "text"

    def __add__(self, other):
        if type(other) in [str]:
            return self.get_value() + other
        elif type(other) is Text:
            return self.get_value() + other.get_value()
        else:
            raise Exception("Operation Not Supported for type: " + str(type(other)))

    __radd__ = __add__

    def __mul__(self, other):
        if type(other) in [str]:
            return self.get_value() * other
        elif type(other) in [list, str, np.array, np.ndarray, pd.Series]:
            return other * self.get_value()
        elif type(other) is Text:
            return self.get_value() * other.get_value()
        else:
            raise Exception("Operation Not Supported for type: " + str(type(other)))

    __rmul__ = __mul__

    def __repr__(self):
        return str(self.get_value())

    def __str__(self):
        return self.__repr__()


@dataclass
class TextComponentInfo:
    id: str
    name: str
    type: str
    value: Any
