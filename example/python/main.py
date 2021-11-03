# core
import json
import os

# dependencies
import numpy as np
import torch
import torchaudio

# lib
import graphs.types as T


def ganntExample() -> None:
	'''
	An example using the Gantt Chart. This little example also contains general info
	about types and how to use T.Graphs.
	'''

	from graphs import GanttChart

	# Each Gantt chart event requires that we include a name, start date and end date. This will paint all Gantt events the
	# same colour, as defined using the settings object.
	e: T.GanttEvent = {
		'event': 'test_1',
		'start': (2019, 9, 13),
		'end': (2019, 9, 15),
	}
	# Alternatively, we can be explicit about our colours. This will produce a colour coded Gantt chart.
	e = {
		'event': 'test_1',
		'start': (2019, 9, 13),
		'end': (2019, 9, 15),
		'color': 'red',
	}
	# And we can of course give these colours a key, which will be displayed to the side of the graph.
	e = {
		'event': 'test_1',
		'start': (2019, 9, 13),
		'end': (2019, 9, 15),
		'color': 'red',
		'reference': 'category_1',
	}
	# If only a reference is given, the colours will be determined by settings['color_map'].
	e = {
		'event': 'test_1',
		'start': (2019, 9, 13),
		'end': (2019, 9, 15),
		'reference': 'category_1',
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
			'export_path': 'example/python/images/gantt-example-0',
			'output_type': 'png',
		},
	)

	# However, each graph can also be instantiated without any initial data, allowing for the main two methods to be called
	# directly and independently.
	g = GanttChart(settings={'output_type': 'png'})
	fig = g.createFigure([
		{'event': 'test_1', 'start': (2019, 9, 13), 'end': (2019, 9, 15)},
		{'event': 'test_2', 'start': (2019, 8, 9), 'end': (2019, 10, 11)},
	])
	g.render(fig, export_path='example/python/images/gantt-example-1')

	# To save loading a new instance in the event that the settings need to be changed, you can also simply use
	g.updateSettings({'output_type': ''})
	fig = g.createFigure([
		{'event': 'test_1', 'start': (2019, 9, 13), 'end': (2019, 9, 15)},
		{'event': 'test_2', 'start': (2019, 8, 9), 'end': (2019, 10, 11)},
	])
	# g.render(fig) # this will now display in your browser

	# And lastly, for type safety, we can assume that all static graphs and figures are of the same type.
	assert isinstance(g, T.Graph)
	assert isinstance(fig, T.Figure)


def matrixExample() -> None:
	'''
	An example of plotting matrices. This demonstrates how PlotMatrix is capable of
	inferring its input representation.
	'''

	from graphs import PlotMatrix

	# PlotMatrix is designed to recognise the dimensionality of its input, and plot the respective matrix accordingly.
	p = PlotMatrix(settings={'show_colorbar': True, 'output_type': 'png'})
	# As a result of this, it is just as easy to plot a 1D matrix...
	p.render(
		p.createFigure(np.random.rand(200)),
		export_path='example/python/images/1d-matrix-example',
	)
	# as it is to plot a 2D matrix.
	p.render(
		p.createFigure(np.random.rand(100, 100)),
		export_path='example/python/images/2d-matrix-example-0',
	)
	p.render(
		p.createFigure(np.random.rand(10, 10).reshape(20, 5)),
		export_path='example/python/images/2d-matrix-example-1',
	)
	p.render(
		p.createFigure(np.random.rand(10, 10).reshape(5, 20)),
		export_path='example/python/images/2d-matrix-example-2',
	)


def polygonExample() -> None:
	'''
	An example of plotting polygons. This example shows how graphs can be used for
	batch processing.
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


def audioExample() -> None:
	'''
	An example of plotting audio data. Exemplefied here are the complex inputs needed
	to represent audio data.
	'''

	from graphs import PlotSpectrogram, PlotWaveform

	# sample rate in hz
	sr = 44100

	# create a one second long, 220hz sawtooth wave
	waveform = 2.0 * np.array([i % 1 for i in (220.0 * (np.arange(2 * sr) / sr))]) - 1.0

	# create a one second long, sinusoidal sweep of the frequency spectrum
	sweep = np.zeros(sr)
	phi = 0.0
	s_l = 1 / sr
	tau = 2 * np.pi
	for i in range(sr):
		f = 20 + ((i / sr) ** 2) * ((sr / 2) - 20)
		sweep[i] = np.sin(phi)
		phi += tau * f * s_l
		if phi > tau:
			phi -= tau

	# Plotting the waveforms is as simple as any other plot...
	p_w = PlotWaveform(settings={'show_grid': False, 'output_type': 'png'})
	# and works fine with either a mono input
	p_w.render(
		p_w.createFigure(waveform[0:500], sr=sr),
		export_path='example/python/images/waveform-example-0',
	)
	# or a multichannel input.
	p_w.render(
		p_w.createFigure(np.array([
			sweep[0: 8000],
			sweep[0: 8000],
		])),
		export_path='example/python/images/waveform-example-1',
	)

	# variables for the spectrograms
	p_s = PlotSpectrogram(
		settings={
			'output_type': 'png',
			'show_colorbar': True,
		},
	)
	f_min = 20.05
	hop_length = 256
	n_bins = 512
	n_mels = 64
	window_length = 512

	# create an fft soectrogram
	fft = torchaudio.transforms.Spectrogram(
		hop_length=hop_length,
		n_fft=n_bins,
		power=2.0,
		win_length=window_length,
	)(torch.as_tensor(sweep))

	# create a mel spectrogram
	torch.set_default_dtype(torch.float64) # not my api 🤷
	mel = torchaudio.transforms.MelSpectrogram(
		f_min=f_min,
		hop_length=hop_length,
		n_fft=n_bins,
		n_mels=n_mels,
		power=2.0,
		sample_rate=sr,
		win_length=window_length,
	)(torch.as_tensor(sweep))

	# plot both spectrograms
	p_s.render(
		p_s.createFigure(
			fft.detach().numpy(),
			hop_length=hop_length,
			input_type='fft',
			sr=sr,
		),
		export_path='example/python/images/spectrogram-fft-example',
	)
	p_s.render(
		p_s.createFigure(
			mel.detach().numpy(),
			f_min=f_min,
			hop_length=hop_length,
			input_type='mel',
			sr=sr,
		),
		export_path='example/python/images/spectrogram-mel-example',
	)


def animationExample() -> None:
	'''
	'''

	from graphs.types import AnimationSettings, GraphSettings
	from graphs import Animation, PlotMatrix

	# Animations are special! They are not Graphs!
	assert not isinstance(Animation(), T.Graph)

	# And similarly, they have their own settings.
	a_settings: AnimationSettings = {
		'output_type': 'mp4v',
	}
	p_settings: GraphSettings = {
		'show_colorbar': False,
	}

	# Animations work sympathetically with Graphs,
	A = Animation(settings=a_settings)
	p = PlotMatrix(settings=p_settings)

	for i in range(10):
		# such that each animation frame starts off as a Figure,
		fig = p.createFigure(np.random.rand(100, 100))
		A.createFrame(fig)
	# before it is finally rendered
	A.render(export_path='example/python/videos/animation-example')


if __name__ == '__main__':
	# ganntExample()
	# matrixExample()
	# polygonExample()
	# audioExample()
	animationExample()
	exit()
