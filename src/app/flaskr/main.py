import os
from flask import Flask, request, send_from_directory
import path_processor
import project_info_reader
import responsifier

ROOT_DIRECTORY = "/var/ftp/jefinko/"
IP = "192.168.1.20"
PORT = 8080
CORS = IP
responsifier.set_cors(CORS)

app = Flask(__name__, static_url_path="/static")


@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)


@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('static/js', path)


@app.route('/fonts/<path:path>')
def send_fonts(path):
    return send_from_directory('static/fonts', path)


@app.route("/")
def index():
    return send_from_directory('static', "index.html")


@app.route("/api/file_list", methods=['POST'])
def file_list():
    req_path = request.values.get("path", 0)
    if req_path == 0:
        return responsifier.make_response((400, {"error": "Path was not set"}))
    req_path = os.path.join(ROOT_DIRECTORY, path_processor.sanitize_input_path(req_path))
    dcpomatic_project_validate = request.values.get("validate_dcp_projects", False)

    if dcpomatic_project_validate:
        return responsifier.make_response(path_processor.list_differentiate_projects(req_path))
    return responsifier.make_response(path_processor.list_differentiate_dirs(req_path))


@app.route("/api/project_info", methods=['POST'])
def project_info():
    projects_directory = request.values.get("projects_directory", 0)
    project = request.values.get("project", 0)

    if project == 0 and projects_directory == 0:
        return responsifier.make_response((400, {"error": "Path was not set"}))

    if project != 0:
        req_path = os.path.join(ROOT_DIRECTORY, path_processor.sanitize_input_path(project))
        if project_info_reader.is_project(req_path):
            return responsifier.make_response(project_info_reader.get_project(req_path))
        else:
            return responsifier.make_response((404, {"error": "Project not found"}))

    else:
        sanitized_path = path_processor.sanitize_input_path(projects_directory)
        req_path = os.path.join(ROOT_DIRECTORY, sanitized_path)
        projects = [sanitized_path]
        projects_names = path_processor.list_differentiate_projects(req_path, return_all=False)

        if type(projects_names) == tuple:
            return responsifier.make_response(projects_names)

        for key in projects_names.keys():
            projects.append(project_info_reader.get_project(key))

        return responsifier.make_response(projects)


app.run(host=IP, port=PORT, debug=False)
