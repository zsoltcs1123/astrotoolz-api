import json
import logging

import humps
from astrotoolz.horoscope.factory.horoscope_factory_builder import (
    build_horoscope_factory,
)
from fastapi import APIRouter, Response

from astrotoolz_api.model.horoscope_request import HoroscopeRequest
from astrotoolz_api.routers.horoscope_utils import (
    to_horoscope_config,
    to_horoscope_factory_config,
)
from astrotoolz_api.utils.custom_json_encoder import CustomJSONEncoder
from astrotoolz_api.utils.date_utls import parse_utc_date

router = APIRouter(prefix="/horoscope", tags=["horoscope"])

logging.basicConfig(level=logging.DEBUG)


@router.post("/")
async def create_horoscope(request: HoroscopeRequest):
    try:
        factory_cfg = to_horoscope_factory_config(request)
        horoscope_factory = build_horoscope_factory(factory_cfg)

        cfg = to_horoscope_config(request)
        date = parse_utc_date(request.date)
        horoscope = horoscope_factory.create_horoscope(date, cfg)

        horoscope_json = json.dumps(horoscope, cls=CustomJSONEncoder)
        camelcase_json = humps.camelize(horoscope_json)

        return Response(content=camelcase_json, media_type="application/json")
    except Exception as e:
        logging.error(f"Error creating horoscope: {e}")
        raise e
        # raise HTTPException(status_code=400, detail=str(e))
