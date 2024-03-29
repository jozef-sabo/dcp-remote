import unittest
from src.app.flaskr import project_info_reader
import os


class Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.project_info = {
            "metadata_version": 37,
            "name": "",
            "content_type": "FTR",
            "container": 185,
            "resolution": "2K",
            "fps": 60,
            "audio_channels": 6,
            "ISDCF_metadata": {
                "audio_lang": "SK",
                "subtitle_lang": "CZ",
                "territory": "SK",
                "rating": "15"
            }, "content": [
                {
                    "file_name": "bbb_sunflower_1080p_60fps_normal.mp4",
                    "type": "video",
                    "fps": 60,
                    "length": 38072,
                    "width": 1920,
                    "height": 1080,
                    "ratio": 178,
                    "audio_length": 30457600,
                    "audio_fps": 48000
                },
                {
                    'file_name': 'Mediterranean.Food.2009.SPANISH.WEBRip.x264-VXT-English.srt',
                    'type': 'subtitles'
                },
                {
                    "file_name": "En-us-Slovakia.ogg",
                    "type": "audio",
                    "audio_length": 79872,
                    "audio_fps": 44100
                },
                {
                    "file_name": "bbb_sunflower_2160p_60fps_normal.mp4",
                    "type": "video",
                    "fps": 60,
                    "length": 38072,
                    "width": 3840,
                    "height": 2160,
                    "ratio": 178,
                    "audio_length": 30457600,
                    "audio_fps": 48000
                }
            ]
        }

    def tearDown(self) -> None:
        rm_path = os.path.join(os.path.dirname(__file__), "projects_testing/normal_folder")
        if os.path.isdir(rm_path):
            os.rmdir(rm_path)

    @classmethod
    def setUpClass(cls) -> None:
        project_info_reader.projects = {}

    def test_get_project(self):
        self.project_info["name"] = "Project_B"
        self.assertEqual(self.project_info, project_info_reader.get_project(
            os.path.join(os.path.dirname(__file__), "projects_testing/proj_b")))
        self.assertEqual(self.project_info, project_info_reader.get_project(
            os.path.join(os.path.dirname(__file__), "projects_testing/proj_b")))

        self.project_info["ISDCF_metadata"]["subtitle_lang"] = ""
        self.project_info["name"] = "Project_C"
        self.assertEqual(self.project_info, project_info_reader.get_project(
            os.path.join(os.path.dirname(__file__), "projects_testing/proj_c")))

        req_path = os.path.join(os.path.dirname(__file__), "projects_testing/normal_folder")
        os.mkdir(req_path)
        self.assertEqual(
            (404, {"error": f"Folder does not exist or the given path is not a project", "requested_path": req_path}),
            project_info_reader.get_project(req_path)
        )

        req_path = os.path.join(os.path.dirname(__file__), "projects_testing/proj_e")
        self.assertEqual(
            (404, {"error": f"The given path is not a project", "requested_path": req_path}),
            project_info_reader.get_project(req_path)
        )

    def test_read(self):
        self.project_info["name"] = "Project_A"
        self.assertEqual(self.project_info, project_info_reader.read(
            os.path.join(os.path.dirname(__file__), "projects_testing/proj_a")))
        self.project_info["name"] = "Project_B"
        self.assertEqual(self.project_info, project_info_reader.read(
            os.path.join(os.path.dirname(__file__), "projects_testing/proj_b")))

        self.project_info["ISDCF_metadata"]["subtitle_lang"] = ""
        self.project_info["name"] = "Project_C"
        self.assertEqual(self.project_info, project_info_reader.read(
            os.path.join(os.path.dirname(__file__), "projects_testing/proj_c")))

        self.project_info["name"] = "Project_D"
        self.project_info["content"].pop(3)
        self.project_info["content"].pop(1)
        self.project_info["content"].pop(0)
        self.assertEqual(self.project_info, project_info_reader.read(
            os.path.join(os.path.dirname(__file__), "projects_testing/proj_d")))

        with self.assertRaises(AttributeError):
            project_info_reader.read(os.path.join(os.path.dirname(__file__), "projects_testing/proj_e"))
        with self.assertRaises(ValueError):
            project_info_reader.read(os.path.join(os.path.dirname(__file__), "projects_testing/proj_f"))

    def test_is_project(self):
        self.assertTrue(project_info_reader.is_project(
            os.path.join(os.path.dirname(__file__), "projects_testing/proj_a")))
        self.assertTrue(project_info_reader.is_project(
            os.path.join(os.path.dirname(__file__), "projects_testing/proj_a"), forcibly_read=False))
        self.assertTrue(project_info_reader.is_project(
            os.path.join(os.path.dirname(__file__), "projects_testing/proj_a"), forcibly_read=True))

        self.assertFalse(project_info_reader.is_project(
            os.path.join(os.path.dirname(__file__), "projects_testing/proj_e")))
        os.mkdir(os.path.join(os.path.dirname(__file__), "projects_testing/normal_folder"))
        self.assertFalse(project_info_reader.is_project(
            os.path.join(os.path.dirname(__file__), "projects_testing/normal_folder")))
