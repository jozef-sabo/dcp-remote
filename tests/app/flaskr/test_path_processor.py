import unittest
from src.app.flaskr import path_processor


class Tests(unittest.TestCase):
    def test_sanitize_input_upper_folder(self):
        self.assertEqual("", path_processor.sanitize_input_path(""))
        self.assertEqual("", path_processor.sanitize_input_path("/"))
        self.assertEqual("", path_processor.sanitize_input_path("///"))
        self.assertEqual("", path_processor.sanitize_input_path("///../"))
        self.assertEqual("", path_processor.sanitize_input_path("../../../"))
        self.assertEqual("bin", path_processor.sanitize_input_path("../../../bin"))
        self.assertEqual("root/bin/", path_processor.sanitize_input_path("./../../root/bin/"))

    def test_sanitize_input_injection(self):
        self.assertEqual("", path_processor.sanitize_input_path("\";"))
        self.assertEqual("cat/etc/passwd", path_processor.sanitize_input_path("\"; cat /etc/passwd"))
        self.assertEqual("uname -a", path_processor.sanitize_input_path("\"; uname -a"))
        self.assertEqual("ps -ef", path_processor.sanitize_input_path("\";  	ps -ef "))
        self.assertEqual("cat/etc/passwd", path_processor.sanitize_input_path("\" && cat /etc/passwd"))
        self.assertEqual("uname -a", path_processor.sanitize_input_path("\" && uname -a"))
        self.assertEqual("ps -ef", path_processor.sanitize_input_path("\"; && ps -ef "))
        self.assertEqual("root/bin/sbin  ps -ef", path_processor.sanitize_input_path("/root/bin/sbin && ps -ef "))
        self.assertEqual("root/bin/sbin ps -ef", path_processor.sanitize_input_path("/root/bin/sbin \nps -ef"))


if __name__ == '__main__':
    unittest.main()
