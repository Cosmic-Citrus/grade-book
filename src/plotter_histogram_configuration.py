import numpy as np
import matplotlib.pyplot as plt
from visual_settings_configuration import (
	Patch,
	HandlerTuple)
from histogram_configuration import HistogramConfiguration
from plotter_base_configuration import BaseGradeBookPlotterConfiguration


class BaseGradeBookHistogramViewerConfiguration():

	def __init__(self, base_plotter):
		super().__init__()
		self.base_plotter = base_plotter

	@staticmethod
	def get_y_at_rug(y_at_rug=0.2):
		return y_at_rug

	@staticmethod
	def get_rug_style(is_show_rug):
		rug_style = "wRUG" if is_show_rug else "woRUG"
		return rug_style

	@staticmethod
	def get_bar_legend_handles_and_labels(first_facecolor, second_facecolor):
		label = "Histogram"
		labels = [
			label]
		first_patch = Patch(
			facecolor=first_facecolor)
		second_patch = Patch(
			facecolor=second_facecolor)
		handles = [[
			first_patch,
			second_patch]]
		handler_map = {
			list : HandlerTuple(
				None)}
		return handles, labels, handler_map

	@staticmethod
	def plot_histogram(ax, histogram, rgb_colors):
		ax.bar(
			histogram.bin_midpoints,
			histogram.bin_counts,
			width=histogram.bin_widths,
			color=rgb_colors,
			align="center")
		return ax

	def get_color_parameters(self, histogram, first_facecolor, second_facecolor, rug_facecolor):
		rgb_colors = list()
		for index_at_bin in range(histogram.number_bins):
			facecolor_at_bin = first_facecolor if index_at_bin % 2 == 0 else second_facecolor
			[rgb_color_at_bin], _ = self.base_plotter.visual_settings.get_rgb_facecolors(
				number_colors=1,
				facecolor=facecolor_at_bin,
				cmap=None)
			rgb_colors.append(
				rgb_color_at_bin)
		(rgb_rug,), _ = self.base_plotter.visual_settings.get_rgb_facecolors(
			number_colors=1,
			facecolor=rug_facecolor,
			cmap=None)
		color_parameters = (
			rgb_colors,
			rgb_rug)
		return color_parameters

	def plot_rug(self, *args, **kwargs):
		raise ValueError("this method should be over-written by a child class")

	def autoformat_plot(self, *args, **kwargs):
		raise ValueError("this method should be over-written by a child class")

