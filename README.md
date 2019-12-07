# [//foss.events](https://foss.events) website

## Build instructions

Requirements:

* Python 3
* pipenv
* virtualenv

```
virtualenv -p /usr/bin/python3 venv
source venv/bin/activate
pipenv install
make
```

Start the dev server

```shell script
pipenv run bin/serve.py
```
