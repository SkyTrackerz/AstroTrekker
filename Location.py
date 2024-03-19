from dataclasses import dataclass

@dataclass
class Location:
    latitude: float = 0
    longitude: float = 0
    elevation: float = 0