from dataclasses import dataclass
from typing import List


@dataclass()
class BaseLayer:
    id: str
    name: str
    visible: bool
    url: str
    subdomains: List[str]
    attribution: str
