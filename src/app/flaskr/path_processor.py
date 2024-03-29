import os.path
import subprocess
try:
    from . import project_info_reader
except Exception as e:
    import project_info_reader
from typing import Union

vulnerable_characters = ["\\", "\"", "\n", "│", "#", ";", "$", "*", "=", "`", "&", "[", "]", "<", ">"]


def sanitize_input_path(req_path: str):
    """
    Sanitizes given path from possibly included injection
    :param req_path: Path to be sanitized
    :return: Sanitized path without injection payload
    """
    # removing vulnerable characters
    req_path = ''.join((filter(lambda ch: ch not in vulnerable_characters, req_path)))
    req_path = req_path.strip().replace("..", "").replace("//", "/")

    # removing leading and trailing whitespaces between /, occasionally also /
    req_path_split = req_path.split("/")
    req_path_split[:] = [item.strip() for item in req_path_split if item]
    req_path = "/".join(req_path_split)

    # removing the leading dots (.) and slashes (/)
    path_length = len(req_path)
    for char_num in range(path_length):
        if req_path[char_num] != "/" and req_path[char_num] != ".":
            path_length = char_num
            break
    req_path = req_path[path_length:]
    return req_path


def list_contents(req_path: str) -> Union[dict, tuple]:
    """
    Returns contents of folder of a given path as dictionary. In order to safety, path need to be first sanitized.
    :param req_path: Path of a folder
    :return: Dictionary of contents. Dictionary keys are content's names and values are information about each entry.
    If folder is not found, there will be an error message with "error" key
    """
    with subprocess.Popen(["ls", "-l", "-Q", req_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE) as execution:
        # OUT
        # total 52
        # drwxr-xr-x 3 owner group 4096 Nov  9 09:20 "Desktop"
        # drwxr-xr-x 2 owner group 4096 Jan  3  2021 "Documents"
        # drwxr-xr-x 8 owner group 4096 Nov 16 21:31 "Downloads"

        if execution.stderr.read():
            return 404, {"error": "Folder does not exist", "requested_path": req_path}

        list_dir = execution.stdout.readlines()

    contents = {}
    for entry in list_dir[1:]:
        entry = entry.decode("UTF-8")
        starting_index = entry.index("\"")
        # drwxr-xr-x 8 owner group 4096 Nov 16 21:31 "Downloads"
        # first occurrence of " will be divider       ^
        contents[entry[starting_index + 1:-2]] = entry[:starting_index - 1]
        # drwxr-xr-x 8 owner group 4096 Nov 16 21:31 "Downloads"
        #                                             ^-------^ folder name: start_at (divider + 1)
        #                                                       up to last character
        # ^----------------------------------------^ info: start_at (first_char) up to (divider -1 (doesnt count))

    return contents


def list_differentiate_dirs(req_path: str) -> Union[dict, tuple]:
    """
    Finds out if contents of a folder is a directory or a file.
    :param req_path: Path of a folder
    :return: Returns dictionary with content's names as a key and
    boolean of decision if entry is a folder or file as a value.
    """
    contents = list_contents(req_path)
    if contents == (404, {"error": "Folder does not exist", "requested_path": req_path}):
        return 404, {"error": "Folder does not exist", "requested_path": req_path}

    contents_dirs = {}
    for key, value in contents.items():
        if value[0] == "d":  # d as directory
            contents_dirs[key] = True
            continue
        if value[0] == "l":  # l as link
            continue
        contents_dirs[key] = False

    return contents_dirs


def list_differentiate_projects(req_path: str, return_all: bool = True) -> Union[dict, tuple]:
    """
    Finds out if contents of a folder is a file, a directory or a project.
    :param return_all: If false, all of returned dictionary keys represent either directory or project not a file.
    :param req_path: Path of a folder
    :return: Returns dictionary with content's names as a key and
    text values "file", "directory", "project" for a file, a directory or a project respectively.
    """
    contents = list_differentiate_dirs(req_path)
    if contents == (404, {"error": "Folder does not exist", "requested_path": req_path}):
        return 404, {"error": "Folder does not exist", "requested_path": req_path}
    project_contents = {}
    for key, value in contents.items():
        if return_all:  # both files and directories
            if not contents[key]:  # from list_differentiate_dirs is not dir, is file
                project_contents[key] = "file"
            else:  # from list_differentiate_dirs is dir so could be a project
                project_contents[key] = "directory"
                if project_info_reader.is_project(os.path.join(req_path, key)):
                    project_contents[key] = "project"
        else:  # only directories
            if value:  # if dir
                if project_info_reader.is_project(os.path.join(req_path, key)):
                    project_contents[key] = True

    return project_contents
