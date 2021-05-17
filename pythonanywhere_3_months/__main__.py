from . import credential_file_name
from .core import get_options, get_credentials, run


def main():
    """Gets options, runs program, cleans up selenium on exception."""
    use_hidden, chromedriver_path = get_options()
    username_or_email_address, password = get_credentials(credential_file_name)
    run(username_or_email_address, password, chromedriver_path, use_hidden)


if __name__ == "__main__":
    main()
