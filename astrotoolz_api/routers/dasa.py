import json
import logging

import humps
import pytz
from astrotoolz.core.enums import NodeCalc, Zodiac
from astrotoolz.core.points import MOON
from astrotoolz.core.positions.factory.geo_factory import GeoFactory
from astrotoolz.core.zodiac.mapper.position_mapper import PositionMapper
from astrotoolz.dasa.dasa import DasaLevel
from astrotoolz.dasa.dasa_factory import generate_dasas
from fastapi import APIRouter, Response

from astrotoolz_api.model.dasa_request import DasaRequest
from astrotoolz_api.utils.custom_json_encoder import CustomJSONEncoder
from astrotoolz_api.utils.date_utls import parse_utc_date

router = APIRouter(prefix="/dasa", tags=["horoscope"])

logging.basicConfig(level=logging.DEBUG)


@router.post("/")
def create_dasa(request: DasaRequest):
    try:
        birth_date = parse_utc_date(request.birth_date).astimezone(pytz.utc)
        dasa_level = DasaLevel.from_string(request.dasa_level)

        position_factory = GeoFactory(NodeCalc.MEAN)
        position_mapper = PositionMapper()
        moon_position = position_factory.create_position(MOON, birth_date)
        moon_mapped = position_mapper.map_position(moon_position, [Zodiac.SIDEREAL])

        dasas = generate_dasas(moon_mapped, dasa_level)

        horoscope_json = json.dumps(dasas, cls=CustomJSONEncoder)
        camelcase_json = humps.camelize(horoscope_json)

        return Response(content=camelcase_json, media_type="application/json")
    except Exception as e:
        logging.error(e)
        return Response(content="Internal Server Error", status_code=500)
