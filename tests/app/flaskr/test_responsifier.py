import unittest
from src.app.flaskr import responsifier


class Tests(unittest.TestCase):
    def setUp(self) -> None:
        responsifier.set_cors("")

    def test_make_response_str(self):
        response = responsifier.make_response("Am I making a good response?")
        self.assertEqual(200, response.status_code)
        self.assertEqual(b"Am I making a good response?", response.data)
        self.assertEqual("utf-8", response.charset)
        self.assertEqual("text/plain; charset=UTF-8", response.content_type)
        self.assertEqual("", response.access_control_allow_origin)
        self.assertFalse(response.is_json)

        responsifier.set_cors("localhost")
        response = responsifier.make_response("Am I making a good response only to localhost?")
        self.assertEqual(200, response.status_code)
        self.assertEqual(b"Am I making a good response only to localhost?", response.data)
        self.assertEqual("utf-8", response.charset)
        self.assertEqual("text/plain; charset=UTF-8", response.content_type)
        self.assertEqual("localhost", response.access_control_allow_origin)
        self.assertFalse(response.is_json)

        response = responsifier.make_response("Am I making a good response only to 127.0.0.1?", cors="127.0.0.1")
        self.assertEqual(200, response.status_code)
        self.assertEqual(b"Am I making a good response only to 127.0.0.1?", response.data)
        self.assertEqual("utf-8", response.charset)
        self.assertEqual("text/plain; charset=UTF-8", response.content_type)
        self.assertEqual("127.0.0.1", response.access_control_allow_origin)
        self.assertFalse(response.is_json)

    def test_make_response_list(self):
        response = responsifier.make_response(["item_a", "item_b"])
        self.assertEqual(200, response.status_code)
        self.assertEqual(b'["item_a", "item_b"]', response.data)
        self.assertEqual("utf-8", response.charset)
        self.assertEqual("application/json; charset=UTF-8", response.content_type)
        self.assertTrue(response.is_json)

    def test_make_response_dict(self):
        response = responsifier.make_response(
            {
                "aa.txt": "file",
                "bb.txt": "file",
                "cc": "file",
                "proj_b": "project",
                "test2": "directory",
                "test3": "directory"
            }
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(b'{"aa.txt": "file", "bb.txt": "file", "cc": "file", "proj_b": "project", "test2": '
                         b'"directory", "test3": "directory"}', response.data)
        self.assertEqual("utf-8", response.charset)
        self.assertEqual("application/json; charset=UTF-8", response.content_type)
        self.assertTrue(response.is_json)

        # response out of error message
        response = responsifier.make_response(
            {
                "error": "Folder does not exist",
                "requested_path": "/root/path"
            }
        )
        self.assertEqual(404, response.status_code)
        self.assertEqual(b'{"error": "Folder does not exist", "requested_path": "/root/path"}', response.data)
        self.assertEqual("utf-8", response.charset)
        self.assertEqual("application/json; charset=UTF-8", response.content_type)
        self.assertTrue(response.is_json)

    def test_make_response_tuple(self):
        response = responsifier.make_response(("item_a",))
        # noinspection Duplicates
        self.assertEqual(200, response.status_code)
        self.assertEqual(b'item_a', response.data)
        self.assertEqual("utf-8", response.charset)
        self.assertEqual("text/plain; charset=UTF-8", response.content_type)
        self.assertFalse(response.is_json)

        response = responsifier.make_response(("item_a", "item_b"))
        # noinspection Duplicates
        self.assertEqual(200, response.status_code)
        self.assertEqual(b'item_a', response.data)
        self.assertEqual("utf-8", response.charset)
        self.assertEqual("text/plain; charset=UTF-8", response.content_type)
        self.assertFalse(response.is_json)

        response = responsifier.make_response((200, 404))
        # noinspection Duplicates
        self.assertEqual(404, response.status_code)
        self.assertEqual(b'200', response.data)
        self.assertEqual("utf-8", response.charset)
        self.assertEqual("text/plain; charset=UTF-8", response.content_type)
        self.assertFalse(response.is_json)

        response = responsifier.make_response((203, "404"))
        # noinspection Duplicates
        self.assertEqual(203, response.status_code)
        self.assertEqual(b'404', response.data)
        self.assertEqual("utf-8", response.charset)
        self.assertEqual("text/plain; charset=UTF-8", response.content_type)
        self.assertFalse(response.is_json)

        response = responsifier.make_response(("nooo", 205))
        # noinspection Duplicates
        self.assertEqual(205, response.status_code)
        self.assertEqual(b'nooo', response.data)
        self.assertEqual("utf-8", response.charset)
        self.assertEqual("text/plain; charset=UTF-8", response.content_type)
        self.assertFalse(response.is_json)

        response = responsifier.make_response((400, ["item_a", "item_b"]))
        # noinspection Duplicates
        self.assertEqual(400, response.status_code)
        self.assertEqual(b'["item_a", "item_b"]', response.data)
        self.assertEqual("utf-8", response.charset)
        self.assertEqual("application/json; charset=UTF-8", response.content_type)
        self.assertTrue(response.is_json)

        response = responsifier.make_response((["item_a", "item_b", "item_c"], 405))
        # noinspection Duplicates
        self.assertEqual(405, response.status_code)
        self.assertEqual(b'["item_a", "item_b", "item_c"]', response.data)
        self.assertEqual("utf-8", response.charset)
        self.assertEqual("application/json; charset=UTF-8", response.content_type)
        self.assertTrue(response.is_json)
