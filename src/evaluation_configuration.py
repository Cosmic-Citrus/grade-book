import numpy as np
from collections import Counter
from data_processing_configuration import GradeBookDataProcessingConfiguration
from histogram_configuration import HistogramConfiguration
from student_configuration import StudentConfiguration


class BaseGradeBookEvaluationConfiguration(GradeBookDataProcessingConfiguration):

	def __init__(self):
		super().__init__()
		self._points = None
		self._statistics = None
		self._is_curved = None
		self._curves = None
		self._side_bias = None
		self._grading_criteria = None
		self._grades = None
		self._grades_counter = None
		self._grades_histogram = None
		self._students = None
		self._number_students = None

	@property
	def points(self):
		return self._points
			
	@property
	def statistics(self):
		return self._statistics

	@property
	def is_curved(self):
		return self._is_curved

	@property
	def curves(self):
		return self._curves
	
	@property
	def side_bias(self):
		return self._side_bias

	@property
	def grading_criteria(self):
		return self._grading_criteria

	@property
	def grades(self):
		return self._grades
	
	@property
	def grades_counter(self):
		return self._grades_counter

	@property
	def grades_histogram(self):
		return self._grades_histogram
			
	@property
	def students(self):
		return self._students
	
	@property
	def number_students(self):
		return self._number_students

	def initialize_grading_criteria(self, points_at_fail=None, points_at_ace=None, in_between_edges=None, side_bias="left"):
		if side_bias is None:
			raise ValueError("invalid side_bias: {}".format(side_bias))
		possible_grades = tuple([
			"F",
			"D-",
			"D",
			"D+",
			"C-",
			"C",
			"C+",
			"B-",
			"B",
			"B+",
			"A-",
			"A",
			"A+"])
		grading_criteria = {
			"possible grades" : possible_grades}
		self._grading_criteria = grading_criteria
		self.update_grading_criteria(
			points_at_fail=points_at_fail,
			points_at_ace=points_at_ace,
			in_between_edges=in_between_edges,
			side_bias=side_bias,
			is_initial=True)

	def update_grading_criteria(self, points_at_fail=None, points_at_ace=None, in_between_edges=None, side_bias="left", is_initial=False):

		def get_autocorrected_points_at_fail_and_ace(points_at_fail, points_at_ace, is_initial):
			if points_at_ace is None:
				if is_initial:
					modified_points_at_ace = float(
						0.95 * self.weights["total"])
				else:
					modified_points_at_ace = float(
						self.grading_criteria["points at ace"])
			else:
				if not isinstance(points_at_ace, (int, float)):
					raise ValueError("invalid type(points_at_ace): {}".format(type(points_at_ace)))
				if points_at_ace > self.weights["total"]:
					raise ValueError("invalid points_at_ace: {}".format(points_at_ace))
				modified_points_at_ace = points_at_ace
			if points_at_fail is None:
				if is_initial:
					modified_points_at_fail = float(
						modified_points_at_ace / 2)
				else:
					modified_points_at_fail = float(
						self.grading_criteria["points at fail"])
			else:
				if not isinstance(points_at_fail, (int, float)):
					raise ValueError("invalid type(points_at_fail): {}".format(type(points_at_fail)))
				if points_at_fail < 0:
					raise ValueError("invalid points_at_fail: {}".format(points_at_fail))
				modified_points_at_fail = points_at_fail
			if modified_points_at_fail >= modified_points_at_ace:
				raise ValueError("modified_points_at_fail={} and modified_points_at_ace={} are not compatible".format(modified_points_at_fail, modified_points_at_ace))
			return modified_points_at_fail, modified_points_at_ace

		def get_autocorrected_side_bias(side_bias, is_initial):
			if side_bias is None:
				if is_initial:
					raise ValueError("invalid side_bias: {}".format(side_bias))
				else:
					side_bias = self.grading_criteria["side-bias"][:]
			elif isinstance(side_bias, str):
				if side_bias not in ("left", "right"):
					raise ValueError("invalid side_bias: {}".format(side_bias))
			else:
				raise ValueError("invalid type(side_bias): {}".format(type(side_bias)))
			modified_side_bias = side_bias[:]
			return modified_side_bias

		def get_edges_at_grade_points(modified_points_at_fail, modified_points_at_ace, number_possible_grades, in_between_edges):
			left_most_edge = -1
			right_most_edge = self.weights["total"] * 10
			if in_between_edges is None:
				modified_in_between_edges = np.linspace(
					modified_points_at_fail,
					modified_points_at_ace,
					number_possible_grades - 1)
			elif isinstance(in_between_edges, (tuple, list, np.ndarray)):
				if isinstance(in_between_edges, (tuple, list)):
					modified_in_between_edges = np.array(
						in_between_edges)
				else:
					modified_in_between_edges = np.copy(
						in_between_edges)
				if not isinstance(modified_in_between_edges, np.ndarray):
					raise ValueError("invalid in_between_edges: {}".format(in_between_edges))
				size_of_shape = len(
					modified_in_between_edges.shape)
				if size_of_shape != 1:
					raise ValueError("invalid in_between_edges: {}".format(in_between_edges))
				if modified_in_between_edges.size != number_possible_grades - 3:
					raise ValueError("invalid len(in_between_edges): {}".format(modified_in_between_edges.size))
				modified_in_between_edges = np.concatenate([
					(modified_points_at_fail,),
					modified_in_between_edges,
					(modified_points_at_ace,)])
			else:
				raise ValueError("invalid type(in_between_edges): {}".format(type(in_between_edges)))
			edges = np.concatenate([
				(left_most_edge,),
				modified_in_between_edges,
				(right_most_edge,)])
			is_monotonically_increasing = np.invert(
				np.any(
					np.diff(edges) <= 0))
			if not is_monotonically_increasing:
				raise ValueError("edges must be in increasing order")
			return edges
		
		def get_string_representation(number_possible_grades, modified_side_bias, edges):
			get_string = lambda string_at_lower_bound, string_at_upper_bound, grade : "\n{} {} score {} {} ==> {}\n".format(
				string_at_lower_bound,
				"≤" if modified_side_bias == "left" else "<",
				"<" if modified_side_bias == "left" else "≤",
				string_at_upper_bound,
				grade)
			get_bin_label = lambda value_at_lower_bound, value_at_upper_bound, grade : "{} {} {} {} {}".format(
				"${:,.2f}$".format(
					value_at_lower_bound),
				"≤" if modified_side_bias == "left" else "<",
				grade,
				"<" if modified_side_bias == "left" else "≤",
				r"$\infty$" if np.isinf(value_at_upper_bound) else "${:,.2f}$".format(
					value_at_upper_bound))
			grading_criteria_per_bin = list()
			bin_labels = list()
			for i, (value_at_lower_bound, value_at_upper_bound, grade) in enumerate(zip(edges[:-1], edges[1:], self.grading_criteria["possible grades"])):
				string_at_lower_bound = "0" if i == 0 else "{}".format(
					value_at_lower_bound)
				string_at_upper_bound = r"$\infty$" if i == number_possible_grades - 1 else "{}".format(
					value_at_upper_bound)
				modified_value_at_upper_bound = np.inf if i == number_possible_grades - 1 else value_at_upper_bound
				string_at_bin = get_string(
					string_at_lower_bound=string_at_lower_bound,
					string_at_upper_bound=string_at_upper_bound,
					grade=grade)
				bin_label = get_bin_label(
					value_at_lower_bound=value_at_lower_bound,
					value_at_upper_bound=modified_value_at_upper_bound,
					grade=grade)
				grading_criteria_per_bin.append(
					string_at_bin)
				bin_labels.append(
					bin_label)
			stringed_grading_criteria = "\n".join(
				grading_criteria_per_bin)
			title = "\n .. Grading Criteria (side-bias={})".format(
				modified_side_bias)
			space_below_title = "\n" + "="*20 + "\n"
			string_representation = "{}{}{}".format(
				title,
				space_below_title,
				stringed_grading_criteria)
			return string_representation, grading_criteria_per_bin, bin_labels

		modified_points_at_fail, modified_points_at_ace = get_autocorrected_points_at_fail_and_ace(
			points_at_fail=points_at_fail,
			points_at_ace=points_at_ace,
			is_initial=is_initial)
		number_possible_grades = len(
			self.grading_criteria["possible grades"])
		edges = get_edges_at_grade_points(
			modified_points_at_fail=modified_points_at_fail,
			modified_points_at_ace=modified_points_at_ace,
			number_possible_grades=number_possible_grades,
			in_between_edges=in_between_edges)
		modified_side_bias = get_autocorrected_side_bias(
			side_bias=side_bias,
			is_initial=is_initial)
		string_representation, grading_criteria_per_bin, bin_labels = get_string_representation(
			number_possible_grades=number_possible_grades,
			modified_side_bias=modified_side_bias,
			edges=edges)
		supplementary_criteria = {
			"points at fail" : modified_points_at_fail,
			"points at ace" : modified_points_at_ace,
			"side-bias" : modified_side_bias,
			"grade-point edges" : edges,
			"string representation" : string_representation,
			"bin labels" : bin_labels}
		self._grading_criteria.update(
			supplementary_criteria)
		if not is_initial:
			self.update_grades()

	def update_grades(self):
		grades = self.get_grades(
			sub_totals=self.points["total"])
		grades_counter = Counter(
			grades)
		self._grades = grades
		self._grades_counter = grades_counter
		self.update_grades_histogram()

	def get_grades(self, sub_totals):
		if self.grading_criteria["side-bias"] == "left":
			side = "right"
		elif self.grading_criteria["side-bias"] == "right":
			side = "left"
		else:
			raise ValueError("invalid side_bias: {}".format(self.grading_criteria["side-bias"]))
		if isinstance(sub_totals, (int, float)):
			index_at_grade = np.searchsorted(
				self.grading_criteria["grade-point edges"][1:-1],
				sub_totals,
				side=side)
			grades = self.grading_criteria["possible grades"][index_at_grade][:]
		elif isinstance(sub_totals, np.ndarray):
			indices_at_grade = np.searchsorted(
				self.grading_criteria["grade-point edges"][1:-1],
				sub_totals,
				side=side)
			grades = [
				self.grading_criteria["possible grades"][index_at_grade]
					for index_at_grade in indices_at_grade]
		else:
			raise ValueError("invalid type(sub_totals): {}".format(type(sub_totals)))
		return grades

	def update_grades_histogram(self):
		grades_histogram = HistogramConfiguration()
		grades_histogram.initialize_distribution_values(
			distribution_values=self.points["total"])
		bin_edges = np.arange(
			self.grading_criteria["grade-point edges"].size)
		bin_counts = np.array([
			self.grades_counter[grade]
				for grade in self.grading_criteria["possible grades"]])
		grades_histogram.initialize_bin_locations(
				bin_selection_method="bin edges",
				bin_edges=bin_edges)
		grades_histogram.initialize_bin_counts(
			side_bias=self.grading_criteria["side-bias"][:],
			bin_counts=bin_counts)
		self._grades_histogram = grades_histogram

