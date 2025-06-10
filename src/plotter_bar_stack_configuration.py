import numpy as np
import matplotlib.pyplot as plt
from plotter_base_configuration import BaseGradeBookPlotterConfiguration


class BaseGradeBookBarStackViewerConfiguration():

	def __init__(self, base_plotter):
		super().__init__()
		self.base_plotter = base_plotter

	@staticmethod
	def get_number_stacks(grouped_headers, diffed_headers, is_differentiate_stacks):
		if not isinstance(is_differentiate_stacks, bool):
			raise ValueError("invalid type(is_differentiate_stacks): {}".format(type(is_differentiate_stacks)))
		if is_differentiate_stacks:
			number_stacks = len(
				diffed_headers)
		else:
			number_stacks = len(
				grouped_headers)
		return number_stacks

	def get_color_parameters(self, cmap, edgecolor, number_stacks):
		rgb_colors, norm = self.base_plotter.visual_settings.get_rgb_facecolors(
			cmap=cmap,
			number_colors=number_stacks)
		if edgecolor is None:
			rgb_edgecolor = "none"
		else:
			(rgb_edgecolor, _) = self.base_plotter.visual_settings.get_rgb_facecolors(
				facecolor=edgecolor,
				number_colors=1)
		return (rgb_colors, rgb_edgecolor, norm)

	def plot_bar_stacks(self, ax, grouped_headers, diffed_headers, frequencies, diffed_points, diffed_weights, rgb_colors, rgb_edgecolor, is_show_perfect_score, is_differentiate_stacks):
		
		def get_autocorrected_height(height, weight, is_show_perfect_score):
			if is_show_perfect_score:
				new_height = np.insert(
					height,
					0,
					weight)
			else:
				new_height = height
			return new_height

		def plot_stacks(ax, x, height, bottom, rgb_color, rgb_edgecolor, label):
			ax.bar(
				x,
				height,
				bottom=bottom,
				color=rgb_color,
				edgecolor=rgb_edgecolor,
				label=label,
				width=1,
				align="center")
			return ax

		def get_updated_bottom(bottom, height):
			values = np.array([
				bottom,
				height])
			new_bottom = np.nansum(
				values,
				axis=0)
			return new_bottom

		if is_show_perfect_score:
			x = np.arange(
				self.base_plotter.number_students + 1)
		else:
			x = np.arange(
				self.base_plotter.number_students)
		bottom = np.full(
			fill_value=0,
			shape=x.shape,
			dtype=float)
		transposed_points = np.copy(diffed_points).T
		if is_differentiate_stacks:
			for diffed_header, sub_scores, weight, rgb_color in zip(diffed_headers, transposed_points, diffed_weights, rgb_colors):
				height = np.copy(
					sub_scores)
				height = get_autocorrected_height(
					height=height,
					weight=weight,
					is_show_perfect_score=is_show_perfect_score)
				ax = plot_stacks(
					ax=ax,
					x=x,
					height=height,
					bottom=bottom,
					rgb_color=rgb_color,
					rgb_edgecolor=rgb_edgecolor,
					label=diffed_header)
				bottom = get_updated_bottom(
					bottom=bottom,
					height=height)
		else:
			it_scores = iter(
				transposed_points)
			it_weights = iter(
				diffed_weights)
			for grouped_header, frequency, rgb_color in zip(grouped_headers, frequencies, rgb_colors):
				current_scores = list()
				current_weights = list()
				for frequency_count in range(frequency):
					current_scores.append(
						next(
							it_scores))
					current_weights.append(
						next(
							it_weights))
				current_scores = np.array(
					current_scores)
				current_weights = np.array(
					current_weights)
				weight = np.sum(
					current_weights)
				height = np.nansum(
					current_scores,
					axis=0)
				height = get_autocorrected_height(
					height=height,
					weight=weight,
					is_show_perfect_score=is_show_perfect_score)
				ax = plot_stacks(
					ax=ax,
					x=x,
					height=height,
					bottom=bottom,
					rgb_color=rgb_color,
					rgb_edgecolor=rgb_edgecolor,
					label=grouped_header)
				bottom = get_updated_bottom(
					bottom=bottom,
					height=height)
		return ax

	def autoformat_plot(self, ax, grouped_headers, diffed_headers, frequencies, sub_totals, total_weight, is_show_perfect_score, student_identifier):
		if is_show_perfect_score:
			x_major_ticks = np.arange(
				self.base_plotter.number_students + 1)
		else:
			x_major_ticks = np.arange(
				self.base_plotter.number_students)
		ticklabel_at_perfect_score = "Perfect\nScore"
		if student_identifier is None:
			if is_show_perfect_score:
				x_major_ticklabels = [ticklabel_at_perfect_score] + [""] * self.base_plotter.number_students
			else:
				x_major_ticklabels = False
		else:
			if student_identifier not in self.base_plotter.student_identifiers:
				raise ValueError("invalid student_identifier: {}".format(student_identifier))
			x_major_ticklabels = list()
			if is_show_perfect_score:
				x_major_ticklabels.append(
					ticklabel_at_perfect_score)

			modified_student_identifier = student_identifier.lower()
			modified_student_identifier = modified_student_identifier.replace(
				" ",
				"_")
			modified_student_identifier = modified_student_identifier.replace(
				"-",
				"_")
			for student in self.base_plotter.students:
				ticklabel = getattr(
					student,
					modified_student_identifier)
				x_major_ticklabels.append(
					ticklabel)
		ax = self.base_plotter.visual_settings.autoformat_axis_ticks_and_ticklabels(
			ax=ax,
			x_major_ticks=x_major_ticks,
			y_major_ticks=True,
			x_minor_ticks=False,
			y_minor_ticks=True,
			x_major_ticklabels=x_major_ticklabels,
			y_major_ticklabels=True)
		if student_identifier is not None:
			for xticklabel in ax.get_xticklabels():
				xticklabel.set_rotation(
					90)
		ax = self.base_plotter.visual_settings.autoformat_grid(
			ax=ax,
			grid_color="gray")
		xlabel = "Students"
		ylabel = "Points"
		title, _ = self.base_plotter.get_title(
			grouped_headers=grouped_headers,
			diffed_headers=diffed_headers,
			frequencies=frequencies,
			is_points=True,
			is_stacked_bars=True)
		ax = self.base_plotter.visual_settings.autoformat_axis_labels(
			ax=ax,
			xlabel=xlabel,
			ylabel=ylabel,
			title=title)
		if total_weight > 0:
			xlim = (
				x_major_ticks[0] - 1,
				x_major_ticks[-1] + 1.5) ## extra space for percentage labels along mirror y-axis
			y_max = float(
				total_weight)
		else:
			xlim = (
				x_major_ticks[0] - 1,
				x_major_ticks[-1] + 1)
			y_max = np.nanmax(
				sub_totals)
		ylim = (
			0,
			1.05 * y_max)
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
				axis="y")
		return ax

