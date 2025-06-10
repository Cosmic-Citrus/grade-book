import numpy as np
import matplotlib.pyplot as plt


class BaseGradeBookPolarChartViewerConfiguration():

	def __init__(self, base_plotter):
		super().__init__()
		self.base_plotter = base_plotter
	
	def get_sector_parameters(self):
		full_grade_labels = list(
			self.base_plotter.grading_criteria["possible grades"])
		full_grade_counts = np.array([
			self.base_plotter.grades_counter[grade_label]
				for grade_label in full_grade_labels])
		is_zero_counts = (full_grade_counts == 0)
		selected_grade_labels, selected_grade_counts = list(), list()
		for is_zero_count, grade_label, grade_count in zip(is_zero_counts, full_grade_labels, full_grade_counts):
			if not is_zero_count:
				selected_grade_labels.append(
					grade_label)
				selected_grade_counts.append(
					grade_count)
		number_full_sectors = int(
			is_zero_counts.size)
		number_selected_sectors = int(
			np.sum(
				np.invert(
					is_zero_counts)))
		sector_parameters = (
			number_full_sectors,
			full_grade_labels,
			full_grade_counts,
			is_zero_counts,
			number_selected_sectors,
			selected_grade_labels,
			selected_grade_counts)
		return sector_parameters

	def get_color_parameters(self, cmap, first_text_color, second_text_color, number_full_sectors, is_zero_counts):
		full_rgb_colors, norm = self.base_plotter.visual_settings.get_rgb_facecolors(
			cmap=cmap,
			number_colors=number_full_sectors)
		selected_rgb_colors = list()
		full_text_colors = list()
		selected_text_colors = list()
		for index_at_color, (rgb_color, is_zero_count) in enumerate(zip(full_rgb_colors, is_zero_counts)):
			color_value = norm(
				index_at_color)
			is_above_color_threshold = color_value > 0.5
			text_color = first_text_color if is_above_color_threshold else second_text_color
			full_text_colors.append(
				text_color)
			if not is_zero_count:
				selected_rgb_colors.append(
					rgb_color)
				selected_text_colors.append(
					text_color)
		color_parameters = (
			(full_rgb_colors, selected_rgb_colors),
			(full_text_colors, selected_text_colors),
			norm)
		return color_parameters

	def get_explode(self, explode_at_F, explode_at_Ds, explode_at_Cs, explode_at_Bs, explode_at_As, number_selected_sectors):
		number_As = int(
			sum([
				self.base_plotter.grades_counter["A+"],
				self.base_plotter.grades_counter["A"],
				self.base_plotter.grades_counter["A-"]]))
		number_Bs = int(
			sum([
				self.base_plotter.grades_counter["B+"],
				self.base_plotter.grades_counter["B"],
				self.base_plotter.grades_counter["B-"]]))
		number_Cs = int(
			sum([
				self.base_plotter.grades_counter["C+"],
				self.base_plotter.grades_counter["C"],
				self.base_plotter.grades_counter["C-"]]))
		number_Ds = int(
			sum([
				self.base_plotter.grades_counter["D+"],
				self.base_plotter.grades_counter["D"],
				self.base_plotter.grades_counter["D-"]]))
		number_F = int(
			self.base_plotter.grades_counter["F"])
		explode = np.full(
			fill_value=0,
			shape=number_selected_sectors,
			dtype=float)
		explosion_groups = (
			(number_As, explode_at_As),
			(number_Bs, explode_at_Bs),
			(number_Cs, explode_at_Cs),
			(number_Ds, explode_at_Ds),
			(number_F, explode_at_F))
		index_at_previous_first_grade = None
		cumulative_frequency = 0
		for group in explosion_groups:
			(frequency, explode_value) = group
			if frequency > 0:
				if explode_value is None:
					modified_explode_value = 0
				else:
					modified_explode_value = float(
						explode_value)
				cumulative_frequency += int(
					frequency)
				if index_at_previous_first_grade is None:
					index_at_previous_first_grade = 0
					index_at_first_grade = int(
						-1 * frequency)
					explode[index_at_first_grade:] = modified_explode_value
				else:
					index_at_first_grade = int(
						-1 * cumulative_frequency)
					explode[index_at_first_grade : index_at_previous_first_grade] = explode_value
			else:
				if index_at_first_grade is not None:
					index_at_first_grade = int(
						index_at_previous_first_grade)
						# cumulative_frequency)
		return explode

	def plot_chart(self, ax, polar_chart_name, selected_grade_counts, selected_grade_labels, selected_rgb_colors, radius, center, startangle, explode):
		wedgeprops = {
			# "edgecolor" : "black",
			# "edgecolor" : ax.get_facecolor(),
			"edgecolor" : "white",
			# "linewidth" : 1,
			"linewidth" : 0,
			"linestyle" : "solid",
			"antialiased" : True}
		kwargs = {
			"radius" : radius,
			"center" : center,
			"startangle" : startangle,
			"explode" : explode}
		if polar_chart_name == "pie":
			kwargs["pctdistance"] = 1.125 ## outside circle (distance > 1)
			kwargs["labeldistance"] = 0.55 ## inside circle (distance < 1)
		elif polar_chart_name == "donut":
			wedgeprops["width"] = 0.5 ## half-radius
			kwargs["pctdistance"] = 1.2 ## outside circle (distance > 1)
			kwargs["labeldistance"] = 0.75 ## inside circle (distance < 1)
		elif polar_chart_name == "annulus":
			wedgeprops["width"] = 0.5 ## half-radius
			kwargs["labeldistance"] = 0.75 ## inside circle (distance < 1)
		else:
			raise ValueError("invalid polar_chart_name: {}".format(polar_chart_name))
		if polar_chart_name == "annulus":
			patches, texts = ax.pie(
				selected_grade_counts,
				labels=selected_grade_labels,
				colors=selected_rgb_colors,
				wedgeprops=wedgeprops,
				**kwargs)
			autotexts = None
		else:
			patches, texts, autotexts = ax.pie(
				selected_grade_counts,
				labels=selected_grade_labels,
				colors=selected_rgb_colors,
				wedgeprops=wedgeprops,
				autopct="%0.2f%%",
				**kwargs)
		return ax, patches, texts, autotexts

	def autoformat_plot(self, fig, ax, polar_chart_name, patches, texts, autotexts, selected_grade_counts, selected_grade_labels, selected_text_colors):
		ax.axis(
			"equal")
		if polar_chart_name == "annulus":
			if autotexts is not None:
				raise ValueError("autotexts should be None for this method")
			for text, text_color in zip(texts, selected_text_colors):
				text.set_color(
					text_color)
				text.set_horizontalalignment(
					"center")
				text.set_verticalalignment(
					"center")
			ax = self.plot_annulus_text_blocks_with_connections_at_sector_angles(
				ax=ax,
				patches=patches,
				selected_grade_counts=selected_grade_counts,
				selected_grade_labels=selected_grade_labels)
		else:
			for text, autotext, text_color in zip(texts, autotexts, selected_text_colors):
				text.set_color(
					text_color)
				text.set_horizontalalignment(
					"center")
				text.set_verticalalignment(
					"center")
				autotext.set_color(
					"black")
				autotext.set_horizontalalignment(
					"center")
				autotext.set_verticalalignment(
					"center")
		# fig.subplots_adjust(
		# 	top=1.2)
		title, _ = self.base_plotter.get_title(
			is_grades=True,
			is_polar_chart=True)
		fig.suptitle(
			title,
			fontsize=self.base_plotter.visual_settings.title_size,
			y=1.005)
		return fig, ax

	def plot_annulus_text_blocks_with_connections_at_sector_angles(self, ax, patches, selected_grade_counts, selected_grade_labels):
		bbox = {
			"boxstyle" : "round,pad=0.3",
			"linewidth" : 0, # 0.75,
			"alpha" : 0,
			"facecolor" : "white",
			"edgecolor" : "black"}
		arrowprops = {
			"arrowstyle" : "-"}
		kwargs = {
			"zorder" : 0,
			"verticalalignment" : "center",
			"bbox" : bbox,
			"arrowprops" : arrowprops}
		for index_at_patch, (patch, grade_count, grade_label) in enumerate(zip(patches, selected_grade_counts, selected_grade_labels)):
			angle_in_degrees = (patch.theta2 - patch.theta1) / float(2) + patch.theta1
			angle_in_radians = np.deg2rad(
				angle_in_degrees)
			x = np.cos(
				angle_in_radians)
			y = np.sin(
				angle_in_radians)
			sign_of_x = np.sign(
				x)
			xt = 1.25 * sign_of_x
			yt = 1.25 * y
			if sign_of_x > 0:
				horizontalalignment = "left"
			elif sign_of_x < 0:
				horizontalalignment = "right"
			else: # sign_of_x == 0:
				horizontalalignment = "center"
			connectionstyle = "angle,angleA=0,angleB={}".format(
				angle_in_degrees)
			kwargs["arrowprops"]["connectionstyle"] = connectionstyle
			annotation_label = self.base_plotter.get_grade_label_with_student_fraction_and_percentage(
				grade_label=grade_label)
			ax.annotate(
				annotation_label,
				xy=(x, y),
				xytext=(xt, yt),
				horizontalalignment=horizontalalignment,
				**kwargs)
		return ax

