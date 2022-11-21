import unittest

from graphs.utils import rgbToHex


class UtilsTests(unittest.TestCase):
	'''
	Tests used in conjunction with `utils.py`.
	'''

	def test_colors(self) -> None:
		# These test assert that the conversion from rgb to hex is working correctly
		self.assertEqual(rgbToHex((255, 255, 255)), '#ffffff')
		self.assertEqual(rgbToHex('rgb(255, 255, 255)'), '#ffffff')
		self.assertEqual(rgbToHex((0, 0, 0)), '#000000')
		self.assertEqual(rgbToHex('rgb(0, 0, 0)'), '#000000')
		self.assertEqual(rgbToHex((134, 235, 135)), '#86eb87')
		self.assertEqual(rgbToHex('rgb(134, 235, 135)'), '#86eb87')
		# test cmap with Viridis...


if __name__ == '__main__':
	unittest.main()
	exit()
