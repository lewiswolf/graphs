# core
import os
import random

# dependencies
import cv2

# lib
from . import types as T


class Animation():
	'''
	A class for animations.
	'''

	# public
	frame_count: int					# how many frames have been created
	id: str								# unique instance id
	settings: T.AnimationSettings = {	# settings object
		'fps': 10,
		'frame_type': 'png',
		'frame_size': 1200,
		'output_type': 'mp4v',
	}

	# private
	__tmp_dir: str = os.path.normpath(f'{os.path.dirname(__file__)}/../tmp')

	def __init__(self, settings: T.AnimationSettings = {}) -> None:
		'''
		As opposed to the Graph type, settings can only set when this class is instantiated.
		This is done to avoid settings conflicts during the class lifecycle.
		'''
		self.frame_count = 0
		self.id = f'{random.getrandbits(64):16x}'
		if settings:
			self.settings.update(settings)

	def createFrame(self, fig: T.Figure) -> None:
		'''
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

		# create image
		fig.write_image(f'{self.__tmp_dir}/{self.id}-{"%08d" % (self.frame_count,)}.{self.settings["frame_type"]}')
		self.frame_count += 1
		del fig

	def render(
		self,
		export_path: str = '',
	) -> None:
		'''
		'''


		if not export_path:
			export_path = self.id
		export_path = f'{export_path}.avi'

		frames = sorted([f for f in os.listdir(self.__tmp_dir) if f.startswith(self.id)])
		encoder = cv2.VideoWriter(
			export_path,
			cv2.VideoWriter_fourcc(*'MJPG'),
			self.settings['fps'],
			(self.settings['frame_size'], self.settings['frame_size']),
		)

		for f in frames:
			encoder.write(cv2.imread(f'{self.__tmp_dir}/{f}'))
			os.remove(f'{self.__tmp_dir}/{f}')

		self.frame_count = 0
		encoder.release()
