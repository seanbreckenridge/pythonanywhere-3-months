import sys
import os
import traceback
import logging
import argparse
from pathlib import Path

import yaml
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

credential_file_name = ".pythonanywhere_credentials.yaml"
login_page = "https://www.pythonanywhere.com/login/"
