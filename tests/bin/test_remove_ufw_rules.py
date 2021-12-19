import unittest
from unittest import mock
import builtins


class Tests(unittest.TestCase):
    @mock.patch.object(builtins, "open", mock.mock_open(
        read_data="""root:x:0:0:root:/root:/bin/bash\nusr1:x:650:650:usr1:/usr/sbin:/usr/sbin/nologin
usr2:x:700:700:usr2:/usr/sbin:/usr/sbin/nologin\nusr3:x:800:800:usr3:/usr/sbin:/usr/sbin/nologin
usr4:x:801:801:usr4:/usr/sbin:/usr/sbin/nologin\nusr5:x:803:802:usr5:/usr/sbin:/usr/sbin/nologin
usr6:x:804:803:usr6:/usr/sbin:/usr/sbin/nologin\nusr:x:805:805:usr7:/usr/sbin:/usr/sbin/nologin
usr8:x:808:850:usr8:/usr/sbin:/usr/sbin/nologin
"""))
    def test_remove_ufw_rules(self):
        with mock.patch("builtins.print") as mock_print:
            from src.bin import return_unused_uid_gid
            mock_print.assert_has_calls(
                [
                    mock.call("uuid", 802),
                    mock.call("ugid", 804),
                ]
            )
