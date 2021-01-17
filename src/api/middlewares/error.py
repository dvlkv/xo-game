from aiohttp.web import middleware, Response
from modules.errors import *
import json
from uuid import uuid4
import logging

@middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
    except FieldError as e:
        response = Response(
            body=json.dumps({"error": True}),
            content_type="application/json",
            status=400,
        )
    except UnauthorizedAccessError:
        response = Response(
            body=json.dumps({"error": True}),
            content_type="application/json",
            status=401,
        )
    except Exception as e:
        uuid = str(uuid4())
        response = Response(
            body=json.dumps({
                "error": True,
                "uuid": uuid,
                "text": "An unexpected error occurred. Please contact me by hi@dvlkv.ru\n Error code: {}".format(uuid)
            }),
            content_type="application/json",
            status=401,
        )
        logging.error("Error code: {}".format(uuid), exc_info=e)

    return response
