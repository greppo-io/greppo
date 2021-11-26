from dataclasses import dataclass
from typing import Any
from typing import Dict
from typing import List
from typing import Union


SELECT_TYPES = Union[int, float, str, bool]


@dataclass
class Select:
    def __init__(
        self,
        name: str,
        options: List[SELECT_TYPES],
        default: SELECT_TYPES,
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
        _type = Select.__name__
        value = str(self.get_value())

        return SelectComponentInfo(
            id=_id, name=name, type=_type, value=value, options=self.options
        )

    @classmethod
    def proxy_name(cls):
        return "select"

    def __repr__(self):
        return str(self.get_value())

    def __str__(self):
        return self.__repr__()


@dataclass
class SelectComponentInfo:
    id: str
    name: str
    type: str
    value: Union[
        int, float, str, bool
    ]  # This can represent the default user supplied value
    options: List[Any]
