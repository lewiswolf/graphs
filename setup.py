# core
import codecs
import os
from setuptools import setup

this = os.path.abspath(os.path.dirname(__file__))
name = 'graphs'
version = '0.0.1'
short_description = 'Graphs in Python. Graphs in JavaScript. Graphs in LaTeX.'

# import long description from readme.md
with codecs.open(os.path.join(this, 'readme.md'), encoding='utf-8') as readme:
	long_description = '\n' + readme.read()

# import packages from Pipfile
with codecs.open(os.path.join(this, 'Pipfile'), encoding='utf-8') as raw_pipfile:
	packages = []
	# read the Pipfile
	pipfile = raw_pipfile.readlines(1)
	raw_pipfile.close()
	# loop over the file
	is_pkg = False
	for line in pipfile:
		line = line.replace('\n', '')
		if not line:
			continue
		# find [packages]
		if line[0] == '[':
			if line == '[packages]':
				is_pkg = True
				continue
			else:
				is_pkg = False
				continue
		# append package names with required version
		if is_pkg:
			line_arr = line.split()
			packages.append(f'{line_arr[0]}{line_arr[2][1:-1] if line_arr[2][1:-1] != "*" else ""}')

setup(
	name=name,
	version=version,
	author='Lewis Wolf',
	description=short_description,
	long_description_content_type='text/markdown',
	long_description=long_description,
	packages=['graphs'],
	install_requires=packages,
	package_data={'graphs': ['py.typed']},
	keywords=['graphs'],
	classifiers=[
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: Microsoft :: Windows',
		'Operating System :: Unix',
		'Programming Language :: Python :: 3',
		'Programming Language :: Python :: 3 :: Only',
		'Programming Language :: Python :: 3.9',
		'Programming Language :: Python :: 3.10',
		'Typing :: Typed',
	],
)
