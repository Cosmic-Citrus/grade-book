import numpy as np
import matplotlib.pyplot as plt
from plotter_base_configuration import BaseGradeBookPlotterConfiguration
from plotter_bar_stack_configuration import GradeBookBarStackViewerConfiguration
from plotter_histogram_configuration import (
	GradeBookPointsHistogramViewerConfiguration,
	GradeBookGradesHistogramViewerConfiguration)
from plotter_polar_chart_configuration import GradeBookPolarChartViewerConfiguration
from plotter_box_plot_configuration import GradeBookBoxPlotViewerConfiguration
from plotter_heat_map_configuration import GradeBookHeatMapViewerConfiguration
from plotter_table_configuration import GradeBookTableViewerConfiguration


class GradeBookPlotterConfiguration(BaseGradeBookPlotterConfiguration):

	def __init__(self):
		super().__init__()

	def view_data_table(self, home_work_indices=None, home_work_headers=None, exam_indices=None, exam_headers=None, extra_credit_indices=None, extra_credit_headers=None, curve_headers=None, is_swap_rows_and_columns=False, first_column_color="gold", second_column_color="orange", first_cell_color="peachpuff", second_cell_color="bisque", first_sub_total_color="lightsteelblue", second_sub_total_color="powderblue", first_grade_color="lavender", second_grade_color="thistle", sub_total_column_color="steelblue", grade_column_color="plum", perfect_row_color="silver", nan_color="black", figsize=None, is_save=False):
		self.verify_visual_settings()
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=home_work_indices,
			home_work_headers=home_work_headers,
			exam_indices=exam_indices,
			exam_headers=exam_headers,
			extra_credit_indices=extra_credit_indices,
			extra_credit_headers=extra_credit_headers,
			curve_headers=curve_headers)
		viewer = GradeBookTableViewerConfiguration(
			base_plotter=self)
		viewer.view_table(
			is_swap_rows_and_columns=is_swap_rows_and_columns,
			first_column_color=first_column_color,
			second_column_color=second_column_color,
			first_cell_color=first_cell_color,
			second_cell_color=second_cell_color,
			first_sub_total_color=first_sub_total_color,
			second_sub_total_color=second_sub_total_color,
			first_grade_color=first_grade_color,
			second_grade_color=second_grade_color,
			sub_total_column_color=sub_total_column_color,
			grade_column_color=grade_column_color,
			perfect_row_color=perfect_row_color,
			nan_color=nan_color,
			figsize=figsize,
			is_save=is_save,
			**indices_and_headers)

	def view_home_work_point_distribution_via_bar_stacks(self, home_work_indices=None, home_work_headers=None, is_differentiate_stacks=True, student_identifier=None, cmap="Greens", edgecolor=None, figsize=None, is_save=False):
		self.verify_visual_settings()
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=home_work_indices,
			home_work_headers=home_work_headers,
			exam_indices=False,
			exam_headers=False,
			extra_credit_indices=False,
			extra_credit_headers=False,
			curve_headers=False)
		viewer = GradeBookBarStackViewerConfiguration(
			base_plotter=self)
		viewer.view_bar_stacks(
			is_differentiate_stacks=is_differentiate_stacks,
			student_identifier=student_identifier,
			cmap=cmap,
			edgecolor=edgecolor,
			figsize=figsize,
			is_save=is_save,
			**indices_and_headers)

	def view_exam_point_distribution_via_bar_stacks(self, exam_indices=None, exam_headers=None, is_differentiate_stacks=True, student_identifier=None, cmap="Reds", edgecolor=None, figsize=None, is_save=False):
		self.verify_visual_settings()
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=False,
			home_work_headers=False,
			exam_indices=exam_indices,
			exam_headers=exam_headers,
			extra_credit_indices=False,
			extra_credit_headers=False,
			curve_headers=False)
		viewer = GradeBookBarStackViewerConfiguration(
			base_plotter=self)
		viewer.view_bar_stacks(
			is_differentiate_stacks=is_differentiate_stacks,
			student_identifier=student_identifier,
			cmap=cmap,
			edgecolor=edgecolor,
			figsize=figsize,
			is_save=is_save,
			**indices_and_headers)

	def view_extra_credit_point_distribution_via_bar_stacks(self, extra_credit_indices=None, extra_credit_headers=None, is_differentiate_stacks=True, student_identifier=None, cmap="Purples", edgecolor=None, figsize=None, is_save=False):
		self.verify_visual_settings()
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=False,
			home_work_headers=False,
			exam_indices=False,
			exam_headers=False,
			extra_credit_indices=extra_credit_indices,
			extra_credit_headers=extra_credit_headers,
			curve_headers=False)
		viewer = GradeBookBarStackViewerConfiguration(
			base_plotter=self)
		viewer.view_bar_stacks(
			is_differentiate_stacks=is_differentiate_stacks,
			student_identifier=student_identifier,
			cmap=cmap,
			edgecolor=edgecolor,
			figsize=figsize,
			is_save=is_save,
			**indices_and_headers)

	def view_curve_point_distribution_via_bar_stacks(self, curve_headers=None, is_differentiate_stacks=True, student_identifier=None, cmap="Blues", edgecolor=None, figsize=None, is_save=False):
		self.verify_visual_settings()
		if not self.is_curved:
			raise ValueError("curve is not applied")
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=False,
			home_work_headers=False,
			exam_indices=False,
			exam_headers=False,
			extra_credit_indices=False,
			extra_credit_headers=False,
			curve_headers=curve_headers)
		viewer = GradeBookBarStackViewerConfiguration(
			base_plotter=self)
		viewer.view_bar_stacks(
			is_differentiate_stacks=is_differentiate_stacks,
			student_identifier=student_identifier,
			cmap=cmap,
			edgecolor=edgecolor,
			figsize=figsize,
			is_save=is_save,
			**indices_and_headers)

	def view_point_distribution_via_bar_stacks(self, home_work_indices=None, home_work_headers=None, exam_indices=None, exam_headers=None, extra_credit_indices=None, extra_credit_headers=None, curve_headers=None, is_differentiate_stacks=True, student_identifier=None, cmap="jet", edgecolor=None, figsize=None, is_save=False):
		self.verify_visual_settings()
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=home_work_indices,
			home_work_headers=home_work_headers,
			exam_indices=exam_indices,
			exam_headers=exam_headers,
			extra_credit_indices=extra_credit_indices,
			extra_credit_headers=extra_credit_headers,
			curve_headers=curve_headers)
		viewer = GradeBookBarStackViewerConfiguration(
			base_plotter=self)
		viewer.view_bar_stacks(
			is_differentiate_stacks=is_differentiate_stacks,
			student_identifier=student_identifier,
			cmap=cmap,
			edgecolor=edgecolor,
			figsize=figsize,
			is_save=is_save,
			**indices_and_headers)

	def view_home_work_point_distribution_via_histogram(self, bin_selection_method, *histogram_args, home_work_indices=None, home_work_headers=None, is_extend_percent_axis=False, is_show_rug=False, is_label_midpoints=False, first_facecolor="limegreen", second_facecolor="forestgreen", rug_facecolor="black", figsize=None, is_save=False, **histogram_kwargs):
		self.verify_visual_settings()
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=home_work_indices,
			home_work_headers=home_work_headers,
			exam_indices=False,
			exam_headers=False,
			extra_credit_indices=False,
			extra_credit_headers=False,
			curve_headers=False)
		viewer = GradeBookPointsHistogramViewerConfiguration(
			base_plotter=self)
		viewer.view_histogram(
			indices_and_headers["home_work_indices"],
			indices_and_headers["home_work_headers"],
			indices_and_headers["exam_indices"],
			indices_and_headers["exam_headers"],
			indices_and_headers["extra_credit_indices"],
			indices_and_headers["extra_credit_headers"],
			indices_and_headers["curve_headers"],
			is_show_rug,
			is_extend_percent_axis,
			is_label_midpoints,
			first_facecolor,
			second_facecolor,
			rug_facecolor,
			figsize,
			is_save,
			bin_selection_method,
			*histogram_args,
			**histogram_kwargs)

	def view_exam_point_distribution_via_histogram(self, bin_selection_method, *histogram_args, exam_indices=None, exam_headers=None, is_show_rug=False, is_extend_percent_axis=False, is_label_midpoints=False, first_facecolor="firebrick", second_facecolor="goldenrod", rug_facecolor="black", figsize=None, is_save=False, **histogram_kwargs):
		self.verify_visual_settings()
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=False,
			home_work_headers=False,
			exam_indices=exam_indices,
			exam_headers=exam_headers,
			extra_credit_indices=False,
			extra_credit_headers=False,
			curve_headers=False)
		viewer = GradeBookPointsHistogramViewerConfiguration(
			base_plotter=self)
		viewer.view_histogram(
			indices_and_headers["home_work_indices"],
			indices_and_headers["home_work_headers"],
			indices_and_headers["exam_indices"],
			indices_and_headers["exam_headers"],
			indices_and_headers["extra_credit_indices"],
			indices_and_headers["extra_credit_headers"],
			indices_and_headers["curve_headers"],
			is_show_rug,
			is_extend_percent_axis,
			is_label_midpoints,
			first_facecolor,
			second_facecolor,
			rug_facecolor,
			figsize,
			is_save,
			bin_selection_method,
			*histogram_args,
			**histogram_kwargs)

	def view_extra_credit_point_distribution_via_histogram(self, bin_selection_method, *histogram_args, extra_credit_indices=None, extra_credit_headers=None, is_show_rug=False, is_extend_percent_axis=False, is_label_midpoints=False, first_facecolor="purple", second_facecolor="thistle", rug_facecolor="black", figsize=None, is_save=False, **histogram_kwargs):
		self.verify_visual_settings()
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=False,
			home_work_headers=False,
			exam_indices=False,
			exam_headers=False,
			extra_credit_indices=extra_credit_indices,
			extra_credit_headers=extra_credit_headers,
			curve_headers=False)
		viewer = GradeBookPointsHistogramViewerConfiguration(
			base_plotter=self)
		viewer.view_histogram(
			indices_and_headers["home_work_indices"],
			indices_and_headers["home_work_headers"],
			indices_and_headers["exam_indices"],
			indices_and_headers["exam_headers"],
			indices_and_headers["extra_credit_indices"],
			indices_and_headers["extra_credit_headers"],
			indices_and_headers["curve_headers"],
			is_show_rug,
			is_extend_percent_axis,
			is_label_midpoints,
			first_facecolor,
			second_facecolor,
			rug_facecolor,
			figsize,
			is_save,
			bin_selection_method,
			*histogram_args,
			**histogram_kwargs)

	def view_curve_point_distribution_via_histogram(self, bin_selection_method, *histogram_args, curve_headers=None, is_show_rug=False, is_extend_percent_axis=False, is_label_midpoints=False, first_facecolor="steelblue", second_facecolor="darkblue", rug_facecolor="black", figsize=None, is_save=False, **histogram_kwargs):
		self.verify_visual_settings()
		if not self.is_curved:
			raise ValueError("curve is not applied")
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=False,
			home_work_headers=False,
			exam_indices=False,
			exam_headers=False,
			extra_credit_indices=False,
			extra_credit_headers=False,
			curve_headers=curve_headers)
		viewer = GradeBookPointsHistogramViewerConfiguration(
			base_plotter=self)
		viewer.view_histogram(
			indices_and_headers["home_work_indices"],
			indices_and_headers["home_work_headers"],
			indices_and_headers["exam_indices"],
			indices_and_headers["exam_headers"],
			indices_and_headers["extra_credit_indices"],
			indices_and_headers["extra_credit_headers"],
			indices_and_headers["curve_headers"],
			is_show_rug,
			is_extend_percent_axis,
			is_label_midpoints,
			first_facecolor,
			second_facecolor,
			rug_facecolor,
			figsize,
			is_save,
			bin_selection_method,
			*histogram_args,
			**histogram_kwargs)

	def view_point_distribution_via_histogram(self, bin_selection_method, *histogram_args, home_work_indices=None, home_work_headers=None, exam_indices=None, exam_headers=None, extra_credit_indices=None, extra_credit_headers=None, curve_headers=None, is_show_rug=False, is_extend_percent_axis=False, is_label_midpoints=False, first_facecolor="darkorange", second_facecolor="gold", rug_facecolor="black", figsize=None, is_save=False, **histogram_kwargs):
		self.verify_visual_settings()
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=home_work_indices,
			home_work_headers=home_work_headers,
			exam_indices=exam_indices,
			exam_headers=exam_headers,
			extra_credit_indices=extra_credit_indices,
			extra_credit_headers=extra_credit_headers,
			curve_headers=curve_headers)
		viewer = GradeBookPointsHistogramViewerConfiguration(
			base_plotter=self)
		viewer.view_histogram(
			indices_and_headers["home_work_indices"],
			indices_and_headers["home_work_headers"],
			indices_and_headers["exam_indices"],
			indices_and_headers["exam_headers"],
			indices_and_headers["extra_credit_indices"],
			indices_and_headers["extra_credit_headers"],
			indices_and_headers["curve_headers"],
			is_show_rug,
			is_extend_percent_axis,
			is_label_midpoints,
			first_facecolor,
			second_facecolor,
			rug_facecolor,
			figsize,
			is_save,
			bin_selection_method,
			*histogram_args,
			**histogram_kwargs)

	def view_grade_distribution_via_histogram(self, is_show_rug=False, first_facecolor="steelblue", second_facecolor="darkorange", rug_facecolor="black", figsize=None, is_save=False):
		viewer = GradeBookGradesHistogramViewerConfiguration(
			base_plotter=self)
		viewer.view_histogram(
			is_show_rug=is_show_rug,
			first_facecolor=first_facecolor,
			second_facecolor=second_facecolor,
			rug_facecolor=rug_facecolor,
			figsize=figsize,
			is_save=is_save)

	def view_grade_distribution_via_polar_pie_chart(self, startangle=90, explode_at_F=None, explode_at_Ds=None, explode_at_Cs=None, explode_at_Bs=None, explode_at_As=None, cmap="Oranges", first_text_color="white", second_text_color="black", figsize=None, is_save=False):
		self.verify_visual_settings()
		viewer = GradeBookPolarChartViewerConfiguration(
			base_plotter=self)
		viewer.view_polar_chart(
			polar_chart_name="pie",
			startangle=startangle,
			explode_at_F=explode_at_F,
			explode_at_Ds=explode_at_Ds,
			explode_at_Cs=explode_at_Cs,
			explode_at_Bs=explode_at_Bs,
			explode_at_As=explode_at_As,
			cmap=cmap,
			first_text_color=first_text_color,
			second_text_color=second_text_color,
			figsize=figsize,
			is_save=is_save)

	def view_grade_distribution_via_polar_donut_chart(self, startangle=90, explode_at_F=None, explode_at_Ds=None, explode_at_Cs=None, explode_at_Bs=None, explode_at_As=None, cmap="Oranges", first_text_color="white", second_text_color="black", figsize=None, is_save=False):
		self.verify_visual_settings()
		viewer = GradeBookPolarChartViewerConfiguration(
			base_plotter=self)
		viewer.view_polar_chart(
			polar_chart_name="donut",
			startangle=startangle,
			explode_at_F=explode_at_F,
			explode_at_Ds=explode_at_Ds,
			explode_at_Cs=explode_at_Cs,
			explode_at_Bs=explode_at_Bs,
			explode_at_As=explode_at_As,
			cmap=cmap,
			first_text_color=first_text_color,
			second_text_color=second_text_color,
			figsize=figsize,
			is_save=is_save)

	def view_grade_distribution_via_polar_annulus_chart(self, startangle=90, explode_at_F=None, explode_at_Ds=None, explode_at_Cs=None, explode_at_Bs=None, explode_at_As=None, cmap="Oranges", first_text_color="white", second_text_color="black", figsize=None, is_save=False):
		self.verify_visual_settings()
		viewer = GradeBookPolarChartViewerConfiguration(
			base_plotter=self)
		viewer.view_polar_chart(
			polar_chart_name="annulus",
			startangle=startangle,
			explode_at_F=explode_at_F,
			explode_at_Ds=explode_at_Ds,
			explode_at_Cs=explode_at_Cs,
			explode_at_Bs=explode_at_Bs,
			explode_at_As=explode_at_As,
			cmap=cmap,
			first_text_color=first_text_color,
			second_text_color=second_text_color,
			figsize=figsize,
			is_save=is_save)
	
	def view_home_work_point_statistics_via_box_plot(self, home_work_indices=None, home_work_headers=None, is_sub_totals=False, box_edge_color="black", box_fill_color="bisque", mean_color="limegreen", median_color="darkorange", fliers_color="purple", whiskers_color="black", q1_color="steelblue", q3_color="firebrick", mean_marker="^", median_linestyle="-", fliers_marker="o", fliers_alpha=0.3, figsize=None, is_save=False):
		self.verify_visual_settings()
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=home_work_indices,
			home_work_headers=home_work_headers,
			exam_indices=False,
			exam_headers=False,
			extra_credit_indices=False,
			extra_credit_headers=False,
			curve_headers=False)
		viewer = GradeBookBoxPlotViewerConfiguration(
			base_plotter=self)
		viewer.view_box_plot(
			is_points=True,
			is_percents=False,
			is_sub_totals=is_sub_totals,
			box_edge_color=box_edge_color,
			box_fill_color=box_fill_color,
			mean_color=mean_color,
			median_color=median_color,
			fliers_color=fliers_color,
			mean_marker=mean_marker,
			median_linestyle=median_linestyle,
			fliers_marker=fliers_marker,
			fliers_alpha=fliers_alpha,
			figsize=figsize,
			is_save=is_save,
			**indices_and_headers)

	def view_home_work_percent_statistics_via_box_plot(self, home_work_indices=None, home_work_headers=None, is_sub_totals=False, box_edge_color="black", box_fill_color="bisque", mean_color="limegreen", median_color="darkorange", fliers_color="purple", whiskers_color="black", q1_color="steelblue", q3_color="firebrick", mean_marker="^", median_linestyle="-", fliers_marker="o", fliers_alpha=0.3, figsize=None, is_save=False):
		self.verify_visual_settings()
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=home_work_indices,
			home_work_headers=home_work_headers,
			exam_indices=False,
			exam_headers=False,
			extra_credit_indices=False,
			extra_credit_headers=False,
			curve_headers=False)
		viewer = GradeBookBoxPlotViewerConfiguration(
			base_plotter=self)
		viewer.view_box_plot(
			is_points=False,
			is_percents=True,
			is_sub_totals=is_sub_totals,
			box_edge_color=box_edge_color,
			box_fill_color=box_fill_color,
			mean_color=mean_color,
			median_color=median_color,
			fliers_color=fliers_color,
			mean_marker=mean_marker,
			median_linestyle=median_linestyle,
			fliers_marker=fliers_marker,
			fliers_alpha=fliers_alpha,
			figsize=figsize,
			is_save=is_save,
			**indices_and_headers)

	def view_exam_point_statistics_via_box_plot(self, exam_indices=None, exam_headers=None, is_sub_totals=False, box_edge_color="black", box_fill_color="bisque", mean_color="limegreen", median_color="darkorange", fliers_color="purple", whiskers_color="black", q1_color="steelblue", q3_color="firebrick", mean_marker="^", median_linestyle="-", fliers_marker="o", fliers_alpha=0.3, figsize=None, is_save=False):
		self.verify_visual_settings()
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=False,
			home_work_headers=False,
			exam_indices=exam_indices,
			exam_headers=exam_headers,
			extra_credit_indices=False,
			extra_credit_headers=False,
			curve_headers=False)
		viewer = GradeBookBoxPlotViewerConfiguration(
			base_plotter=self)
		viewer.view_box_plot(
			is_points=True,
			is_percents=False,
			is_sub_totals=is_sub_totals,
			box_edge_color=box_edge_color,
			box_fill_color=box_fill_color,
			mean_color=mean_color,
			median_color=median_color,
			fliers_color=fliers_color,
			mean_marker=mean_marker,
			median_linestyle=median_linestyle,
			fliers_marker=fliers_marker,
			fliers_alpha=fliers_alpha,
			figsize=figsize,
			is_save=is_save,
			**indices_and_headers)

	def view_exam_percent_statistics_via_box_plot(self, exam_indices=None, exam_headers=None, is_sub_totals=False, box_edge_color="black", box_fill_color="bisque", mean_color="limegreen", median_color="darkorange", fliers_color="purple", whiskers_color="black", q1_color="steelblue", q3_color="firebrick", mean_marker="^", median_linestyle="-", fliers_marker="o", fliers_alpha=0.3, figsize=None, is_save=False):
		self.verify_visual_settings()
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=False,
			home_work_headers=False,
			exam_indices=exam_indices,
			exam_headers=exam_headers,
			extra_credit_indices=False,
			extra_credit_headers=False,
			curve_headers=False)
		viewer = GradeBookBoxPlotViewerConfiguration(
			base_plotter=self)
		viewer.view_box_plot(
			is_points=False,
			is_percents=True,
			is_sub_totals=is_sub_totals,
			box_edge_color=box_edge_color,
			box_fill_color=box_fill_color,
			mean_color=mean_color,
			median_color=median_color,
			fliers_color=fliers_color,
			mean_marker=mean_marker,
			median_linestyle=median_linestyle,
			fliers_marker=fliers_marker,
			fliers_alpha=fliers_alpha,
			figsize=figsize,
			is_save=is_save,
			**indices_and_headers)

	def view_extra_credit_point_statistics_via_box_plot(self, extra_credit_indices=None, extra_credit_headers=None, is_sub_totals=False, box_edge_color="black", box_fill_color="bisque", mean_color="limegreen", median_color="darkorange", fliers_color="purple", whiskers_color="black", q1_color="steelblue", q3_color="firebrick", mean_marker="^", median_linestyle="-", fliers_marker="o", fliers_alpha=0.3, figsize=None, is_save=False):
		self.verify_visual_settings()
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=False,
			home_work_headers=False,
			exam_indices=False,
			exam_headers=False,
			extra_credit_indices=extra_credit_indices,
			extra_credit_headers=extra_credit_headers,
			curve_headers=False)
		viewer = GradeBookBoxPlotViewerConfiguration(
			base_plotter=self)
		viewer.view_box_plot(
			is_points=True,
			is_percents=False,
			is_sub_totals=is_sub_totals,
			box_edge_color=box_edge_color,
			box_fill_color=box_fill_color,
			mean_color=mean_color,
			median_color=median_color,
			fliers_color=fliers_color,
			mean_marker=mean_marker,
			median_linestyle=median_linestyle,
			fliers_marker=fliers_marker,
			fliers_alpha=fliers_alpha,
			figsize=figsize,
			is_save=is_save,
			**indices_and_headers)

	def view_extra_credit_percent_statistics_via_box_plot(self, extra_credit_indices=None, extra_credit_headers=None, is_sub_totals=False, box_edge_color="black", box_fill_color="bisque", mean_color="limegreen", median_color="darkorange", fliers_color="purple", whiskers_color="black", q1_color="steelblue", q3_color="firebrick", mean_marker="^", median_linestyle="-", fliers_marker="o", fliers_alpha=0.3, figsize=None, is_save=False):
		self.verify_visual_settings()
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=False,
			home_work_headers=False,
			exam_indices=False,
			exam_headers=False,
			extra_credit_indices=extra_credit_indices,
			extra_credit_headers=extra_credit_headers,
			curve_headers=False)
		viewer = GradeBookBoxPlotViewerConfiguration(
			base_plotter=self)
		viewer.view_box_plot(
			is_points=False,
			is_percents=True,
			is_sub_totals=is_sub_totals,
			box_edge_color=box_edge_color,
			box_fill_color=box_fill_color,
			mean_color=mean_color,
			median_color=median_color,
			fliers_color=fliers_color,
			mean_marker=mean_marker,
			median_linestyle=median_linestyle,
			fliers_marker=fliers_marker,
			fliers_alpha=fliers_alpha,
			figsize=figsize,
			is_save=is_save,
			**indices_and_headers)

	def view_curve_point_statistics_via_box_plot(self, curve_headers=None, is_sub_totals=False, box_edge_color="black", box_fill_color="bisque", mean_color="limegreen", median_color="darkorange", fliers_color="purple", whiskers_color="black", q1_color="steelblue", q3_color="firebrick", mean_marker="^", median_linestyle="-", fliers_marker="o", fliers_alpha=0.3, figsize=None, is_save=False):
		self.verify_visual_settings()
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=False,
			home_work_headers=False,
			exam_indices=False,
			exam_headers=False,
			extra_credit_indices=False,
			extra_credit_headers=False,
			curve_headers=curve_headers)
		viewer = GradeBookBoxPlotViewerConfiguration(
			base_plotter=self)
		viewer.view_box_plot(
			is_points=True,
			is_percents=False,
			is_sub_totals=is_sub_totals,
			box_edge_color=box_edge_color,
			box_fill_color=box_fill_color,
			mean_color=mean_color,
			median_color=median_color,
			fliers_color=fliers_color,
			mean_marker=mean_marker,
			median_linestyle=median_linestyle,
			fliers_marker=fliers_marker,
			fliers_alpha=fliers_alpha,
			figsize=figsize,
			is_save=is_save,
			**indices_and_headers)

	def view_point_statistics_via_box_plot(self, home_work_indices=None, home_work_headers=None, exam_indices=None, exam_headers=None, extra_credit_indices=None, extra_credit_headers=None, curve_headers=None, is_sub_totals=False, box_edge_color="black", box_fill_color="bisque", mean_color="limegreen", median_color="darkorange", fliers_color="purple", whiskers_color="black", q1_color="steelblue", q3_color="firebrick", mean_marker="^", median_linestyle="-", fliers_marker="o", fliers_alpha=0.3, figsize=None, is_save=False):
		self.verify_visual_settings()
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=home_work_indices,
			home_work_headers=home_work_headers,
			exam_indices=exam_indices,
			exam_headers=exam_headers,
			extra_credit_indices=extra_credit_indices,
			extra_credit_headers=extra_credit_headers,
			curve_headers=curve_headers)
		viewer = GradeBookBoxPlotViewerConfiguration(
			base_plotter=self)
		viewer.view_box_plot(
			is_points=True,
			is_percents=False,
			is_sub_totals=is_sub_totals,
			box_edge_color=box_edge_color,
			box_fill_color=box_fill_color,
			mean_color=mean_color,
			median_color=median_color,
			fliers_color=fliers_color,
			mean_marker=mean_marker,
			median_linestyle=median_linestyle,
			fliers_marker=fliers_marker,
			fliers_alpha=fliers_alpha,
			figsize=figsize,
			is_save=is_save,
			**indices_and_headers)

	def view_percent_statistics_via_box_plot(self, home_work_indices=None, home_work_headers=None, exam_indices=None, exam_headers=None, extra_credit_indices=None, extra_credit_headers=None, curve_headers=None, is_sub_totals=False, box_edge_color="black", box_fill_color="bisque", mean_color="limegreen", median_color="darkorange", fliers_color="purple", whiskers_color="black", q1_color="steelblue", q3_color="firebrick", mean_marker="^", median_linestyle="-", fliers_marker="o", fliers_alpha=0.3, figsize=None, is_save=False):
		self.verify_visual_settings()
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=home_work_indices,
			home_work_headers=home_work_headers,
			exam_indices=exam_indices,
			exam_headers=exam_headers,
			extra_credit_indices=extra_credit_indices,
			extra_credit_headers=extra_credit_headers,
			curve_headers=curve_headers)
		viewer = GradeBookBoxPlotViewerConfiguration(
			base_plotter=self)
		viewer.view_box_plot(
			is_points=False,
			is_percents=True,
			is_sub_totals=is_sub_totals,
			box_edge_color=box_edge_color,
			box_fill_color=box_fill_color,
			mean_color=mean_color,
			median_color=median_color,
			fliers_color=fliers_color,
			mean_marker=mean_marker,
			median_linestyle=median_linestyle,
			fliers_marker=fliers_marker,
			fliers_alpha=fliers_alpha,
			figsize=figsize,
			is_save=is_save,
			**indices_and_headers)

	def view_home_work_point_differences_via_heat_map(self, home_work_indices=None, home_work_headers=None, student_identifier=None, distance_metric="manhattan", is_label_dissimilarity=False, cmap="Greens", first_text_color="white", second_text_color="black", diagonal_color=None, figsize=None, is_save=False):
		self.verify_visual_settings()
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=home_work_indices,
			home_work_headers=home_work_headers,
			exam_indices=False,
			exam_headers=False,
			extra_credit_indices=False,
			extra_credit_headers=False,
			curve_headers=False)
		viewer = GradeBookHeatMapViewerConfiguration(
			base_plotter=self)
		viewer.view_heat_map(
			student_identifier=student_identifier,
			distance_metric=distance_metric,
			is_label_dissimilarity=is_label_dissimilarity,
			cmap=cmap,
			first_text_color=first_text_color,
			second_text_color=second_text_color,
			diagonal_color=diagonal_color,
			figsize=figsize,
			is_save=is_save,
			**indices_and_headers)

	def view_exam_point_differences_via_heat_map(self, exam_indices=None, exam_headers=None, student_identifier=None, distance_metric="manhattan", is_label_dissimilarity=False, cmap="Reds", first_text_color="white", second_text_color="black", diagonal_color=None, figsize=None, is_save=False):
		self.verify_visual_settings()
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=False,
			home_work_headers=False,
			exam_indices=exam_indices,
			exam_headers=exam_headers,
			extra_credit_indices=False,
			extra_credit_headers=False,
			curve_headers=False)
		viewer = GradeBookHeatMapViewerConfiguration(
			base_plotter=self)
		viewer.view_heat_map(
			student_identifier=student_identifier,
			distance_metric=distance_metric,
			is_label_dissimilarity=is_label_dissimilarity,
			cmap=cmap,
			first_text_color=first_text_color,
			second_text_color=second_text_color,
			diagonal_color=diagonal_color,
			figsize=figsize,
			is_save=is_save,
			**indices_and_headers)

	def view_extra_credit_point_differences_via_heat_map(self, extra_credit_indices=None, extra_credit_headers=None, student_identifier=None, distance_metric="manhattan", is_label_dissimilarity=False, cmap="Purples", first_text_color="white", second_text_color="black", diagonal_color=None, figsize=None, is_save=False):
		self.verify_visual_settings()
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=False,
			home_work_headers=False,
			exam_indices=False,
			exam_headers=False,
			extra_credit_indices=extra_credit_indices,
			extra_credit_headers=extra_credit_headers,
			curve_headers=False)
		viewer = GradeBookHeatMapViewerConfiguration(
			base_plotter=self)
		viewer.view_heat_map(
			student_identifier=student_identifier,
			distance_metric=distance_metric,
			is_label_dissimilarity=is_label_dissimilarity,
			cmap=cmap,
			first_text_color=first_text_color,
			second_text_color=second_text_color,
			diagonal_color=diagonal_color,
			figsize=figsize,
			is_save=is_save,
			**indices_and_headers)

	def view_curve_point_differences_via_heat_map(self, curve_headers=None, student_identifier=None, distance_metric="manhattan", is_label_dissimilarity=False, cmap="Blues", first_text_color="white", second_text_color="black", diagonal_color=None, figsize=None, is_save=False):
		self.verify_visual_settings()
		if not self.is_curved:
			raise ValueError("curve is not applied")
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=False,
			home_work_headers=False,
			exam_indices=False,
			exam_headers=False,
			extra_credit_indices=False,
			extra_credit_headers=False,
			curve_headers=curve_headers)
		viewer = GradeBookHeatMapViewerConfiguration(
			base_plotter=self)
		viewer.view_heat_map(
			student_identifier=student_identifier,
			distance_metric=distance_metric,
			is_label_dissimilarity=is_label_dissimilarity,
			cmap=cmap,
			first_text_color=first_text_color,
			second_text_color=second_text_color,
			diagonal_color=diagonal_color,
			figsize=figsize,
			is_save=is_save,
			**indices_and_headers)

	def view_point_differences_via_heat_map(self, home_work_indices=None, home_work_headers=None, exam_indices=None, exam_headers=None, extra_credit_indices=None, extra_credit_headers=None, curve_headers=None, student_identifier=None, distance_metric="manhattan", is_label_dissimilarity=False, cmap="jet", first_text_color="white", second_text_color="black", diagonal_color=None, figsize=None, is_save=False):
		self.verify_visual_settings()
		indices_and_headers = self.get_default_indices_and_headers(
			home_work_indices=home_work_indices,
			home_work_headers=home_work_headers,
			exam_indices=exam_indices,
			exam_headers=exam_headers,
			extra_credit_indices=extra_credit_indices,
			extra_credit_headers=extra_credit_headers,
			curve_headers=curve_headers)
		viewer = GradeBookHeatMapViewerConfiguration(
			base_plotter=self)
		viewer.view_heat_map(
			student_identifier=student_identifier,
			distance_metric=distance_metric,
			is_label_dissimilarity=is_label_dissimilarity,
			cmap=cmap,
			first_text_color=first_text_color,
			second_text_color=second_text_color,
			diagonal_color=diagonal_color,
			figsize=figsize,
			is_save=is_save,
			**indices_and_headers)

##