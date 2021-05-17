#!/usr/local/env python3

import os
import sys
import traceback
import logging
import argparse
from time import time
from pathlib import Path

import yaml
from selenium import webdriver  # type: ignore[import]
from selenium.webdriver.chrome.options import Options  # type: ignore[import]

from pythonanywhere_3_months import (
    last_run_at_absolute_path,
    credential_file_name,
    login_page,
)


logging.basicConfig(level=logging.DEBUG, format="%(asctime)s %(levelno)s - %(message)s")


def create_webdriver(chromedriver_path, hide):
    """Creates a webdriver, hides if requested."""
    options = Options()
    if hide:
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        logging.debug("Creating hidden chrome browser")
    return webdriver.Chrome(chromedriver_path, options=options)


def get_options():
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
    )
    args = parser.parse_args()
    if args.chromedriver_path is None and sys.platform == "darwin":
        logging.debug(
            "On Mac, defaulting chromedriver path to to '/usr/local/bin/chromedriver'"
        )
        args.chromedriver_path = "/usr/local/bin/chromedriver"  # default on mac
    elif args.chromedriver_path is None:
        logging.warning(
            "Didn't receive a path to chromedriver. Provide one like '-c /path/to/chromedriver'"
        )
        sys.exit(1)
    else:
        logging.debug("Chromedriver path: {}".format(args.chromedriver_path))
    return args.hidden, args.chromedriver_path


def get_credentials(filepath):
    """Gets pythonanywhere credentials from the dotfile"""
    absolute_path = os.path.abspath(os.path.join(Path.home(), filepath))
    logging.debug("Credential File Location: {}".format(absolute_path))
    with open(absolute_path, "r") as cred:
        creds = yaml.load(cred, Loader=yaml.FullLoader)
    return creds["username"], creds["password"]


def main():
    """Gets options, runs program, cleans up selenium on exception."""
    use_hidden, chromedriver_path = get_options()
    username_or_email_address, password = get_credentials(credential_file_name)
    try:
        driver = create_webdriver(chromedriver_path, use_hidden)

        # Login
        driver.get(login_page)
        email_input = driver.find_element_by_id("id_auth-username")
        password_input = driver.find_element_by_id("id_auth-password")
        email_input.send_keys(username_or_email_address)
        password_input.send_keys(password)
        driver.find_element_by_id("id_next").click()

        # Go to "Web" page
        driver.get(driver.current_url + "/webapps")

        # Click 'Run until 3 months from today'
        driver.find_element_by_css_selector(
            "input.webapp_extend[type='submit']"
        ).click()
    except:
        traceback.print_exc()
    finally:
        driver.quit()
        # save current time to 'last run time file', so we can check if we need to run this again
        with open(last_run_at_absolute_path, "w") as f:
            f.write(str(time()))


if __name__ == "__main__":
    main()
