import numpy as np
import matplotlib.pyplot as plt
from visual_settings_configuration import (
	Patch,
	Line2D)
from plotter_base_configuration import BaseGradeBookPlotterConfiguration


class BaseGradeBookBoxPlotViewerConfiguration():

	def __init__(self, base_plotter):
		super().__init__()
		self.base_plotter = base_plotter

	@staticmethod
	def plot_box_plot(ax, box_statistics, box_edge_color, box_fill_color, mean_color, median_color, fliers_color, mean_marker, median_linestyle, fliers_marker, fliers_alpha):
		ax.bxp(
			box_statistics,
			showmeans=True,
			showfliers=True,
			patch_artist=True,
			boxprops={
				"facecolor" : box_fill_color,
				"edgecolor" : box_edge_color},
			meanprops={
				"marker" : mean_marker,
				"markerfacecolor" : mean_color},
			medianprops={
				"color" : median_color,
				"linestyle" : median_linestyle},
			flierprops={
				"marker" : fliers_marker,
				"markerfacecolor" : fliers_color,
				"markeredgecolor" : fliers_color,
				"alpha" : fliers_alpha})
		return ax

	@staticmethod
	def get_side_legend_handles_and_labels(box_fill_color, box_edge_color, mean_color, median_color, fliers_color, mean_marker, median_linestyle, fliers_marker, fliers_alpha):
		handle_at_box = Patch(
			label="IQR",
			facecolor=box_fill_color,
			edgecolor=box_edge_color)
		handle_at_mean = Line2D(
			list(),
			list(),
			label="mean",
			color=mean_color,
			linewidth=0,
			marker=mean_marker)
		handle_at_median = Line2D(
			list(),
			list(),
			label="median",
			color=median_color,
			linestyle=median_linestyle)
		handle_at_fliers = Line2D(
			list(),
			list(),
			label="fliers",
			color=fliers_color,
			linewidth=0,
			marker=fliers_marker,
			alpha=fliers_alpha)
		handles = [
			handle_at_box,
			handle_at_mean,
			handle_at_median,
			handle_at_fliers]
		labels = [
			handle.get_label()
				for handle in handles]
		return handles, labels

	@staticmethod
	def get_selected_box_parameters(is_points, is_percents, is_sub_totals, diffed_weights, total_weight, diffed_points, diffed_percents, sub_total_points, sub_total_percents, statistics_by_diffed_points, statistics_by_diffed_percents, statistics_by_sub_total_points, statistics_by_sub_total_percents):
		if is_sub_totals:
			box_weights = float(
				total_weight)
			if is_points:
				box_scores = sub_total_points
				tmp_statistics = statistics_by_sub_total_points
			elif is_percents:
				box_scores = sub_total_percents
				tmp_statistics = statistics_by_sub_total_percents
			else:
				raise ValueError("invalid combination of is_points={} and is_percents={}".format(is_points, is_percents))
		else:
			box_weights = np.copy(
				diffed_weights)
			if is_points:
				box_scores = diffed_points
				tmp_statistics = statistics_by_diffed_points
			elif is_percents:
				box_scores = diffed_percents
				tmp_statistics = statistics_by_diffed_percents
			else:
				raise ValueError("invalid combination of is_points={} and is_percents={}".format(is_points, is_percents))
		return box_scores, box_weights, tmp_statistics

	def get_box_transformed_statistics(self, is_points, is_percents, is_sub_totals, diffed_headers, scores, weights, statistics):

		def get_box_statistic_parameters(is_points, is_percents, values, weight, statistics, label):
			whis = 1.5 ## ctrl + f: "turkey" --> https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.boxplot.html#matplotlib.axes.Axes.boxplot
			first_and_third_quantiles = (
				0.25,
				0.75)
			(q1, q3) = np.nanquantile(
				values,
				first_and_third_quantiles)
			iqr = q3 - q1
			true_whislo = q1 - iqr * whis
			true_whishi = q3 + iqr * whis
			fliers_condition_one = (values < true_whislo) | (values > true_whishi)
			fliers_condition_two = np.invert(
				np.isnan(
					values))
			true_fliers = values[(fliers_condition_one & fliers_condition_two)].tolist()
			box_statistic_parameters = {
				# "iqr" : iqr,
				"whis" : whis,
				"q1" : q1,
				"q3" : q3,
				"whislo" : 0, # whislo,
				"whishi" : weight, # whishi,
				"fliers" : true_fliers}
			if is_points:
				box_statistic_parameters["whislo"] = 0 # whislo
				box_statistic_parameters["whishi"] = weight # whishi
				box_statistic_parameters["fliers"] = true_fliers
			elif is_percents:
				modified_fliers = np.array(
					true_fliers)
				percent_fliers = self.base_plotter.get_percents_from_weighted_scores(
					values=modified_fliers,
					weights=weight)
				percent_fliers = percent_fliers.tolist()
				box_statistic_parameters["whislo"] = 0 # whislo / weight
				box_statistic_parameters["whishi"] = 100 # whishi / weight
				box_statistic_parameters["fliers"] = percent_fliers
			else:
				raise ValueError("invalid combination of is_points={} and is_percents={}".format(is_points, is_percents))
			modified_label = label.replace(
				" ",
				"\n")
			box_statistic_parameters["mean"] = statistics["mean"]
			box_statistic_parameters["med"] = statistics["median"]
			box_statistic_parameters["label"] = modified_label
			return box_statistic_parameters

		box_statistics = list()
		if is_sub_totals:
			partial_box_statistics = get_box_statistic_parameters(
				is_points=is_points,
				is_percents=is_percents,
				values=scores,
				weight=weights,
				statistics=statistics,
				label="Total")
			box_statistics.append(
				partial_box_statistics)
		else:
			for diffed_header, values, weight, diffed_statistics in zip(diffed_headers, scores.T, weights, statistics):
				partial_box_statistics = get_box_statistic_parameters(
					is_points=is_points,
					is_percents=is_percents,
					values=values,
					weight=weight,
					statistics=diffed_statistics,
					label=diffed_header)
				box_statistics.append(
					partial_box_statistics)
		return box_statistics

	def autoformat_plot(self, ax, is_points, is_percents, is_sub_totals, grouped_headers, diffed_headers, frequencies, values, weights):
		
		def update_ticks_and_ticklabels(ax, is_points, is_percents):
			x_major_ticks = ax.get_xticks()
			x_major_ticklabels = ax.get_xticklabels()
			if is_points:
				y_major_ticks = True
				y_minor_ticks = True
				y_major_fmt = "{:,.2f}"
			elif is_percents:
				y_major_ticks = np.arange(
					0,
					101,
					10,
					dtype=int)
				y_minor_ticks = np.arange(
					5,
					101,
					10,
					dtype=int)
				y_major_fmt = r"{:,.2f} $\%$"
			else:
				raise ValueError("invalid combination of is_points={} and is_percents={}".format(is_points, is_percents))
			ax = self.base_plotter.visual_settings.autoformat_axis_ticks_and_ticklabels(
				ax=ax,
				x_major_ticks=x_major_ticks,
				x_major_ticklabels=x_major_ticklabels,
				y_major_ticks=y_major_ticks,
				y_major_ticklabels=True,
				y_major_fmt=y_major_fmt,
				y_minor_ticks=y_minor_ticks,
				y_minor_ticklabels=False,
				x_minor_ticks=False)
			ax = self.base_plotter.visual_settings.autoformat_grid(
				ax=ax,
				grid_color="gray")
			return ax

		def update_axis_labels(ax, is_points, is_percents, grouped_headers, diffed_headers, frequencies):
			xlabel = "Sources"
			if is_points:
				ylabel = "Points"
			elif is_percents:
				ylabel = "Percents"
			else:
				raise ValueError("invalid combination of is_points={} and is_percents={}".format(is_points, is_percents))
			title, _ = self.base_plotter.get_title(
				grouped_headers=grouped_headers,
				diffed_headers=diffed_headers,
				frequencies=frequencies,
				is_points=is_points,
				is_percents=is_percents,
				is_box_plot=True)
			ax = self.base_plotter.visual_settings.autoformat_axis_labels(
				ax=ax,
				xlabel=xlabel,
				ylabel=ylabel,
				title=title)
			return ax

		def update_axis_limits(ax, is_points, is_percents, values, weights):
			if is_points:
				largest_value = np.nanmax(
					values)
				if isinstance(weights, np.ndarray):
					largest_weight = np.max(
						weights)
				elif isinstance(weights, (int, float)):
					largest_weight = float(
						weights)
				else:
					raise ValueError("invalid type(weights): {}".format(type(weights)))
				largest_y = max([
					largest_value,
					largest_weight])
				y_max = 1.025 * largest_y
				y_min = 0 - (y_max - largest_y)
			elif is_percents:
				y_min = -1
				y_max = 101
			else:
				raise ValueError("invalid combination of is_points={} and is_percents={}".format(is_points, is_percents))
			ylim = (
				y_min,
				y_max)
			ax = self.base_plotter.visual_settings.autoformat_axis_limits(
				ax=ax,
				ylim=ylim)
			return ax

		ax = update_ticks_and_ticklabels(
			ax=ax,
			is_points=is_points,
			is_percents=is_percents)
		ax = update_axis_labels(
			ax=ax,
			is_points=is_points,
			is_percents=is_percents,
			grouped_headers=grouped_headers,
			diffed_headers=diffed_headers,
			frequencies=frequencies)
		ax = update_axis_limits(
			ax=ax,
			is_points=is_points,
			is_percents=is_percents,
			values=values,
			weights=weights)
		return ax

