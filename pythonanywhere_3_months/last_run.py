import sys

from pythonanywhere_3_months import *

def check():
    """Checks if its been more than 2 months since the script has been run, reports to user on stdout"""
    with open(last_run_at_absolute_path) as f:
        # if last time this ran was more than 2 months ago
        if time() - float(f.read().strip()) > 5184000:
            print("Its been more than 2 months since you've ran 'pythonanywhere_3_months'!")
            sys.exit(1)
    sys.exit(0)
