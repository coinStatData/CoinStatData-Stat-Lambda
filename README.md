# CoinStatData-Python-Stat-Lambda

Window:
- py -3 -m venv venv OR virtualenv --python=python3.9 venv
- venv\Scripts\activate
- pip install stuff

Mac:
- python3 -m venv venv
- . venv/bin/activate
- pip install stuff


```
## Deploying

$ pip freeze > requirements.txt
$ cat requirements.txt
$ chalice deploy
  or
$ chalice --debug deploy --stage dev --connection-timeout 360
```

```
## Local setup

$ pip install -r /path/to/requirements.txt
$ flask --app app --debug run
```