# core
import datetime
from typing import Optional

# dependencies
import numpy as np					# maths
import numpy.typing as npt			# typing for maths
import pandas as pd					# dataframes
import plotly.colors as cmaps		# colours and colour maps
import plotly.express as px			# pretty plots
import plotly.graph_objects as go	# more plots

# lib
from . import types as T
from . import utils
__all__ = ['GanttChart', 'Plot2DMatrix', 'PlotPolygon', 'PlotVertices']


class GanttChart(T.Graph):
	'''
	Render a stylised plot of a Gannt chart.
	'''

	def __init__(self, events: Optional[list[T.GanttEvent]] = None, settings: T.GraphSettings = {}) -> None:
		'''
		Uniquely typed init method.
		'''

		super().__init__()
		if settings:
			self.updateSettings(settings)
		if events is not None:
			self.render(self.createFigure(events))

	def createFigure(self, events: list[T.GanttEvent]) -> T.Figure:
		'''
		Create a stylised Gantt chart. The input list of dictionaries is converted...
		'''

		# convert the input TypedDict to a pandas DataFrame
		df = pd.DataFrame(events)
		df['start'] = [datetime.date(*date) for date in df['start']]
		df['end'] = [datetime.date(*date) for date in df['end']]

		# handle references and colors
		colors = []
		show_legend = True
		if 'reference' in df and 'color' in df:
			for c in df['color']:
				if c not in colors:
					colors.append(c)
		elif 'reference' in df:
			colors = [
				utils.getContinuousColor(cmaps.PLOTLY_SCALES[self.settings['color_map']], f)
				for f in np.linspace(0.0, 1.0, num=len(set(df['reference'])))
			]
		elif 'color' in df:
			df = df.assign(reference=[c for c in df['color']])
			for c in df['color']:
				if c not in colors:
					colors.append(c)
			show_legend = False
		else:
			colors = [self.settings['content_color']]

		# create figure
		fig = px.timeline(
			df,
			color='reference' if 'reference' in df else None,
			color_discrete_sequence=colors,
			x_start='start',
			x_end='end',
			y='event',
		)

		# configure layout
		fig.update_layout(legend_title_text='', showlegend=show_legend)
		fig.update_yaxes(autorange='reversed', title_text='')
		return fig


class Plot2DMatrix(T.Graph):
	'''
	Render a stylised plot of a 2D matrix from a 2D numpy array.
	'''

	def __init__(self, m: Optional[npt.NDArray[np.float64]] = None, settings: T.GraphSettings = {}) -> None:
		'''
		Uniquely typed init method.
		'''

		super().__init__()
		if settings:
			self.updateSettings(settings)
		if m is not None:
			self.render(self.createFigure(m))

	def createFigure(self, m: npt.NDArray[np.float64]) -> T.Figure:
		'''
		'''

		# type check input
		assert m.ndim == 2

		# create figure
		fig = px.imshow(
			m,
			color_continuous_scale=self.settings['color_map'],
			origin='lower',
		)

		# configure layout
		longest_side = max(*m.shape)
		fig.update_layout(
			height=(550 * (m.shape[0] / longest_side)),
			width=(550 * (m.shape[1] / longest_side)) + 150,
		)
		fig.update_xaxes(showticklabels=False)
		fig.update_yaxes(showticklabels=False)
		return fig


class PlotPolygon(T.Graph):
	'''
	Render a stylised plot of a polygon from an input array of vertices.
	'''

	def __init__(self, vertices: Optional[npt.NDArray[np.float64]] = None, settings: T.GraphSettings = {}) -> None:
		'''
		Uniquely typed init method.
		'''

		super().__init__()
		if settings:
			self.updateSettings(settings)
		if vertices is not None:
			self.render(self.createFigure(vertices))

	def createFigure(self, vertices: npt.NDArray[np.float64]) -> T.Figure:
		'''
		'''

		# convert vertices to svg path
		path = f'M{vertices[0, 0]} {vertices[0, 1]} '
		for i in range(1, len(vertices)):
			path += f'L{vertices[i, 0]} {vertices[i, 1]} '
		path += 'Z'

		# create figure
		fig = go.Figure(layout={
			'height': 700,
			'width': 700,
			'plot_bgcolor': 'rgba(0, 0, 0, 0)',
			'shapes': [{
				'type': 'path',
				'path': path,
				'fillcolor': self.settings['content_color'],
				'line_color': self.settings['emphasis_color'],
			}],
		})

		# configure layout
		v_min, v_max = np.min(vertices) - 0.01, np.max(vertices) + 0.01
		fig.update_xaxes(range=[v_min, v_max], showgrid=False, showticklabels=False, visible=False)
		fig.update_yaxes(range=[v_min, v_max], showgrid=False, showticklabels=False, visible=False)
		return fig


class PlotVertices(T.Graph):
	'''
	Render a stylised plot of a polygon from an input array of vertices.
	'''

	def __init__(self, vertices: Optional[npt.NDArray[np.float64]] = None, settings: T.GraphSettings = {}) -> None:
		'''
		Uniquely typed init method.
		'''

		super().__init__()
		if settings:
			self.updateSettings(settings)
		if vertices is not None:
			self.render(self.createFigure(vertices))

	def createFigure(self, vertices: npt.NDArray[np.float64]) -> T.Figure:
		'''
		'''

		# configure vertices
		vertices = np.append(vertices, [vertices[0]], axis=0)

		# create figure
		fig = go.Figure(
			go.Scatter(
				marker={'color': self.settings['emphasis_color']},
				mode='markers+lines',
				x=vertices[:, 0].tolist(),
				y=vertices[:, 1].tolist(),
			),
			layout={
				'height': 700,
				'width': 700,
			},
		)

		# configure layout
		v_min, v_max = np.min(vertices) - 0.02, np.max(vertices) + 0.02
		fig.update_xaxes(range=[v_min, v_max])
		fig.update_yaxes(range=[v_min, v_max])
		return fig
