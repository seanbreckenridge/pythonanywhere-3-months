import os
from time import time
from pathlib import Path

credential_file_name = ".pythonanywhere_credentials.yaml"
last_run_at_file_name = ".pythonanywhere_lastrun.txt"
last_run_at_absolute_path = os.path.abspath(os.path.join(Path.home(), last_run_at_file_name))
login_page = "https://www.pythonanywhere.com/login/"
