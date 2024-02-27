import json
import logging

import humps
from astrotoolz.tools.timeline.timeline_factory_builder import build_timeline_factory
from fastapi import APIRouter, HTTPException, Request, Response

from astrotoolz_api.utils.custom_json_encoder import CustomJSONEncoder
from astrotoolz_api.utils.timeline_config_parser import parse_json_to_timeline_config

router = APIRouter(prefix="/timeline", tags=["timeline"])

logging.basicConfig(level=logging.DEBUG)


@router.post("/")
async def create_timeline(request: Request):
    try:
        # Receive the JSON payload as a string
        json_str = await request.body()
        # Convert bytes to string if necessary
        json_str = json_str.decode("utf-8")

        # Use your existing parser function
        cfg = parse_json_to_timeline_config(json_str)

        timeline_factory = build_timeline_factory(cfg)
        timeline = timeline_factory.create_timeline(cfg)

        timeline_json = json.dumps(timeline, cls=CustomJSONEncoder)
        camelcase_json = humps.camelize(timeline_json)

        return Response(content=camelcase_json, media_type="application/json")
    except Exception as e:
        logging.error(f"Error creating timeline: {e}")
        raise HTTPException(status_code=400, detail=str(e))
