import unittest
from src.app.flaskr import path_processor
import os
import shutil


class Tests(unittest.TestCase):
    def setUp(self) -> None:
        os.mkdir((os.path.join(os.getcwd(), "test")))

    def tearDown(self) -> None:
        shutil.rmtree((os.path.join(os.getcwd(), "test")))

    def test_sanitize_input_upper_folder(self):
        self.assertEqual("", path_processor.sanitize_input_path(""))
        self.assertEqual("", path_processor.sanitize_input_path("/"))
        self.assertEqual("", path_processor.sanitize_input_path("///"))
        self.assertEqual("", path_processor.sanitize_input_path("///../"))
        self.assertEqual("", path_processor.sanitize_input_path("../../../"))
        self.assertEqual("bin", path_processor.sanitize_input_path("../../../bin"))
        self.assertEqual("root/bin", path_processor.sanitize_input_path("./../../root/bin/"))
        self.assertEqual("bin", path_processor.sanitize_input_path("/bin/../../../"))
        self.assertEqual("bin", path_processor.sanitize_input_path("bin/"))

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

    def test_list_contents(self):
        self.assertEqual(
            (404, {'error': 'Folder does not exist'}),
            path_processor.list_contents(os.path.join(os.getcwd(), "test/test2"))
        )
        os.mkdir(os.path.join(os.getcwd(), "test/test2"))
        open("test/aa.txt", "w").close()
        open("test/bb.txt", "w").close()

        list_dir = path_processor.list_contents(os.path.join(os.getcwd(), "test"))
        for value in list_dir.values():
            self.assertTrue(value)
        self.assertEqual(
            ["aa.txt", "bb.txt", "test2"],
            list(list_dir.keys())
        )

        open("test/cc", "w").close()
        self.assertEqual(
            ["aa.txt", "bb.txt", "cc", "test2"],
            list(path_processor.list_contents(os.path.join(os.getcwd(), "test")).keys())
        )

    def test_differentiate_dirs(self):
        self.assertEqual(
            (404, {'error': 'Folder does not exist'}),
            path_processor.list_differentiate_dirs(os.path.join(os.getcwd(), "test/test2"))
        )
        os.mkdir(os.path.join(os.getcwd(), "test/test2"))
        os.mkdir(os.path.join(os.getcwd(), "test/test3"))
        open("test/aa.txt", "w").close()
        open("test/bb.txt", "w").close()
        open("test/cc", "w").close()

        self.assertEqual(
            {
                "aa.txt": False,
                "bb.txt": False,
                "cc": False,
                "test2": True,
                "test3": True
            },
            path_processor.list_differentiate_dirs(os.path.join(os.getcwd(), "test"))
        )

        os.symlink(
            os.path.join(os.getcwd(), "test/test3"),
            os.path.join(os.getcwd(), "test/sl_to_test_3")
        )
        self.assertEqual(
            {
                "aa.txt": False,
                "bb.txt": False,
                "cc": False,
                "test2": True,
                "test3": True
            },
            path_processor.list_differentiate_dirs(os.path.join(os.getcwd(), "test"))
        )

        open("test/dd.json", "w").close()
        self.assertEqual(
            {
                "aa.txt": False,
                "bb.txt": False,
                "cc": False,
                "dd.json": False,
                "test2": True,
                "test3": True
            },
            path_processor.list_differentiate_dirs(os.path.join(os.getcwd(), "test"))
        )

    def test_differentiate_projects(self):
        self.assertEqual(
            (404, {'error': 'Folder does not exist'}),
            path_processor.list_differentiate_projects(os.path.join(os.getcwd(), "test/test2"))
        )


if __name__ == '__main__':
    unittest.main()
