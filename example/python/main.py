# core
import json
import os

# dependencies
import numpy as np

# lib
import graphs.types as T


def ganntExample() -> None:
	'''
	An example using the Gantt Chart.
	'''

	from graphs import GanttChart

	# Each Gantt chart event requires that we include a name, start date and end date. This will paint all Gantt events the
	# same colour, as defined using the settings object.
	e: T.GanttEvent = {
		'event': 'test1',
		'start': (2019, 9, 13),
		'end': (2019, 9, 15),
	}
	# Alternatively, we can be explicit about our colours. This will produce a colour coded Gantt chart.
	e = {
		'event': 'test1',
		'start': (2019, 9, 13),
		'end': (2019, 9, 15),
		'color': 'red',
	}
	# And we can of course give these colours a key, which will be displayed to the side of the graph.
	e = {
		'event': 'test1',
		'start': (2019, 9, 13),
		'end': (2019, 9, 15),
		'color': 'red',
		'reference': 'category1',
	}
	# If only a reference is given, the colours will be determined by settings['colour_map'].
	e = {
		'event': 'test1',
		'start': (2019, 9, 13),
		'end': (2019, 9, 15),
		'reference': 'category1',
	}
	del e

	# This packagae was designed to allow for each class to generate and export a graph upon instantiation.
	# In this example, we load and display our data from `gantt.json`.
	gantt_data = json.load(open(f'{os.getcwd()}/example/python/gantt.json', 'r'))
	for obj in gantt_data:
		obj['start'] = tuple(obj['start'])
		obj['end'] = tuple(obj['end'])

	GanttChart(
		gantt_data,
		settings={
			'output_type': 'png',
			'export_path': 'example/python/images/gantt-example-1',
		},
	)

	# However, each graph can also be instantiated without any initial data, allowing for the main two methods to be called
	# directly and independently.
	g = GanttChart(settings={'output_type': 'png'})
	fig = g.createFigure([
		{'event': 'test1', 'start': (2019, 9, 13), 'end': (2019, 9, 15)},
		{'event': 'test2', 'start': (2019, 8, 9), 'end': (2019, 10, 11)},
	])
	g.render(fig, export_path='example/python/images/gantt-example-2')

	# To save loading a new instance in the event that the settings need to be changed, you can also simply call:
	g.updateSettings({'output_type': ''})

	# And for type safety, we can assume that all static graphs and figures are of the same type.
	assert isinstance(g, T.Graph)
	assert isinstance(fig, T.Figure)


def matrixExample() -> None:
	'''
	An example of plotting matrices.
	'''

	from graphs import Plot2DMatrix

	two_d = np.random.rand(10, 10)

	Plot2DMatrix(two_d.reshape((20, 5)))


def polygonExample() -> None:
	'''
	An example of plotting polygons.
	'''

	from graphs import PlotPolygon, PlotVertices

	polygons = [
		np.array([
			[0.6368783849865679, 0.0],
			[0.9463254267273256, 0.7341606519188468],
			[0.05367457327267443, 1.0],
		]),
		np.array([
			[0.36809424893232445, 0.856570608502107],
			[0.24875225494073921, 0.10567716066106668],
			[0.7512477450592607, 0.0],
			[0.7369134688707913, 1.0],
		]),
	]

	# In this example, we create two plots of a polygon, both with different looks and feels.
	plots = [PlotPolygon(), PlotVertices()]
	for p in plots:
		p.updateSettings({'output_type': 'png'})

	# And now we simply loop over all the polygons we want to export.
	for i in range(len(polygons)):
		for p in plots:
			p.render(
				p.createFigure(polygons[i]),
				export_path=f'example/python/images/{p.__class__.__name__}-example-{i}',
			)


if __name__ == '__main__':
	ganntExample()
	matrixExample()
	polygonExample()
	exit()
