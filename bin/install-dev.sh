# install js dependencies
cd example/js
	npm install
	cd ../../

# install dev dependencies
pipenv install -d
pipenv lock # pipenv doesn't delete all the egg folders...

