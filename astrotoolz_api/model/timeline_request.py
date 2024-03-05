from typing import List

from astrotoolz_api.utils.camel_model import CamelModel


class AspectRequest(CamelModel):
    angle: int
    family: bool
    orb: float | None = None
    targets: List[str] | None = None


class TimelineRequest(CamelModel):
    coordinate_system: str
    start_date: str
    end_date: str
    interval_minutes: int
    points: List[str]
    events: List[str] | None = None
    aspects: List[AspectRequest] | None = None
    zodiacs: List[str] | None = None
    node_calc: str | None = None
