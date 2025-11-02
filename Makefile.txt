install:
	poetry install

build:
	poetry build

publish:
	poetry publish --dry-run

package-install:
	python -m pip install dist/*.whl

run:
	poetry run project

start:
	poetry run python -m labyrinth_game.main

test:
	poetry run pytest

clean:
	del /s /q *.pyc
	rmdir /s /q __pycache__ 2>nul

env:
	poetry env activate