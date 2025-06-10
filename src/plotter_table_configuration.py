import numpy as np
import matplotlib.pyplot as plt
from plotter_base_configuration import BaseGradeBookPlotterConfiguration


class BaseGradeBookTableViewerConfiguration():

	def __init__(self, base_plotter):
		super().__init__()
		self.base_plotter = base_plotter

	@staticmethod
	def plot_table(ax, row_labels, column_labels, cell_text, row_colors, column_colors, cell_colors):
		table = ax.table(
			rowLabels=row_labels,
			colLabels=column_labels,
			cellText=cell_text,
			colColours=column_colors,
			rowColours=row_colors,
			cellColours=cell_colors,
			loc="center",
			colLoc="center",
			rowLoc="center",
			cellLoc="center")
		return ax, table

	def get_table_parameters(self, diffed_headers, diffed_scores, diffed_weights, sub_total_scores):

		def get_row_parameters():
			row_labels = None
			number_header_rows = 0
			if self.base_plotter.index_at_weighted_row is not None:
				number_header_rows += 1
			number_rows = self.base_plotter.number_students + number_header_rows
			row_parameters = (
				number_rows,
				row_labels)
			return row_parameters

		def get_column_parameters(diffed_headers):
			column_labels = list()
			for identifier in self.base_plotter.student_identifiers:
				column_label = identifier[:]
				column_labels.append(
					column_label)
			column_labels.extend(
				list(
					diffed_headers))
			column_labels.extend([
				"sub-total",
				"grade"])
			number_columns = len(
				column_labels)
			column_parameters = (
				number_columns,
				column_labels)
			return column_parameters

		def get_cell_text_by_identifiers():
			is_perfect_score_identifier_used = False
			cell_text = list()
			for identifier in self.base_plotter.student_identifiers:
				attribute = identifier.lower()
				attribute = attribute.replace(
					" ",
					"_")
				attribute = attribute.replace(
					"-",
					"_")
				column = list()
				for index_at_row, student in enumerate(self.base_plotter.students):
					value = getattr(
						student,
						attribute)
					column.append(
						value)
				if self.base_plotter.index_at_weighted_row is not None:
					if is_perfect_score_identifier_used:
						last_value = ""
					else:
						last_value = "Perfect Score"
						is_perfect_score_identifier_used = True
					column.insert(
						0,
						last_value)
				cell_text.append(
					column)
			return cell_text

		def get_cell_text_by_scores(diffed_scores, diffed_weights):
			cell_text = list()
			for sub_scores, weight in zip(diffed_scores.T, diffed_weights):
				column = sub_scores.tolist()
				if self.base_plotter.index_at_weighted_row is not None:
					column.insert(
						0,
						weight)
				modified_column = [
					r"${:,.2f}$".format(value)
						for value in column]
				cell_text.append(
					modified_column)
			return cell_text

		def get_cell_text_by_sub_total_and_grades(sub_total_scores, diffed_weights):
			cell_text = list()
			left_column = sub_total_scores.tolist()
			grades = self.base_plotter.get_grades(
				sub_totals=sub_total_scores)
			if self.base_plotter.index_at_weighted_row is not None:
				perfect_score = np.sum(
					diffed_weights)
				grade_at_perfect_score = self.base_plotter.get_grades(
					sub_totals=perfect_score)
				left_column.insert(
					0,
					perfect_score)
				grades.insert(
					0,
					grade_at_perfect_score)
			modified_left_column = [
				r"${:,.2f}$".format(value)
					for value in left_column]
			cell_text.append(
				modified_left_column)
			cell_text.append(
				grades)
			return cell_text

		row_parameters = get_row_parameters()
		(number_rows, row_labels) = row_parameters
		column_parameters = get_column_parameters(
			diffed_headers=diffed_headers)
		(number_columns, column_labels) = column_parameters
		cell_text_by_identifiers = get_cell_text_by_identifiers()
		cell_text_by_scores = get_cell_text_by_scores(
			diffed_scores=diffed_scores,
			diffed_weights=diffed_weights)
		cell_text_by_grades = get_cell_text_by_sub_total_and_grades(
			sub_total_scores=sub_total_scores,
			diffed_weights=diffed_weights)
		cell_text = [
			*cell_text_by_identifiers,
			*cell_text_by_scores,
			*cell_text_by_grades]
		cell_text = list(
			zip(
				*cell_text))
		table_parameters = (
			(number_rows, number_columns),
			(row_labels, column_labels, cell_text))
		return table_parameters

	def get_color_parameters(self, number_rows, number_columns, cell_text, first_column_color, second_column_color, first_cell_color, second_cell_color, first_sub_total_color, second_sub_total_color, first_grade_color, second_grade_color, sub_total_column_color, grade_column_color, perfect_row_color, nan_color):

		def get_column_colors(number_columns, first_column_color, second_column_color, sub_total_column_color, grade_column_color):
			column_colors = list()
			for index_at_column in range(number_columns):
				if index_at_column == number_columns - 1:
					color_at_column = grade_column_color[:]
				elif index_at_column == number_columns - 2:
					color_at_column = sub_total_column_color[:]
				else:
					if index_at_column % 2 == 0:
						color_at_column = first_column_color[:]
					else:
						color_at_column = second_column_color[:]
				column_colors.append(
					color_at_column)
			return column_colors

		def get_cell_colors(number_rows, number_columns, cell_text, first_cell_color, second_cell_color, first_sub_total_color, second_sub_total_color, first_grade_color, second_grade_color, perfect_row_color):
			cell_colors = self.base_plotter.visual_settings.get_diagonal_table_colors(
				even_color=first_cell_color,
				odd_color=second_cell_color,
				number_rows=number_rows,
				number_columns=number_columns)
			for index_at_row in range(number_rows):
				if index_at_row % 2 == 0:
					color_at_left_last_column = first_sub_total_color
					color_at_last_column = first_grade_color
				else:
					color_at_left_last_column = second_sub_total_color
					color_at_last_column = second_grade_color
				cell_colors[index_at_row][-2] = color_at_left_last_column
				cell_colors[index_at_row][-1] = color_at_last_column
			index_at_first_nan_able_column = len(
				self.base_plotter.student_identifiers)
			for index_at_row in range(number_rows):
				for index_at_column in range(index_at_first_nan_able_column, number_columns - 1):
					value = cell_text[index_at_row][index_at_column]
					modified_value = float(
						value.replace(
							"$",
							""))
					if np.isnan(modified_value):
						cell_colors[index_at_row][index_at_column] = nan_color
			if self.base_plotter.index_at_weighted_row is not None:
				for index_at_column in range(number_columns):
					cell_colors[self.base_plotter.index_at_weighted_row][index_at_column] = perfect_row_color
			return cell_colors

		row_colors = None
		column_colors = get_column_colors(
			number_columns=number_columns,
			first_column_color=first_column_color,
			second_column_color=second_column_color,
			sub_total_column_color=sub_total_column_color,
			grade_column_color=grade_column_color)
		cell_colors = get_cell_colors(
			number_rows=number_rows,
			number_columns=number_columns,
			cell_text=cell_text,
			first_cell_color=first_cell_color,
			second_cell_color=second_cell_color,
			first_sub_total_color=first_sub_total_color,
			second_sub_total_color=second_sub_total_color,
			first_grade_color=first_grade_color,
			second_grade_color=second_grade_color,
			perfect_row_color=perfect_row_color)
		color_parameters = (
			row_colors,
			column_colors,
			cell_colors)
		return color_parameters