class GradeBookPointsEvaluationConfiguration(BaseGradeBookEvaluationConfiguration):

	def __init__(self):
		super().__init__()

	@staticmethod
	def get_number_missing(arr, axis=None):
		number_missing = np.sum(
			np.isnan(
				arr),
			axis=axis)
		return number_missing

	def initialize_points(self):
		points = dict()
		number_students = self.get_number_students()
		pts = np.full(
			fill_value=0,
			shape=number_students,
			dtype=float)
		for genre in self.genres:
			total_score_by_genre = np.nansum(
				self.scores[genre],
				axis=1)
			pts += total_score_by_genre
		points["without curve"] = pts
		self._points = points
		self.update_points()

	def update_points(self):
		number_students = self.get_number_students()
		points_by_curve = np.full(
			fill_value=0,
			shape=number_students,
			dtype=float)
		if self.is_curved:
			for genre, pts in self.curves.items():
				points_by_curve = np.add(
					points_by_curve,
					pts)
		points_by_total = self.points["without curve"] + points_by_curve
		self._points["curve"] = points_by_curve
		self._points["total"] = points_by_total

	def initialize_statistics(self):
		number_missing = 0
		statistics_by_genre = dict()
		for genre in self.genres:
			statistics_at_genre = self.get_statistics(
				self.scores[genre],
				axis=0,
				ddof=0)
			number_missing_at_genre = int(
				np.sum(
					statistics_at_genre["number missing"]))
			number_missing += number_missing_at_genre
			statistics_by_genre[genre] = statistics_at_genre
		statistics_by_points_without_curve = self.get_statistics(
			self.points["without curve"],
			axis=None,
			ddof=0)
		statistics_by_points_without_curve["number missing"] = number_missing
		statistics_by_points = {
			"without curve" : statistics_by_points_without_curve}
		statistics = {
			"genre" : statistics_by_genre,
			"points" : statistics_by_points}
		self._statistics = statistics
		self.update_statistics()

	def update_statistics(self):
		statistics_by_points_at_total = self.get_statistics(
			self.points["total"],
			axis=0,
			ddof=0)
		statistics_by_points_at_total["number missing"] = int(
			self.statistics["points"]["without curve"]["number missing"])
		self._statistics["points"]["total"] = statistics_by_points_at_total
		if self.is_curved:
			statistics_by_curve = dict()
			for curve_method, curve_scores in self.curves.items():
				statistics_at_curve = self.get_statistics(
					self.curves[curve_method],
					axis=None)
				statistics_by_curve[curve_method] = statistics_at_curve
			statistics_by_points_at_curve = self.get_statistics(
				self.points["curve"],
				axis=None)
			self._statistics["curves"] = statistics_by_curve
			self._statistics["points"]["curves"] = statistics_by_points_at_curve
		else:
			if "curves" in self.statistics.keys():
				del self._statistics["curves"]
			if "curves" in self.statistics["points"].keys():
				del self._statistics["points"]["curves"]

	def get_statistics(self, arr, axis=None, ddof=0):
		statistics = {
			"mean" : np.nanmean(
				arr,
				axis=axis),
			"median" : np.nanmedian(
				arr,
				axis=axis),
			"maximum" : np.nanmax(
				arr,
				axis=axis),
			"minimum" : np.nanmin(
				arr,
				axis=axis),
			"standard deviation" : np.nanstd(
				arr,
				axis=axis,
				ddof=ddof),
			"total" : np.nansum(
				arr,
				axis=axis),
			"number missing" : self.get_number_missing(
				arr,
				axis=axis)}
		return statistics

