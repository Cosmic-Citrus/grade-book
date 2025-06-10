import numpy as np
import matplotlib.pyplot as plt
from evaluation_configuration import GradeBookEvaluationConfiguration
from visual_settings_configuration import VisualSettingsConfiguration


class BaseGradeBookPlotterConvenienceFunctionsConfiguration(GradeBookEvaluationConfiguration):

	def __init__(self):
		super().__init__()

	@staticmethod
	def verify_value_method(is_points=False, is_percents=False, is_grades=False):
		if not isinstance(is_points, bool):
			raise ValueError("invalid type(is_points): {}".format(type(is_points)))
		if not isinstance(is_grades, bool):
			raise ValueError("invalid type(is_grades): {}".format(type(is_grades)))
		if not isinstance(is_percents, bool):
			raise ValueError("invalid type(is_percents): {}".format(type(is_percents)))
		if is_grades and (is_points or is_percents):
			raise ValueError("invalid combination of is_grades={}, is_percents={}, and is_points={}".format(is_grades, is_percents, is_points))
		data_representation_args = np.array([
			is_points,
			is_percents,
			is_grades])
		if data_representation_args.sum() <= 0:
			raise ValueError("invalid combination: is_points={}, is_grades={}, is_percents={}".format(is_points, is_grades, is_percents))

	@staticmethod
	def verify_plot_method(is_stacked_bars=False, is_histogram=False, is_polar_chart=False, is_heat_map=False, is_box_plot=False, is_table=False):
		if not isinstance(is_stacked_bars, bool):
			raise ValueError("invalid type(is_stacked_bars): {}".format(type(is_stacked_bars)))
		if not isinstance(is_histogram, bool):
			raise ValueError("invalid type(is_histogram): {}".format(type(is_histogram)))
		if not isinstance(is_polar_chart, bool):
			raise ValueError("invalid type(is_polar_chart): {}".format(type(is_polar_chart)))
		if not isinstance(is_heat_map, bool):
			raise ValueError("invalid type(is_heat_map): {}".format(type(is_heat_map)))
		if not isinstance(is_box_plot, bool):
			raise ValueError("invalid type(is_box_plot): {}".format(type(is_box_plot)))
		if not isinstance(is_table, bool):
			raise ValueError("invalid type(is_table): {}".format(type(is_table)))
		plot_method_args = np.array([
			is_stacked_bars,
			is_histogram,
			is_polar_chart,
			is_heat_map,
			is_box_plot,
			is_table])
		if plot_method_args.sum() != 1:
			raise ValueError("invalid combination: is_stacked_bars={}, is_histogram={}, is_polar_chart={}, is_heat_map={}, is_box_plot={}, is_table={}".format(is_stacked_bars, is_histogram, is_polar_chart, is_heat_map, is_box_plot, is_table))

	@staticmethod
	def verify_selection_headers(grouped_headers, diffed_headers, frequencies):
		condition_one = (
			(grouped_headers is None) and (
				(diffed_headers is not None) or (frequencies is not None)))
		condition_two = (
			(diffed_headers is None) and (
				(grouped_headers is not None) or (frequencies is not None)))
		condition_three = (
			(frequencies is None) and (
				(grouped_headers is not None) or (diffed_headers is not None)))
		if (condition_one or condition_two or condition_three):
			raise ValueError("invalid combination of grouped_headers, diffed_headers, and frequencies")

	@staticmethod
	def get_status_of_only_curve_selection(grouped_headers, diffed_headers):
		number_grouped_headers = len(
			grouped_headers)
		condition_one = (
			(number_grouped_headers == 1) and (grouped_headers[0] == "curve"))
		condition_two = all([
			"curve" in diffed_header
				for diffed_header in diffed_headers])
		is_only_curve_selected = (
			condition_one or condition_two)
		return is_only_curve_selected

	def get_status_of_group_selection(self, grouped_header, diffed_headers):
		...

	def get_status_of_all_selection(self, grouped_headers, diffed_headers, frequencies):
		...


