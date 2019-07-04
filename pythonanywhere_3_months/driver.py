#!/usr/local/env python3

from pythonanywhere_3_months import *


logging.basicConfig(level=logging.DEBUG)


def create_webdriver(chromedriver_path, hide):
    """Creates a webdriver, hides if requested."""
    options = Options()
    if hide:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        logging.debug("Creating hidden chrome browser")
    return webdriver.Chrome(chromedriver_path, options=options)


def get_options():
    """Gets options from user"""
    parser = argparse.ArgumentParser(description="Clicks the 'Run until 3 months from today' on pythonanywhere")
    parser.add_argument("-H", "--hidden", help="Hide the ChromeDriver.", action="store_true")
    parser.add_argument("-c", "--chromedriver-path", help="Provides the location of ChromeDriver. Should probably be the full path.")
    args = parser.parse_args()
    if args.chromedriver_path is None and sys.platform == "darwin":
        logging.debug("On Mac, defaulting chromedriver path to to '/usr/local/bin/chromedriver'")
        args.chromedriver_path = "/usr/local/bin/chromedriver"  # default on mac
    elif args.chromedriver_path is None:
        logging.warning("Didn't recieve a path to chromedriver. Provide one with like '-c /path/to/chromedriver'")
    else:
        logging.debug("Chromedriver path: {}".format(args.chromedriver_path))
    return args.hidden, args.chromedriver_path


def get_credentials(filepath):
    absolute_path = os.path.abspath(os.path.join(Path.home(), filepath))
    logging.debug("Credential File Location: {}".format(absolute_path))
    with open(absolute_path, 'r') as cred:
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

        # Go to Web page
        driver.find_element_by_id("id_web_app_link").click()

        # Click 'Run until 3 months from today'
        driver.find_element_by_css_selector("input.webapp_extend[type='submit']").click()

        print("Finished Successfully")

    except:
        traceback.print_exc()
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
