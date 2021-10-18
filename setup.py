# core
import codecs
import os
from setuptools import setup

this = os.path.abspath(os.path.dirname(__file__))
name = 'graphs'
version = '0.0.1'
short_description = 'Graphs in Python. Graphs in JavaScript. Graphs in LaTeX.'

# import long description from readme.md
with codecs.open(os.path.join(this, 'readme.md'), encoding='utf-8') as rm:
	long_description = '\n' + rm.read()

# import packages from Pipfile
with codecs.open(os.path.join(this, 'Pipfile'), encoding='utf-8') as pf:
	packages = []
	# loop over Pipfile
	p = pf.readlines(1)
	pf.close()
	b = False
	for line in p:
		line = line.replace('\n', '')
		if not line:
			continue
		# find [packages]
		if line[0] == '[':
			if line == '[packages]':
				b = True
				continue
			else:
				b = False
				continue
		# append package names
		if b:
			packages.append(line.split()[0])

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
		'Programming Language :: Python :: 3',
		'Operating System :: Unix',
		'Operating System :: MacOS :: MacOS X',
		'Operating System :: Microsoft :: Windows',
		'Typing :: Typed',
	],
)