class GradeBookTableViewerConfiguration(BaseGradeBookTableViewerConfiguration):

	def __init__(self, base_plotter):
		super().__init__(
			base_plotter=base_plotter)

	def view_table(self, home_work_indices, home_work_headers, exam_indices, exam_headers, extra_credit_indices, extra_credit_headers, curve_headers, is_swap_rows_and_columns, first_column_color, second_column_color, first_cell_color, second_cell_color, first_sub_total_color, second_sub_total_color, first_grade_color, second_grade_color, sub_total_column_color, grade_column_color, perfect_row_color, nan_color, figsize, is_save):
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
		table_parameters = self.get_table_parameters(
			diffed_headers=diffed_headers,
			diffed_scores=diffed_points,
			diffed_weights=diffed_weights,
			sub_total_scores=sub_total_points)
		(args_by_indexable_number, args_by_label) = table_parameters
		(number_rows, number_columns) = args_by_indexable_number
		(row_labels, column_labels, cell_text) = args_by_label
		color_parameters = self.get_color_parameters(
			number_rows=number_rows,
			number_columns=number_columns,
			cell_text=cell_text,
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
			nan_color=nan_color)
		(row_colors, column_colors, cell_colors) = color_parameters
		if not isinstance(is_swap_rows_and_columns, bool):
			raise ValueError("invalid type(is_swap_rows_and_columns): {}".format(type(is_swap_rows_and_columns)))
		if is_swap_rows_and_columns:
			swapped_parameters = self.base_plotter.visual_settings.get_swapped_row_and_column_parameters(
				number_rows=number_rows,
				number_columns=number_columns,
				row_labels=row_labels,
				column_labels=column_labels,
				cell_text=cell_text,
				row_colors=row_colors,
				column_colors=column_colors,
				cell_colors=cell_colors)
			(number_rows, number_columns, row_labels, column_labels, cell_text, row_colors, column_colors, cell_colors) = swapped_parameters
		fig, ax = plt.subplots(
			figsize=figsize)
		# fig.patch.set_visible(
		# 	False)
		# ax.axis(
		# 	"off")
		# ax.axis(
		# 	"tight")
		ax, table = self.plot_table(
			ax=ax,
			row_labels=row_labels,
			column_labels=column_labels,
			cell_text=cell_text,
			row_colors=row_colors,
			column_colors=column_colors,
			cell_colors=cell_colors)
		table = self.base_plotter.visual_settings.autoformat_table(
			ax=ax,
			table=table,
			size=self.base_plotter.visual_settings.label_size)
		table.auto_set_column_width(
			col=list(
				range(
					number_columns)))
		fig, ax, leg = self.base_plotter.plot_statistics_in_legend(
			fig=fig,
			ax=ax,
			is_grades=True,
			statistics=self.base_plotter.statistics["points"]["total"],
			leg_title="Statistics")
		save_name, save_name_segments = self.base_plotter.get_save_name(
			is_grades=True,
			is_table=True,
			is_save=is_save)
		if is_save:
			(prefix, base_name, suffix) = save_name_segments
			table_style = "wSWAP" if is_swap_rows_and_columns else "woSWAP"
			modified_prefix = "{}-{}".format(
				prefix,
				table_style)
			save_name = save_name.replace(
				prefix,
				modified_prefix)			
		self.base_plotter.visual_settings.display_image(
			fig=fig,
			save_name=save_name,
			space_replacement="_")

##