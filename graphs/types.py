# core
import os
import random
from typing import Any, Literal, TypedDict

# dependencies
from plotly.graph_objects import Figure


__all__ = ['Figure', 'GanttEvent', 'Graph', 'GraphSettings']


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


class GraphSettings(TypedDict, total=False):
	'''
	Type hints for the BaseGraph settings. These are both used to set
	the default class properties for BaseGraph, as well as update the
	settings for each instance.
	'''

	# display options
	color_map: str				# default color map (see plotly.colors)
	content_color: str			# default color used for a graph (hex eg. '#ffffff')
	emphasis_color: str			# secondary color used for accenting (hex eg. '#ffffff')
	font_family: str			# Which font family?
	font_size: int				# what's the global font size?
	# heading_size: int			# what's the font size for a heading/title?
	# export options
	export_path: str			# if the graph is being exported, where should it go? (relative path)
	image_size: int				# the length of the largest side of an exported image (pixels)
	output_type: Literal[		# how is the graph rendered?
		'',
		'png',
		'svg',
		# 'html',
	]
	# plotly config
	config: dict[str, Any]		# a clone of the fig.show() parameter config


class Graph():
	'''
	'''

	settings: GraphSettings

	def __init__(self) -> None:
		self.settings = {
			# display options
			'color_map': 'Greens',
			'content_color': '#1B9E31',
			'emphasis_color': '#126B21',
			'font_family': 'Computer Modern',
			'font_size': 18,
			# 'heading_size': 20,
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

		# use default export path if a new was not provided.
		if not export_path:
			export_path = self.settings['export_path']

		# apply global layout settings
		fig.update_layout(
			font={
				'family': self.settings['font_family'],
				'size': self.settings['font_size'],
			},
			margin={'t': 0, 'r': 0, 'b': 0, 'l': 0},
		)

		# handle image export
		if self.settings['output_type']:
			# make all images the same size
			if self.settings['output_type'] == 'png':
				height = fig.layout['height'] or 500
				width = fig.layout['width'] or 700
				font = round(self.settings['font_size'] * (self.settings['image_size'] / max(height, width)))
				fig.update_layout(
					height=round(self.settings['image_size'] * (1.0 if height > width else height / width)),
					width=round(self.settings['image_size'] * (1.0 if width > height else width / height)),
					font={'size': font},
				)
			# export
			fig.write_image(os.path.normpath(
				f'{os.getcwd()}/{export_path}.{self.settings["output_type"]}',
			))

		# handle simple implementation
		else:
			fig.show(config=self.settings['config'])

	def updateSettings(self, settings: GraphSettings) -> None:
		'''
		A type safe way to update self.settings.
		'''
		self.settings.update(settings)
