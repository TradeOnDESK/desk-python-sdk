#!make
include .env
export $(shell sed 's/=.*//' .env)

test:
	poetry run pytest

test-all:
	nox

build:
	poetry build --ansi

publish:
	poetry publish
