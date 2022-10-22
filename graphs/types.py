# core
import pathlib
import random
import string
from typing import Callable, Literal, TypedDict

# dependencies
from bokeh.io.export import get_screenshot_as_png
from bokeh.io import export_svg
from bokeh.plotting import Figure, show
import chromedriver_binary # noqa F401
import cv2
import numpy as np
from selenium import webdriver

__all__ = [
	'AnimationSettings',
	'Graph',
	'GraphSettings',
	'Figure',
]


class AnimationSettings(TypedDict, total=False):
	'''
	Type hints for the Animation settings. These are both used to set the default class properties for an Animation, as
	well as specify the settings for each instance.
	'''

	fps: float					# frames per second
	frame_size: int				# maximum side length of a frame (px)
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
	Type hints for the Graph settings. These are both used to set the default class properties for a Graph, as well as
	specify the settings for each instance.
	'''
	axis_color: str				# what is the global axis color?
	bg_color: str				# background color of the plot
	color_map: str				# default color map (see bokeh.palettes)
	colorbar_horizontal: bool	# is the colourbar horizontal? else vertical (only affects PlotMatrix())
	content_color: str			# default color used for a graph (hex eg. '#ffffff')
	emphasis_color: str			# secondary color used for accenting (hex eg. '#ffffff')
	font_family: str			# Which font family?
	font_size: int				# what's the global font size?
	show_colorbar: bool			# should the colorbar be visible?
	show_grid: bool				# is the grid visible?
	show_toolbar: bool			# is the bokeh toolbar visible
	# export options
	export_path: str			# if the graph is being exported, where should it go? (relative path)
	image_size: int				# the length of the largest side of an exported image (pixels)
	output_type: Literal[		# how is the graph rendered?
		'',
		'png',
		'jpeg',
		'svg',
	]


class Graph():
	'''
	This class is used by all static graphs.
	'''

	createFigure: Callable
	driver: webdriver.remote.webdriver.WebDriver
	settings: GraphSettings

	def __init__(self) -> None:
		# init settings
		self.settings = {
			# display options
			'axis_color': '#000000',
			'background_color': None,
			'color_map': 'Greens',
			'colorbar_horizontal': False,
			'content_color': '#1B9E31',
			'emphasis_color': '#126B21',
			'font_family': 'CMU Serif',
			'font_size': 18,
			'show_colorbar': True,
			'show_grid': True,
			'show_toolbar': False,
			# export options
			'export_path': ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10)),
			'image_size': 1200,
			'output_type': '',
		}
		# init webdriver
		options = webdriver.chrome.options.Options()
		options.add_argument('--headless')
		self.driver = webdriver.Chrome('chromedriver', options=options)

	def applySettings(self, fig: Figure) -> Figure:
		''' Apply global settings after createFigure. '''

		# axis colour
		fig.axis.axis_label_text_color = self.settings['axis_color']
		fig.axis.axis_line_color = self.settings['axis_color']
		fig.axis.major_label_text_color = self.settings['axis_color']
		fig.axis.major_tick_line_color = self.settings['axis_color']
		fig.axis.minor_tick_line_color = self.settings['axis_color']

		# background colour
		fig.background_fill_color = self.settings['background_color']
		fig.border_fill_color = self.settings['background_color']

		# font family
		fig.axis.axis_label_text_font = self.settings['font_family']
		fig.axis.major_label_text_font = self.settings['font_family']
		fig.title.text_font = self.settings['font_family']

		# grid
		fig.xgrid.grid_line_color = self.settings['axis_color'] if self.settings['show_grid'] else None
		fig.ygrid.grid_line_color = self.settings['axis_color'] if self.settings['show_grid'] else None

		# toolbar
		fig.toolbar.logo = None
		fig.toolbar_location = 'right' if self.settings['show_toolbar'] else None
		return fig

	def updateSettings(self, settings: GraphSettings) -> None:
		''' A type safe way to update self.settings. '''

		self.settings.update(settings)

	def render(self, fig: Figure, export_path: str = '') -> None:
		'''
		The global render method for each Graph. This was designed to be called with the export_path variable, which allows
		one to use multiple paths without first calling updateSettings(). Given an input figure, this function will then
		apply the default layout parameters, and finally either export the figure as an image, or display it in Chrome.
		'''

		# use default export path if a new one was not provided.
		if not export_path:
			export_path = self.settings['export_path']
		export_path = export_path + (f'.{self.settings["output_type"]}' if not pathlib.Path(export_path).suffix else '')

		# make all images the same size
		if self.settings['output_type'] != '':
			tmp_height = fig.height
			tmp_width = fig.width
			font_size = round(self.settings["font_size"] * (self.settings["image_size"] / max(tmp_height, tmp_width)))
			fig.height = round(self.settings['image_size'] * (1. if tmp_height > tmp_width else tmp_height / tmp_width))
			fig.width = round(self.settings['image_size'] * (1. if tmp_width > tmp_height else tmp_width / tmp_height))
			fig.axis.axis_label_text_font_size = f'{font_size}px'
			fig.axis.major_label_text_font_size = f'{font_size - 2}px'

		# export png & jpeg
		if self.settings['output_type'] == 'png' or self.settings['output_type'] == 'jpeg':
			cv2.imwrite(
				export_path,
				cv2.cvtColor(np.asarray(get_screenshot_as_png(fig, driver=self.driver)), cv2.COLOR_BGRA2RGBA),
			)
		# export svg
		elif self.settings['output_type'] == 'svg':
			fig.output_backend = 'svg'
			export_svg(fig, filename=export_path, webdriver=self.driver)
		# display in the browser
		else:
			show(fig)
