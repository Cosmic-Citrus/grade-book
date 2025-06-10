import numpy as np


class BaseStudentConfiguration():

	def __init__(self):
		super().__init__()
		self._index_at_student = None
		self._name = None
		self._email_address = None
		self._id_number = None
		self._home_work = None
		self._exam = None
		self._extra_credit = None
		self._curves = None
		self._is_curved = None
		self._points = None
		self._grade = None

	@property
	def index_at_student(self):
		return self._index_at_student
	
	@property
	def name(self):
		return self._name
	
	@property
	def email_address(self):
		return self._email_address
	
	@property
	def id_number(self):
		return self._id_number
	
	@property
	def home_work(self):
		return self._home_work
	
	@property
	def exam(self):
		return self._exam
	
	@property
	def extra_credit(self):
		return self._extra_credit
	
	@property
	def curves(self):
		return self._curves

	@property
	def is_curved(self):
		return self._is_curved
	
	@property
	def points(self):
		return self._points
	
	@property
	def grade(self):
		return self._grade

	@staticmethod
	def get_score_parameters(scores, weights, statistics, headers):
		condition_at_scores = isinstance(
			scores,
			np.ndarray)
		condition_at_weights = isinstance(
			weights,
			np.ndarray)
		condition_at_statistics = isinstance(
			statistics,
			dict)
		condition_at_headers = isinstance(
			headers,
			(tuple, list))
		conditions = (
			condition_at_scores,
			condition_at_weights,
			condition_at_statistics,
			condition_at_headers)
		if all(conditions):
			if len(scores.shape) != 1:
				raise ValueError("invalid scores.shape: {}".format(scores.shape))
			if (scores.shape != weights.shape):
				raise ValueError("scores.shape={} and weights.shape={} are not compatible".format(scores.shape, weights.shape))
			number_headers = len(
				headers)
			if scores.size != number_headers:
				raise ValueError("scores.size={} and len(headers)={} are not compatible".format(scores.size, number_headers))
			parameters = {
				"scores" : scores,
				"weights" : weights,
				"statistics" : statistics,
				"headers" : headers}
		else:
			number_satisfied_conditions = sum(
				conditions)
			if number_satisfied_conditions > 0:
				raise ValueError("invalid combination of scores, weights, statistics, and headers")
			parameters = None
		return parameters

	def initialize_scores(self, home_work_scores=None, home_work_weights=None, home_work_statistics=None, home_work_headers=None, exam_scores=None, exam_weights=None, exam_statistics=None, exam_headers=None, extra_credit_scores=None, extra_credit_weights=None, extra_credit_statistics=None, extra_credit_headers=None):
		home_work = self.get_score_parameters(
			scores=home_work_scores,
			weights=home_work_weights,
			statistics=home_work_statistics,
			headers=home_work_headers)
		exam = self.get_score_parameters(
			scores=exam_scores,
			weights=exam_weights,
			statistics=exam_statistics,
			headers=exam_headers)
		extra_credit = self.get_score_parameters(
			scores=extra_credit_scores,
			weights=extra_credit_weights,
			statistics=extra_credit_statistics,
			headers=extra_credit_headers)
		self._home_work = home_work
		self._exam = exam
		self._extra_credit = extra_credit

	def update_curves(self, curve_scores=None, curve_statistics=None, curve_headers=None):
		if curve_scores is None:
			if (curve_statistics is not None) or (curve_headers is not None):
				raise ValueError("invalid combination of curve_scores, curve_statistics, and curve_headers")
			curves = None
		else:
			if not isinstance(curve_scores, np.ndarray):
				raise ValueError("invalid type(curve_scores): {}".format(type(curve_scores)))
			zero_weights = np.full(
				fill_value=0,
				shape=curve_scores.shape,
				dtype=int)
			curves = self.get_score_parameters(
				scores=curve_scores,
				weights=zero_weights,
				statistics=curve_statistics,
				headers=curve_headers)
		self._curves = curves

	def update_points_and_grade(self, points, grade):
		self._points = points
		self._grade = grade

	def initialize_identifiers(self, index_at_student, name=None, id_number=None, email_address=None):
		if name is not None:
			if not isinstance(name, str):
				raise ValueError("invalid type(name): {}".format(type(name)))
		if id_number is not None:
			if not isinstance(id_number, str): #(int, np.int64)):
				raise ValueError("invalid type(id_number): {}".format(type(id_number)))
		if email_address is not None:
			if not isinstance(email_address, str):
				raise ValueError("invalid type(email_address): {}".format(type(email_address)))
		self._index_at_student = index_at_student
		self._name = name
		self._id_number = id_number
		self._email_address = email_address

