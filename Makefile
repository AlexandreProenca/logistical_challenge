init:
	pip install .

development:
	pip install pip-tools && \
	pip-compile --generate-hashes requirements/requirements-dev.in && \
	pip install -r requirements/requirements-dev.txt

pretty:
	black app && \
	isort app/* && \
	pyflakes app && \
	flake8 app

secure:
	prospector --path=app && \
	bandit -r app && \
	safety check -r requirements/requirements-prod.txt

test:
	tox

run-test:
	cargo_truck assets/cargo.csv assets/trucks.csv

clean:
	find app -name *.pyc -exec rm -rf {} \;
	find tests -name *.pyc -exec rm -rf {} \;
	rm -rf app/__pycache__
	rm -rf tests/__pycache__
	rm -rf .tox
	rm -rf .pytest_cache
	rm -rf cargo_assignments.egg-info
	rm -rf .coverage

.PHONY: init