class GradeBookBoxPlotViewerConfiguration(BaseGradeBookBoxPlotViewerConfiguration):

	def __init__(self, base_plotter):
		super().__init__(
			base_plotter=base_plotter)

	def view_box_plot(self, home_work_indices, home_work_headers, exam_indices, exam_headers, extra_credit_indices, extra_credit_headers, curve_headers, is_points, is_percents, is_sub_totals, box_edge_color, box_fill_color, mean_color, median_color, fliers_color, mean_marker, median_linestyle, fliers_marker, fliers_alpha, figsize, is_save):
		if not isinstance(is_sub_totals, bool):
			raise ValueError("invalid type(is_sub_totals): {}".format(type(is_sub_totals)))
		self.base_plotter.verify_value_method(
			is_points=is_points,
			is_percents=is_percents)
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
		if is_only_curve_selected and is_percents:
			raise ValueError("cannot show percents with only curves because curves are not weighted")
		box_scores, box_weights, tmp_statistics = self.get_selected_box_parameters(
			is_points=is_points,
			is_percents=is_percents,
			is_sub_totals=is_sub_totals,
			diffed_weights=diffed_weights,
			total_weight=total_weight,
			diffed_points=diffed_points,
			diffed_percents=diffed_percents,
			sub_total_points=sub_total_points,
			sub_total_percents=sub_total_percents,
			statistics_by_diffed_points=statistics_by_diffed_points,
			statistics_by_diffed_percents=statistics_by_diffed_percents,
			statistics_by_sub_total_points=statistics_by_sub_total_points,
			statistics_by_sub_total_percents=statistics_by_sub_total_percents)
		box_statistics = self.get_box_transformed_statistics(
			is_points=is_points,
			is_percents=is_percents,
			is_sub_totals=is_sub_totals,
			diffed_headers=diffed_headers,
			scores=box_scores,
			weights=box_weights,
			statistics=tmp_statistics)
		fig, ax = plt.subplots(
			figsize=figsize)
		ax = self.plot_box_plot(
			ax=ax,
			box_statistics=box_statistics,
			box_edge_color=box_edge_color,
			box_fill_color=box_fill_color,
			mean_color=mean_color,
			median_color=median_color,
			fliers_color=fliers_color,
			mean_marker=mean_marker,
			median_linestyle=median_linestyle,
			fliers_marker=fliers_marker,
			fliers_alpha=fliers_alpha)
		ax = self.autoformat_plot(
			ax=ax,
			is_points=is_points,
			is_percents=is_percents,
			is_sub_totals=is_sub_totals,
			grouped_headers=grouped_headers,
			diffed_headers=diffed_headers,
			frequencies=frequencies,
			values=box_scores,
			weights=box_weights)
		handles, labels = self.get_side_legend_handles_and_labels(
			box_fill_color=box_fill_color,
			box_edge_color=box_edge_color,
			mean_color=mean_color,
			median_color=median_color,
			fliers_color=fliers_color,
			mean_marker=mean_marker,
			median_linestyle=median_linestyle,
			fliers_marker=fliers_marker,
			fliers_alpha=fliers_alpha)
		ax, side_leg = self.base_plotter.plot_handles_and_labels_in_side_legend(
			ax=ax,
			handles=handles,
			labels=labels,
			ncol=1)
		if is_points:
			leg_statistics = statistics_by_sub_total_points
		elif is_percents:
			leg_statistics = statistics_by_sub_total_percents
		else:
			raise ValueError("invalid combination of is_points={} and is_percents={}".format(is_points, is_percents))
		fig, ax, leg = self.base_plotter.plot_statistics_in_legend(
			fig=fig,
			ax=ax,
			is_points=is_points,
			is_percents=is_percents,
			statistics=leg_statistics,
			leg_title="Statistics")
		save_name, save_name_segments = self.base_plotter.get_save_name(
			grouped_headers=grouped_headers,
			diffed_headers=diffed_headers,
			frequencies=frequencies,
			is_points=is_points,
			is_percents=is_percents,
			is_box_plot=True,
			is_save=is_save)
		if (is_save and is_sub_totals):
			(prefix, base_name, suffix) = save_name_segments
			box_style = "SubTotal"
			modified_prefix = "{}-{}".format(
				prefix,
				box_style)
			save_name = save_name.replace(
				prefix,
				modified_prefix)
		self.base_plotter.visual_settings.display_image(
			fig=fig,
			save_name=save_name,
			space_replacement="_")

##