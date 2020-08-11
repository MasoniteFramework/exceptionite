init:
	cp .env-example .env
	pip install --upgrade pip
	pip install .
	pip install -r requirements.txt
	pip install pytest
test:
	python -m pytest tests
ci:
	make test
	make lint
lint:
	python -m flake8 src/exceptionite/ --ignore=E501,F401,E128,E402,E731,F821,E712,W503
format:
	black src/exceptionite
coverage:
	python -m pytest --cov-report term --cov-report xml --cov=src/exceptionite tests/
	python -m coveralls
publish:
	pip install 'twine>=1.5.0'
	python setup.py sdist bdist_wheel
	twine upload dist/*
	rm -fr build dist .egg masonite.egg-info

