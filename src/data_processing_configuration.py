import pandas as pd
import numpy as np


class BaseGradeBookDataProcessingConfiguration():

	def __init__(self):
		super().__init__()
		self._df = None
		self._modified_df = None
		self._index_at_weighted_row = None
		self._indices_at_scorable_rows = None
		self._columns_by_identifier = None
		self._columns_by_genre = None
		self._headers_by_row = None
		self._headers_by_column = None
		self._weights = None
		self._is_weighted = None
		self._scores = None
		self._student_identifiers = None
		self._genres = None
		self._genre_mapping = None

	@property
	def df(self):
		return self._df
	
	@property
	def modified_df(self):
		return self._modified_df
	
	@property
	def index_at_weighted_row(self):
		return self._index_at_weighted_row
	
	@property
	def indices_at_scorable_rows(self):
		return self._indices_at_scorable_rows

	@property
	def columns_by_identifier(self):
		return self._columns_by_identifier
	
	@property
	def columns_by_genre(self):
		return self._columns_by_genre

	@property
	def headers_by_row(self):
		return self._headers_by_row
	
	@property
	def headers_by_column(self):
		return self._headers_by_column

	@property
	def weights(self):
		return self._weights
	
	@property
	def is_weighted(self):
		return self._is_weighted
	
	@property
	def scores(self):
		return self._scores

	@property
	def student_identifiers(self):
		return self._student_identifiers
	
	@property
	def genres(self):
		return self._genres
	
	@property
	def genre_mapping(self):
		return self._genre_mapping
	
	@staticmethod
	def get_data_frame(path_to_data):
		if not isinstance(path_to_data, str):
			raise ValueError("invalid type(path_to_data): {}".format(type(path_to_data)))
		if path_to_data.endswith(".csv") or path_to_data.endswith(".txt"):
			df = pd.read_csv(
				path_to_data,
				dtype=str,
				)
		elif path_to_data.endswith(".xls") or path_to_data.endswith(".xlsx"):
			df = pd.read_excel(
				path_to_data,
				dtype=str,
				)
		else:
			raise ValueError("invalid path_to_data extension")
		return df

	@staticmethod
	def get_indices_at_scorable_rows(df, index_at_weighted_row=None):
		indices = list(
			range(
				df.shape[0]))
		if index_at_weighted_row is not None:
			if not isinstance(index_at_weighted_row, int):
				raise ValueError("invalid type(index_at_weighted_row): {}".format(type(index_at_weighted_row)))
			indices.pop(
				index_at_weighted_row)
		indices = np.array(
			indices)
		return indices

	@staticmethod
	def get_headers_by_row(indices_at_scorable_rows, index_at_weighted_row):
		headers_by_row = dict()
		for index_at_scorable_row in indices_at_scorable_rows:
			headers_by_row[index_at_scorable_row] = "score"
		if index_at_weighted_row is not None:
			if not isinstance(index_at_weighted_row, int):
				raise ValueError("invalid type(index_at_weighted_row): {}".format(type(index_at_weighted_row)))
			headers_by_row[index_at_weighted_row] = "weight"
		return headers_by_row

	@staticmethod
	def get_headers_by_column(df, index_at_names_column=None, index_at_email_column=None, index_at_id_column=None, indices_at_home_work_columns=None, indices_at_exam_columns=None, indices_at_extra_credit_columns=None):
		headers = df.columns.values.tolist()
		headers_by_column = dict()
		columns_by_identifier = {
			"name" : None,
			"ID number" : None,
			"email address" : None}
		columns_by_genre = {
			"home-work" : list(),
			"exam" : list(),
			"extra credit" : list()}

		def update_column_at_identifier(identifier, column):
			columns_by_identifier[identifier] = column
			headers_by_column[column] = identifier

		def update_column_at_genre(genre, columns):
			if isinstance(columns, int):
				columns = [columns]
			for column in columns:
				columns_by_genre[genre].append(
					column)
				headers_by_column[column] = headers[column]

		if index_at_names_column is not None:
			update_column_at_identifier(
				identifier="name",
				column=index_at_names_column)
		if index_at_email_column is not None:
			update_column_at_identifier(
				identifier="email address",
				column=index_at_email_column)
		if index_at_id_column is not None:
			update_column_at_identifier(
				identifier="ID number",
				column=index_at_id_column)
		if indices_at_home_work_columns is not None:
			update_column_at_genre(
				genre="home-work",
				columns=indices_at_home_work_columns)
		if indices_at_exam_columns is not None:
			update_column_at_genre(
				genre="exam",
				columns=indices_at_exam_columns)
		if indices_at_extra_credit_columns is not None:
			update_column_at_genre(
				genre="extra credit",
				columns=indices_at_extra_credit_columns)
		for genre, columns in columns_by_genre.items():
			number_columns = len(
				columns)
			if number_columns == 0:
				columns_by_genre[genre] = None
		return headers_by_column, columns_by_identifier, columns_by_genre

	@staticmethod
	def get_weights_and_scores_by_genre(df, index_at_weighted_row, indices_at_scorable_rows, indices_at_home_work_columns, indices_at_exam_columns, indices_at_extra_credit_columns):
		weights = dict()
		scores = dict()
		total_weight = 0
		genres = list()

		def update(genre, columns, total_weight):
			scores_at_genre = df.iloc[indices_at_scorable_rows, columns].values.astype(
				float)
			scores[genre] = scores_at_genre
			genres.append(
				genre)
			if index_at_weighted_row is not None:
				if not isinstance(index_at_weighted_row, int):
					raise ValueError("invalid type(index_at_weighted_row): {}".format(type(index_at_weighted_row)))
				weights_at_genre = df.iloc[index_at_weighted_row, columns].values.astype(
					float)
				total_weight += np.sum(
					weights_at_genre)
				weights[genre] = weights_at_genre
			else:
				weights_at_genre = np.full(
					fill_value=np.nan,
					shape=scores_at_genre.shape,
					dtype=float)
				weights[genre] = weights_at_genre
				total_weight = np.nan
			return total_weight

		it_genres = (
			"home-work",
			"exam",
			"extra credit")
		it_columns = (
			indices_at_home_work_columns,
			indices_at_exam_columns,
			indices_at_extra_credit_columns)
		for genre, columns in zip(it_genres, it_columns):
			if columns is not None:
				total_weight = update(
					genre=genre,
					columns=columns,
					total_weight=total_weight)
		genres = tuple(
			genres)
		weights["total"] = total_weight
		return weights, scores, genres

	@staticmethod
	def get_genre_mapping(headers_by_column, columns_by_genre):
		genre_mapping = dict()
		for genre, columns in columns_by_genre.items():
			if columns is not None:
				headers = list()
				for column in columns:
					header = headers_by_column[column]
					headers.append(
						header)
				headers = tuple(
					headers)
				genre_mapping[genre] = headers
		return genre_mapping

	@staticmethod
	def get_student_identifiers(columns_by_identifier):
		student_identifiers = list()
		for student_identifier, column in columns_by_identifier.items():
			if column is not None:
				student_identifiers.append(
					student_identifier)
		student_identifiers = tuple(
			student_identifiers)
		return student_identifiers

	def get_number_students(self):
		number_students = int(
			self.df.shape[0])
		if self.index_at_weighted_row is not None:
			number_students -= 1
		return number_students

