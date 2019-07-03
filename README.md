# pythonanywhere-3-months

Logs into your [pythonanywhere](https://www.pythonanywhere.com/) account and clicks the 'Run until 3 months from today' button, so your website doesn't deactivate automatically.

Requires: `python3 -m pip install --user selenium PyYaml` and a chromedriver binary. See [here](https://gist.github.com/seanbreckenridge/709a824b8c56ea22dbf4e86a7804287d) for chromedriver.

```
usage: driver.py [-h] [-H] [-c CHROMEDRIVER_PATH]

Clicks the 'Run until 3 months from today' on pythonanywhere

optional arguments:
  -h, --help            show this help message and exit
  -H, --hidden          Hide the ChromeDriver.
  -c CHROMEDRIVER_PATH, --chromedriver-path CHROMEDRIVER_PATH
                        Provides the location of ChromeDriver. Should probably
                        be the full path.
```

Put pythonanywhere credentials in a file named `credentials.yaml` in the same directory as `driver.py` with contents like:

```
username: yourusername
password: 2UGArHcjfKz@9GCGuNXN
```

#### Run:

```
git clone https://github.com/seanbreckenridge/pythonanywhere-3-months
cd pythonanywhere-3-months
python3 -m pip install --user selenium PyYaml
python3 driver.py -Hc /usr/local/bin/chromedriver # pass chromedriver binary path
```