class GradeBookPercentPlotterConvenienceFunctionsConfiguration(BaseGradeBookPlotterConvenienceFunctionsConfiguration):

	def __init__(self):
		super().__init__()

	@staticmethod
	def select_percents(percents):
		if isinstance(percents, bool):
			if percents:
				modified_percents = np.array([
					0,
					25,
					50,
					75,
					100,
					])
			else:
				raise ValueError("invalid percents: {}".format(percents))
		else:
			if isinstance(percents, (int, float)):
				modified_percents = np.array([
					percents])
			elif isinstance(percents, (tuple, list)):
				modified_percents = np.array(
					percents)
			elif not isinstance(percents, np.ndarray):
				raise ValueError("invalid type(percents): {}".format(type(percents)))
			if len(modified_percents.shape) > 1:
				raise ValueError("invalid percents.shape: {}".format(modified_percents.shape))
			if np.any(modified_percents < 0):
				raise ValueError("percents must be non-negative")
			if np.any(modified_percents > 100):
				raise ValueError("percents cannot exceed 100")
		return modified_percents

	@staticmethod
	def get_percents_from_weighted_scores(values, weights):
		percents = 100 * values / weights
		return percents

	def add_mirror_axis_with_uniform_percents(self, ax, percents, total_weight, axis):
		if not isinstance(percents, np.ndarray):
			raise ValueError("invalid type(percents): {}".format(type(percents)))
		mirror_ticks = total_weight * percents / 100
		mirror_ticklabels = np.core.defchararray.add(
			percents.astype(
				str),
			[" %"] * percents.size)
		mirror_ax = self.visual_settings.get_mirror_ax(
			ax=ax,
			frameon=False)
		if axis == "x":
			x_major_ticks = mirror_ticks
			x_major_ticklabels = mirror_ticklabels
			x_minor_ticks = False
			y_major_ticks = False
			y_major_ticklabels = False
			y_minor_ticks = False
		elif axis == "y":
			x_major_ticks = False
			x_major_ticklabels = False
			x_minor_ticks = False
			y_major_ticks = mirror_ticks
			y_major_ticklabels = mirror_ticklabels
			y_minor_ticks = False
		else:
			raise ValueError("invalid axis: {}".format(axis))
		mirror_ax = self.visual_settings.autoformat_axis_ticks_and_ticklabels(
			ax=mirror_ax,
			x_major_ticks=x_major_ticks,
			x_major_ticklabels=x_major_ticklabels,
			x_minor_ticks=x_minor_ticks,
			y_major_ticks=y_major_ticks,
			y_major_ticklabels=y_major_ticklabels,
			y_minor_ticks=y_minor_ticks)
		mirror_ax.tick_params(
			axis=axis,
			direction="in",
			pad=-15)
		# if axis == "y":
		# 	mirror_ax.yaxis.tick_right()
		# 	mirror_ax.yaxis.set_label_position(
		# 		"right")
		mirror_ax.set_xlim(
			ax.get_xlim())
		mirror_ax.set_ylim(
			ax.get_ylim())
		return ax, mirror_ax

