import os.path
import subprocess
import project_info_reader
from typing import Union


def list_contents(req_path: str) -> Union[dict, tuple]:
    execution = subprocess.Popen(["ls", "-l", "-Q", req_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # OUT
    # total 52
    # drwxr-xr-x 3 owner group 4096 Nov  9 09:20 "Desktop"
    # drwxr-xr-x 2 owner group 4096 Jan  3  2021 "Documents"
    # drwxr-xr-x 8 owner group 4096 Nov 16 21:31 "Downloads"

    execution.wait()
    if execution.stderr.read():
        return 404, {"error": "Folder does not exist"}

    list_dir = execution.stdout.readlines()
    contents = {}
    for entry in list_dir[1:]:
        entry = entry.decode("UTF-8")
        starting_index = entry.index("\"")
        # drwxr-xr-x 8 owner group 4096 Nov 16 21:31 "Downloads"
        # first occurence of " will be divider       ^
        contents[entry[starting_index + 1:-2]] = entry[:starting_index - 1]
        # drwxr-xr-x 8 owner group 4096 Nov 16 21:31 "Downloads"
        #                                             ^-------^ folder name: start_at (divider + 1)
        #                                                       up to last character
        # ^----------------------------------------^ info: start_at (first_char) up to (divider -1 (doesnt count))

    return contents


def list_diferenciate_dirs(req_path: str) -> Union[dict, tuple]:
    contents = list_contents(req_path)
    if contents == (404, {"error": "Folder does not exist"}):
        return 404, {"error": "Folder does not exist"}
    for key, value in contents.items():
        if value[0] == "d":  # d as directory
            contents[key] = True
            continue
        if value[0] == "l":  # l as link
            contents.pop(key)
            continue
        contents[key] = False

    return contents


def list_diferenciate_projects(req_path: str, return_all: bool = True) -> Union[dict, tuple]:
    contents = list_diferenciate_dirs(req_path)
    if contents == (404, {"error": "Folder does not exist"}):
        return 404, {"error": "Folder does not exist"}
    project_contents = {}
    for key, value in contents.items():
        if return_all:  # both files and directories
            if not contents[key]:  # from list_diferenciate_dirs is not dir, is file
                project_contents[key] = "file"
            else:  # from list_diferenciate_dirs is dir so could be a project
                project_contents[key] = "directory"
                if project_info_reader.is_project(os.path.join(req_path, key)):
                    project_contents[key] = "project"
        else:  # only directories
            if value:  # if dir
                if project_info_reader.is_project(os.path.join(req_path, key)):
                    project_contents[key] = True

    return project_contents
