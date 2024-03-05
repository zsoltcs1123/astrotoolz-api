from typing import List

from astrotoolz_api.model.timeline_request import AspectRequest
from astrotoolz_api.utils.camel_model import CamelModel


class HoroscopeRequest(CamelModel):
    name: str
    date: str
    coordinate_system: str
    points: List[str]
    lat: float | None = None
    lon: float | None = None
    aspects: List[AspectRequest] | None = None
    zodiac: str | None = None
    node_calc: str | None = None
    house_system: str | None = None
