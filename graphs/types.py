# core
import os
import random
from typing import Any, Callable, Literal, TypedDict

# dependencies
from plotly.graph_objects import Figure


__all__ = ['AnimationSettings', 'Figure', 'GanttEvent', 'Graph', 'GraphSettings']


class GanttEvent(TypedDict, total=False):
	'''
	Type hints for arguments passed to graphs.GanttChart().
	'''

	# mandatory
	event: str						# event title
	start: tuple[int, int, int]		# start date (year, month, day)
	end: tuple[int, int, int]		# end date (year, month, day)
	# optional
	color: str						# color of event
	reference: str					# name of group, to appear in key


class AnimationSettings(TypedDict, total=False):
	'''
	Type hints for the Animation settings. These are both used to set the
	default class properties for a Animation, as well as specify the settings
	for each instance.
	'''

	fps: float					# frames per second
	frame_size: int				# maximum side length of a frame (px)
	frame_type: Literal[		# what format is each frame rendered as?
		'png',
		'jpeg',
	]
	output_codec: Literal[		# what is the video coded?
		'avc1',
		'mp4v',
	]
	output_container: Literal[	# what format is exported?
		'mov',
		'mp4',
	]


class GraphSettings(TypedDict, total=False):
	'''
	Type hints for the Graph settings. These are both used to set the
	default class properties for a Graph, as well as specify the settings
	for each instance.
	'''

	# display options
	axis_color: str				# what is the global axis color?
	bg_color: str				# background color of the plot
	color_map: str				# default color map (see plotly.colors)
	content_color: str			# default color used for a graph (hex eg. '#ffffff')
	emphasis_color: str			# secondary color used for accenting (hex eg. '#ffffff')
	font_family: str			# Which font family?
	font_size: int				# what's the global font size?
	show_colorbar: bool			# should the colorbar be visible?
	show_grid: bool				# is the grid visible?
	# export options
	export_path: str			# if the graph is being exported, where should it go? (relative path)
	image_size: int				# the length of the largest side of an exported image (pixels)
	output_type: Literal[		# how is the graph rendered?
		'',
		'png',
		'svg',
	]
	# plotly config
	config: dict[str, Any]		# a clone of the fig.show() parameter `config`


class Graph():
	'''
	This class is used by all static graphs.
	'''

	createFigure: Callable
	settings: GraphSettings

	def __init__(self) -> None:
		self.settings = {
			# display options
			'axis_color': '#000000',
			'bg_color': 'rgba(0, 0, 0, 0)',
			'color_map': 'Greens',
			'content_color': '#1B9E31',
			'emphasis_color': '#126B21',
			'font_family': 'CMU Serif',
			'font_size': 18,
			'show_colorbar': True,
			'show_grid': True,
			# export options
			'export_path': f'{random.getrandbits(64):16x}',
			'image_size': 1200,
			'output_type': '',
			# plotly config
			'config': {
				'displaylogo': False,
				'displayModeBar': False,
				'showAxisDragHandles': False,
				'staticPlot': False,
			},
		}

	def applySettings(self, fig: Figure) -> Figure:
		'''
		This function is used to apply the global settings to a figure. It has been broken
		out of the main render() method here, so that figures can be styled independtly
		from it.
		'''

		# annotations
		fig.update_annotations(
			font={'color': self.settings['axis_color']},
		)

		# color bar
		fig.update_coloraxes(
			colorbar_tickfont_color=self.settings['axis_color'],
			colorbar_title_font_color=self.settings['axis_color'],
			colorbar_y=1.0,
			colorbar_yanchor='top',
			colorbar_ypad=0,
			showscale=self.settings['show_colorbar'],
		)

		# layout
		fig.update_layout(
			font={
				'family': self.settings["font_family"],
				'size': self.settings['font_size'],
			},
			legend_font={'color': self.settings['axis_color']},
			margin={'t': 5, 'r': 5, 'b': 5, 'l': 5},
			paper_bgcolor='rgba(0, 0, 0, 0)',
			plot_bgcolor=self.settings['bg_color'],
		)

		# axes
		axes = {
			'color': self.settings['axis_color'],
			'gridcolor': self.settings['axis_color'] if self.settings['show_grid'] else 'rgba(0, 0, 0, 0)',
			'linecolor': self.settings['axis_color'],
			'zerolinecolor': self.settings['axis_color'] if self.settings['show_grid'] else 'rgba(0, 0, 0, 0)',
			'zerolinewidth': 1,
		}
		fig.update_xaxes(**axes)
		fig.update_yaxes(**axes)

		return fig

	def updateSettings(self, settings: GraphSettings) -> None:
		'''
		A type safe way to update self.settings.
		'''

		self.settings.update(settings)

	def render(
		self,
		fig: Figure,
		export_path: str = '',
	) -> None:
		'''
		The global render method for each Graph. This was designed to be called with the export_path
		variable, which allows one to call this using multiple paths without first calling updateSettings().
		Given an input figure, this function will then apply the default layout parameters, and finally either
		export the figure as an image, or display it in your favourite browser.
		'''

		# use default export path if a new one was not provided.
		if not export_path:
			export_path = self.settings['export_path']
		export_path = os.path.normpath(
			f'{os.getcwd()}/{export_path}.{self.settings["output_type"]}',
		)

		# export both pngs and svgs
		if self.settings['output_type'] == 'png' or self.settings['output_type'] == 'svg':
			# make all images the same size
			height = fig.layout['height'] or 500
			width = fig.layout['width'] or 700
			font = round(self.settings['font_size'] * (self.settings['image_size'] / max(height, width)))
			fig.update_layout(
				height=round(self.settings['image_size'] * (1.0 if height > width else height / width)),
				width=round(self.settings['image_size'] * (1.0 if width > height else width / height)),
				font={'size': font},
			)
			fig.write_image(export_path)

		# handle simple implementation
		if self.settings['output_type'] == '':
			fig.show(config=self.settings['config'])
