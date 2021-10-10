pipenv run flake8 --config=test/test.cfg setup.py graphs test example
pipenv run mypy --config-file=test/test.cfg setup.py graphs test example
pipenv run python test/tests.py