## graphs.py

- 	Support for all plotly colour maps.

	Largely due to plotly being an untyped language, not all colour maps are formatted the same, and for this reason not all colour maps work across the codebase. This particularly effects the `GanttChart()`, as this class uses the colour maps to define colours for each category of gantt events. This was loosely accounted for using the various functions in `utils.py`, but still needs work to account for all colour maps. For example, the `viridis` format does not work.

- 	Spectrogram width is inconsistent.

	When creating spectrograms of varying kinds, their widths are sometimes inconsistent. Ideally, all spectrograms would have the same width.