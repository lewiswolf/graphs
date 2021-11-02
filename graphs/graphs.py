# core
import datetime
from typing import Literal, Optional

# dependencies
import numpy as np							# maths
import numpy.typing as npt					# typing for maths
import pandas as pd							# dataframes
import plotly.colors as cmaps				# colours and colour maps
import plotly.express as px					# pretty plots
import plotly.graph_objects as go			# more plots
from plotly.subplots import make_subplots	# subplot support

# lib
from . import types as T
from . import utils
__all__ = ['GanttChart', 'PlotMatrix', 'PlotPolygon', 'PlotSpectrogram', 'PlotVertices', 'PlotWaveform']


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
		Create a stylised Gantt chart using px.timeline. The input is converted into a pandas
		dataframe, and, depending on the information contained in the input array, the correct
		colours and labels are applied to each gantt event.
		'''

		# type check input
		for g in events:
			keys = g.keys()
			if 'event' not in keys:
				raise ValueError('A GanttEvent requires an "event" name.')
			if 'start' not in keys:
				raise ValueError('A GanttEvent requires a "start" date.')
			if 'end' not in keys:
				raise ValueError('A GanttEvent requires a "end" date.')

		# convert the input TypedDict to a pandas DataFrame
		df = pd.DataFrame(events)
		df['start'] = [datetime.date(*date) for date in df['start']]
		df['end'] = [datetime.date(*date) for date in df['end']]

		# handle references and colors
		colors = []
		show_legend = True
		# create ordered colour array from GanttEvents
		if 'reference' in df and 'color' in df:
			for c in df['color']:
				if c not in colors:
					colors.append(c)
		# create colour array from colour map to match references
		elif 'reference' in df:
			# TO FIX: Plotly is poorly typed, so this doesn't work for all colour maps
			colors = [
				utils.getContinuousColor(cmaps.PLOTLY_SCALES[self.settings['color_map']], f)
				for f in np.linspace(0.0, 1.0, num=len(set(df['reference'])))
			]
		# create references that refer to the colours given for each event
		elif 'color' in df:
			df = df.assign(reference=[c for c in df['color']])
			for c in df['color']:
				if c not in colors:
					colors.append(c)
			show_legend = False
		# or finally, give the gantt chart a single colour if no labels are used
		else:
			colors = [self.settings['content_color']]
			show_legend = False

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
		fig.update_layout(legend_title_text='', showlegend=show_legend, width=(900 if show_legend else 700))
		fig.update_yaxes(autorange='reversed', title_text='')
		return fig


class PlotMatrix(T.Graph):
	'''
	Render a stylised plot of a matrix from a 1D or 2D numpy array.
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
		A given matrix is plotted using px.imshow. If the matrix is 1D, the graph is scaled using
		custom x and y axis ranges. If the matrix is 2D, its aspect ratio is preserved.
		'''

		# type check input
		dim = m.ndim
		if dim > 2:
			raise ValueError('PlotMatrix only supports 1D and 2D inputs.')

		# resize input
		if dim == 1:
			m = m.reshape(1, m.shape[0])

		# create figure
		fig = go.Figure(
			px.imshow(
				m,
				color_continuous_scale=self.settings['color_map'],
				origin='lower',
				**{
					'x': np.arange(m.shape[1]),
					'y': np.zeros(1),
				} if dim == 1 else {},
			),
			# preseve aspect ratio if matrix is 2D
			# TO FIX: The 1D graph does not look great, as plotly does not currently support a horizontal colorbar.
			layout={
				'height': 550 if dim == 1 else 550 * (m.shape[0] / max(*m.shape)),
				'width': (700 if dim == 1 else 550 * (m.shape[1] / max(*m.shape))) + (150 if self.settings['show_colorbar'] else 0),
			},
		)

		# configure axes and scale if dim == 1
		fig.update_coloraxes(colorbar_len=1)
		fig.update_xaxes(showticklabels=False, **{'scaleratio': (700 / 550) * 1 / m.shape[1]} if dim == 1 else {})
		fig.update_yaxes(showticklabels=False, **{'scaleratio': m.shape[1]} if dim == 1 else {})
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
		This function creates a blank figure, on which the polygon is rendered as a vector
		using XML syntax.
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


class PlotSpectrogram(T.Graph):
	'''
	Render a stylised plot of a spectrogram.
	'''

	def __init__(
		self,
		spectrogram: Optional[npt.NDArray[np.float64]] = None,
		f_min: float = 20.05,
		hop_length: Optional[int] = None,
		input_type: Optional[Literal['cqt', 'fft', 'mel']] = None,
		sr: Optional[int] = None,
		settings: T.GraphSettings = {},
	) -> None:
		'''
		Uniquely typed init method.
		'''

		super().__init__()
		if settings:
			self.updateSettings(settings)
		if spectrogram is not None:
			self.render(self.createFigure(
				spectrogram,
				f_min=f_min,
				hop_length=hop_length,
				input_type=input_type,
				sr=sr,
			))

	def createFigure(
		self,
		spectrogram: npt.NDArray[np.float64],
		f_min: float = 20.05,
		hop_length: Optional[int] = None,
		input_type: Optional[Literal['cqt', 'fft', 'mel']] = None,
		sr: Optional[int] = None,
	) -> T.Figure:
		'''
		'''

		# map x axis to frames or seconds
		x_ticks = np.linspace(0, spectrogram.shape[1], num=spectrogram.shape[1] + 1)
		if hop_length and sr:
			x_ticks = np.linspace(0, hop_length * spectrogram.shape[1] / sr, num=spectrogram.shape[1] + 1)

		# map y axis to bins or frequency
		y_ticks = np.linspace(0, spectrogram.shape[0], num=spectrogram.shape[0] + 1)
		if input_type and sr:
			if input_type == 'cqt':
				y_ticks = np.linspace(0, spectrogram.shape[0], num=spectrogram.shape[0] + 1)
				y_ticks = f_min * 2 ** (y_ticks / np.ceil(spectrogram.shape[0] / np.log2(sr * 0.5 / f_min)))
			if input_type == 'fft':
				y_ticks = np.linspace(0, sr * 0.5, num=spectrogram.shape[0] + 1)
			if input_type == 'mel':
				y_ticks = np.linspace(np.log10(1 + f_min / 700.0), np.log10(1 + sr * 0.5 / 700.0), num=spectrogram.shape[0] + 1)
				y_ticks = 700.0 * (10.0 ** y_ticks - 1.0)

		# create figure
		fig = px.imshow(
			spectrogram,
			color_continuous_scale=self.settings['color_map'],
			origin='lower',
			x=x_ticks[0:spectrogram.shape[1]],
			y=y_ticks[0:spectrogram.shape[0]],
		)

		# configure layout
		fig.update_coloraxes(
			colorbar_len=1.064,
			colorbar_title='Power',
			colorbar_title_side='bottom',
		)
		# TO FIX: lengths of x axes are inconsistent when input_type is changed
		fig.update_xaxes(
			scaleratio=((700 / 500) * np.max(y_ticks)) / np.max(x_ticks),
			title='Time (Seconds)' if hop_length and sr else 'Frames',
		)
		fig.update_yaxes(
			scaleratio=1 / np.max(y_ticks),
			title='Frequency (Hz)' if input_type and sr else 'Bins',
		)
		fig.update_layout(
			height=500,
			width=700 + (120 if self.settings['show_colorbar'] else 0),
		)

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
		This function renders an array of vertices as a scatter plot, with each point connected
		by a line.
		'''

		# configure vertices
		vertices = np.append(vertices, [vertices[0]], axis=0)

		# create figure
		fig = go.Figure(
			go.Scatter(
				line={'width': 4},
				marker={'color': self.settings['content_color']},
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


class PlotWaveform(T.Graph):
	'''
	Render a stylised plot of a waveform from an input array.
	'''

	def __init__(
		self,
		waveform: Optional[npt.NDArray[np.float64]] = None,
		sr: Optional[int] = None,
		settings: T.GraphSettings = {},
	) -> None:
		'''
		Uniquely typed init method.
		'''

		super().__init__()
		if settings:
			self.updateSettings(settings)
		if waveform is not None:
			self.render(self.createFigure(waveform, sr=sr))

	def createFigure(self, waveform: npt.NDArray[np.float64], sr: Optional[int] = None) -> T.Figure:
		'''
		A waveform is plotted using a scatter graph. Each channel is given its own subplot, as this function
		is designed to accept any number of multichannel inputs. If the sample rate is provided, the x axis
		is mapped to time, whilst the default is audio samples. The y axis is given a custom label, shared
		across the multiple subplots.
		'''

		# type check and reshape input
		if waveform.ndim > 2:
			raise ValueError('PlotWaveform only supports mono (samples,) and multichannel (number of channels, samples) inputs.')
		elif waveform.ndim == 1:
			waveform = waveform.reshape(1, waveform.shape[0])

		# configure x axis
		x = np.arange(waveform.shape[1]) / (sr if sr else 1)

		# create figure
		c = waveform.shape[0]
		fig = make_subplots(cols=1, rows=c)
		for i in range(c):
			fig.add_trace(
				go.Scatter(
					marker={'color': self.settings['content_color']},
					mode='lines',
					name=f'Channel {i + 1}',
					x=x,
					y=waveform[i],
				),
				col=1,
				row=i + 1,
			)

		# configure layout
		fig.update_layout(showlegend=False, yaxis_title='')
		fig.update_xaxes(
			col=1,
			row=waveform.shape[0],
			title_text='Time (Seconds)' if sr else 'Audio Samples',
		)
		fig.add_annotation(
			font={'size': 24 if self.settings['output_type'] == '' else round(24 * (self.settings['image_size'] / 700))},
			showarrow=False,
			text='Amplitude',
			textangle=270,
			x=-0.05 if self.settings['output_type'] == '' else -0.1,
			xref='paper',
			y=0.5,
			yref='paper',
		)
		return fig