class GradeBookStringPlotterConvenienceFunctionsConfiguration(GradeBookPercentPlotterConvenienceFunctionsConfiguration):

	def __init__(self):
		super().__init__()

	def get_grade_label_with_student_fraction_and_percentage(self, grade_label):
		number_students_at_grade = self.grades_counter[grade_label]
		student_fraction_label = r"$\dfrac{%s}{%s}$ students" % (
			number_students_at_grade,
			self.number_students)
		percentage_at_grade = self.get_percents_from_weighted_scores(
			values=number_students_at_grade,
			weights=self.number_students)
		percentage_label = r"${:.2f}\%$".format(
			np.round(
				percentage_at_grade,
				decimals=2))
		label = r"{} $\approx$ {}".format(
			student_fraction_label,
			percentage_label)
		return label

	def get_title(self, grouped_headers=None, diffed_headers=None, frequencies=None, is_points=False, is_percents=False, is_grades=False, is_stacked_bars=False, is_histogram=False, is_polar_chart=False, is_heat_map=False, is_box_plot=False, is_table=False):

		def get_prefix(is_points, is_percents, is_grades, is_stacked_bars, is_histogram, is_polar_chart, is_heat_map, is_box_plot, is_table):
			if is_table:
				suffix = None
			else:
				if (is_points and is_percents and is_grades):
					suffix = "of Points and Grades with Percents"
				else:
					if (is_points and is_percents):
						suffix = "of Points with Percents"
					elif (is_points and is_grades):
						suffix = "of Points and Grades"
					elif (is_grades and is_percents):
						suffix = "of Grades with Percents"
					else:
						if is_points:
							suffix = "of Points"
						elif is_grades:
							suffix = "of Grades"
						elif is_percents:
							suffix = "of Point Percentages"
						else:
							raise ValueError("invalid combination of is_points, is_grades, and is_percents")
			if is_stacked_bars:
				base_name = "Distribution"
			elif is_histogram:
				if is_grades:
					base_name = "Distribution"
				else:
					base_name = "Histogram"
			elif is_polar_chart:
				base_name = "Distribution"
			elif is_heat_map:
				base_name = "Heat-Map of Differences"
			elif is_box_plot:
				base_name = "Box-Plot of Statistics"
			elif is_table:
				base_name = "Data Table"
			else:
				raise ValueError("plot_method is not selected")
			if suffix is None:
				prefix = base_name
			else:
				prefix = "{} {}".format(
					base_name,
					suffix)
			return prefix

		def get_suffix(grouped_headers, diffed_headers, frequencies):
			if (grouped_headers is None) and (diffed_headers is None) and (frequencies is None):
				suffix = None
			else:
				self.verify_selection_headers(
					grouped_headers=grouped_headers,
					diffed_headers=diffed_headers,
					frequencies=frequencies)
				is_all_selected = self.get_status_of_all_selection(
					grouped_headers=grouped_headers,
					diffed_headers=diffed_headers,
					frequencies=frequencies)
				if is_all_selected:
					suffix = None
				else:
					number_diffed_headers = len(
						diffed_headers)
					if number_diffed_headers == 0:
						raise ValueError("diffed_headers is empty")
					elif number_diffed_headers == 1:
						suffix = "{}".format(
							diffed_headers[0])
					elif number_diffed_headers == 2:
						suffix = "{} and {}".format(
							*diffed_headers)
					else:
						separator = ", "
						suffix = separator.join(
							diffed_headers)
						index_at_last_separator = suffix.rfind(
							separator)
						if index_at_last_separator > -1:
							index_at_replacement = index_at_last_separator + len(separator)
						suffix = "{}, and {}".format(
							suffix[:index_at_last_separator],
							suffix[index_at_replacement:])
			return suffix

		self.verify_value_method(
			is_points=is_points,
			is_percents=is_percents,
			is_grades=is_grades)
		self.verify_plot_method(
			is_stacked_bars=is_stacked_bars,
			is_histogram=is_histogram,
			is_polar_chart=is_polar_chart,
			is_heat_map=is_heat_map,
			is_box_plot=is_box_plot,
			is_table=is_table)
		prefix = get_prefix(
			is_points=is_points,
			is_percents=is_percents,
			is_grades=is_grades,
			is_stacked_bars=is_stacked_bars,
			is_histogram=is_histogram,
			is_polar_chart=is_polar_chart,
			is_heat_map=is_heat_map,
			is_box_plot=is_box_plot,
			is_table=is_table)
		students_label = r"$N$ $=$ ${:,}$ Students".format(
			self.number_students)
		suffix = get_suffix(
			grouped_headers=grouped_headers,
			diffed_headers=diffed_headers,
			frequencies=frequencies)
		title_segments = (
			prefix,
			students_label,
			suffix)
		if suffix is None:
			title = "{}\n{}".format(
				prefix,
				students_label)
		else:
			title = "{} ({})\n{}".format(
				prefix,
				students_label,
				suffix)
		return title, title_segments

	def get_save_name(self, grouped_headers=None, diffed_headers=None, frequencies=None, is_points=False, is_percents=False, is_grades=False, is_stacked_bars=False, is_histogram=False, is_polar_chart=False, is_heat_map=False, is_box_plot=False, is_table=False, is_save=False):

		def get_prefix(is_stacked_bars, is_histogram, is_polar_chart, is_heat_map, is_box_plot, is_table):
			if is_stacked_bars:
				prefix = "BarStack"
			elif is_histogram:
				prefix = "Hist"
			elif is_polar_chart:
				prefix = "PolarChart"
			elif is_heat_map:
				prefix = "HeatMap"
			elif is_box_plot:
				prefix = "BoxPlot"
			elif is_table:
				prefix = "Table"
			else:
				raise ValueError("plot_method is not selected")
			return prefix

		def get_base_name(grouped_headers, diffed_headers, frequencies):
			if (grouped_headers is None) and (diffed_headers is None) and (frequencies is None):
				base_name = None
			else:
				self.verify_selection_headers(
					grouped_headers=grouped_headers,
					diffed_headers=diffed_headers,
					frequencies=frequencies)
				is_all_selected = self.get_status_of_all_selection(
					grouped_headers=grouped_headers,
					diffed_headers=diffed_headers,
					frequencies=frequencies)
				if is_all_selected:
					base_name = "All"
				else:
					modified_diffed_headers = list()
					for diffed_header in diffed_headers:
						modified_diffed_header = diffed_header.replace(
							" ",
							"_")
						modified_diffed_header = modified_diffed_header.replace(
							"-",
							"_")
						modified_diffed_headers.append(
							modified_diffed_header)
					base_name = "_".join(
						modified_diffed_headers)
			return base_name

		def get_suffix(is_points, is_percents, is_grades):
			suffixes = list()
			if is_points:
				suffixes.append(
					"Points")
			if is_percents:
				suffixes.append(
					"Percents")
			if is_grades:
				suffixes.append(
					"Grades")
			merged_suffixes = "".join(
				suffixes)
			suffix = "By{}".format(
				merged_suffixes)
			return suffix

		self.verify_value_method(
			is_points=is_points,
			is_percents=is_percents,
			is_grades=is_grades)
		self.verify_plot_method(
			is_stacked_bars=is_stacked_bars,
			is_histogram=is_histogram,
			is_polar_chart=is_polar_chart,
			is_heat_map=is_heat_map,
			is_box_plot=is_box_plot,
			is_table=is_table)
		if is_save:
			prefix = get_prefix(
				is_stacked_bars=is_stacked_bars,
				is_histogram=is_histogram,
				is_polar_chart=is_polar_chart,
				is_heat_map=is_heat_map,
				is_box_plot=is_box_plot,
				is_table=is_table)
			base_name = get_base_name(
				grouped_headers=grouped_headers,
				diffed_headers=diffed_headers,
				frequencies=frequencies)
			suffix = get_suffix(
				is_points=is_points,
				is_percents=is_percents,
				is_grades=is_grades)
			save_name_segments = (
				prefix,
				base_name,
				suffix)
			if base_name is None:
				save_name = "{}-{}".format(
					prefix,
					suffix)
			else:
				save_name = "{}-{}-{}".format(
					prefix,
					base_name,
					suffix)
		else:
			save_name_segments = None
			save_name = None
		return save_name, save_name_segments

