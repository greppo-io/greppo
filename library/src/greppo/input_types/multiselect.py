from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import List
from typing import Union


SELECT_TYPES = Union[int, float, str, bool]


@dataclass
class Multiselect:
    def __init__(
        self,
        name: str,
        options: List[SELECT_TYPES],
        default: List[SELECT_TYPES],
        input_updates: Dict[str, Any] = {},
    ):
        self.input_name = name
        self.options = options
        self.default = default

        self.input_updates = input_updates

    def get_value(self):
        id, name = self.input_name.split("_")
        return self.input_updates.get(name, self.default)

    def convert_to_component_info(self):
        _id, name = self.input_name.split("_")
        _type = Multiselect.__name__
        value = self.get_value()

        return MultiselectComponentInfo(
            id=_id, name=name, type=_type, value=value, options=self.options
        )

    @classmethod
    def proxy_name(cls):
        return "multiselect"

    def __repr__(self):
        return str(self.get_value())

    def __str__(self):
        return self.__repr__()


@dataclass
class MultiselectComponentInfo:
    id: str
    name: str
    type: str
    value: Union[
        int, float, str, bool
    ]  # This can represent the default user supplied value
    options: List[Any]
