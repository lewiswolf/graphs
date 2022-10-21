# core
from typing import Optional

# dependencies
from bokeh.plotting import figure

# src
from . import types as T

__all__ = [
	'PlotCircle',
]


class PlotCircle(T.Graph):
	'''
	Render a stylised plot of a circle.
	'''

	def __init__(self, diameter: Optional[float] = None, settings: T.GraphSettings = {}) -> None:
		'''
		Uniquely typed init method.
		'''

		super().__init__()
		if settings:
			self.updateSettings(settings)
		if diameter is not None:
			self.render(self.createFigure(diameter))

	def createFigure(self, diameter: float) -> T.Figure:
		fig = figure()
		fig.circle(x=0., y=0., radius=diameter / 2, fill_color='red')

		return self.applySettings(fig)
