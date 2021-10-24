# Usage: $ make {command}

.ONESHELL:

.PHONY: all
all: clean

.PHONY: serve-dev
serve-dev:
	npm run --prefix ./frontend serve & python ./tests/test_server/test.py &

.PHONY: build-frontend
build-frontend:	
	cd frontend && npm run build

.PHONY: build-package
build-package:	
	cd library && python -m build

.PHONY: run-unit-tests
run-unit-tests:
	pytest library/tests/unit_tests

.PHONY: clean
clean:
	echo "To be implemented..."
