from flask import Response
from typing import Union
import json

CORS = ""
C_TYPE_PLAIN = "text/plain; charset=UTF-8"
C_TYPE_JSON = "application/json; charset=UTF-8"


def set_cors(cors: str):
    global CORS
    CORS = cors


def make_response(data: Union[dict, tuple, str, list], **kwargs) -> Response:
    cors = kwargs.get("cors", CORS)
    if type(data) == tuple and len(data) == 1:
        data = data[0]

    if type(data) == str:
        response = Response(
            data,
            status=200
        )
        response.headers["Cross-Origin-Resource-Policy"] = cors
        response.headers["Content-Type"] = C_TYPE_PLAIN
        return response

    if type(data) == dict or type(data) == list:
        response = Response(
            json.dumps(data),
            status=200
        )
        response.headers["Cross-Origin-Resource-Policy"] = cors
        response.headers["Content-Type"] = C_TYPE_JSON
        return response

    text = ""
    content_type = C_TYPE_PLAIN
    if type(data[0]) == int:  # (200, 200)
        if type(data[1]) == int:  # (text: 200, response_code: 200)
            text = str(data[0])
        else:  # (text: 200, response_code: "text")
            data = (data[1], data[0])

    status_code = data[1]
    if type(data[0]) == str:
        text = data[0]

    if type(data[0]) == dict or type(data) == list:
        text = json.dumps(data[0])
        content_type = C_TYPE_JSON

    response = Response(
        text,
        status=status_code
    )
    response.headers["Cross-Origin-Resource-Policy"] = cors
    response.headers["Content-Type"] = content_type

    return response
