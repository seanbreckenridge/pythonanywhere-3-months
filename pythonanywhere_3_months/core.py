#!/usr/local/env python3

import os
import sys
import traceback
import logging
import argparse
from time import time
from pathlib import Path
from typing import Tuple, Optional, Union

import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By

from . import (
    last_run_at_absolute_path,
    login_page,
)


def setup_debug_logging() -> None:
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s %(levelno)s - %(message)s"
    )


def create_webdriver(
    chromedriver_path: Union[str, None], hide: bool
) -> webdriver.Chrome:
    """Creates a webdriver, hides if requested."""
    options = webdriver.ChromeOptions()
    if hide:
        options.add_argument("headless")
        options.add_argument("disable-gpu")
        options.add_argument("window-size=1920x1080")
        logging.debug("Creating hidden chrome browser")
    service: Optional[webdriver.ChromeService] = None
    if chromedriver_path is not None:
        service = webdriver.ChromeService(chromedriver_path)
        logging.debug("Using custom chromedriver path: {}".format(chromedriver_path))
    return webdriver.Chrome(options=options, service=service)  # type: ignore


def get_options() -> Tuple[bool, str]:
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
        default=None,
    )
    parser.add_argument("-d", "--debug", help="Prints debug logs", action="store_true")
    args = parser.parse_args()
    if args.debug:
        setup_debug_logging()
    logging.debug("Custom chromedriver path: {}".format(args.chromedriver_path))
    return args.hidden, args.chromedriver_path


def get_credentials(filepath: str) -> Tuple[str, str]:
    """Gets pythonanywhere credentials from the dotfile"""
    absolute_path = os.path.abspath(os.path.join(Path.home(), filepath))
    logging.debug("Credential File Location: {}".format(absolute_path))
    with open(absolute_path, "r") as cred:
        creds = yaml.load(cred, Loader=yaml.FullLoader)
    return creds["username"], creds["password"]


# global variables so someone can monkey patch
# if they want to -- in case this breaks
LOGIN_ID = "id_auth-username"
PASSWORD_ID = "id_auth-password"
LOGIN_BUTTON = "id_next"
RUN_BUTTON_SELECTOR = "input.webapp_extend[type='submit']"


# encapsulate main functionality, can import any use in code instead
# of running from cmdline
def run(
    username: str, password: str, chromedriver_path: str, use_hidden: bool = False
) -> None:
    driver: Optional[webdriver.Chrome] = None
    try:
        driver = create_webdriver(chromedriver_path, use_hidden)

        # Login
        driver.get(login_page)
        email_input = driver.find_element(By.ID, LOGIN_ID)
        password_input = driver.find_element(By.ID, PASSWORD_ID)
        email_input.send_keys(username)
        password_input.send_keys(password)
        driver.find_element(By.ID, LOGIN_BUTTON).click()

        # Go to "Web" page
        driver.get(driver.current_url + "/webapps")

        # Click 'Run until 3 months from today'
        driver.find_element(By.CSS_SELECTOR, RUN_BUTTON_SELECTOR).click()

        # save current time to 'last run time file', so we can check if we need to run this again
        with open(last_run_at_absolute_path, "w") as f:
            f.write(str(time()))

        print("Done!", file=sys.stderr)
    except Exception:
        traceback.print_exc()
    finally:
        if driver:
            driver.quit()
