# For backend

## Development
`pip install pre-commit`
`pre-commit install`
`pip install -r requirements.txt`
`pip install -e .`

## Run Backend Server
`greppo serve tests/app.py`

docs -- build and source are separated `make clean && make html` to generate the docs as html files.

In `docs/`
`sphinx-apidoc -o source/ ../src` on making source changes in `src` dir under library

## Unit tests
We use pytests, `pytest tests/unit_tests`

# Checklist for build and deploy to pypi

- [ ] Build frontend: `cd frontend` and `npm run build`
- [ ] Update setup.cfg: bump version number
- [ ] Build backend: `cd library` and `python -m build`
- [ ] Upload to pypi using twine: `twine upload --verbose --skip-existing dist/*`