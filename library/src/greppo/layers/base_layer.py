from dataclasses import dataclass
from typing import List, Union

def prepare_base_layer():
    id = uuid.uuid4().hex
    tile_provider = None

    if provider and isinstance(provider, str):
        try:
            tile_provider = xyzservices.providers.query_name(provider)
        except ValueError:
            raise ValueError(
                f"No matching provider found for: '{provider}'.")

    if isinstance(provider, xyzservices.TileProvider):
        tile_provider = provider

    if tile_provider is not None:
        name = name if name else tile_provider.name.replace(
            ".", " - ")
        url = url if url else tile_provider.build_url(fill_subdomain=False)
        attribution = attribution if attribution else tile_provider.attribution if 'attribution' in tile_provider else tile_provider.html_attribution
        subdomains = subdomains if subdomains else tile_provider.subdomains if 'subdomains' in tile_provider else ''
        
        return BaseLayer(id, name, visible, url, subdomains, attribution)
        
    else:
        if not name: raise ValueError("If 'provider' is not passed for 'base_layer', please pass in 'name'.")
        if not url: raise ValueError("If 'provider' is not passed for 'base_layer', please pass in 'url'.")
        
        return BaseLayer(id, name, visible, url, subdomains, attribution)
        

@dataclass()
class BaseLayer:
    id: str
    name: str
    visible: bool
    url: str
    subdomains: Union[str, List[str]]
    attribution: str
