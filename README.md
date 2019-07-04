# pythonanywhere-3-months

Logs into your [pythonanywhere](https://www.pythonanywhere.com/) account and clicks the 'Run until 3 months from today' button, so your website doesn't deactivate automatically.

Requires: Python 3.4+ and a chromedriver binary. See [here](https://gist.github.com/seanbreckenridge/709a824b8c56ea22dbf4e86a7804287d) for chromedriver.

#### Install and Run:

```
python3 -m pip install git+https://github.com/seanbreckenridge/pythonanywhere-3-months
pythonanywhere_3_months -Hc /usr/local/bin/chromedriver
```


```
usage: pythonanywhere_3_months [-h] [-H] [-c CHROMEDRIVER_PATH]

Clicks the 'Run until 3 months from today' on pythonanywhere

optional arguments:
  -h, --help            show this help message and exit
  -H, --hidden          Hide the ChromeDriver.
  -c CHROMEDRIVER_PATH, --chromedriver-path CHROMEDRIVER_PATH
                        Provides the location of ChromeDriver. Should probably
                        be the full path.
```

Put pythonanywhere credentials in your home directory; at `~/.pythonanywhere_credentials.yaml` with contents like:

```
username: yourusername
password: 2UGArHcjfKz@9GCGuNXN
```