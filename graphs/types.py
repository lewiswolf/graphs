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
	'Graph',
	'GraphSettings',
]


class GraphSettings(TypedDict, total=False):
	'''
	Type hints for the Graph settings. These are both used to set the
	default class properties for a Graph, as well as specify the settings
	for each instance.
	'''
	# display options
	show_toolbar: bool
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
			'show_toolbar': False,
			# 	'axis_color': '#000000',
			# 	'bg_color': 'rgba(0, 0, 0, 0)',
			# 	'color_map': 'Greens',
			# 	'colorbar_horizontal': False,
			# 	'content_color': '#1B9E31',
			# 	'emphasis_color': '#126B21',
			# 	'font_family': 'CMU Serif',
			# 	'font_size': 18,
			# 	'show_colorbar': True,
			# 	'show_grid': True,
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

		# export as an image
		# if self.settings['output_type'] != '':
		# make all images the same size
		# height = fig.layout['height'] or 500
		# width = fig.layout['width'] or 700
		# font = round(self.settings['font_size'] * (self.settings['image_size'] / max(height, width)))
		# fig.update_layout(
		# 	height=round(self.settings['image_size'] * (1.0 if height > width else height / width)),
		# 	width=round(self.settings['image_size'] * (1.0 if width > height else width / height)),
		# 	font={'size': font},
		# )

		# export png
		if self.settings['output_type'] == 'png' or self.settings['output_type'] == 'jpeg':
			cv2.imwrite(
				export_path,
				cv2.cvtColor(np.asarray(get_screenshot_as_png(fig, driver=self.driver)), cv2.COLOR_BGR2RGB),
			)
		elif self.settings['output_type'] == 'svg':
			fig.output_backend = 'svg'
			export_svg(fig, filename=export_path, webdriver=self.driver)
		else:
			show(fig)
