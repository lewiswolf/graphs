# core
import pathlib
import random
import string

# dependencies
from bokeh.io.export import get_screenshot_as_png
import chromedriver_binary # noqa F401
import cv2
import numpy as np
from selenium import webdriver

# lib
from . import types as T


class Animation():
	'''
	A class for animations.
	'''

	driver: webdriver.remote.webdriver.WebDriver	# bokeh image capture
	encoder: cv2.VideoWriter						# video encoder
	id: str											# unique instance id
	settings: T.AnimationSettings = {				# settings object
		'fps': 10,
		'frame_size': 1200,
		'output_codec': 'avc1',
		'output_container': 'mp4',
	}

	def __init__(
		self,
		export_path: str = '',
		settings: T.AnimationSettings = {},
	) -> None:
		'''
		This init method first creates an instance of cv2.VideoWriter(), and confirms
		that it is working correctly. As opposed to the Graph type, settings can only
		be set when this class is instantiated. This is done to avoid settings conflicts
		during the class lifecycle.
		'''

		# initialise instance
		self.id = ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(10))
		if settings:
			self.settings.update(settings)

		# configure export path
		export_path = export_path + (f'.{self.settings["output_container"]}' if not pathlib.Path(export_path).suffix else '')

		# initialise encoder
		self.encoder = cv2.VideoWriter(
			export_path,
			cv2.VideoWriter_fourcc(*self.settings['output_codec']),
			self.settings['fps'],
			(self.settings['frame_size'], self.settings['frame_size']),
		)
		if not self.encoder.isOpened():
			raise ValueError(
				'Something went wrong when initialising the video encoder for your animation...\n'
				'Perhaps it\'s the export path?',
			)

		# init webdriver
		options = webdriver.chrome.options.Options()
		options.add_argument('--headless')
		self.driver = webdriver.Chrome('chromedriver', options=options)

	def createFrame(self, fig: T.Figure) -> None:
		'''
		Each video frame is here generated using a Figure, by first conforming its
		dimensions, and then converting it into a numpy array.
		'''

		# scale image
		tmp_height = fig.height
		tmp_width = fig.width
		font_size = round(
			float(fig.axis.axis_label_text_font_size[0][:-2]) * (self.settings["frame_size"] / max(tmp_height, tmp_width)),
		)
		fig.height = round(self.settings['frame_size'] * (1. if tmp_height > tmp_width else tmp_height / tmp_width))
		fig.width = round(self.settings['frame_size'] * (1. if tmp_width > tmp_height else tmp_width / tmp_height))
		fig.axis.axis_label_text_font_size = f'{font_size}px'
		fig.axis.major_label_text_font_size = f'{font_size - 2}px'

		# append image to movie
		self.encoder.write(cv2.cvtColor(np.array(get_screenshot_as_png(fig, driver=self.driver)), cv2.COLOR_BGRA2RGB))

	def render(self) -> None:
		'''
		Finish writing the video file.
		'''

		self.encoder.release()
