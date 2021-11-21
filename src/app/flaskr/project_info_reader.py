import os
from lxml import etree  # faster than xml.ElementTree
import time
from typing import Union

projects = {}
TIME_TO_LIVE = 5 * 60


def read(path_to_folder: str) -> dict:
    metadata_file = os.path.join(path_to_folder, "metadata.xml")

    tree = etree.parse(metadata_file)
    root = tree.getroot()
    metadata = {
        "metadata_version": int(root.find("Version").text),
        "name": root.find("Name").text,
        "content_type": root.find("DCPContentType").text,
        "container": int(root.find("Container").text),
        "resolution": root.find("Resolution").text,
        "fps": int(root.find("VideoFrameRate").text),
        "audio_channels": int(root.find("AudioChannels").text),
        "ISDCF_metadata": {
            "audio_lang": root.find("ISDCFMetadata").find("AudioLanguage").text,
            "territory": root.find("ISDCFMetadata").find("Territory").text,
            "rating": root.find("ISDCFMetadata").find("Rating").text,
        },
        "content": []
    }

    subtitle_lang_tag = root.find("ISDCFMetadata").find("SubtitleLanguage")
    if subtitle_lang_tag is not None:
        metadata["ISDCF_metadata"]["subtitle_lang"] = subtitle_lang_tag.text
    else:
        metadata["ISDCF_metadata"]["subtitle_lang"] = ""

    playlist = root.find("Playlist")
    for content in playlist:
        if content.tag == "Content":
            content_dict = {
                "file_name": content.find("Path").text.split("/")[-1],
                "type": "audio"
            }

            if content.find("VideoLength") is not None:
                content_dict["type"] = "video"
                content_dict["fps"] = int(content.find("VideoFrameRate").text)
                content_dict["length"] = int(content.find("VideoLength").text)
                content_dict["width"] = int(content.find("VideoWidth").text)
                content_dict["height"] = int(content.find("VideoHeight").text)
                content_dict["ratio"] = int(content.find("Scale").find("Ratio").text)

            audio_stream = content.find("AudioStream")
            content_dict["audio_length"] = int(audio_stream.find("Length").text)
            content_dict["audio_fps"] = int(audio_stream.find("FrameRate").text)

            metadata["content"].append(content_dict)

    projects[path_to_folder.split("/")[-1]] = [metadata, int(time.time())]
    return metadata


def is_project(path_to_folder: str, forcibly_read: bool = False) -> bool:
    project_name = path_to_folder.split("/")[-1]
    if not forcibly_read:
        if project_name in projects:
            if int(time.time()) - projects[project_name][1] < TIME_TO_LIVE:
                return projects[project_name][0]

    try:
        metadata = read(path_to_folder)
    except AttributeError:
        return False
    except OSError:
        return False
    else:
        projects[project_name] = [metadata, int(time.time())]
        return True


def get_project(path_to_folder: str) -> Union[dict, tuple]:
    project_name = path_to_folder.split("/")[-1]

    metadata = projects.get(project_name)
    if metadata:
        if int(time.time()) - projects[project_name][1] < TIME_TO_LIVE:
            return projects[project_name][0]

    try:
        metadata = read(path_to_folder)
    except AttributeError:
        return 404, {"error": f"The given path is not a project", "requested_path": path_to_folder}
    except OSError:
        return 404, {"error": f"Folder does not exist or the given path is not a project",
                     "requested_path": path_to_folder}
    else:
        projects[project_name] = [metadata, int(time.time())]
        return metadata