class GradeBookBarStackViewerConfiguration(BaseGradeBookBarStackViewerConfiguration):

	def __init__(self, base_plotter):
		super().__init__(
			base_plotter=base_plotter)

	def view_bar_stacks(self, home_work_indices, home_work_headers, exam_indices, exam_headers, extra_credit_indices, extra_credit_headers, curve_headers, is_differentiate_stacks, student_identifier, cmap, edgecolor, figsize, is_save):
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
		is_show_perfect_score = np.invert(
			is_only_curve_selected)
		number_stacks = self.get_number_stacks(
			grouped_headers=grouped_headers,
			diffed_headers=diffed_headers,
			is_differentiate_stacks=is_differentiate_stacks)
		color_parameters = self.get_color_parameters(
			cmap=cmap,
			edgecolor=edgecolor,
			number_stacks=number_stacks)
		(rgb_colors, rgb_edgecolor, _) = color_parameters
		fig, ax = plt.subplots(
			figsize=figsize)
		ax = self.plot_bar_stacks(
			ax=ax,
			grouped_headers=grouped_headers,
			diffed_headers=diffed_headers,
			frequencies=frequencies,
			diffed_points=diffed_points,
			diffed_weights=diffed_weights,
			rgb_colors=rgb_colors,
			rgb_edgecolor=rgb_edgecolor,
			is_show_perfect_score=is_show_perfect_score,
			is_differentiate_stacks=is_differentiate_stacks)
		ax = self.autoformat_plot(
			ax=ax,
			grouped_headers=grouped_headers,
			diffed_headers=diffed_headers,
			frequencies=frequencies,
			sub_totals=sub_total_points,
			total_weight=total_weight,
			is_show_perfect_score=is_show_perfect_score,
			student_identifier=student_identifier)
		handles, labels = ax.get_legend_handles_labels()
		ax, side_leg = self.base_plotter.plot_handles_and_labels_in_side_legend(
			ax=ax,
			handles=handles,
			labels=labels,
			ncol=1)		
		leg_kwargs = dict()
		if student_identifier in ("name", "email address"):
			bbox_to_anchor = [
				0,
				-0.1375,
				1,
				1]
			leg_kwargs["bbox_to_anchor"] = bbox_to_anchor
			leg_kwargs["bbox_transform"] = fig.transFigure
		fig, ax, leg = self.base_plotter.plot_statistics_in_legend(
			fig=fig,
			ax=ax,
			is_grades=True,
			statistics=statistics_by_sub_total_points,
			leg_title="Statistics",
			**leg_kwargs)
		save_name, save_name_segments = self.base_plotter.get_save_name(
			grouped_headers=grouped_headers,
			diffed_headers=diffed_headers,
			frequencies=frequencies,
			is_points=True,
			is_stacked_bars=True,
			is_save=is_save)
		if is_save:
			(prefix, base_name, suffix) = save_name_segments
			stack_style = "wDIFF" if is_differentiate_stacks else "woDIFF"
			modified_prefix = "{}-{}".format(
				prefix,
				stack_style)
			save_name = save_name.replace(
				prefix,
				modified_prefix)
		self.base_plotter.visual_settings.display_image(
			fig=fig,
			save_name=save_name,
			space_replacement="_")

##