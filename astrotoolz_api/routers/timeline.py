import json
import logging

import humps
from astrotoolz.timeline.timeline_factory_builder import build_timeline_factory
from fastapi import APIRouter, HTTPException, Response

from astrotoolz_api.model.timeline_request import TimelineRequest
from astrotoolz_api.routers.timeline_utils import to_timeline_config
from astrotoolz_api.utils.custom_json_encoder import CustomJSONEncoder

router = APIRouter(prefix="/timeline", tags=["timeline"])

logging.basicConfig(level=logging.DEBUG)


@router.post("/")
async def create_timeline(request: TimelineRequest):
    try:
        cfg = to_timeline_config(request)

        timeline_factory = build_timeline_factory(cfg)
        timeline = timeline_factory.create_timeline(cfg)

        timeline_json = json.dumps(timeline, cls=CustomJSONEncoder)
        camelcase_json = humps.camelize(timeline_json)

        return Response(content=camelcase_json, media_type="application/json")
    except Exception as e:
        logging.error(f"Error creating timeline: {e}")
        raise e
        # raise HTTPException(status_code=400, detail=str(e))