class BaseGradeBookPlotterSelectionParameterizationConfiguration(GradeBookStringPlotterConvenienceFunctionsConfiguration):

	def __init__(self):
		super().__init__()

	def get_index_parameters_at_score_by_genre(self, grouped_header, diffed_headers=False, diffed_indices=False):
		
		def get_index_parameters_by_headers(diffed_headers, true_diffed_headers):
			if isinstance(diffed_headers, bool):
				if diffed_headers:
					number_true_diffed_headers = len(
						true_diffed_headers)
					indices_by_headers = list(
						range(
							number_true_diffed_headers))
				else:
					indices_by_headers = list()
			else:
				if isinstance(diffed_headers, str):
					modified_diffed_headers = [diffed_headers]
				elif isinstance(diffed_headers, tuple):
					modified_diffed_headers = list(
						diffed_headers)
				elif isinstance(diffed_headers, list):
					modified_diffed_headers = diffed_headers[:]
				else:
					raise ValueError("invalid type(diffed_headers): {}".format(type(diffed_headers)))
				indices_by_headers = list()
				for diffed_header in modified_diffed_headers:
					if diffed_header not in true_diffed_headers:
						raise ValueError("invalid diffed_header in diffed_headers: {}".format(diffed_header))
					index_by_headers = true_diffed_headers.index(
						diffed_header)
					indices_by_headers.append(
						index_by_headers)
			return indices_by_headers
				
		def get_index_parameters_by_indices(diffed_indices, true_diffed_headers):
			if isinstance(diffed_indices, bool):
				if diffed_indices:
					number_true_diffed_headers = len(
						true_diffed_headers)
					indices_by_indices = list(
						range(
							number_true_diffed_headers))
				else:
					indices_by_indices = list()
			else:
				if isinstance(diffed_indices, int):
					indices_by_indices = [
						diffed_indices]
				elif isinstance(diffed_indices, (tuple, list, np.ndarray)):
					if isinstance(diffed_indices, np.ndarray):
						modified_indices = np.copy(
							diffed_indices)
					else:
						modified_indices = np.array(
							diffed_indices)
					size_of_shape = len(
						modified_indices.shape)
					if size_of_shape != 1:
						raise ValueError("invalid array(diffed_indices).shape: {}".format(modified_indices.shape))
					indices_by_indices = modified_indices.tolist()
				else:
					raise ValueError("invalid type(diffed_indices): {}".format(type(diffed_indices)))
			return indices_by_indices

		if grouped_header not in self.genres:
			raise ValueError("invalid grouped_header: {}".format(grouped_header))
		true_diffed_headers = list(
			self.genre_mapping[grouped_header])
		indices_by_headers = get_index_parameters_by_headers(
			diffed_headers=diffed_headers,
			true_diffed_headers=true_diffed_headers)
		indices_by_indices = get_index_parameters_by_indices(
			diffed_indices=diffed_indices,
			true_diffed_headers=true_diffed_headers)
		combined_indices = indices_by_headers + indices_by_indices
		number_combined_indices = len(
			combined_indices)
		if number_combined_indices == 0:
			selected_indices = list()
			selected_headers = list()
		else:
			unique_indices = np.unique(
				combined_indices)
			selected_indices = unique_indices.tolist()
			selected_headers = [
				self.genre_mapping[grouped_header][index_at_selection]
					for index_at_selection in selected_indices]
		return selected_headers, selected_indices

	def get_index_parameters_at_score_by_other(self, grouped_header, diffed_headers=False):
		if grouped_header == "curve":
			# if not self.is_curved:
			# 	raise ValueError("cannot extract curve parameters because curve was not applied")
			true_diffed_headers = list(
				self.curves.keys())
			if isinstance(diffed_headers, bool):
				if diffed_headers:
					selected_headers = list(
						self.curves.keys())
				else:
					selected_headers = list()
			else:
				if isinstance(diffed_headers, str):
					modified_diffed_headers = [diffed_headers]
				elif isinstance(diffed_headers, tuple):
					modified_diffed_headers = list(
						diffed_headers)
				elif isinstance(diffed_headers, list):
					modified_diffed_headers = diffed_headers[:]
				else:
					raise ValueError("invalid type(diffed_headers): {}".format(type(diffed_headers)))
				visited_diffed_headers = set()
				selected_headers = list()
				for diffed_header in modified_diffed_headers:
					if diffed_header not in true_diffed_headers:
						raise ValueError("invalid diffed_header in diffed_headers: {}".format(diffed_header))
					if diffed_header not in visited_diffed_headers:
						visited_diffed_headers.add(
							diffed_header)
						selected_headers.append(
							diffed_header)
		# elif ...
		else:
			raise ValueError("invalid grouped_header: {}".format(grouped_header))
		number_selected_headers = len(
			selected_headers)
		if number_selected_headers == 0:
			selected_indices = list()
		else:
			selected_indices = [
				None
					for _ in range(
						number_selected_headers)]
		return selected_headers, selected_indices

	def get_index_parameters(self, home_work_indices=False, home_work_headers=False, exam_indices=False, exam_headers=False, extra_credit_indices=False, extra_credit_headers=False, curve_headers=False):
		true_grouped_headers = (
			"home-work",
			"exam",
			"extra credit")
		true_other_grouped_headers = (
			"curve",)
		grouped_headers = list()
		diffed_headers = list()
		diffed_indices = list()
		frequencies = list()
		args_at_indices = (
			home_work_indices,
			exam_indices,
			extra_credit_indices)
		args_at_headers = (
			home_work_headers,
			exam_headers,
			extra_credit_headers)
		for grouped_header, partial_diffed_indices, partial_diffed_headers in zip(true_grouped_headers, args_at_indices, args_at_headers):
			if grouped_header in self.genres:
				selected_headers, selected_indices = self.get_index_parameters_at_score_by_genre(
					grouped_header=grouped_header,
					diffed_headers=partial_diffed_headers,
					diffed_indices=partial_diffed_indices)
				frequency = len(
					selected_headers)
				if frequency > 0:
					grouped_headers.append(
						grouped_header)
					diffed_headers.extend(
						selected_headers)
					diffed_indices.extend(
						selected_indices)
					frequencies.append(
						frequency)
			else:
				if not isinstance(partial_diffed_indices, bool):
					raise ValueError("{} is not initialized ==> invalid type(partial_diffed_indices): {}".format(grouped_header, type(partial_diffed_indices)))
				if not isinstance(partial_diffed_headers, bool):
					raise ValueError("{} is not initialized ==> invalid type(partial_diffed_headers): {}".format(grouped_header, type(partial_diffed_headers)))
				if partial_diffed_indices:
					raise ValueError("{} is not initialized".format(grouped_header))
				if partial_diffed_headers:
					raise ValueError("{} is not initialized".format(grouped_header))
		for other_grouped_header in ("curve", ):
			other_selected_headers, other_selected_indices = self.get_index_parameters_at_score_by_other(
				grouped_header=other_grouped_header,
				diffed_headers=curve_headers)
			other_frequency = len(
				other_selected_headers)
			if other_frequency > 0:
				grouped_headers.append(
					other_grouped_header)
				diffed_headers.extend(
					other_selected_headers)
				diffed_indices.extend(
					other_selected_indices)
				frequencies.append(
					other_frequency)
		number_grouped_headers = len(
			grouped_headers)
		if number_grouped_headers == 0:
			raise ValueError("no headers or indices were selected")
		parameters_at_indexing = (
			grouped_headers,
			diffed_headers,
			diffed_indices,
			frequencies)
		return parameters_at_indexing

	def get_weighted_score_parameters(self, grouped_headers, diffed_headers, diffed_indices, frequencies):
		it_diffed_headers = iter(
			diffed_headers)
		it_diffed_indices = iter(
			diffed_indices)
		diffed_weights = list()
		diffed_points = list()
		diffed_percents = list()
		for index_at_group, (grouped_header, frequency) in enumerate(zip(grouped_headers, frequencies)):
			for index_at_frequency in range(frequency):
				diffed_header = next(
					it_diffed_headers)
				index_at_diffed_header = next(
					it_diffed_indices)
				if grouped_header in self.genres:
					weight = float(
						self.weights[grouped_header][index_at_diffed_header])
					scores = np.copy(
						self.scores[grouped_header][:, index_at_diffed_header])
					percents = self.get_percents_from_weighted_scores(
						values=scores,
						weights=weight)
				elif grouped_header == "curve":
					weight = 0
					scores = np.copy(
						self.curves[diffed_header])
					percents = np.full(
						fill_value=0,
						shape=scores.shape,
						dtype=float)
				else:
					raise ValueError("invalid grouped_header: {}".format(grouped_header))
				diffed_weights.append(
					weight)
				diffed_points.append(
					scores)
				diffed_percents.append(
					percents)
		diffed_weights = np.array(
			diffed_weights)
		diffed_points = np.array(
			diffed_points).T
		diffed_percents = np.array(
			diffed_percents).T
		total_weight = np.sum(
			diffed_weights)
		sub_total_points = np.nansum(
			diffed_points,
			axis=1)
		sub_total_percents = self.get_percents_from_weighted_scores(
			values=sub_total_points,
			weights=total_weight)
		parameters_at_weights = (
			diffed_weights,
			total_weight)
		parameters_at_points = (
			diffed_points,
			sub_total_points)
		parameters_at_percents = (
			diffed_percents,
			sub_total_percents)
		weighted_score_parameters = (
			parameters_at_weights,
			parameters_at_points,
			parameters_at_percents)
		return weighted_score_parameters

	def get_statistic_parameters(self, diffed_points, sub_total_points, diffed_percents, sub_total_percents, number_selected_scores_per_student):
		prelim_statistics_by_diffed_points = self.get_statistics(
			diffed_points,
			ddof=0,
			axis=0)
		prelim_statistics_by_diffed_percents = self.get_statistics(
			diffed_percents,
			ddof=0,
			axis=0)
		statistics_by_diffed_points = list()
		statistics_by_diffed_percents = list()
		statistic_names = (
			"mean",
			"median",
			"standard deviation",
			"minimum",
			"maximum",
			"total",
			"number missing")
		for index_at_source in range(number_selected_scores_per_student):
			partial_statistics_by_diffed_points = dict()
			partial_statistics_by_diffed_percents = dict()
			for statistic_name in statistic_names:
				partial_statistics_by_diffed_points[statistic_name] = prelim_statistics_by_diffed_points[statistic_name][index_at_source]
				partial_statistics_by_diffed_percents[statistic_name] = prelim_statistics_by_diffed_percents[statistic_name][index_at_source]
			statistics_by_diffed_points.append(
				partial_statistics_by_diffed_points)
			statistics_by_diffed_percents.append(
				partial_statistics_by_diffed_percents)
		statistics_by_sub_total_points = self.get_statistics(
			sub_total_points,
			ddof=0,
			axis=None)
		statistics_by_sub_total_percents = self.get_statistics(
			sub_total_percents,
			ddof=0,
			axis=None)
		number_missing_by_sub_total_points = int(
			np.sum(
				prelim_statistics_by_diffed_points["number missing"]))
		number_missing_by_sub_total_percents = int(
			np.sum(
				prelim_statistics_by_diffed_percents["number missing"]))
		if number_missing_by_sub_total_points != number_missing_by_sub_total_percents:
			raise ValueError("number_missing_by_sub_total_points={} and number_missing_by_sub_total_percents={} are not compatible".format(number_missing_by_sub_total_points, number_missing_by_sub_total_percents))
		statistics_by_sub_total_points["number missing"] = number_missing_by_sub_total_points
		statistics_by_sub_total_percents["number missing"] = number_missing_by_sub_total_percents
		statistic_parameters = (
			statistics_by_diffed_points,
			statistics_by_sub_total_points,
			statistics_by_diffed_percents,
			statistics_by_sub_total_percents)
		return statistic_parameters

