import os
from pathlib import Path

local_directory: str = os.environ.get(
    "XDG_DATA_HOME", os.path.join(Path.home(), ".local/share")
)
os.makedirs(local_directory, exist_ok=True)

credential_file_name: str = os.path.join(
    local_directory, "pythonanywhere_credentials.yaml"
)
last_run_at_file_name: str = os.path.join(local_directory, "pythonanywhere_lastrun.txt")
last_run_at_absolute_path: str = os.path.abspath(
    os.path.join(Path.home(), last_run_at_file_name)
)
login_page: str = "https://www.pythonanywhere.com/login/"