class GradeBookPolarChartViewerConfiguration(BaseGradeBookPolarChartViewerConfiguration):

	def __init__(self, base_plotter):
		super().__init__(
			base_plotter=base_plotter)

	def view_polar_chart(self, polar_chart_name, startangle, explode_at_F, explode_at_Ds, explode_at_Cs, explode_at_Bs, explode_at_As, cmap, first_text_color, second_text_color, figsize, is_save):
		sector_parameters = self.get_sector_parameters()
		(number_full_sectors, full_grade_labels, full_grade_counts, is_zero_counts, number_selected_sectors, selected_grade_labels, selected_grade_counts) = sector_parameters
		color_parameters = self.get_color_parameters(
			cmap=cmap,
			first_text_color=first_text_color,
			second_text_color=second_text_color,
			number_full_sectors=number_full_sectors,
			is_zero_counts=is_zero_counts)
		(rgb_colors, text_colors, norm) = color_parameters
		(full_rgb_colors, selected_rgb_colors) = rgb_colors
		(full_text_colors, selected_text_colors) = text_colors
		explode = self.get_explode(
			explode_at_F=explode_at_F,
			explode_at_Ds=explode_at_Ds,
			explode_at_Cs=explode_at_Cs,
			explode_at_Bs=explode_at_Bs,
			explode_at_As=explode_at_As,
			number_selected_sectors=number_selected_sectors)
		radius, center = 1, (0, 0)
		fig, ax = plt.subplots(
			figsize=figsize)
		ax, patches, texts, autotexts = self.plot_chart(
			ax=ax,
			polar_chart_name=polar_chart_name,
			selected_grade_counts=selected_grade_counts,
			selected_grade_labels=selected_grade_labels,
			selected_rgb_colors=selected_rgb_colors,
			radius=radius,
			center=center,
			startangle=startangle,
			explode=explode)
		fig, ax = self.autoformat_plot(
			fig=fig,
			ax=ax,
			polar_chart_name=polar_chart_name,
			patches=patches,
			texts=texts,
			autotexts=autotexts,
			selected_grade_counts=selected_grade_counts,
			selected_grade_labels=selected_grade_labels,
			selected_text_colors=selected_text_colors)
		grade_handles, grade_labels = self.base_plotter.get_grade_handles_and_labels(
			ax=ax)
		ax, side_leg = self.base_plotter.plot_handles_and_labels_in_side_legend(
			ax=ax,
			handles=grade_handles,
			labels=grade_labels,
			ncol=2)		
		fig, ax, leg = self.base_plotter.plot_statistics_in_legend(
			fig=fig,
			ax=ax,
			is_grades=True,
			statistics=self.base_plotter.statistics["points"]["total"],
			leg_title="Statistics")
		save_name, save_name_segments = self.base_plotter.get_save_name(
			is_grades=True,
			is_polar_chart=True,
			is_save=is_save)
		if is_save:
			(prefix, base_name, suffix) = save_name_segments
			modified_prefix = "{}-{}".format(
				prefix,
				polar_chart_name.title())
			save_name = save_name.replace(
				prefix,
				modified_prefix)
		self.base_plotter.visual_settings.display_image(
			fig=fig,
			save_name=save_name,
			space_replacement="_")

##