from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import Union

import numpy as np
import pandas as pd


@dataclass
class Display:
    def __init__(self, name: str, value: str, input_updates: Dict[str, Any] = {}):
        self.input_name = name
        self.value = value

    def get_value(self):
        id, name = self.input_name.split("_")

        return self.value

    def convert_to_component_info(self):
        _id, name = self.input_name.split("_")
        _type = Display.__name__
        value = str(self.get_value())

        return DisplayComponentInfo(id=_id, name=name, type=_type, value=value)

    @classmethod
    def proxy_name(cls):
        return "display"

    def __repr__(self):
        return str(self.get_value())

    def __str__(self):
        return self.__repr__()


@dataclass
class DisplayComponentInfo:
    id: str
    name: str
    type: str
    value: Any
