from dataclasses import dataclass
from typing import Optional


@dataclass
class PackageItem:
    name: str
    new_version: str
    origin: str
    old_version: Optional[str] = None
