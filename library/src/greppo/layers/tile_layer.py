from dataclasses import dataclass
from typing import List

@dataclass()
class TileLayer:
    id: str
    url: str
    name: str
    visible: bool
    opacity: float
    min_zoom: int
    max_zoom: int
    subdomains: List[str]
    attribution: str
