import subprocess


def encode(project_name: str):
    with open("../output.txt", "w", encoding="UTF-8") as f:
        proc = subprocess.Popen(["dcpomatic2_cli", project_name], stdout=f, stderr=f)
        with open("../encoding.pid", "w", encoding="UTF-8") as pid_file:
            pid_file.write(str(proc.pid))