class GradeBookPlotterSelectionParameterizationConfiguration(BaseGradeBookPlotterSelectionParameterizationConfiguration):

	def __init__(self):
		super().__init__()

	def get_default_indices_and_headers(self, home_work_indices=None, home_work_headers=None, exam_indices=None, exam_headers=None, extra_credit_indices=None, extra_credit_headers=None, curve_headers=None):
		
		def get_autocorrected_indices(grouped_header, indices, is_off_by_default):
			if indices is None:
				if is_off_by_default:
					modified_indices = list()
				else:
					if grouped_header in self.genres:
						number_sources = len(
							self.genre_mapping[grouped_header])
						modified_indices = np.arange(
							number_sources,
							dtype=int)
					else:
						raise ValueError("invalid grouped_header: {}".format(grouped_header))
			else:
				modified_indices = indices
			return modified_indices

		def get_autocorrected_headers(grouped_header, headers, is_off_by_default):
			if headers is None:
				if is_off_by_default:
					modified_headers = list()
				else:
					if grouped_header in self.genres:
						modified_headers = list(
							self.genre_mapping[grouped_header])
					elif (grouped_header == "curve") or (grouped_header in self.curves.keys()):
						modified_headers = list(
							self.curves.keys())
					else:
						raise ValueError("invalid grouped_header: {}".format(grouped_header))
			else:
				modified_headers = headers
			return modified_headers

		def get_key(grouped_header, suffix):
			prefix = grouped_header.replace(
				" ",
				"_")
			prefix = prefix.replace(
				"-",
				"_")
			key = "{}_{}".format(
				prefix,
				suffix)
			return key

		get_key_at_headers = lambda grouped_header : get_key(
			grouped_header=grouped_header,
			suffix="headers")
		get_key_at_indices = lambda grouped_header : get_key(
			grouped_header=grouped_header,
			suffix="indices")
		parameters = (
			("home-work", home_work_indices, home_work_headers),
			("exam", exam_indices, exam_headers),
			("extra credit", extra_credit_indices, extra_credit_headers),
			("curve", None, curve_headers))
		kwargs = dict()
		for sub_parameters in parameters:
			(grouped_header, indices, headers) = sub_parameters
			key_at_headers = get_key_at_headers(
				grouped_header=grouped_header)
			key_at_indices = get_key_at_indices(
				grouped_header=grouped_header)
			if grouped_header in self.genres:
				if (indices is None) and (headers is None):
					is_off_by_default = False
				else:
					is_off_by_default = True
				modified_headers = get_autocorrected_headers(
					grouped_header=grouped_header,
					headers=headers,
					is_off_by_default=is_off_by_default)
				modified_indices = get_autocorrected_indices(
					grouped_header=grouped_header,
					indices=indices,
					is_off_by_default=is_off_by_default)
				kwargs[key_at_headers] = modified_headers
				kwargs[key_at_indices] = modified_indices
			elif (grouped_header == "curve") or (grouped_header in self.curves.keys()):
				is_off_by_default = np.invert(
					self.is_curved)
				modified_headers = get_autocorrected_headers(
					grouped_header=grouped_header,
					headers=headers,
					is_off_by_default=is_off_by_default)
				kwargs[key_at_headers] = modified_headers
			else:
				kwargs[key_at_headers] = False
				kwargs[key_at_indices] = False
		return kwargs

	def get_score_parameters(self, home_work_indices=False, home_work_headers=False, exam_indices=False, exam_headers=False, extra_credit_indices=False, extra_credit_headers=False, curve_headers=False):
		index_parameters = self.get_index_parameters(
			home_work_indices=home_work_indices,
			home_work_headers=home_work_headers,
			exam_indices=exam_indices,
			exam_headers=exam_headers,
			extra_credit_indices=extra_credit_indices,
			extra_credit_headers=extra_credit_headers,
			curve_headers=curve_headers)
		(grouped_headers, diffed_headers, diffed_indices, frequencies) = index_parameters
		number_diffed_headers = len(
			diffed_headers)
		if number_diffed_headers == 0:
			raise ValueError("no scores were selected")
		is_only_curve_selected = self.get_status_of_only_curve_selection(
			grouped_headers=grouped_headers,
			diffed_headers=diffed_headers)
		weighted_score_parameters = self.get_weighted_score_parameters(
			grouped_headers=grouped_headers,
			diffed_headers=diffed_headers,
			diffed_indices=diffed_indices,
			frequencies=frequencies)
		(weight_parameters, point_parameters, percent_parameters) = weighted_score_parameters
		(diffed_weights, total_weight) = weight_parameters
		(diffed_points, sub_total_points) = point_parameters
		(diffed_percents, sub_total_percents) = percent_parameters
		statistics_parameters = self.get_statistic_parameters(
			diffed_points=diffed_points,
			sub_total_points=sub_total_points,
			diffed_percents=diffed_percents,
			sub_total_percents=sub_total_percents,
			number_selected_scores_per_student=number_diffed_headers)
		(statistics_by_diffed_points, statistics_by_sub_total_points, statistics_by_diffed_percents, statistics_by_sub_total_percents) = statistics_parameters
		parameters = (
			index_parameters,
			is_only_curve_selected,
			weighted_score_parameters,
			statistics_parameters)
		return parameters

