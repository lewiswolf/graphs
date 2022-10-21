# core
import os


def circleExample() -> None:
	from graphs import PlotCircle

	PlotCircle(2., settings={
		'export_path': os.path.normpath(f'{__file__}/../images/circle'),
		'output_type': 'jpeg',
	})


if __name__ == '__main__':
	circleExample()
	exit()
