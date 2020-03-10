.PHONY: clean deps develop clean-build lint test coverage coverage-html tox migrate runserver
COVER := next_scraper
APP := src/

help:
	@echo "clean-build - remove build artifacts"
	@echo "clean-pyc - remove Python file artifacts"
	@echo "setup-docker - install all packages required for development"
	@echo "lint - check style with flake8"
	@echo "test - run tests quickly with the default Python"
	@echo "coverage - generate test coverage report"
	@echo "coverage-html - generate test coverage report, html output"
	@echo "tox - Run all tests in a tox container"


clean: clean-build clean-pyc


deps:
	@echo "--> Installing python dependencies"
	pip install --upgrade pip setuptools wheel
	pip install -r requirements.txt
	@echo ""


develop: deps

clean-build:
	@rm -fr build/ src/build
	@rm -fr dist/ src/dist
	@rm -fr *.egg-info src/*.egg-info
	@rm -fr htmlcov/
	$(MAKE) -C docs clean

test: lint
	docker-compose exec web pytest $(APP) $(ARGS)

lint:
	docker-compose exec web flake8 src/

coverage:
	docker-compose exec web pytest --cov=${COVER} --cov-report=term-missing ${APP}

coverage-html:
	docker-compose exec web pytest --cov=${COVER} --cov-report=html ${APP}

tdd:
	docker-compose exec web pytest -x --pdb $(ARGS) $(APP)

test-failed:
	docker-compose exec web pytest --lf $(ARGS) $(APP)

update-docker:
	docker-compose exec web make develop

migrate-docker:
	docker-compose exec web ./manage.py migrate

setup-docker: update-docker migrate-docker

shell:
	docker-compose exec web bash

djshell:
	docker-compose exec web ./manage.py shell

dbshell:
	docker-compose exec web ./manage.py dbshell
