#!/usr/local/env python3

import os
import sys
import traceback
import logging
import argparse
import shutil
from time import time
from pathlib import Path
from typing import Tuple, Optional

import yaml
from selenium import webdriver  # type: ignore[import]
from selenium.webdriver.chrome.options import Options  # type: ignore[import]

from . import (
    last_run_at_absolute_path,
    login_page,
)


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelno)s - %(message)s")


def create_webdriver(chromedriver_path: str, hide: bool) -> webdriver.Chrome:
    """Creates a webdriver, hides if requested."""
    options = Options()
    if hide:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        logging.debug("Creating hidden chrome browser")
    return webdriver.Chrome(chromedriver_path, options=options)


def get_options() -> Tuple[str, bool]:
    """Gets options from user"""
    parser = argparse.ArgumentParser(
        description="Clicks the 'Run until 3 months from today' on pythonanywhere"
    )
    parser.add_argument(
        "-H", "--hidden", help="Hide the ChromeDriver.", action="store_true"
    )
    parser.add_argument(
        "-c",
        "--chromedriver-path",
        help="Provides the location of ChromeDriver. Should probably be the full path.",
        default=shutil.which("chromedriver"),
    )
    args = parser.parse_args()
    if args.chromedriver_path is None:
        logging.warning(
            "Couldn't find the location of a chromedriver. Provide one like '-c /path/to/chromedriver'"
        )
        sys.exit(1)
    else:
        logging.debug("Chromedriver path: {}".format(args.chromedriver_path))
    return args.hidden, args.chromedriver_path


def get_credentials(filepath: str) -> Tuple[str, str]:
    """Gets pythonanywhere credentials from the dotfile"""
    absolute_path = os.path.abspath(os.path.join(Path.home(), filepath))
    logging.debug("Credential File Location: {}".format(absolute_path))
    with open(absolute_path, "r") as cred:
        creds = yaml.load(cred, Loader=yaml.FullLoader)
    return creds["username"], creds["password"]


# global variables so someone can monkey patch
# if they want to -- incase this breaks
LOGIN_ID = "id_auth-username"
PASSWORD_ID = "id_auth-password"
LOGIN_BUTTON = "id_next"
RUN_BUTTON_SELECTOR = "input.webapp_extend[type='submit']"


# encapsulate main functionality, can import any use in code instead
# of running from cmdline
def run(
    username: str, password: str, chromedriver_path: str, use_hidden: bool = False
) -> None:
    try:
        driver: webdriver.Chrome = create_webdriver(chromedriver_path, use_hidden)

        # Login
        driver.get(login_page)
        email_input = driver.find_element_by_id(LOGIN_ID)
        password_input = driver.find_element_by_id(PASSWORD_ID)
        email_input.send_keys(username)
        password_input.send_keys(password)
        driver.find_element_by_id(LOGIN_BUTTON).click()

        # Go to "Web" page
        driver.get(driver.current_url + "/webapps")

        # Click 'Run until 3 months from today'
        driver.find_element_by_css_selector(RUN_BUTTON_SELECTOR).click()
    except:
        traceback.print_exc()
    finally:
        driver.quit()
        # save current time to 'last run time file', so we can check if we need to run this again
        with open(last_run_at_absolute_path, "w") as f:
            f.write(str(time()))
