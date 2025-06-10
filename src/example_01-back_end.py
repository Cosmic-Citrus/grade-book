import numpy as np
from back_end_configuration import GradeBookBackEndConfiguration


## specify paths
path_to_data = "/Users/owner/Desktop/programming/grade_book/data/data.csv"
# is_save, path_to_save_directory = False, None
is_save, path_to_save_directory = True, "/Users/owner/Desktop/programming/grade_book/output/"

## specify indices by row/column
index_at_weighted_row = 0
index_at_names_column = 0
index_at_id_column = 1
index_at_email_column = None # 2
indices_at_home_work_columns = np.arange(
	3,
	13,
	dtype=int)
indices_at_exam_columns = np.array([
	13,
	14])
indices_at_extra_credit_columns = None

## specify curves
flat_curve = 5 # None
is_home_work_improvement_curve = True # False
is_exam_improvement_curve = True # False
is_extra_credit_improvement_curve = False # True

## specify grading criteria
points_at_fail = 80 ## 0 < x < 80 ==> F
points_at_ace = 150 ## x > 150 ==> A+
in_between_edges = None # (score_at_D_minus, ..., score_at_A)
side_bias = "left" # "right"


if __name__ == "__main__":

	## initialize grade-book
	grade_book = GradeBookBackEndConfiguration()
	grade_book.initialize_back_end(
		path_to_data=path_to_data,
		path_to_save_directory=path_to_save_directory,
		index_at_weighted_row=index_at_weighted_row,
		index_at_names_column=index_at_names_column,
		index_at_email_column=index_at_email_column,
		index_at_id_column=index_at_id_column,
		indices_at_home_work_columns=indices_at_home_work_columns,
		indices_at_exam_columns=indices_at_exam_columns,
		indices_at_extra_credit_columns=indices_at_extra_credit_columns,
		flat_curve=flat_curve,
		is_home_work_improvement_curve=is_home_work_improvement_curve,
		is_exam_improvement_curve=is_exam_improvement_curve,
		is_extra_credit_improvement_curve=is_extra_credit_improvement_curve,
		points_at_fail=points_at_fail,
		points_at_ace=points_at_ace,
		in_between_edges=in_between_edges,
		side_bias=side_bias)
	# grade_book.remove_curves(
	# 	is_flat_curve=True,
	# 	is_home_work_improvement_curve=True,
	# 	is_exam_improvement_curve=True,
	# 	is_extra_credit_improvement_curve=True)
	# grade_book.add_curves(
	# 	flat_curve=flat_curve,
	# 	is_home_work_improvement_curve=is_home_work_improvement_curve,
	# 	is_exam_improvement_curve=is_exam_improvement_curve)

	## write data to file
	grade_book.write_data_frame_to_file(
		extension=".csv")
	grade_book.write_data_frame_to_file(
		extension=".xlsx")
	grade_book.write_student_data_to_file(
		extension=".txt")

	## view data-table
	grade_book.view_data_table(
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_data_table(
		is_swap_rows_and_columns=True,
		figsize=(12, 7),
		is_save=is_save)

	## view bar-stacks of points
	grade_book.view_home_work_point_distribution_via_bar_stacks(
		student_identifier="ID number",
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_home_work_point_distribution_via_bar_stacks(
		student_identifier="ID number",
		home_work_indices=(0, 1),
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_home_work_point_distribution_via_bar_stacks(
		student_identifier="ID number",
		home_work_headers=("HW 1", "HW 2", "HW 3", "HW 4"),
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_home_work_point_distribution_via_bar_stacks(
		student_identifier="ID number",
		home_work_indices=7,
		home_work_headers=("HW 1", "HW 2", "HW 3", "HW 4"),
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_exam_point_distribution_via_bar_stacks(
		student_identifier="name",
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_curve_point_distribution_via_bar_stacks(
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_point_distribution_via_bar_stacks(
		cmap="hot",
		edgecolor="black",
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_point_distribution_via_bar_stacks(
		is_differentiate_stacks=False,
		cmap="viridis",
		figsize=(12, 7),
		is_save=is_save)

	## view histogram of points
	grade_book.view_home_work_point_distribution_via_histogram(
		bin_selection_method="equivalent bin widths",
		bin_widths=2,
		round_to_base=10,
		is_label_midpoints=True,
		home_work_indices=0,
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_home_work_point_distribution_via_histogram(
		bin_selection_method="equivalent bin widths",
		bin_widths=2,
		round_to_base=10,
		is_show_rug=True,
		is_label_midpoints=True,
		home_work_indices=0,
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_home_work_point_distribution_via_histogram(
		bin_selection_method="equivalent bin widths",
		bin_widths=2,
		round_to_base=10,
		home_work_headers=("HW 1", "HW 2"),
		is_extend_percent_axis=True,
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_home_work_point_distribution_via_histogram(
		bin_selection_method="equivalent bin widths",
		bin_widths=2,
		round_to_base=10,
		home_work_headers=("HW 1", "HW 2"),
		is_show_rug=True,
		is_extend_percent_axis=True,
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_home_work_point_distribution_via_histogram(
		bin_selection_method="equivalent bin widths",
		bin_widths=5,
		round_to_base=10,
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_exam_point_distribution_via_histogram(
		bin_selection_method="equivalent bin widths",
		bin_widths=5,
		round_to_base=10,
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_curve_point_distribution_via_histogram(
		bin_selection_method="equivalent bin widths",
		bin_widths=2,
		round_to_base=10,
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_point_distribution_via_histogram(
		bin_selection_method="equivalent bin widths",
		bin_widths=5,
		round_to_base=10,
		home_work_headers=("HW 1", "HW 2"),
		exam_indices=0,
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_point_distribution_via_histogram(
		bin_selection_method="number bins",
		number_bins=10,
		round_to_base=10,
		is_extend_percent_axis=True,
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_point_distribution_via_histogram(
		bin_selection_method="number bins",
		number_bins=10,
		round_to_base=10,
		is_show_rug=True,
		is_extend_percent_axis=True,
		figsize=(12, 7),
		is_save=is_save)
	
	## view distribution of grades
	grade_book.view_grade_distribution_via_histogram(
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_grade_distribution_via_histogram(
		is_show_rug=True,
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_grade_distribution_via_polar_pie_chart(
		explode_at_As=0.05,
		explode_at_Bs=0.025,
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_grade_distribution_via_polar_donut_chart(
		explode_at_As=0.05,
		explode_at_Bs=0.025,
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_grade_distribution_via_polar_annulus_chart(
		startangle=77,
		figsize=(12, 7),
		is_save=is_save)

	## view box-plot of statistics
	grade_book.view_home_work_point_statistics_via_box_plot(
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_home_work_percent_statistics_via_box_plot(
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_home_work_point_statistics_via_box_plot(
		is_sub_totals=True,
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_home_work_percent_statistics_via_box_plot(
		is_sub_totals=True,
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_exam_point_statistics_via_box_plot(
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_exam_percent_statistics_via_box_plot(
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_curve_point_statistics_via_box_plot(
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_point_statistics_via_box_plot(
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_percent_statistics_via_box_plot(
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_point_statistics_via_box_plot(
		is_sub_totals=True,
		figsize=(12, 7),
		is_save=is_save)
	grade_book.view_percent_statistics_via_box_plot(
		is_sub_totals=True,
		figsize=(12, 7),
		is_save=is_save)

	## view heat-map of point-differences
	grade_book.view_home_work_point_differences_via_heat_map(
		figsize=(12, 9),
		is_save=is_save)
	grade_book.view_home_work_point_differences_via_heat_map(
		home_work_indices=0,
		is_label_dissimilarity=True,
		figsize=(12, 9),
		is_save=is_save)
	grade_book.view_home_work_point_differences_via_heat_map(
		home_work_indices=(0, 1),
		figsize=(12, 9),
		is_save=is_save)
	grade_book.view_home_work_point_differences_via_heat_map(
		home_work_headers=("HW 1", "HW 2", "HW 3", "HW 4"),
		diagonal_color="silver",
		figsize=(12, 9),
		is_save=is_save)
	grade_book.view_exam_point_differences_via_heat_map(
		student_identifier="ID number",
		figsize=(12, 9),
		is_save=is_save)
	grade_book.view_curve_point_differences_via_heat_map(
		student_identifier="name",
		diagonal_color="silver",
		figsize=(12, 9),
		is_save=is_save)
	grade_book.view_point_differences_via_heat_map(
		student_identifier="ID number",
		is_label_dissimilarity=True,
		cmap="hot",
		first_text_color="black",
		second_text_color="white",
		diagonal_color="silver",
		figsize=(12, 9),
		is_save=is_save)

##