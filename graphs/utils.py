# core
from typing import Union

# dependencies
import plotly.colors as cmaps


def getContinuousColor(colorscale: list[list[int]], intermed: float) -> str:
	"""
	Adapted from: https://stackoverflow.com/questions/62710057/access-color-from-plotly-color-scale

	Plotly continuous colorscales assign colors to the range [0, 1]. This function computes the intermediate
	color for any value in that range.

	Plotly doesn't make the colorscales directly accessible in a common format.
	Some are ready to use:

		colorscale = plotly.colors.PLOTLY_SCALES["Greens"]

	Others are just swatches that need to be constructed into a colorscale:

		viridis_colors, scale = plotly.colors.convert_colors_to_same_type(plotly.colors.sequential.Viridis)
		colorscale = plotly.colors.make_colorscale(viridis_colors, scale=scale)

	:param colorscale: A plotly continuous colorscale defined with RGB string colors.
	:param intermed: value in the range [0, 1]
	"""

	if len(colorscale) < 1:
		raise ValueError("Colorscale must have at least one color.")

	if intermed <= 0 or len(colorscale) == 1:
		return rgbToHex(str(colorscale[0][1]))
	if intermed >= 1:
		return rgbToHex(str(colorscale[-1][1]))

	for cutoff, color in colorscale:
		if intermed > cutoff:
			low_cutoff, low_color = cutoff, eval(str(color).replace('rgb', ''))
		else:
			high_cutoff, high_color = cutoff, eval(str(color).replace('rgb', ''))
			break

	t = cmaps.find_intermediate_color(
		lowcolor=low_color,
		highcolor=high_color,
		intermed=((intermed - low_cutoff) / (high_cutoff - low_cutoff)),
	)

	return rgbToHex((int(t[0]), int(t[1]), int(t[2])))


def rgbToHex(rgb: Union[str, tuple[int, int, int]]) -> str:
	if type(rgb) == str:
		rgb = eval(rgb.replace('rgb', ''))
	return f'#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}'
