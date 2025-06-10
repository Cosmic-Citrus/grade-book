import numpy as np


class BaseDistanceMatrixConfiguration():

	def __init__(self):
		super().__init__()
		self._distance_metric = None
		self._get_distance = None

	@property
	def distance_metric(self):
		return self._distance_metric
	
	@property
	def get_distance(self):
		return self._get_distance
	
	@staticmethod
	def verify_matrix_is_square(mat):
		if not isinstance(mat, np.ndarray):
			raise ValueError("invalid type(mat): {}".format(type(mat)))
		if len(mat.shape) != len(["x", "y"]):
			raise ValueError("invalid mat.shape: {}".format(mat.shape))
		if mat.shape[0] != mat.shape[1]:
			raise ValueError("invalid mat.shape: {} is not square".format(shape))

	@staticmethod
	def get_displacement(coordinates):
		if not isinstance(coordinates, np.ndarray):
			raise ValueError("invalid type(coordinates): {}".format(type(coordinates)))
		size_of_shape = len(
			coordinates.shape)
		if size_of_shape == 1:
			zero_coordinates = np.full(
				fill_value=0,
				shape=coordinates.shape,
				dtype=float)
			modified_coordinates = np.array([
				coordinates,
				zero_coordinates]).T
		elif size_of_shape == 2:
			modified_coordinates = np.copy(
				coordinates)
		else:
			raise ValueError("invalid coordinates.shape: {}".format(coordinates.shape))
		transformed_coordinates = modified_coordinates.reshape((
			modified_coordinates.shape[0],
			1,
			modified_coordinates.shape[1]))
		displacement = modified_coordinates - transformed_coordinates
		return displacement

	def get_matrix_with_masked_diagonal(self, mat, mask_value):
		self.verify_matrix_is_square(
			mat=mat)
		modified_mat = mat.astype(
			float)
		number_sides = modified_mat.shape[0]
		modified_mat[range(number_sides), range(number_sides)] = mask_value
		return modified_mat

	def get_flat_upper_triangle(self, mat):
		self.verify_matrix_is_square(
			mat=mat)
		flat_upper_triangle = list()
		for r in range(mat.shape[0]):
			for c in range(mat.shape[1]):
				if c > r:
					flat_upper_triangle.append(
						mat[r, c])
		flat_upper_triangle = np.array(
			flat_upper_triangle)
		return flat_upper_triangle

	def update_distance_metric(self, distance_metric):

		def get_manhattan_distance(displacement, axis):
			distance = np.nansum(
				np.abs(
					displacement),
				axis=axis)
			return distance

		def get_euclidean_square_distance(displacement, axis):
			distance = np.nansum(
				np.square(
					displacement),
				axis=axis)
			return distance

		def get_euclidean_distance(displacement, axis):
			sq_distance = get_euclidean_square_distance(
				displacement=displacement,
				axis=axis)
			distance = np.sqrt(
				sq_distance)
			return distance

		metric_to_function_mapping = {
			"manhattan" : get_manhattan_distance,
			"euclidean square" : get_euclidean_square_distance,
			"euclidean" : get_euclidean_distance}
		if distance_metric not in metric_to_function_mapping.keys():
			raise ValueError("invalid distance_metric: {}".format(distance_metric))
		get_distance = metric_to_function_mapping[distance_metric]
		self._distance_metric = distance_metric
		self._get_distance = get_distance

class DistanceMatrixConfiguration(BaseDistanceMatrixConfiguration):

	def __init__(self):
		super().__init__()

	def get_distance_matrix(self, coordinates, distance_metric=None, is_mask_diagonal=False, mask_value=np.nan):
		if distance_metric is not None:
			self.update_distance_metric(
				distance_metric=distance_metric)
		if self.distance_metric is None:
			raise ValueError("distance_metric is not initialized")
		displacement = self.get_displacement(
			coordinates=coordinates)
		distance_matrix = self.get_distance(
			displacement=displacement,
			axis=-1)
		if not isinstance(is_mask_diagonal, bool):
			raise ValueError("invalid type(is_mask_diagonal): {}".format(type(is_mask_diagonal)))
		if is_mask_diagonal:
			distance_matrix = self.get_matrix_with_masked_diagonal(
				mat=distance_matrix,
				mask_value=mask_value)
		return distance_matrix


if __name__ == "__main__":

	dm = DistanceMatrixConfiguration()
	dm.update_distance_metric(
		distance_metric="manhattan",
		# distance_metric="euclidean square",
		# distance_metric="euclidean",
		)
	coordinates = np.arange(
		11,
		dtype=int)
	distance_matrix = dm.get_distance_matrix(
		coordinates=coordinates,
		is_mask_diagonal=True,
		)
	flat_upper_triangle = dm.get_flat_upper_triangle(
		mat=distance_matrix)

	print("\n .. COORDINATES (shape={}):\n{}\n".format(
		coordinates.shape,
		coordinates))
	print("\n .. DISTANCE MATRIX (shape={}):\n{}\n".format(
		distance_matrix.shape,
		distance_matrix))
	print("\n .. FLAT UPPER TRIANGLE (shape={}):\n{}\n".format(
		flat_upper_triangle.shape,
		flat_upper_triangle))

##