class StudentStringConfiguration(BaseStudentConfiguration):

	def __init__(self):
		super().__init__()

	def get_stringed_identifiers(self):
		name = self.get_autoformatted_string(
			parameter="NAME",
			value=self.name,
			number_indents=0)
		id_number = self.get_autoformatted_string(
			parameter="ID NUMBER",
			value=self.id_number,
			number_indents=0)
		email_address = self.get_autoformatted_string(
			parameter="EMAIL ADDRESS",
			value=self.email_address,
			number_indents=0)
		s = "{}{}{}".format(
			name,
			id_number,
			email_address)
		return s

	def get_stringed_scores(self):

		def get_rearranged_data(parameters):
			data = dict()
			if np.all(parameters["weights"] == 0):
				for header, score in zip(parameters["headers"], parameters["scores"]):
					data[header] = "{:,.2f}".format(
						score)
			else:
				for header, score, weight in zip(parameters["headers"], parameters["scores"], parameters["weights"]):
					data[header] = "{:,.2f} / {:,.2f}".format(
						score,
						weight)
			data["statistics"] = dict(
				parameters["statistics"])
			return data

		if self.home_work is None:
			home_work = self.get_null_string(
				parameter="HOME-WORK",
				number_indents=0)
		else:
			home_work_data = get_rearranged_data(
				parameters=self.home_work)
			home_work = self.get_autoformatted_string(
				parameter="HOME-WORK",
				value=home_work_data,
				number_indents=0)
		if self.exam is None:
			exam = self.get_null_string(
				parameter="EXAM",
				number_indents=0)
		else:
			exam_data = get_rearranged_data(
				parameters=self.exam)
			exam = self.get_autoformatted_string(
				parameter="EXAM",
				value=exam_data,
				number_indents=0)
		if self.extra_credit is None:
			extra_credit = self.get_null_string(
				parameter="EXTRA CREDIT",
				number_indents=0)
		else:
			extra_credit_data = get_rearranged_data(
				parameters=self.extra_credit)
			extra_credit = self.get_autoformatted_string(
				parameter="EXTRA CREDIT",
				value=extra_credit_data,
				number_indents=0)
		if self.curves is None:
			curves = self.get_null_string(
				parameter="CURVE",
				number_indents=0)
		else:
			curves_data = get_rearranged_data(
				parameters=self.curves)
			curves = self.get_autoformatted_string(
				parameter="CURVES",
				value=curves_data,
				number_indents=0)
		s = "\n{}\n{}\n{}\n{}\n".format(
			home_work,
			exam,
			extra_credit,
			curves)
		return s

	def get_stringed_points_and_grade(self):
		points = self.get_autoformatted_string(
			parameter="POINTS",
			value=self.points,
			number_indents=0)
		grade = self.get_autoformatted_string(
			parameter="GRADE",
			value=self.grade,
			number_indents=0)
		s = "{}{}".format(
			points,
			grade)
		return s

	def get_autoformatted_string(self, parameter, value, number_indents=0):

		def transform_none_to_string(parameter, value, number_indents):
			title = "\n" + "\t" * number_indents + " .. {}:".format(
				parameter)
			body = "\n" + "\t" * number_indents + "{}\n".format(
				value)
			s = "{}\n{}".format(
				title,
				body)
			return s

		def transform_float_to_string(parameter, value, number_indents):
			title = "\n" + "\t" * number_indents + " .. {}:".format(
				parameter)
			body = "\n" + "\t" * number_indents + "{:,.2f}\n".format(
				value)
			s = "{}\n{}".format(
				title,
				body)
			return s

		def transform_integer_to_string(parameter, value, number_indents):
			title = "\n" + "\t" * number_indents + " .. {}:".format(
				parameter)
			body = "\n" + "\t" * number_indents + "{:,}\n".format(
				value)
			s = "{}\n{}".format(
				title,
				body)
			return s

		def transform_string_to_string(parameter, value, number_indents):
			title = "\n" + "\t" * number_indents + " .. {}:".format(
				parameter)
			body = "\n" + "\t" * number_indents + "{}\n".format(
				value)
			s = "{}\n{}".format(
				title,
				body)
			return s

		def transform_container_to_string(parameter, value, number_indents):
			if isinstance(value, (tuple, list)):
				size = len(
					value)
				title = "\n" + "\t" * number_indents + " .. {} (len={}):".format(
					size,
					parameter)
				body = "\n" + "\t" * number_indents + "{}\n".format(
					value)
			elif isinstance(value, np.ndarray):
				title = "\n" + "\t" * number_indents + " .. {} (shape={}):".format(
					value.shape,
					parameter)
				body = "\n" + "\t" * number_indents + "{}\n".format(
					value)
			else:
				raise ValueError("invalid type(value): {}".format(type(value)))
			s = "{}\n{}".format(
				title,
				body)
			return s

		def transform_dictionary_to_string(parameter, value, number_indents):
			title = "\n" + "\t" * number_indents + " .. {}:\n".format(
				parameter)
			incremented_number_indents = number_indents + 1
			partial_bodies = list()
			for sub_title, sub_value in value.items():
				partial_body = self.get_autoformatted_string(
					parameter=sub_title,
					value=sub_value,
					number_indents=incremented_number_indents)
				partial_bodies.append(
					partial_body)
			body = "\n".join(
				partial_bodies)
			s = "{}\n{}".format(
				title,
				body)
			return s

		if value is None:
			s = transform_none_to_string(
				parameter=parameter,
				value=value,
				number_indents=number_indents)
		elif isinstance(value, float):
			s = transform_float_to_string(
				parameter=parameter,
				value=value,
				number_indents=number_indents)
		elif isinstance(value, (int, np.int64)):
			s = transform_integer_to_string(
				parameter=parameter,
				value=value,
				number_indents=number_indents)
		elif isinstance(value, str):
			s = transform_string_to_string(
				parameter=parameter,
				value=value,
				number_indents=number_indents)
		elif isinstance(value, (tuple, list, np.ndarray)):
			s = transform_container_to_string(
				parameter=parameter,
				value=value,
				number_indents=number_indents)
		elif isinstance(value, dict):
			s = transform_dictionary_to_string(
				parameter=parameter,
				value=value,
				number_indents=number_indents)
		else:
			raise ValueError("invalid type(value): {}".format(type(value)))
		return s

	def get_null_string(self, parameter, number_indents=0):
		s = self.get_autoformatted_string(
			parameter=parameter,
			value=None,
			number_indents=number_indents)
		return s

class StudentConfiguration(StudentStringConfiguration):

	def __init__(self):
		super().__init__()

	def __repr__(self):
		return "StudentConfiguration()"

	def __str__(self):
		stringed_identifiers = self.get_stringed_identifiers()
		stringed_scores = self.get_stringed_scores()
		stringed_points_and_grade = self.get_stringed_points_and_grade()
		s = "{}{}{}".format(
			stringed_identifiers,
			stringed_scores,
			stringed_points_and_grade)
		return s

	def initialize(self, index_at_student, points, grade, *args, curve_scores=None, curve_statistics=None, curve_headers=None, name=None, id_number=None, email_address=None, **kwargs):
		self.initialize_identifiers(
			index_at_student=index_at_student,
			name=name,
			id_number=id_number,
			email_address=email_address)
		self.initialize_scores(
			*args,
			**kwargs)
		self.update_curves(
			curve_scores=curve_scores,
			curve_statistics=curve_statistics,
			curve_headers=curve_headers)
		self.update_points_and_grade(
			points=points,
			grade=grade)

##