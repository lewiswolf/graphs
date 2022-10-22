# core
from typing import Optional

# dependencies
from bokeh.plotting import figure
from bokeh.models import BasicTicker, ColorBar, LinearColorMapper
import numpy as np
import numpy.typing as npt

# src
from . import types as T

__all__ = [
	'PlotCircle',
	'PlotMatrix',
]


class PlotCircle(T.Graph):
	''' Render a stylised plot of a circle. '''

	def __init__(self, diameter: Optional[float] = None, settings: T.GraphSettings = {}) -> None:
		''' Uniquely typed init method. '''

		super().__init__()
		if settings:
			self.updateSettings(settings)
		if diameter is not None:
			self.render(self.createFigure(diameter))

	def createFigure(self, diameter: float) -> T.Figure:
		'''
		A circle is plotted using fig.circle.
		'''

		fig = figure()
		fig.circle(
			fill_color=self.settings['content_color'],
			line_color=self.settings['emphasis_color'],
			radius=diameter / 2,
			x=0.,
			y=0.,
		)
		fig.height = 582 # correct axis deformation
		return self.applySettings(fig)


class PlotMatrix(T.Graph):
	''' Render a stylised plot of a matrix from a 1D or 2D numpy array. '''

	def __init__(self, m: Optional[npt.NDArray[np.float64]] = None, settings: T.GraphSettings = {}) -> None:
		''' Uniquely typed init method. '''

		super().__init__()
		if settings:
			self.updateSettings(settings)
		if m is not None:
			self.render(self.createFigure(m))

	def createFigure(self, m: npt.NDArray[np.float64]) -> T.Figure:
		'''
		A given matrix is plotted using fig.image. If the matrix is 1D, the graph is scaled using custom x and y axis ranges.
		If the matrix is 2D, its aspect ratio is preserved.
		'''

		# type check input
		dim = m.ndim
		if dim > 2:
			raise ValueError('PlotMatrix only supports 1D and 2D inputs.')

		# resize input
		if dim == 1:
			m = m.reshape(1, m.shape[0])

		# create matrix plot
		color_mapper = LinearColorMapper(palette=f'{self.settings["color_map"]}256', low=m.min(), high=m.max())
		fig = figure(x_range=(0., m.shape[1]), y_range=(0., m.shape[0]))
		fig.image(image=[m], color_mapper=color_mapper, dh=[m.shape[0]], dw=[m.shape[1]], x=[0], y=[0])

		# hide y axis if 1D
		if dim == 1:
			fig.yaxis.visible = False

		# colorbar
		if self.settings['show_colorbar']:
			cb = ColorBar(color_mapper=color_mapper, ticker=BasicTicker(), location=(0, 0))

			# couldn't figure out how to edit the colorbar after it was added to the figure
			cb.padding = 30
			cb.major_label_text_font = self.settings['font_family']
			if self.settings['output_type'] != '':
				cb.major_label_text_font_size = (
					f'{round(self.settings["font_size"] * (self.settings["image_size"] / max(fig.height, fig.width))) - 2}px'
				)

			fig.add_layout(cb, 'below' if self.settings['colorbar_horizontal'] else 'right')
		return self.applySettings(fig)