class BaseGradeBookPointsHistogramViewerConfiguration(BaseGradeBookHistogramViewerConfiguration):

	def __init__(self, base_plotter):
		super().__init__(
			base_plotter=base_plotter)

	def get_histogram(self, sub_totals, bin_selection_method, *histogram_args, **histogram_kwargs):
		histogram = HistogramConfiguration()
		histogram.initialize_distribution_values(
			distribution_values=sub_totals)
		histogram.initialize_bin_locations(
			bin_selection_method,
			*histogram_args,
			**histogram_kwargs)
		histogram.initialize_bin_counts(
			side_bias=self.base_plotter.grading_criteria["side-bias"],
			bin_counts=None)
		return histogram

	def plot_rug(self, ax, histogram, rgb_rug, rug_marker="x", rug_alpha=0.35):
		y_at_rug = self.get_y_at_rug()
		y = np.full(
			fill_value=y_at_rug,
			shape=histogram.distribution_values.size,
			dtype=float)
		rug_handle = ax.scatter(
			histogram.distribution_values,
			y,
			label="Rug",
			color=rgb_rug,
			marker=rug_marker,
			alpha=rug_alpha)
		return ax, rug_handle

	def autoformat_plot(self, ax, histogram, grouped_headers, diffed_headers, frequencies, total_weight, is_show_rug, is_extend_percent_axis, is_label_midpoints):

		def get_left_extended_ticks(ticks, step, bound):
			while True:
				if ticks[0] > 0:
					ticks.insert(
						0,
						ticks[0] - step)
				else:
					break
			return ticks

		def get_right_extended_ticks(ticks, step, bound):
			while True:
				if ticks[-1] < bound:
					ticks.append(
						ticks[-1] + step)
				else:
					break
			return ticks
		
		def get_step_parameters(histogram, total_weight):
			if histogram.bin_edges[0] >= 0:
				dx = histogram.bin_edges[1] - histogram.bin_edges[0]
			else:
				dx = float(
					histogram.bin_edges[1]) # - 0
			left_bound = 0
			right_bound = float(
				total_weight)
			for curve_method, curve_values in self.base_plotter.curves.items():
				largest_curve = np.max(
					curve_values)
				right_bound += largest_curve
			right_bound *= 1.125 ## extra ticks; limits can shrink later
			step_parameters = (
				left_bound,
				right_bound,
				dx)
			return step_parameters

		def get_x_ticks(histogram, dx, left_bound, right_bound, is_label_midpoints):
			x_major_ticks = np.copy(
				histogram.bin_midpoints).tolist()
			x_minor_ticks = np.copy(
				histogram.bin_edges).tolist()
			x_major_ticks = get_left_extended_ticks(
				ticks=x_major_ticks,
				step=dx,
				bound=left_bound)
			x_major_ticks = get_right_extended_ticks(
				ticks=x_major_ticks,
				step=dx,
				bound=right_bound)
			x_minor_ticks = get_left_extended_ticks(
				ticks=x_minor_ticks,
				step=dx,
				bound=left_bound)
			x_minor_ticks = get_right_extended_ticks(
				ticks=x_minor_ticks,
				step=dx,
				bound=right_bound)
			if not is_label_midpoints:
				x_major_ticks, x_minor_ticks = x_minor_ticks, x_major_ticks
			x_major_ticklabels = True
			x_minor_ticklabels = False
			x_major_fmt = "{:,.2f}"
			x_ticks = (
				x_major_ticks,
				x_minor_ticks,
				x_major_ticklabels,
				x_minor_ticklabels,
				x_major_fmt)
			return x_ticks

		def get_y_ticks():
			y_major_ticks = np.arange(
				1,
				self.base_plotter.number_students * 2,
				2,
				dtype=int)
			y_minor_ticks = np.arange(
				0,
				self.base_plotter.number_students * 2,
				2,
				dtype=int)
			y_major_ticklabels = True
			y_minor_ticklabels = False
			y_ticks = (
				y_major_ticks,
				y_minor_ticks,
				y_major_ticklabels,
				y_minor_ticklabels)
			return y_ticks

		def get_limits(histogram, grouped_headers, diffed_headers, frequencies, total_weight, is_show_rug, is_extend_percent_axis):
			if is_extend_percent_axis:
				x_min = 0
				x_max = float(
					total_weight)
				for grouped_header, frequency in zip(grouped_headers, frequencies):
					if grouped_header == "curve":
						for curve_method in self.base_plotter.curves.keys():
							if curve_method in diffed_headers:
								largest_curve = np.max(
									self.base_plotter.curves[curve_method])
								x_max += largest_curve
			else:
				x_min = max([
					0,
					histogram.bin_edges[0]])
				if np.isinf(histogram.bin_edges[-1]):
					x_max = float(
						histogram.bin_edges[-2])
				else:
					x_max = float(
						histogram.bin_edges[-1])
			xlim = (
				x_min,
				x_max)
			largest_bin_count = np.max(
				histogram.bin_counts)
			y_max = 1.15 * largest_bin_count
			if is_show_rug:
				y_at_rug = self.get_y_at_rug()
				if y_at_rug > 0:
					y_min = 0
				elif y_at_rug < 0:
					y_min = y_at_rug - (y_max - largest_bin_count)
				else: # elif y_at_rug == 0:
					y_min = -0.1
			else:
				y_min = 0
			xlim = (
				x_min,
				x_max)
			ylim = (
				y_min,
				y_max)
			limits = (
				xlim,
				ylim)
			return limits

		if not isinstance(is_extend_percent_axis, bool):
			raise ValueError("invalid type(is_extend_percent_axis): {}".format(type(is_extend_percent_axis)))
		if not isinstance(is_label_midpoints, bool):
			raise ValueError("invalid type(is_label_midpoints): {}".format(type(is_label_midpoints)))
		step_parameters = get_step_parameters(
			histogram=histogram,
			total_weight=total_weight)
		(left_bound, right_bound, dx) = step_parameters
		x_ticks = get_x_ticks(
			histogram=histogram,
			dx=dx,
			left_bound=left_bound,
			right_bound=right_bound,
			is_label_midpoints=is_label_midpoints)
		y_ticks = get_y_ticks()
		(x_major_ticks, x_minor_ticks, x_major_ticklabels, x_minor_ticklabels, x_major_fmt) = x_ticks
		(y_major_ticks, y_minor_ticks, y_major_ticklabels, y_minor_ticklabels) = y_ticks
		ax = self.base_plotter.visual_settings.autoformat_axis_ticks_and_ticklabels(
			ax=ax,
			x_major_ticks=x_major_ticks,
			x_major_ticklabels=x_major_ticklabels,
			x_minor_ticks=x_minor_ticks,
			x_minor_ticklabels=x_minor_ticklabels,
			x_major_fmt=x_major_fmt,
			y_major_ticks=y_major_ticks,
			y_major_ticklabels=y_major_ticklabels,
			y_minor_ticks=y_minor_ticks,
			y_minor_ticklabels=y_minor_ticklabels)
		ax = self.base_plotter.visual_settings.autoformat_grid(
			ax=ax,
			grid_color="gray")
		xlabel = "Points"
		ylabel = "Number of Students"
		title, _ = self.base_plotter.get_title(
			grouped_headers=grouped_headers,
			diffed_headers=diffed_headers,
			frequencies=frequencies,
			is_points=True,
			is_histogram=True)
		ax = self.base_plotter.visual_settings.autoformat_axis_labels(
			ax=ax,
			xlabel=xlabel,
			ylabel=ylabel,
			title=title)
		limits = get_limits(
			histogram=histogram,
			grouped_headers=grouped_headers,
			diffed_headers=diffed_headers,
			frequencies=frequencies,
			total_weight=total_weight,
			is_show_rug=is_show_rug,
			is_extend_percent_axis=is_extend_percent_axis)
		(xlim, ylim) = limits
		ax = self.base_plotter.visual_settings.autoformat_axis_limits(
			ax=ax,
			xlim=xlim,
			ylim=ylim)
		if total_weight > 0:
			percents = self.base_plotter.select_percents(
				percents=True)
			ax, mirror_ax = self.base_plotter.add_mirror_axis_with_uniform_percents(
				ax=ax,
				percents=percents,
				total_weight=total_weight,
				axis="x")
		return ax

