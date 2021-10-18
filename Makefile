# Usage: $ make {command}

.ONESHELL:

.PHONY: all
all: hello development

.PHONY: hello
hello:
	@echo " "
	@echo "Hello World..."
	@echo " "
	@echo "This is greppo."
	@echo " "
	@echo "An open-source platform build and deploy your geo-spatial web-applications."
	@echo " "
	@echo "Development is underway."
	@echo " "

.PHONY: serve-dev
serve-dev:
	npm run --prefix ./frontend serve & python ./tests/test_server/test.py &

.PHONY: dev-init
dev-init:
	@cd frontend ; npm install

.PHONY: build-vue
build-vue:
	@cd frontend ; npm run build

.PHONY: serve-vue
serve-vue:
	@cd frontend ; npm run serve

.PHONY: serve-star
serve-star:
	@cd tests/test_server ; python test.py

.PHONY: run-unit-tests
run-unit-tests:
	pytest library/tests/unit_tests

.PHONY: build-html-docs
build-docs:
	# Sphinx should be installed before doing this
	cd library && sphinx-apidoc -f -o ../docs/source/ src
	cd docs && make html

.PHONY: clean
clean:
	echo "To be implemented..."