class BaseGradeBookPlotterConfiguration(GradeBookPlotterSelectionParameterizationConfiguration):

	def __init__(self):
		super().__init__()
		self._visual_settings = None

	@property
	def visual_settings(self):
		return self._visual_settings
	
	def initialize_visual_settings(self, *args, **kwargs):
		self._visual_settings = VisualSettingsConfiguration(
			*args,
			**kwargs)

	def update_save_directory(self, path_to_save_directory=None):
		self.verify_visual_settings()
		self._visual_settings.update_save_directory(
			path_to_save_directory=path_to_save_directory)

	def verify_visual_settings(self):
		if self.visual_settings is None:
			raise ValueError("visual_settings is not initialized")
		if not isinstance(self.visual_settings, VisualSettingsConfiguration):
			raise ValueError("invalid type(self.visual_settings): {}".format(type(self.visual_settings)))

	def get_grade_handles_and_labels(self, ax):
		handles, labels = list(), list()
		# for letter_grade, label in zip(self.grading_criteria["possible grades"], self.grading_criteria["bin labels"]):
		for label in self.grading_criteria["bin labels"]:
			handle = self.visual_settings.get_empty_scatter_handle(
				ax=ax)
			handles.append(
				handle)
			labels.append(
				label)
		return handles, labels

	def plot_handles_and_labels_in_side_legend(self, ax, handles, labels, ncol=1, **kwargs):
		side_leg = ax.legend(
			handles=handles,
			labels=labels,
			ncol=ncol,
			bbox_to_anchor=(1.04, 0.5),
			loc="center left",
			borderaxespad=0,
			**kwargs)
		return ax, side_leg

	def plot_statistics_in_legend(self, fig, ax, statistics, is_points=False, is_percents=False, is_grades=False, leg_title="Statistics", **leg_kwargs):
		label_mapping = {
			"mean" : "mean",
			"median" : "median",
			"standard deviation" : "standard\ndeviation",
			"minimum" : "minimum",
			"maximum" : "maximum",
			"number missing" : "number missing\nstudent scores"}
		handles, labels = list(), list()
		for statistic_name, label_name in label_mapping.items():
			statistic_value = statistics[statistic_name]
			if statistic_name == "number missing":
				label = r"{}: ${:,}$".format(
					label_name,
					int(
						statistic_value))
			else:
				if is_grades:
					grade_value = self.get_grades(
						sub_totals=statistic_value)
					label = r"{}: ${:,.2f}$, {}".format(
						label_name,
						statistic_value,
						grade_value)
				else:
					if is_points:
						label = r"{}: ${:,.2f}$".format(
							label_name,
							statistic_value)
					elif is_percents:
						label = r"{}: ${:,.2f}$$\%$".format(
							label_name,
							statistic_value)
					else:
						raise ValueError("invalid combination of is_grades={}, is_points={}, and is_percents={}".format(is_grades, is_points, is_percents))
			handle = self.visual_settings.get_empty_scatter_handle(
				ax=ax)
			labels.append(
				label)
			handles.append(
				handle)
		number_legend_columns = len(
			label_mapping.keys())
		leg = self.visual_settings.get_legend(
			fig=fig,
			ax=ax,
			handles=handles,
			labels=labels,
			title=leg_title,
			number_columns=number_legend_columns,
			**leg_kwargs)
		return fig, ax, leg

##