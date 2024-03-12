from typing import List, Type

from astrotoolz.core.enums import CoordinateSystem, NodeCalc, Zodiac
from astrotoolz.core.events.orb_calculator import StaticOrbCalculator
from astrotoolz.timeline.aspect_config import AspectsConfig
from astrotoolz.timeline.timeline_config import TimelineConfig

from astrotoolz_api.model.timeline_request import AspectRequest, TimelineRequest
from astrotoolz_api.utils.date_utls import parse_utc_date


def parse_to_timeline_config(request: TimelineRequest) -> TimelineConfig:
    coord_system = _parse_coordinate_system(request.coordinate_system)
    start_date = parse_utc_date(request.start_date)
    end_date = parse_utc_date(request.end_date)
    events = _parse_events(request.events) if request.events else []
    aspects = _parse_aspects(request.aspects) if request.aspects else []
    zodiacs = _parse_zodiacs(request.zodiacs) if request.zodiacs else []
    node_calc = _parse_node_calc(request.node_calc) if request.node_calc else None

    timeline_config = TimelineConfig(
        coord_system,
        start_date,
        end_date,
        request.interval_minutes,
        request.points,
        events,
        aspects,
        zodiacs,
        node_calc,
    )

    return timeline_config


def _parse_coordinate_system(coordinate_system: str) -> CoordinateSystem:
    return CoordinateSystem.from_string(coordinate_system)


def _parse_events(events: List[str]) -> List[Type]:
    if not events:
        return []
    event_classes = [globals().get(event) for event in events]
    if None in event_classes:
        missing_events = [
            event for event, cls in zip(events, event_classes) if cls is None
        ]
        raise ValueError(f"Unknown events: {', '.join(missing_events)}")
    return event_classes


def _parse_aspects(requests: List[AspectRequest]) -> List[AspectsConfig]:
    return [
        AspectsConfig(
            request.angle,
            request.family,
            StaticOrbCalculator(request.orb),
            request.targets,
        )
        for request in requests
    ]


def _parse_zodiacs(zodiacs: List[str]) -> List[Zodiac]:
    return [Zodiac.from_string(zodiac) for zodiac in zodiacs]


def _parse_node_calc(node_calc: str) -> NodeCalc:
    return NodeCalc.from_string(node_calc)
