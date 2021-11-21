import unittest
from unittest import mock
import os
import io


class Tests(unittest.TestCase):
    def test_return_unused_uid_gid(self):
        real = os
        real.popen = mock.MagicMock()
        real.popen.return_value = io.TextIOWrapper(io.BytesIO(b""" \n[ 5] DCPomaticRemote          ALLOW IN    Anywhere 
[47] DCPomaticRemote                ALLOW IN    Anywhere (v6)   """))
        from src.bin import remove_ufw_rules
        real.popen.assert_has_calls(
            [
                mock.call("ufw status numbered | grep DCPomaticRemote"),
                mock.call("ufw --force delete 5"),
                mock.call("ufw --force delete 47")
            ]
        )