class GradeBookDataProcessingConfiguration(BaseGradeBookDataProcessingConfiguration):

	def __init__(self):
		super().__init__()

	def initialize_data(self, path_to_data, index_at_weighted_row=None, index_at_names_column=None, index_at_email_column=None, index_at_id_column=None, indices_at_home_work_columns=None, indices_at_exam_columns=None, indices_at_extra_credit_columns=None):
		if index_at_weighted_row is not None:
			if not isinstance(index_at_weighted_row, int):
				raise ValueError("invalid type(index_at_weighted_row): {}".format(type(index_at_weighted_row)))
		df = self.get_data_frame(
			path_to_data=path_to_data)
		indices_at_scorable_rows = self.get_indices_at_scorable_rows(
			df=df,
			index_at_weighted_row=index_at_weighted_row)
		headers_by_row = self.get_headers_by_row(
			indices_at_scorable_rows=indices_at_scorable_rows,
			index_at_weighted_row=index_at_weighted_row)
		headers_by_column, columns_by_identifier, columns_by_genre = self.get_headers_by_column(
			df=df,
			index_at_names_column=index_at_names_column,
			index_at_email_column=index_at_email_column,
			index_at_id_column=index_at_id_column,
			indices_at_home_work_columns=indices_at_home_work_columns,
			indices_at_exam_columns=indices_at_exam_columns,
			indices_at_extra_credit_columns=indices_at_extra_credit_columns)
		student_identifiers = self.get_student_identifiers(
			columns_by_identifier=columns_by_identifier)
		weights, scores, genres = self.get_weights_and_scores_by_genre(
			df=df,
			index_at_weighted_row=index_at_weighted_row,
			indices_at_scorable_rows=indices_at_scorable_rows,
			indices_at_home_work_columns=indices_at_home_work_columns,
			indices_at_exam_columns=indices_at_exam_columns,
			indices_at_extra_credit_columns=indices_at_extra_credit_columns)
		genre_mapping = self.get_genre_mapping(
			headers_by_column=headers_by_column,
			columns_by_genre=columns_by_genre)
		is_weighted = np.invert(
			np.isnan(
				weights["total"]))
		self._df = df
		self._index_at_weighted_row = index_at_weighted_row
		self._indices_at_scorable_rows = indices_at_scorable_rows
		self._headers_by_row = headers_by_row
		self._headers_by_column = headers_by_column
		self._columns_by_identifier = columns_by_identifier
		self._columns_by_genre = columns_by_genre
		self._weights = weights
		self._is_weighted = is_weighted
		self._scores = scores
		self._student_identifiers = student_identifiers
		self._genres = genres
		self._genre_mapping = genre_mapping

	def update_modified_df(self, curves, points, grades):
		modified_df = self.df.copy(
			deep=True)
		for curve_method, curve_scores in curves.items():
			if self.index_at_weighted_row is None:
				modified_df[curve_method] = curve_scores
			else:
				modified_curve_scores = curve_scores.tolist()
				modified_curve_scores.insert(
					self.index_at_weighted_row,
					0)
				modified_df[curve_method] = modified_curve_scores
		for point_method, point_scores in points.items():
			if point_method == "without curve":
				modified_point_method = "sub-total points without curve"
			elif point_method == "curve":
				modified_point_method = "points from curve"
			elif point_method == "total":
				modified_point_method = "sub-total points with curve"
			if self.index_at_weighted_row is None:
				modified_df[modified_point_method] = point_scores
			else:
				modified_point_scores = point_scores.tolist()
				if modified_point_method == "points from curve":
					point_weight = 0
				else:
					point_weight = float(
						self.weights["total"])
				modified_point_scores.insert(
					self.index_at_weighted_row,
					point_weight)
				modified_df[modified_point_method] = modified_point_scores
		if self.index_at_weighted_row is None:
			modified_df["grades"] = grades
		else:
			modified_grades = list(
				grades)
			modified_grades.insert(
				self.index_at_weighted_row,
				"A+")
			modified_df["grades"] = modified_grades
		self._modified_df = modified_df

##