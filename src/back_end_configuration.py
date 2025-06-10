import numpy as np
from email_configuration import GradeBookEmailConfiguration


class BaseGradeBookBackEndConfiguration(GradeBookEmailConfiguration):

	def __init__(self):
		super().__init__()

	def write_student_data_to_file(self, extension=".txt"):
		self.verify_visual_settings()
		if self.visual_settings.path_to_save_directory is None:
			raise ValueError("visual_settings.path_to_save_directory is not initialized")
		allowed_extensions = (
			".txt",
			)
		if extension not in allowed_extensions:
			raise ValueError("invalid extension: {}".format(extension))
		file_name = "student_data"
		output_path = "{}{}{}".format(
			self.visual_settings.path_to_save_directory,
			file_name,
			extension)
		partial_strings = list()
		for student in self.students:
			partial_string = str(
				student)
			partial_strings.append(
				partial_string)
		string_divider = "\n" + "="*10 + "\n"
		s = string_divider.join(
			partial_strings)
		with open(output_path, "w") as data_file:
			data_file.write(
				s)

	def write_data_frame_to_file(self, extension):
		
		def write_to_csv(output_path):
			self.modified_df.to_csv(
				output_path,
				index=False)

		def write_to_xlsx(output_path):
			self.modified_df.to_excel(
				output_path)

		self.verify_visual_settings()
		if self.visual_settings.path_to_save_directory is None:
			raise ValueError("visual_settings.path_to_save_directory is not initialized")
		extension_to_writer_mapping = {
			".csv" : write_to_csv,
			".xlsx" : write_to_xlsx}
		if extension not in extension_to_writer_mapping.keys():
			raise ValueError("invalid extension: {}".format(extension))
		file_name = "data_frame"
		output_path = "{}{}{}".format(
			self.visual_settings.path_to_save_directory,
			file_name,
			extension)
		write_data_frame = extension_to_writer_mapping[extension]
		write_data_frame(
			output_path=output_path)

class GradeBookBackEndConfiguration(BaseGradeBookBackEndConfiguration):

	def __init__(self):
		super().__init__()

	def initialize_back_end(self, path_to_data, path_to_save_directory=None, index_at_weighted_row=None, index_at_names_column=None, index_at_email_column=None, index_at_id_column=None, indices_at_home_work_columns=None, indices_at_exam_columns=None, indices_at_extra_credit_columns=None, flat_curve=None, is_home_work_improvement_curve=False, is_exam_improvement_curve=False, is_extra_credit_improvement_curve=False, points_at_fail=None, points_at_ace=None, in_between_edges=None, side_bias="left"):
		self.initialize_visual_settings()
		self.update_save_directory(
			path_to_save_directory=path_to_save_directory)
		self.initialize_data(
			path_to_data=path_to_data,
			index_at_weighted_row=index_at_weighted_row,
			index_at_names_column=index_at_names_column,
			index_at_email_column=index_at_email_column,
			index_at_id_column=index_at_id_column,
			indices_at_home_work_columns=indices_at_home_work_columns,
			indices_at_exam_columns=indices_at_exam_columns,
			indices_at_extra_credit_columns=indices_at_extra_credit_columns)
		self.initialize_evaluation(
			flat_curve=flat_curve,
			is_home_work_improvement_curve=is_home_work_improvement_curve,
			is_exam_improvement_curve=is_exam_improvement_curve,
			is_extra_credit_improvement_curve=is_extra_credit_improvement_curve,
			points_at_fail=points_at_fail,
			points_at_ace=points_at_ace,
			in_between_edges=in_between_edges,
			side_bias=side_bias)
		# self.initialize_email_functionality(
		# 	...)

##