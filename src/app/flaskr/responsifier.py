from flask import Response
from typing import Union
import json

CORS = ""
C_TYPE_PLAIN = "text/plain; charset=UTF-8"
C_TYPE_JSON = "application/json; charset=UTF-8"


def set_cors(cors: str) -> None:
    """
    Changes default CORS value.
    :param cors: IP address or hostname of website where data will be shown
    """
    global CORS
    CORS = cors


def make_response(data: Union[dict, tuple, str, list], **kwargs) -> Response:
    """
    Takes given data and makes a response out of them. Default status_code is 200 (OK). \n
    Reformable data types:
        - **string**: Returns response of text type
        - **list**: JSON-ifies the list and returns it in json-format response
        - **dictionary**:  JSON-ifies the dictionary and returns it in json-format response
        - **tuple**: Finds the integer value which will be set as status_code. If there are present two integer values,
        the status code will be the second value. Processing of the non-status_code value is described above
    :param data: Data of optional data type
    :param kwargs: cors: create response with other (local) CORS value. It doesn't rewrite the global value.
    :return: Final response object which could already be returned to the user
    """
    cors = kwargs.get("cors", CORS)
    if type(data) == tuple and len(data) == 1:
        data = data[0]

    if type(data) == str:
        response = Response(
            data,
            status=200
        )
        response.headers["Access-Control-Allow-Origin"] = cors
        response.headers["Content-Type"] = C_TYPE_PLAIN
        return response

    if type(data) == dict or type(data) == list:
        response = Response(
            json.dumps(data),
            status=200
        )
        if type(data) == dict:
            if data.get("error") is not None:
                response = Response(
                    json.dumps(data),
                    status=404
                )
        response.headers["Access-Control-Allow-Origin"] = cors
        response.headers["Content-Type"] = C_TYPE_JSON
        return response

    text = ""
    content_type = C_TYPE_PLAIN
    if type(data[0]) == int:  # (200, 200)
        if type(data[1]) == int:  # (text: 200, response_code: 200)
            text = str(data[0])
        else:  # (text: 200, response_code: "text")
            data = (data[1], data[0])

    status_code = data[1] if type(data[1]) == int else 200
    if type(data[0]) == str:
        text = data[0]

    if type(data[0]) == dict or type(data[0]) == list:
        text = json.dumps(data[0])
        content_type = C_TYPE_JSON

    response = Response(
        text,
        status=status_code
    )
    response.headers["Access-Control-Allow-Origin"] = cors
    response.headers["Content-Type"] = content_type

    return response