class GradeBookPointsHistogramViewerConfiguration(BaseGradeBookPointsHistogramViewerConfiguration):

	def __init__(self, base_plotter):
		super().__init__(
			base_plotter=base_plotter)

	def view_histogram(self, home_work_indices, home_work_headers, exam_indices, exam_headers, extra_credit_indices, extra_credit_headers, curve_headers, is_show_rug, is_extend_percent_axis, is_label_midpoints, first_facecolor, second_facecolor, rug_facecolor, figsize, is_save, bin_selection_method, *histogram_args, **histogram_kwargs):
		score_parameters = self.base_plotter.get_score_parameters(
			home_work_indices=home_work_indices,
			home_work_headers=home_work_headers,
			exam_indices=exam_indices,
			exam_headers=exam_headers,
			extra_credit_indices=extra_credit_indices,
			extra_credit_headers=extra_credit_headers,
			curve_headers=curve_headers)
		(index_parameters, is_only_curve_selected, weighted_score_parameters, statistics_parameters) = score_parameters
		(grouped_headers, diffed_headers, diffed_indices, frequencies) = index_parameters
		(weight_parameters, point_parameters, percent_parameters) = weighted_score_parameters
		(diffed_weights, total_weight) = weight_parameters
		(diffed_points, sub_total_points) = point_parameters
		(diffed_percents, sub_total_percents) = percent_parameters
		(statistics_by_diffed_points, statistics_by_sub_total_points, statistics_by_diffed_percents, statistics_by_sub_total_percents) = statistics_parameters
		histogram = self.get_histogram(
			sub_total_points,
			bin_selection_method,
			*histogram_args,
			**histogram_kwargs)
		color_parameters = self.get_color_parameters(
			histogram=histogram,
			first_facecolor=first_facecolor,
			second_facecolor=second_facecolor,
			rug_facecolor=rug_facecolor)
		(rgb_colors, rgb_rug) = color_parameters
		fig, ax = plt.subplots(
			figsize=figsize)
		ax = self.plot_histogram(
			ax=ax,
			rgb_colors=rgb_colors,
			histogram=histogram)
		handles, labels, handler_map = self.get_bar_legend_handles_and_labels(
			first_facecolor=first_facecolor,
			second_facecolor=second_facecolor)
		if not isinstance(is_show_rug, bool):
			raise ValueError("invalid type(is_show_rug): {}".format(type(is_show_rug)))
		if is_show_rug:
			ax, rug_handle = self.plot_rug(
				ax=ax,
				histogram=histogram,
				rgb_rug=rgb_rug)
			handles.append(
				rug_handle)
			labels.append(
				rug_handle.get_label())
		ax = self.autoformat_plot(
			ax=ax,
			histogram=histogram,
			grouped_headers=grouped_headers,
			diffed_headers=diffed_headers,
			frequencies=frequencies,
			total_weight=total_weight,
			is_show_rug=is_show_rug,
			is_extend_percent_axis=is_extend_percent_axis,
			is_label_midpoints=is_label_midpoints)
		ax, side_leg = self.base_plotter.plot_handles_and_labels_in_side_legend(
			ax=ax,
			handles=handles,
			labels=labels,
			ncol=1,
			handler_map=handler_map)
		fig, ax, leg = self.base_plotter.plot_statistics_in_legend(
			fig=fig,
			ax=ax,
			is_points=True,
			statistics=statistics_by_sub_total_points,
			leg_title="Statistics")
		save_name, save_name_segments = self.base_plotter.get_save_name(
			grouped_headers=grouped_headers,
			diffed_headers=diffed_headers,
			frequencies=frequencies,
			is_points=True,
			is_histogram=True,
			is_save=is_save)
		if is_save:
			(prefix, base_name, suffix) = save_name_segments
			rug_style = self.get_rug_style(
				is_show_rug=is_show_rug)
			axis_style = "wEXT" if is_extend_percent_axis else "woEXT"
			modified_prefix = "{}-{}-{}".format(
				prefix,
				rug_style,
				axis_style)
			save_name = save_name.replace(
				prefix,
				modified_prefix)
		self.base_plotter.visual_settings.display_image(
			fig=fig,
			save_name=save_name,
			space_replacement="_")

