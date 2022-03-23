# Usage: $ make {command}

.ONESHELL:

.PHONY: all
all: clean

.PHONY: serve-dev
serve-dev:
	npm run --prefix ./frontend serve & python ./tests/test_server/test.py &

.PHONY: serve-fe
serve-fe:	
	cd frontend && npm run serve

.PHONY: serve-be
serve-be:	
	cd library && greppo serve tests/app.py

.PHONY: build-frontend
build-frontend:	
	cd frontend && npm run build

.PHONY: build-package
build-package:	
	cd library && python -m build

.PHONY: upload-package
upload-package: 
	cd library && twine upload -u "__token__" -p "$(PYPI_BARFI_API)" --skip-existing --verbose dist/*

.PHONY: run-unit-tests
run-unit-tests:
	pytest library/tests/unit_tests

.PHONY: clean
clean:
	echo "To be implemented..."
