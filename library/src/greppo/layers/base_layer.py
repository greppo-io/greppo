from dataclasses import dataclass
from typing import List, Union
import xyzservices
import uuid


@dataclass
class BaseLayerComponent:
    def __init__(
        self,
        provider: Union[str, xyzservices.TileProvider] = '',
        name: str = '',
        visible: bool = False,
        url: str = '',
        attribution: str = '',
        subdomains: Union[str, List[str]] = '',
        min_zoom: int = 0,
        max_zoom: int = 18,
        bounds: List[List[int]] = [],
    ):
        self.provider = provider
        self.name = name
        self.visible = visible
        self.url = url
        self.attribution = attribution
        self.subdomains = subdomains
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        self.bounds = bounds

    def convert_to_dataclass(self):
        id = uuid.uuid4().hex
        tile_provider = None

        if self.provider and isinstance(self.provider, str):
            try:
                tile_provider = xyzservices.providers.query_name(self.provider)
            except ValueError:
                raise ValueError(
                    f"No matching provider found for: '{self.provider}'.")

        if isinstance(self.provider, xyzservices.TileProvider):
            tile_provider = self.provider

        if tile_provider is not None:
            name = self.name if self.name else tile_provider.name.replace(
                ".", " - ")
            url = self.url if self.url else tile_provider.build_url(
                fill_subdomain=False)
            attribution = self.attribution if self.attribution else tile_provider.attribution if 'attribution' in tile_provider else tile_provider.html_attribution
            subdomains = self.subdomains if self.subdomains else tile_provider.subdomains if 'subdomains' in tile_provider else ''

            return BaseLayer(id, name=name, visible=self.visible, url=url, subdomains=subdomains, attribution=attribution)

        else:
            if not self.name:
                raise ValueError(
                    "If 'provider' is not passed for 'base_layer', please pass in 'name'.")
            if not self.url:
                raise ValueError(
                    "If 'provider' is not passed for 'base_layer', please pass in 'url'.")

            return BaseLayer(id, name=self.name, visible=self.visible, url=self.url, subdomains=self.subdomains, attribution=self.attribution)


@dataclass()
class BaseLayer:
    id: str
    name: str
    visible: bool
    url: str
    subdomains: Union[str, List[str]]
    attribution: str