class BaseGradeBookGradesHistogramViewerConfiguration(BaseGradeBookHistogramViewerConfiguration):

	def __init__(self, base_plotter):
		super().__init__(
			base_plotter=base_plotter)

	@staticmethod
	def get_offset_at_points_greater_than_weight(offset=0.5):
		return offset

	def get_rescaled_point_value_by_grades(self, point_value):
		
		def get_interpolated_value_between_edges(index_at_right_edge):
			index_at_left_edge = index_at_right_edge - 1
			point_edges = np.copy(
				self.base_plotter.grading_criteria["grade-point edges"])
			total_weight = float(
				self.base_plotter.weights["total"])
			edge_at_left = float(
				point_edges[index_at_left_edge])
			edge_at_right = float(
				point_edges[index_at_right_edge])
			if np.isinf(edge_at_right):
				modified_edge_at_right = float(
					total_weight)
			elif edge_at_right >= total_weight:
				modified_edge_at_right = float(
					total_weight)
			else:
				modified_edge_at_right = float(
					edge_at_right)
			width = modified_edge_at_right - edge_at_left
			# displacement_from_left = point_value - edge_at_left
			# delta = displacement_from_left / width
			# rescaled_point_value = index_at_left_edge + delta
			displacement_from_right = modified_edge_at_right - point_value
			delta = displacement_from_right / width
			rescaled_point_value = index_at_right_edge - delta
			return rescaled_point_value

		if np.isnan(point_value):
			rescaled_point_value = np.nan
		else:
			if point_value == 0:
				rescaled_point_value = float(
					0)
			else:
				points_at_fail = float(
					self.base_plotter.grading_criteria["points at fail"])
				total_weight = float(
					self.base_plotter.weights["total"])
				tick_at_fail = 1 ## fail-score ==> bin-edge at index=1
				tick_at_weight = len(
					self.base_plotter.grading_criteria["grade-point edges"]) - 1
				if point_value < points_at_fail:
					index_at_right_edge = int(
						tick_at_fail)
					rescaled_point_value = get_interpolated_value_between_edges(
						index_at_right_edge=index_at_right_edge)
				elif point_value == points_at_fail:
					rescaled_point_value = float(
						tick_at_fail)
				elif (points_at_fail < point_value) and (point_value < total_weight):
					index_at_right_edge = int(
						np.searchsorted(
							self.base_plotter.grading_criteria["grade-point edges"],
							point_value))
					rescaled_point_value = get_interpolated_value_between_edges(
						index_at_right_edge=index_at_right_edge)
				elif point_value == total_weight:
					rescaled_point_value = float(
						tick_at_weight)
				else: # elif point_value > total_weight:
					offset_at_points_gt_weight = self.get_offset_at_points_greater_than_weight()
					rescaled_point_value = tick_at_weight + offset_at_points_gt_weight
		return rescaled_point_value

	def add_mirror_axis_with_non_uniform_percents(self, ax, percents):
		if not isinstance(percents, np.ndarray):
			raise ValueError("invalid type(percents): {}".format(type(percents)))
		total_weight = float(
			self.base_plotter.weights["total"])
		points = percents / 100 * total_weight
		x_major_ticklabels = np.core.defchararray.add(
			percents.astype(
				str),
			[" %"] * percents.size)
		x_major_ticks = list()
		for point_value in points:
			tick_value = self.get_rescaled_point_value_by_grades(
				point_value=point_value)
			x_major_ticks.append(
				tick_value)
		mirror_ax = self.base_plotter.visual_settings.get_mirror_ax(
			ax=ax,
			frameon=False)
		mirror_ax = self.base_plotter.visual_settings.autoformat_axis_ticks_and_ticklabels(
			ax=mirror_ax,
			x_major_ticks=x_major_ticks,
			x_major_ticklabels=x_major_ticklabels,
			x_minor_ticks=False,
			y_major_ticks=False,
			y_major_ticklabels=False,
			y_minor_ticks=False)
		mirror_ax.tick_params(
			axis="x",
			direction="in",
			pad=-15)
		mirror_ax.set_xlim(
			ax.get_xlim())
		mirror_ax.set_ylim(
			ax.get_ylim())
		return ax, mirror_ax

	def plot_grade_labels(self, ax, rgb_colors, vertical_offset=0.325):
		for x, y, grade_label, rgb_color in zip(self.base_plotter.grades_histogram.bin_midpoints, self.base_plotter.grades_histogram.bin_counts, self.base_plotter.grading_criteria["possible grades"], rgb_colors):
			ax.text(
				x,
				y + vertical_offset,
				grade_label,
				fontsize=self.base_plotter.visual_settings.label_size,
				color=rgb_color,
				ha="center")
		return ax

	def plot_rug(self, ax, rgb_rug, rug_marker="x", rug_alpha=0.35):
		x = list()
		for point_value in self.base_plotter.grades_histogram.distribution_values:
			x_at_rug = self.get_rescaled_point_value_by_grades(
				point_value=point_value)
			x.append(
				x_at_rug)
		y_at_rug = self.get_y_at_rug()
		y = np.full(
			fill_value=y_at_rug,
			shape=self.base_plotter.grades_histogram.distribution_values.size,
			dtype=float)
		rug_handle = ax.scatter(
			x,
			y,
			label="Rug",
			color=rgb_rug,
			marker=rug_marker,
			alpha=rug_alpha)
		return ax, rug_handle

	def autoformat_plot(self, ax, edges_at_points):

		def update_ticks_and_ticklabels(ax, edges_at_points):
			y_major_ticks = np.arange(
				1,
				self.base_plotter.number_students * 2,
				2,
				dtype=int)
			y_minor_ticks = np.arange(
				0,
				self.base_plotter.number_students * 2,
				2,
				dtype=int)
			x_major_ticks = np.copy(
				self.base_plotter.grades_histogram.bin_edges)
			x_minor_ticks = np.copy(
				self.base_plotter.grades_histogram.bin_midpoints)
			x_major_ticklabels = [
				r"${:,.2f}$".format(bin_edge)
					for bin_edge in edges_at_points]
			x_major_ticklabels[0] = r"$-1$ $\leftarrow$ $0$"
			x_major_ticklabels[-1] = r"${:,.2f}$ $\rightarrow$ $\infty$".format(
				self.base_plotter.weights["total"])
			ax = self.base_plotter.visual_settings.autoformat_axis_ticks_and_ticklabels(
				ax=ax,
				x_major_ticks=x_major_ticks,
				y_major_ticks=y_major_ticks,
				x_minor_ticks=x_minor_ticks,
				y_minor_ticks=y_minor_ticks,
				x_major_ticklabels=x_major_ticklabels,
				y_major_ticklabels=True,
				x_minor_ticklabels=False,
				y_minor_ticklabels=False)
			ax = self.base_plotter.visual_settings.autoformat_grid(
				ax=ax,
				grid_color="gray")
			return ax

		def update_axis_labels(ax):
			xlabel = "Points"
			ylabel = "Number of Students"
			title, _ = self.base_plotter.get_title(
				is_grades=True,
				is_histogram=True)
			ax = self.base_plotter.visual_settings.autoformat_axis_labels(
				ax=ax,
				xlabel=xlabel,
				ylabel=ylabel,
				title=title)
			return ax

		def update_axis_limits(ax):
			if np.any(self.base_plotter.points["total"] > self.base_plotter.weights["total"]):
				offset_at_points_gt_weight = self.get_offset_at_points_greater_than_weight()
				x_max = self.base_plotter.grades_histogram.bin_edges[-1] + (2 * offset_at_points_gt_weight)
			else:
				x_max = float(
					self.base_plotter.grades_histogram.bin_edges[-1])
			xlim = (
				self.base_plotter.grades_histogram.bin_edges[0],
				x_max)
			ylim = (
				0,
				1.125 * np.max(
					self.base_plotter.grades_histogram.bin_counts))
			ax = self.base_plotter.visual_settings.autoformat_axis_limits(
				ax=ax,
				xlim=xlim,
				ylim=ylim)
			return ax

		ax = update_ticks_and_ticklabels(
			ax=ax,
			edges_at_points=edges_at_points)
		ax = update_axis_labels(
			ax=ax)
		ax = update_axis_limits(
			ax=ax)
		return ax

