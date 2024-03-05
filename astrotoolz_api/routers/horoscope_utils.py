from typing import List

from astrotoolz.core.enums import CoordinateSystem, HouseSystem, NodeCalc, Zodiac
from astrotoolz.core.events.orb_calculator import DynamicOrbCalculator
from astrotoolz.horoscope.factory.horoscope_factory_config import HoroscopeFactoryConfig
from astrotoolz.horoscope.horoscope_config import HoroscopeConfig
from astrotoolz.timeline.aspect_config import AspectsConfig

from astrotoolz_api.model.horoscope_request import HoroscopeRequest
from astrotoolz_api.model.timeline_request import AspectRequest


def to_horoscope_factory_config(request: HoroscopeRequest) -> HoroscopeFactoryConfig:
    coord_system = CoordinateSystem.from_string(request.coordinate_system)
    node_calc = NodeCalc.from_string(request.node_calc) if request.node_calc else None
    return HoroscopeFactoryConfig(
        coord_system,
        (True if request.aspects else False),
        node_calc,
    )


def to_horoscope_config(request: HoroscopeRequest) -> HoroscopeConfig:
    aspects = _parse_aspects(request.aspects) if request.aspects else []
    zodiac = Zodiac.from_string(request.zodiac) if request.zodiac else None
    house_system = (
        HouseSystem.from_string(request.house_system) if request.house_system else None
    )

    return HoroscopeConfig(
        request.name,
        request.points,
        request.lat,
        request.lon,
        aspects,
        zodiac,
        house_system,
    )


def _parse_aspects(requests: List[AspectRequest]) -> List[AspectsConfig]:
    return [
        AspectsConfig(
            request.angle,
            request.family,
            DynamicOrbCalculator(),
            request.targets,
        )
        for request in requests
    ]
