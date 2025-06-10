import numpy as np
import matplotlib.pyplot as plt
from distance_matrix_configuration import DistanceMatrixConfiguration
from plotter_base_configuration import BaseGradeBookPlotterConfiguration
from visual_settings_configuration import (
	ListedColormap,
	ScalarMappable,
	Colorbar,
	make_axes_locatable)


class BaseGradeBookHeatMapViewerConfiguration():

	def __init__(self, base_plotter):
		super().__init__()
		self.base_plotter = base_plotter

	@staticmethod
	def plot_heat_map(ax, distance_matrix, true_cmap, norm):
		handle = ax.imshow(
			distance_matrix,
			cmap=true_cmap,
			norm=norm,
			interpolation="nearest",
			origin="upper")
		return ax, handle

	@staticmethod
	def get_sub_totals(sub_total_points, sub_total_percents, total_weight, is_show_perfect_score):

		def get_modified_sub_total_points(sub_total_points, total_weight, is_show_perfect_score):
			if is_show_perfect_score:
				modified_sub_total_points = np.insert(
					sub_total_points,
					0,
					total_weight)
			else:
				modified_sub_total_points = np.copy(
					sub_total_points)
			return modified_sub_total_points

		def get_modified_sub_total_percents(sub_total_percents, is_show_perfect_score):
			if is_show_perfect_score:
				modified_sub_total_percents = np.insert(
					sub_total_percents,
					0,
					100)
			else:
				modified_sub_total_percents = np.copy(
					sub_total_percents)
			return modified_sub_total_percents

		modified_sub_total_points = get_modified_sub_total_points(
			sub_total_points=sub_total_points,
			total_weight=total_weight,
			is_show_perfect_score=is_show_perfect_score)
		modified_sub_total_percents = get_modified_sub_total_percents(
			sub_total_percents=sub_total_percents,
			is_show_perfect_score=is_show_perfect_score)
		return (modified_sub_total_points, modified_sub_total_percents)

	def get_color_parameters(self, cmap, diagonal_color, distance_matrix):
		number_colors = int(
			np.ceil(
				np.nanmax(
					distance_matrix)))
		_, norm = self.base_plotter.visual_settings.get_rgb_facecolors(
			cmap=cmap,
			number_colors=number_colors)
		true_cmap = plt.get_cmap(
			cmap)
		if diagonal_color is not None:
			true_cmap.set_bad(
				diagonal_color)
		color_parameters = (
			true_cmap,
			norm)
		return color_parameters

	def add_dissimilarity_labels(self, ax, distance_matrix, norm, first_text_color, second_text_color):
		dissimilarity_matrix = np.round(
			distance_matrix,
			decimals=1)
		for c in range(dissimilarity_matrix.shape[1]):
			for r in range(dissimilarity_matrix.shape[0]):
				if r == c:
					text_color = "gray"
					s = ""
				else:
					dissimilarity_value = float(
						distance_matrix[r, c])
					color_value = norm(
						dissimilarity_value)
					is_above_color_threshold = color_value > 0.5
					text_color = first_text_color if is_above_color_threshold else second_text_color
					s = r"${:,.1f}$".format(
						dissimilarity_value)
				ax.text(
					r,
					c,
					s,
					color=text_color,
					ha="center",
					va="center",
					weight="semibold",
					fontsize=self.base_plotter.visual_settings.text_size)
		return ax

	def autoformat_plot(self, ax, grouped_headers, diffed_headers, frequencies, is_show_perfect_score, student_identifier):

		def get_ticks_and_ticklabels(is_show_perfect_score, student_identifier):
			ticks = list(
				range(
					self.base_plotter.number_students))
			if is_show_perfect_score:
				ticks.append(
					self.base_plotter.number_students)
			ticks = np.array(
				ticks)
			if student_identifier is None:
				ticklabels = [
					""
						for _ in range(
							self.base_plotter.number_students)]
			else:
				if student_identifier not in self.base_plotter.student_identifiers:
					raise ValueError("invalid student_identifier: {}".format(student_identifier))
				modified_student_identifier = student_identifier.lower()
				modified_student_identifier = modified_student_identifier.replace(
					" ",
					"_")
				modified_student_identifier = modified_student_identifier.replace(
					"-",
					"_")
				ticklabels = list()
				for student in self.base_plotter.students:
					ticklabel = getattr(
						student,
						modified_student_identifier)
					ticklabels.append(
						ticklabel)
			if is_show_perfect_score:
				ticklabels.insert(
					0,
					"Perfect Score")
			return (ticks, ticklabels)

		(ticks, ticklabels) = get_ticks_and_ticklabels(
			is_show_perfect_score=is_show_perfect_score,
			student_identifier=student_identifier)
		ax = self.base_plotter.visual_settings.autoformat_axis_ticks_and_ticklabels(
			ax=ax,
			x_major_ticks=ticks,
			y_major_ticks=ticks,
			x_minor_ticks=False,
			y_minor_ticks=False,
			x_major_ticklabels=ticklabels,
			y_major_ticklabels=ticklabels,
			x_minor_ticklabels=False,
			y_minor_ticklabels=False)
		for xticklabel in ax.get_xticklabels():
			xticklabel.set_rotation(
				90)
		ax.tick_params(
			axis="both",
			colors="gray")
		ax = self.base_plotter.visual_settings.autoformat_grid(
			ax=ax,
			grid_color="gray")
		axis_label = "Students"
		title, _ = self.base_plotter.get_title(
			grouped_headers=grouped_headers,
			diffed_headers=diffed_headers,
			frequencies=frequencies,
			is_points=True,
			is_percents=False,
			is_heat_map=True)
		title += "\n"
		ax = self.base_plotter.visual_settings.autoformat_axis_labels(
			ax=ax,
			xlabel=axis_label,
			ylabel=axis_label,
			title=title)
		return ax

	def add_color_bar(self, fig, ax, handle, true_cmap, diagonal_color, is_only_curve_selected, flat_upper_triangle, total_weight):
		cbar = fig.colorbar(
			handle,
			ax=ax,
			orientation="vertical",
			shrink=0.5,
			pad=0.1,
			extend="max")
		if not is_only_curve_selected:
			largest_point_difference = np.max(
				flat_upper_triangle)
			largest_percent_difference = self.base_plotter.get_percents_from_weighted_scores(
				values=largest_point_difference,
				weights=total_weight)
			rounded_percent_difference = int(
				np.ceil(largest_percent_difference / 10) * 10)
			major_percent_spacing = 25
			if rounded_percent_difference <= major_percent_spacing:
				rounded_percent_difference = 100
			cbar.ax.yaxis.set_ticks_position(
				"left")
			cbar.ax.yaxis.set_label_position(
				"left")
			mirror_major_ticks = np.arange(
				0,
				rounded_percent_difference + 1,
				major_percent_spacing,
				dtype=int)
			mirror_major_ticklabels = [
				r"${} \%$".format(tick)
					for tick in mirror_major_ticks]
			mirror_minor_ticks = np.arange(
				0,
				rounded_percent_difference + 1,
				5,
				dtype=int)
			major_ticks = mirror_major_ticks * total_weight / 100
			minor_ticks = mirror_minor_ticks * total_weight / 100
			mirror_ax = cbar.ax.twinx()
			mirror_ax = self.base_plotter.visual_settings.autoformat_axis_ticks_and_ticklabels(
				ax=mirror_ax,
				x_major_ticks=False,
				y_major_ticks=major_ticks,
				x_minor_ticks=False,
				y_minor_ticks=minor_ticks,
				x_major_ticklabels=False,
				y_major_ticklabels=mirror_major_ticklabels,
				x_minor_ticklabels=False,
				y_minor_ticklabels=False)
			mirror_ax.set_ylim(
				cbar.ax.get_ylim())
			cbar.ax.set_ylabel(
				"Point Difference",
				fontsize=self.base_plotter.visual_settings.label_size)
			mirror_ax.set_ylabel(
				"Percent of Total Weight",
				fontsize=self.base_plotter.visual_settings.label_size)
		cbar.ax.tick_params(
			labelsize=self.base_plotter.visual_settings.tick_size)
		cbar.ax.set_title(
			"Dis-Similarity\nof Scores",
			fontsize=self.base_plotter.visual_settings.label_size)
		if diagonal_color is None:
			diagonal_cbar = None
		else:
			if is_only_curve_selected:
				scalar_cmap = ListedColormap([
					true_cmap.get_bad()])
				scalar_mappable = ScalarMappable(
					cmap=scalar_cmap)
				divider = make_axes_locatable(
					cbar.ax)
				scalar_ax = divider.append_axes(
					"bottom",
					size="5%",
					pad="3%",
					aspect=1,
					anchor=cbar.ax.get_anchor())
				scalar_ax.grid(
					visible=False,
					which="both",
					axis="both")
				diagonal_cbar = Colorbar(
					ax=scalar_ax,
					mappable=scalar_mappable,
					orientation="vertical")
				scalar_ticks = [
					0.5]
				scalar_ticklabels = [
					"diagonal"]
				diagonal_cbar.set_ticks(
					scalar_ticks,
					labels=scalar_ticklabels)
				diagonal_cbar.ax.tick_params(
					length=0,
					labelsize=self.base_plotter.visual_settings.tick_size)
			else:
				diagonal_cbar = None
		return fig, ax, cbar, diagonal_cbar

