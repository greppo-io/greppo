from dataclasses import dataclass
from typing import Any


@dataclass
class LayerControl:
    def __init__(self, base: bool, overlay: bool, input_updates: dict[str, Any] = {}):
        self.input_name = "Layer Control"
        self.base = base
        self.overlay = overlay

        self.input_updates = input_updates

    def get_value(self):
        return None

    def convert_to_component_info(self):
        base = self.base
        overlay = self.overlay
        _type = LayerControl.__name__

        return LayerControlComponentInfo(
            name=self.input_name, type=_type, base=base, overlay=overlay
        )

    @classmethod
    def proxy_name(cls):
        return "layer_control"

    def __repr__(self):
        return str(self.get_value())

    def __str__(self):
        return self.__repr__()


@dataclass
class LayerControlComponentInfo:
    name: str
    type: str
    base: bool
    overlay: bool
