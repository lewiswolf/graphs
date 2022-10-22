# core
import os

# dependencies
import numpy as np


def matrixExample() -> None:
	'''
	An example of plotting matrices. This demonstrates how PlotMatrix is capable of
	inferring its input representation.
	'''

	from graphs import PlotMatrix

	# PlotMatrix is designed to recognise the dimensionality of its input, and plot the respective matrix accordingly.
	p = PlotMatrix(settings={'output_type': 'png'})
	# As a result of this, it is just as easy to plot a 1D matrix...
	p.render(
		p.createFigure(np.random.rand(200)),
		export_path=os.path.normpath(f'{__file__}/../images/1d-matrix-example'),
	)
	# as it is to plot a 2D matrix.
	p.render(
		p.createFigure(np.random.rand(100, 100)),
		export_path=os.path.normpath(f'{__file__}/../images/2d-matrix-example-0'),
	)
	p.render(
		p.createFigure(np.random.rand(10, 10).reshape(20, 5)),
		export_path=os.path.normpath(f'{__file__}/../images/2d-matrix-example-1'),
	)
	p.render(
		p.createFigure(np.random.rand(10, 10).reshape(5, 20)),
		export_path=os.path.normpath(f'{__file__}/../images/2d-matrix-example-2'),
	)


def animationExample() -> None:
	'''
	An example that shows how to create animations from multiple figures.
	'''

	from graphs.types import AnimationSettings, Graph, GraphSettings
	from graphs import Animation, PlotMatrix

	# Animations are special! They are not Graphs!
	assert not isinstance(Animation, Graph)

	# And similarly, they have their own settings.
	a_settings: AnimationSettings = {
		'output_codec': 'avc1',
		'output_container': 'mp4',
	}
	p_settings: GraphSettings = {
		'show_colorbar': False,
	}

	# Animations instead work sympathetically with Graphs,
	A = Animation(
		export_path=os.path.normpath(f'{__file__}/../videos/animation-example'),
		settings=a_settings,
	)
	p = PlotMatrix(settings=p_settings)

	for i in range(20):
		# such that each animation frame starts off as a Figure,
		fig = p.createFigure(np.random.rand(100, 100))
		A.createFrame(fig)
	# before it is finally rendered.
	A.render()


if __name__ == '__main__':
	# matrixExample()
	animationExample()
	exit()
