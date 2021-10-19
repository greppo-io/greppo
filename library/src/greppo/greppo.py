import dataclasses
import json
import logging
import uuid
from typing import Any
from typing import List

from greppo import osm
from geopandas import GeoDataFrame as gdf
from .input_types import BarChart
from .input_types import ComponentInfo
from .input_types import DrawFeature
from .input_types import GreppoInputs
from .input_types import LineChart
from .input_types import Multiselect
from .input_types import Number
from .input_types import Select
from .layers.base_layer import BaseLayer
from .layers.overlay_layer import OverlayLayer


class GreppoApp(object):
    """
    The main Greppo class that is the entry point for user scripts. User scripts will use this class via a module
    import variable `gpo`.

    This class provides an interface around available frontend component elements. The methods simply point to the
    backend representation of those frontend component elements (ie. `Number` is the backend class that a user script
    can access via `self.number`.
    """

    def __init__(self, title: str = "Untitled App"):
        self.title: str = title

        self.select = Select
        self.multiselect = Multiselect
        self.draw_feature = DrawFeature
        self.bar_chart = BarChart
        self.line_chart = LineChart

    # UX component proxy methods
    @staticmethod
    def number():
        """
        Interactive Number value rendered on the frontend.
        """
        return Number


class GreppoAppProxy(object):
    """
    Proxy object that mirrors the `GreppoApp` class. Adds additional methods that user scripts don't need to know about.
    These methods are used by a Greppo server to obtain an output from the user script that is then rendered by the
    frontend.
    """
    def __init__(self):
        # Map component data
        self.base_layers: List[BaseLayer] = []
        self.overlay_layers: List[OverlayLayer] = []
        self.registered_inputs: List[ComponentInfo] = []

        # Input updates
        self.inputs = {}

    def number(self, **kwargs):
        number = Number(**kwargs)
        self.register_input(number)
        return number

    def select(self, **kwargs):
        select = Select(**kwargs)
        self.register_input(select)
        return select

    def multiselect(self, **kwargs):
        multiselect = Multiselect(**kwargs)
        self.register_input(multiselect)
        return multiselect

    def draw_feature(self, **kwargs):
        draw_feature = DrawFeature(**kwargs)
        self.register_input(draw_feature)
        return draw_feature

    def bar_chart(self, **kwargs):
        bar_chart = BarChart(**kwargs)
        self.register_input(bar_chart)
        return bar_chart

    def line_chart(self, **kwargs):
        line_chart = LineChart(**kwargs)
        self.register_input(line_chart)
        return line_chart

    def base_layer(
        self,
        name: str,
        visible: bool,
        url: str,
        subdomains: List[str],
        attribution: str,
    ):
        id = uuid.uuid4().hex
        self.base_layers.append(
            BaseLayer(id, name, visible, url, subdomains, attribution)
        )

    def overlay_layer(
        self, data: gdf, title: str, description: str, style: dict, visible: bool
    ):
        id = uuid.uuid4().hex
        minx = data.geometry.bounds.minx.min()
        miny = data.geometry.bounds.miny.min()
        maxx = data.geometry.bounds.maxx.max()
        maxy = data.geometry.bounds.maxy.max()
        bnds = [miny, minx, maxy, maxx]
        viewzoom = [(miny + maxy) / 2, (minx + maxx) / 2, osm.Map(bnds).z]
        self.overlay_layers.append(
            OverlayLayer(id, data, title, description, style, visible, viewzoom)
        )

    def update_inputs(self, inputs: dict[str, Any]):
        self.inputs = inputs

    def register_input(self, discovered_input: GreppoInputs):
        component_info = discovered_input.convert_to_component_info()
        self.registered_inputs.append(component_info)

        return discovered_input

    def gpo_prepare_data(self):
        """
        Take output of run script and setup the payload for the front-end to read.
        """

        app_output = {
            "base_layer_info": [],
            "overlay_layer_data": [],
            "component_info": [],
        }
        for _base_layer in self.base_layers:
            s = {}
            for k, v in _base_layer.__dict__.items():
                _v = v
                if k == "data":
                    _v = json.loads(v.to_json())
                s[k] = _v
            app_output["base_layer_info"].append(s)

        for _overlay_layer in self.overlay_layers:
            s = {}
            for k, v in _overlay_layer.__dict__.items():
                _v = v
                if k == "data":
                    _v = json.loads(v.to_json())
                s[k] = _v

            app_output["overlay_layer_data"].append(s)

        app_output["component_info"] = [
            dataclasses.asdict(i) for i in self.registered_inputs
        ]

        logging.info("Len component info: ", len(app_output["component_info"]))

        return app_output


app = GreppoApp()
