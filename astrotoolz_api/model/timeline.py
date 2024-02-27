from typing import List, Optional

from pydantic import BaseModel


class BasePosition(BaseModel):
    lon: float
    lat: float
    speed: float
    ra: float
    dec: float


class Tropical(BaseModel):
    zodiacal_position: str
    sign: str
    sign_ruler: str
    decan: str
    term: str
    house: int


class Vedic(BaseModel):
    zodiacal_position: str
    sign: str
    sign_ruler: str
    nakshatra: str
    nakshatra_lord: str
    house: int


class SourceOrTarget(BaseModel):
    base_position: BasePosition
    tropical: Tropical
    vedic: Vedic
    point: str
    retrograde: Optional[bool]
    stationary: Optional[bool]
    direction: Optional[str]


class Angle(BaseModel):
    source: SourceOrTarget
    target: SourceOrTarget
    abs_diff: float
    real_diff: float
    circular_diff: float


class AstroEvent(BaseModel):
    dt: str
    angle: Angle
    asp_type: str
    target_diff: int
    coord_system: str


class TimelineResponse(BaseModel):
    events: List[AstroEvent]