class GradeBookHeatMapViewerConfiguration(BaseGradeBookHeatMapViewerConfiguration):

	def __init__(self, base_plotter):
		super().__init__(
			base_plotter=base_plotter)

	def view_heat_map(self, home_work_indices, home_work_headers, exam_indices, exam_headers, extra_credit_indices, extra_credit_headers, curve_headers, student_identifier, distance_metric, is_label_dissimilarity, cmap, first_text_color, second_text_color, diagonal_color, figsize, is_save):
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
		(modified_sub_total_points, modified_sub_total_percents) = self.get_sub_totals(
			sub_total_points=sub_total_points,
			sub_total_percents=sub_total_percents,
			total_weight=total_weight,
			is_show_perfect_score=is_show_perfect_score)
		distance_matrix = DistanceMatrixConfiguration().get_distance_matrix(
			coordinates=modified_sub_total_points,
			distance_metric=distance_metric,
			is_mask_diagonal=True,
			mask_value=np.nan)
		flat_upper_triangle = DistanceMatrixConfiguration().get_flat_upper_triangle(
			mat=distance_matrix)
		statistics_by_flat_upper_triangle = self.base_plotter.get_statistics(
			flat_upper_triangle,
			ddof=0,
			axis=None)
		color_parameters = self.get_color_parameters(
			cmap=cmap,
			diagonal_color=diagonal_color,
			distance_matrix=distance_matrix)
		(true_cmap, norm) = color_parameters
		fig, ax = plt.subplots(
			figsize=figsize)
		ax, handle = self.plot_heat_map(
			ax=ax,
			distance_matrix=distance_matrix,
			true_cmap=true_cmap,
			norm=norm)
		if is_label_dissimilarity:
			ax = self.add_dissimilarity_labels(
				ax=ax,
				distance_matrix=distance_matrix,
				norm=norm,
				first_text_color=first_text_color,
				second_text_color=second_text_color)
		ax = self.autoformat_plot(
			ax=ax,
			grouped_headers=grouped_headers,
			diffed_headers=diffed_headers,
			frequencies=frequencies,
			is_show_perfect_score=is_show_perfect_score,
			student_identifier=student_identifier)
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
			statistics=statistics_by_flat_upper_triangle,
			leg_title="Statistics",
			**leg_kwargs)
		fig, ax, cbar, diagonal_cbar = self.add_color_bar(
			fig=fig,
			ax=ax,
			handle=handle,
			true_cmap=true_cmap,
			diagonal_color=diagonal_color,
			is_only_curve_selected=is_only_curve_selected,
			flat_upper_triangle=flat_upper_triangle,
			total_weight=total_weight)
		save_name, _ = self.base_plotter.get_save_name(
			grouped_headers=grouped_headers,
			diffed_headers=diffed_headers,
			frequencies=frequencies,
			is_points=True,
			is_percents=False,
			is_heat_map=True,
			is_save=is_save)
		self.base_plotter.visual_settings.display_image(
			fig=fig,
			save_name=save_name,
			space_replacement="_")

##