class GradeBookStudentsConfiguration(GradeBookPointsEvaluationConfiguration):

	def __init__(self):
		super().__init__()

	def initialize_students(self):
		is_with_name = (self.columns_by_identifier["name"] is not None)
		is_with_email_address = (self.columns_by_identifier["email address"] is not None)
		is_with_id_number = (self.columns_by_identifier["ID number"] is not None)
		is_with_home_work = ("home-work" in self.genres)
		is_with_exam = ("exam" in self.genres)
		is_with_extra_credit = ("extra credit" in self.genres)		
		students = list()
		for index_at_student, index_at_scorable_row in enumerate(self.indices_at_scorable_rows):
			points = float(
				self.points["total"][index_at_student])
			grade = str(
				self.grades[index_at_student])
			kwargs = dict()
			if is_with_name:
				kwargs["name"] = self.df.iloc[index_at_scorable_row, self.columns_by_identifier["name"]]
			if is_with_email_address:
				kwargs["email_address"] = self.df.iloc[index_at_scorable_row, self.columns_by_identifier["email address"]]
			if is_with_id_number:
				kwargs["id_number"] = self.df.iloc[index_at_scorable_row, self.columns_by_identifier["ID number"]]
			if is_with_home_work:
				home_work_scores = np.copy(
					self.scores["home-work"][index_at_student, :])
				home_work_statistics = self.get_statistics(
					home_work_scores,
					ddof=0,
					axis=None)
				kwargs["home_work_scores"] = home_work_scores
				kwargs["home_work_weights"] = np.copy(
					self.weights["home-work"])
				kwargs["home_work_statistics"] = home_work_statistics
				kwargs["home_work_headers"] = tuple(
					self.genre_mapping["home-work"])
			if is_with_exam:
				exam_scores = np.copy(
					self.scores["exam"][index_at_student, :])
				exam_statistics = self.get_statistics(
					exam_scores,
					ddof=0,
					axis=None)
				kwargs["exam_scores"] = exam_scores
				kwargs["exam_weights"] = np.copy(
					self.weights["exam"])
				kwargs["exam_statistics"] = exam_statistics
				kwargs["exam_headers"] = tuple(
					self.genre_mapping["exam"])
			if is_with_extra_credit:
				extra_credit_scores = np.copy(
					self.scores["exam"][index_at_student, :])
				extra_credit_statistics = self.get_statistics(
					exam_scores,
					ddof=0,
					axis=None)
				kwargs["extra_credit_scores"] = extra_credit_scores
				kwargs["extra_credit_weights"] = np.copy(
					self.weights["extra credit"])
				kwargs["extra_credit_statistics"] = extra_credit_statistics
				kwargs["extra_credit_headers"] = tuple(
					self.genre_mapping["extra credit"])
			if self.is_curved:
				partial_curve_headers, partial_curve_scores = list(), list()
				for curve_method, curve_scores in self.curves.items():
					partial_curve_headers.append(
						curve_method)
					partial_curve_scores.append(
						curve_scores[index_at_student])
				partial_curve_scores = np.array(
					partial_curve_scores)
				partial_curve_headers = tuple(
					partial_curve_headers)
				partial_curve_statistics = self.get_statistics(
					partial_curve_scores,
					ddof=0,
					axis=None)
				kwargs["curve_scores"] = partial_curve_scores
				kwargs["curve_statistics"] = partial_curve_statistics
				kwargs["curve_headers"] = partial_curve_headers
			student = StudentConfiguration()
			student.initialize(
				index_at_student=index_at_student,
				points=points,
				grade=grade,
				**kwargs)
			students.append(
				student)
		# number_students = self.get_number_students()
		number_students = len(
			students)
		self._students = students
		self._number_students = number_students

	def update_students(self):
		curve_headers = list(
			self.curves.items())
		number_curve_headers = len(
			curve_headers)
		for index_at_student, (student, points, grade) in enumerate(zip(self._students, self.points["total"], self.grades)):
			if number_curve_headers == 0:
				modified_curve_headers = None
				curve_scores = None
				curve_statistics = None
			else:
				modified_curve_headers = curve_headers[:]
				curve_scores = list()
				for curve_header in curve_headers:
					curve_score = self.curves[curve_header][index_at_student]
					curve_scores.append(
						curve_score)
				curve_scores = np.array(
					curve_scores)
				curve_statistics = self.get_statistics(
					curve_scores,
					ddof=0,
					axis=None)
			student.update_curves(
				curve_scores=curve_scores,
				curve_statistics=curve_statistics,
				curve_headers=modified_curve_headers)
			student.update_points_and_grade(
				points=points,
				grade=grade)

