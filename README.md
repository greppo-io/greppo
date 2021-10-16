# Greppo

## The library

Integrates the frontend code with the backend library.

## Development

- Install pre-commit, requirements
```
pre-commit install
pip install -r requirements.txt
```

- Install Lib
```
pip install -e .
```

- Run commands
```shell
uvicorn cli.py:app

# or
python test_app.py
```

### Run backend server

Assuming your node/JS environment is already initialized with the required packages installed.

```shell

$make backend_server

```

### Run front server

Assuming your python environment is already running with the required packages.

```shell

$make frontend_server

```
