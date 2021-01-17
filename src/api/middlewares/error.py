from aiohttp.web import middleware, json_response
from aiohttp.web_exceptions import HTTPException
from modules.errors import *
import json
from uuid import uuid4
import logging

@middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
    except FieldError as e:
        response = json_response({
                "error": True,
                "field": e.field,
                "text": e.text
            },
            status=400,
        )
    except UnauthorizedAccessError:
        response = json_response({
                "error": True,
                "text": "You need to be authorized to use this method"
            },
            status=401,
        )
    except EntityAlreadyExists as e:
        response = json_response({
                "error": True,
                "text": e.text
            },
            status=409,
        )
    except HTTPException as e:
        response = json_response({
                "error": True,
                "text": e.text
            },
            status=e.status
        )
    except Exception as e:
        uuid = str(uuid4())
        response = json_response({
                "error": True,
                "uuid": uuid,
                "text": "An unexpected error occurred. Please contact me by hi@dvlkv.ru\n Error code: {}".format(uuid)
            },
            status=401,
        )
        logging.error(" {}".format(uuid), exc_info=e)

    return response