class GradeBookGradesHistogramViewerConfiguration(BaseGradeBookGradesHistogramViewerConfiguration):

	def __init__(self, base_plotter):
		super().__init__(
			base_plotter=base_plotter)

	def view_histogram(self, is_show_rug, first_facecolor, second_facecolor, rug_facecolor, figsize, is_save):
		edges_at_points = np.copy(
			self.base_plotter.grading_criteria["grade-point edges"])
		color_parameters = self.get_color_parameters(
			histogram=self.base_plotter.grades_histogram,
			first_facecolor=first_facecolor,
			second_facecolor=second_facecolor,
			rug_facecolor=rug_facecolor)
		(rgb_colors, rgb_rug) = color_parameters
		fig, ax = plt.subplots(
			figsize=figsize)
		ax = self.plot_histogram(
			ax=ax,
			rgb_colors=rgb_colors,
			histogram=self.base_plotter.grades_histogram)
		handles, labels, handler_map = self.get_bar_legend_handles_and_labels(
			first_facecolor=first_facecolor,
			second_facecolor=second_facecolor)
		ax = self.plot_grade_labels(
			ax=ax,
			rgb_colors=rgb_colors)
		if not isinstance(is_show_rug, bool):
			raise ValueError("invalid type(is_show_rug): {}".format(type(is_show_rug)))
		if is_show_rug:
			ax, rug_handle = self.plot_rug(
				ax=ax,
				rgb_rug=rgb_rug)
			handles.append(
				rug_handle)
			labels.append(
				rug_handle.get_label())
		grade_handles, grade_labels = self.base_plotter.get_grade_handles_and_labels(
			ax=ax)
		handles.extend(
			grade_handles)
		labels.extend(
			grade_labels)
		ax = self.autoformat_plot(
			ax=ax,
			edges_at_points=edges_at_points)
		percents = self.base_plotter.select_percents(
			percents=True)
		ax, mirror_ax = self.add_mirror_axis_with_non_uniform_percents(
			ax=ax,
			percents=percents)
		ax, side_leg = self.base_plotter.plot_handles_and_labels_in_side_legend(
			ax=ax,
			handles=handles,
			labels=labels,
			ncol=1,
			handler_map=handler_map)
		fig, ax, leg = self.base_plotter.plot_statistics_in_legend(
			fig=fig,
			ax=ax,
			is_grades=True,
			statistics=self.base_plotter.statistics["points"]["total"],
			leg_title="Statistics")
		save_name, save_name_segments = self.base_plotter.get_save_name(
			is_grades=True,
			is_histogram=True,
			is_save=is_save)
		if is_save:
			(prefix, base_name, suffix) = save_name_segments
			rug_style = self.get_rug_style(
				is_show_rug=is_show_rug)
			modified_prefix = "{}-{}".format(
				prefix,
				rug_style)
			save_name = save_name.replace(
				prefix,
				modified_prefix)
		self.base_plotter.visual_settings.display_image(
			fig=fig,
			save_name=save_name,
			space_replacement="_")

##