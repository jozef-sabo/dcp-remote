import unittest
from src.app.flaskr import path_processor
import os
import shutil


class Tests(unittest.TestCase):
    def setUp(self) -> None:
        os.mkdir((os.path.join(os.path.dirname(__file__), "test")))

    def tearDown(self) -> None:
        shutil.rmtree((os.path.join(os.path.dirname(__file__), "test")))

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
        req_path = os.path.join(os.path.dirname(__file__), "test/test2")
        self.assertEqual(
            (404, {'error': 'Folder does not exist', "requested_path": req_path}),
            path_processor.list_contents(req_path)
        )
        os.mkdir(os.path.join(os.path.dirname(__file__), "test/test2"))
        open(os.path.join(os.path.dirname(__file__), "test/aa.txt"), "w").close()
        open(os.path.join(os.path.dirname(__file__), "test/bb.txt"), "w").close()

        list_dir = path_processor.list_contents(os.path.join(os.path.dirname(__file__), "test"))
        for value in list_dir.values():
            self.assertTrue(value)
        self.assertEqual(
            ["aa.txt", "bb.txt", "test2"],
            list(list_dir.keys())
        )

        open(os.path.join(os.path.dirname(__file__), "test/cc"), "w").close()
        self.assertEqual(
            ["aa.txt", "bb.txt", "cc", "test2"],
            list(path_processor.list_contents(os.path.join(os.path.dirname(__file__), "test")).keys())
        )

    def test_differentiate_dirs(self):
        req_path = os.path.join(os.path.dirname(__file__), "test/test2")
        self.assertEqual(
            (404, {'error': 'Folder does not exist', "requested_path": req_path}),
            path_processor.list_differentiate_dirs(req_path)
        )
        os.mkdir(os.path.join(os.path.dirname(__file__), "test/test2"))
        os.mkdir(os.path.join(os.path.dirname(__file__), "test/test3"))
        open(os.path.join(os.path.dirname(__file__), "test/aa.txt"), "w").close()
        open(os.path.join(os.path.dirname(__file__), "test/bb.txt"), "w").close()
        open(os.path.join(os.path.dirname(__file__), "test/cc"), "w").close()

        self.assertEqual(
            {
                "aa.txt": False,
                "bb.txt": False,
                "cc": False,
                "test2": True,
                "test3": True
            },
            path_processor.list_differentiate_dirs(os.path.join(os.path.dirname(__file__), "test"))
        )

        os.symlink(
            os.path.join(os.path.dirname(__file__), "test/test3"),
            os.path.join(os.path.dirname(__file__), "test/sl_to_test_3")
        )
        self.assertEqual(
            {
                "aa.txt": False,
                "bb.txt": False,
                "cc": False,
                "test2": True,
                "test3": True
            },
            path_processor.list_differentiate_dirs(os.path.join(os.path.dirname(__file__), "test"))
        )

        open(os.path.join(os.path.dirname(__file__), "test/dd.json"), "w").close()
        self.assertEqual(
            {
                "aa.txt": False,
                "bb.txt": False,
                "cc": False,
                "dd.json": False,
                "test2": True,
                "test3": True
            },
            path_processor.list_differentiate_dirs(os.path.join(os.path.dirname(__file__), "test"))
        )

    def test_differentiate_projects(self):
        req_path = os.path.join(os.path.dirname(__file__), "test/test2")
        self.assertEqual(
            (404, {'error': 'Folder does not exist', "requested_path": req_path}),
            path_processor.list_differentiate_projects(req_path)
        )

        os.mkdir(os.path.join(os.path.dirname(__file__), "test/test2"))
        os.mkdir(os.path.join(os.path.dirname(__file__), "test/test3"))
        open(os.path.join(os.path.dirname(__file__), "test/aa.txt"), "w").close()
        open(os.path.join(os.path.dirname(__file__), "test/bb.txt"), "w").close()
        open(os.path.join(os.path.dirname(__file__), "test/cc"), "w").close()

        self.assertEqual(
            {
                "aa.txt": "file",
                "bb.txt": "file",
                "cc": "file",
                "test2": "directory",
                "test3": "directory"
            },
            path_processor.list_differentiate_projects(os.path.join(os.path.dirname(__file__), "test"))
        )

        self.assertEqual(
            {},
            path_processor.list_differentiate_projects(os.path.join(os.path.dirname(__file__), "test"),
                                                       return_all=False)
        )

        shutil.copytree(os.path.join(os.path.dirname(__file__), "projects_testing/proj_b"),
                        os.path.join(os.path.dirname(__file__), "test/proj_b"))

        self.assertEqual(
            {
                "aa.txt": "file",
                "bb.txt": "file",
                "cc": "file",
                "proj_b": "project",
                "test2": "directory",
                "test3": "directory"
            },
            path_processor.list_differentiate_projects(os.path.join(os.path.dirname(__file__), "test"))
        )
        self.assertEqual(
            {"proj_b": True},
            path_processor.list_differentiate_projects(os.path.join(os.path.dirname(__file__), "test"),
                                                       return_all=False)
        )

        shutil.copytree(os.path.join(os.path.dirname(__file__), "projects_testing/proj_c"),
                        os.path.join(os.path.dirname(__file__), "test/proj_c"))

        self.assertEqual(
            {
                "aa.txt": "file",
                "bb.txt": "file",
                "cc": "file",
                "proj_b": "project",
                "proj_c": "project",
                "test2": "directory",
                "test3": "directory"
            },
            path_processor.list_differentiate_projects(os.path.join(os.path.dirname(__file__), "test"))
        )
        self.assertEqual(
            {
                "proj_b": True,
                "proj_c": True
            },
            path_processor.list_differentiate_projects(os.path.join(os.path.dirname(__file__), "test"),
                                                       return_all=False)
        )
