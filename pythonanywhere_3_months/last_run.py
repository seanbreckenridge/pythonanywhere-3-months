
from pythonanywhere_3_months import *

def check():
    """Checks if its been more than 2 months since the script has been run, reports to user on stdout"""
    with open(last_run_at_absolute_path) as f:
        time_since_run = time() - int(float(f.read().strip()))
    two_months_in_seconds = 5184000
    if time_since_run > two_months_in_seconds:
        print("Its been more than 2 months since you've ran 'pythonanywhere_3_months'!")