class GradeBookCurvesConfiguration(GradeBookStudentsConfiguration):

	def __init__(self):
		super().__init__()

	def initialize_curves(self):
		curves = dict()
		self._curves = curves

	def update_curve_status(self):
		number_curve_methods = len(
			self.curves.keys())
		is_curved = (number_curve_methods > 0)
		self._is_curved = is_curved

	def add_curves(self, flat_curve=None, is_home_work_improvement_curve=False, is_exam_improvement_curve=False, is_extra_credit_improvement_curve=False, is_initial=False):

		def get_flat_curve(flat_curve):
			number_students = self.get_number_students()
			curve_by_flat_method = np.full(
				fill_value=flat_curve,
				shape=number_students,
				dtype=float)
			return curve_by_flat_method

		def get_improvement_curve(genre, scale):
			if not self.is_weighted:
				raise ValueError("cannot evaluate improvement without weights")
			number_scores = len(
				self.columns_by_genre[genre])
			if number_scores < 2:
				raise ValueError("cannot evaluate improvement from one score")
			weights = self.weights[genre]
			scores = self.scores[genre]
			weighted_scores = scores / weights
			index_at_middle = weighted_scores.shape[1] // 2
			weighted_scores_at_first_half = weighted_scores[:, :index_at_middle]
			weighted_scores_at_second_half = weighted_scores[:, -1 * index_at_middle:]
			average_points_at_first_half = np.nanmean(
				weighted_scores_at_first_half,
				axis=1)
			average_points_at_second_half = np.nanmean(
				weighted_scores_at_second_half,
				axis=1)
			difference = average_points_at_second_half - average_points_at_first_half
			difference[difference < 0] = 0
			difference[np.isnan(difference)] = 0
			average_weight = np.mean(
				weights)
			improvement_curve = difference * average_weight * scale
			return improvement_curve

		curves = dict()
		if flat_curve is None:
			is_flat_curve = False
		else:
			if not isinstance(flat_curve, (int, float)):
				raise ValueError("invalid type(flat_curve): {}".format(type(flat_curve)))
			if flat_curve <= 0:
				raise ValueError("invalid flat_curve: {}".format(flat_curve))
			is_flat_curve = True
			curve_by_flat_method = get_flat_curve(
				flat_curve=flat_curve)
			curves["flat curve"] = curve_by_flat_method
		improvement_states = (
			is_home_work_improvement_curve,
			is_exam_improvement_curve,
			is_extra_credit_improvement_curve)
		improvement_genres = (
			"home-work",
			"exam",
			"extra credit")
		for is_improvement_curve, genre in zip(improvement_states, improvement_genres):
			if is_improvement_curve:
				curve_method = "{} improvement curve".format(
					genre)
				improvement_curve = get_improvement_curve(
					genre=genre,
					scale=0.5)
				curves[curve_method] = improvement_curve
		# self._curves = curves
		self._curves.update(
			curves)
		self.update_curve_status()
		self.update_points()
		self.update_statistics()
		self.update_grades()
		if not is_initial:
			self.update_students()
		self.update_modified_df(
			curves=self.curves,
			points=self.points,
			grades=self.grades)

	def remove_curves(self, is_flat_curve=False, is_home_work_improvement_curve=False, is_exam_improvement_curve=False, is_extra_credit_improvement_curve=False, is_initial=False):
		
		def remove_curve(curve_method):
			if curve_method in self.curves.keys():
				del self._curves[curve_method]

		if is_flat_curve:
			remove_curve(
				curve_method="flat curve")
		if is_home_work_improvement_curve:
			remove_curve(
				curve_method="home-work improvement curve")
		if is_exam_improvement_curve:
			remove_curve(
				curve_method="exam improvement curve")
		if is_extra_credit_improvement_curve:
			remove_curve(
				curve_method="extra credit improvement curve")
		self.update_curve_status()
		self.update_points()
		self.update_statistics()
		self.update_grades()
		if not is_initial:
			self.update_students()
		self.update_modified_df(
			curves=self.curves,
			points=self.points,
			grades=self.grades)

class GradeBookEvaluationConfiguration(GradeBookCurvesConfiguration):

	def __init__(self):
		super().__init__()

	def initialize_evaluation(self, flat_curve=None, is_home_work_improvement_curve=False, is_exam_improvement_curve=False, is_extra_credit_improvement_curve=False, points_at_fail=None, points_at_ace=None, in_between_edges=None, side_bias="left"):
		self.initialize_grading_criteria(
			points_at_fail=points_at_fail,
			points_at_ace=points_at_ace,
			in_between_edges=in_between_edges,
			side_bias=side_bias)
		self.initialize_points()
		self.initialize_statistics()
		self.initialize_curves()
		self.add_curves(
			flat_curve=flat_curve,
			is_home_work_improvement_curve=is_home_work_improvement_curve,
			is_exam_improvement_curve=is_exam_improvement_curve,
			is_extra_credit_improvement_curve=is_extra_credit_improvement_curve,
			is_initial=True)
		self.initialize_students()

##