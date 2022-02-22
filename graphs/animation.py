# core
import random

# dependencies
import cv2
import numpy as np

# lib
from . import types as T


class Animation():
	'''
	A class for animations.
	'''

	# public
	encoder: cv2.VideoWriter			# video encoder
	export_path: str					# relative export path
	id: str								# unique instance id
	settings: T.AnimationSettings = {	# settings object
		'fps': 10,
		'frame_size': 1200,
		'frame_type': 'png',
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
		self.id = f'{random.getrandbits(64):16x}'
		if settings:
			self.settings.update(settings)

		# configure relative export path
		if not export_path:
			export_path = self.id
		self.export_path = f'{export_path}.{self.settings["output_container"]}'

		# initialise encoder
		self.encoder = cv2.VideoWriter(
			self.export_path,
			cv2.VideoWriter_fourcc(*self.settings['output_codec']),
			self.settings['fps'],
			(self.settings['frame_size'], self.settings['frame_size']),
		)

		if not self.encoder.isOpened():
			raise ValueError(
				'Something went wrong when initialising the video encoder for your animation...\n'
				'Perhaps it\'s the export path?',
			)

	def createFrame(self, fig: T.Figure) -> None:
		'''
		Each video frame is here generated using a Figure, by first conforming its
		dimensions, and then converting it into a numpy array.
		'''

		# make all images the same size
		height = fig.layout['height'] or 500
		width = fig.layout['width'] or 700
		font = round(fig.layout['font']['size'] * (self.settings['frame_size'] / max(height, width)))
		fig.update_layout(
			height=round(self.settings['frame_size'] * (1.0 if height > width else height / width)),
			width=round(self.settings['frame_size'] * (1.0 if width > height else width / height)),
			font={'size': font},
		)

		# append image to movie
		self.encoder.write(
			cv2.imdecode(np.frombuffer(
				fig.to_image(format=self.settings['frame_type']),
				np.uint8,
			), 1),
		)

	def render(self) -> None:
		'''
		Finish writing the video file.
		'''

		self.encoder.release()
