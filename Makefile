SPHINXOPTS    ?=
SPHINXBUILD   ?= sphinx-build
SOURCEDIR     = .
BUILDDIR      = _build

translate:
	pybabel compile -d ./locale -l fa -D fa_IR

install:
	pip3 install -r requirements.txt
	pybabel compile -d ./locale -l fa -D fa_IR

config:
	cp .env.sample .env

setup:
	make install
	make config
	docker-compose up -d

develop:
	docker-compose start
	FLASK_ENV=development FLASK_APP=main.py flask run

build_swagger:
	cd swagger && npm run build

sphinx:
	sphinx-build -b html . docs/html

all:
	make setup
	make develop

