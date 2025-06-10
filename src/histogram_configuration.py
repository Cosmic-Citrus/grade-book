import numpy as np


class BaseHistogramConfiguration():

	def __init__(self):
		super().__init__()
		self._distribution_values = None
		self._side_bias = None
		self._number_bins = None
		self._bin_edges = None
		self._bin_widths = None
		self._bin_midpoints = None
		self._bin_counts = None
		self._cumulative_bin_counts = None
		self._is_bins_equivalent_widths = None
		self._is_bin_locations_modified = None

	@property
	def distribution_values(self):
		return self._distribution_values
	
	@property
	def side_bias(self):
		return self._side_bias
	
	@property
	def number_bins(self):
		return self._number_bins
	
	@property
	def bin_edges(self):
		return self._bin_edges
	
	@property
	def bin_widths(self):
		return self._bin_widths
	
	@property
	def bin_midpoints(self):
		return self._bin_midpoints
		
	@property
	def bin_counts(self):
		return self._bin_counts
	
	@property
	def cumulative_bin_counts(self):
		return self._cumulative_bin_counts
	
	@property
	def is_bins_equivalent_widths(self):
		return self._is_bins_equivalent_widths

	@property
	def is_bin_locations_modified(self):
		return self._is_bin_locations_modified

	@staticmethod
	def get_rounded_number(number, base=10, f=None):
		if f is None:
			rounded_number = base * round(number / base)
		else:
			rounded_number = base * int(
				f(number / base))
		return rounded_number

	@staticmethod
	def verify_container_is_flat_numerical_array(container):
		if not isinstance(container, np.ndarray):
			raise ValueError("invalid type(container): {}".format(type(container)))
		if not (np.issubdtype(container.dtype, np.integer) or np.issubdtype(container.dtype, np.floating)):
			raise ValueError("invalid container.dtype: {}".format(container.dtype))
		size_at_shape = len(
			container.shape)
		if size_at_shape != 1:
			raise ValueError("invalid container.shape: {}".format(arr.container))

	def verify_container_is_strictly_positive(self, container):
		modified_container = np.array(
			container)
		self.verify_container_is_flat_numerical_array(
			container=modified_container)
		if np.any(modified_container <= 0):
			raise ValueError("container contains value less than or equal to zero")

	def verify_container_is_increasing(self, container):
		modified_container = np.array(
			container)
		self.verify_container_is_flat_numerical_array(
			container=modified_container)
		consecutive_differences = np.diff(
			modified_container)
		if np.any(consecutive_differences <= 0):
			raise ValueError("container is not increasing")

	def get_up_rounded_number(self, number, base=10):
		rounded_number = self.get_rounded_number(
			number=number,
			base=base,
			f=np.ceil)
		return rounded_number

	def get_down_rounded_number(self, number, base=10):
		rounded_number = self.get_rounded_number(
			number=number,
			base=base,
			f=np.floor)
		return rounded_number

	def get_autocorrected_array(self, values, number_values=None, is_strictly_positive=False, is_increasing=False):
		if not isinstance(is_strictly_positive, bool):
			raise ValueError("invalid type(is_strictly_positive): {}".format(type(is_strictly_positive)))
		if not isinstance(is_increasing, bool):
			raise ValueError("invalid type(is_increasing): {}".format(type(is_increasing)))
		if isinstance(values, (int, float)):
			if not isinstance(number_values, int):
				raise ValueError("invalid type(number_values): {}".format(type(number_values)))
			if number_values <= 0:
				raise ValueError("invalid number_values: {}".format(number_values))
			container = np.array([
				values
					for index_at_value in range(
						number_values)])
		elif isinstance(values, (tuple, list, np.ndarray)):
			if number_values is not None:
				raise ValueError("invalid number_values: {}".format(number_values))
			container = np.array(
				values)
		else:
			raise ValueError("invalid type(values): {}".format(type(values)))
		self.verify_container_is_flat_numerical_array(
			container=container)
		if is_strictly_positive:
			self.verify_container_is_strictly_positive(
				container=container)
		if is_increasing:
			self.verify_container_is_increasing(
				container=container)
		return container

class BaseHistogramBinsConfiguration(BaseHistogramConfiguration):

	def __init__(self):
		super().__init__()

	@staticmethod
	def get_midpoints(bin_edges):
		bin_midpoints = (bin_edges[1:] + bin_edges[:-1]) / 2
		return bin_midpoints

	def get_leftmost_and_rightmost_bin_edges(self, leftmost_edge=None, rightmost_edge=None, round_to_base=None):
		is_modified = False
		if leftmost_edge is None:
			leftmost_edge = np.nanmin(
				self.distribution_values)
		if rightmost_edge is None:
			rightmost_edge = np.nanmax(
				self.distribution_values)
		if not isinstance(leftmost_edge, (int, float)):
			raise ValueError("invalid type(leftmost_edge): {}".format(type(leftmost_edge)))
		if not isinstance(rightmost_edge, (int, float)):
			raise ValueError("invalid type(rightmost_edge): {}".format(type(rightmost_edge)))
		if (round_to_base is not None) and (leftmost_edge != rightmost_edge):
			leftmost_edge = self.get_down_rounded_number(
				leftmost_edge,
				base=round_to_base)
			rightmost_edge = self.get_up_rounded_number(
				rightmost_edge,
				base=round_to_base)
		# if rightmost_edge <= leftmost_edge:
		# 	raise ValueError("leftmost_edge={} is not less than rightmost_edge={}".format(leftmost_edge, rightmost_edge))
		if rightmost_edge < leftmost_edge:
			leftmost_edge, rightmost_edge = rightmost_edge, leftmost_edge
		if leftmost_edge == rightmost_edge:
			if round_to_base is None:
				leftmost_edge -= 1
				rightmost_edge += 1
			else:
				leftmost_edge -= float(
					round_to_base)
				rightmost_edge += float(
					round_to_base)
			is_modified = True
		return leftmost_edge, rightmost_edge, is_modified

	def get_bins_by_number(self, number_bins, leftmost_edge=None, rightmost_edge=None, round_to_base=None):
		modified_leftmost_edge, modified_rightmost_edge, is_modified = self.get_leftmost_and_rightmost_bin_edges(
			leftmost_edge=leftmost_edge,
			rightmost_edge=rightmost_edge,
			round_to_base=round_to_base)
		if is_modified:
			modified_bin_edges = np.array([
				modified_leftmost_edge,
				modified_rightmost_edge])
		else:
			modified_bin_edges = np.linspace(
				modified_leftmost_edge,
				modified_rightmost_edge,
				number_bins)
		return modified_bin_edges

	def get_bins_by_edges(self, bin_edges):
		modified_bin_edges = self.get_autocorrected_array(
			values=bin_edges,
			is_increasing=True)
		return modified_bin_edges

	def get_bins_by_equivalent_width(self, bin_widths, leftmost_edge=None, rightmost_edge=None, round_to_base=None):
		if not isinstance(bin_widths, (int, float)):
			raise ValueError("invalid type(bin_widths): {}".format(type(bin_widths)))
		modified_leftmost_edge, modified_rightmost_edge, is_modified = self.get_leftmost_and_rightmost_bin_edges(
			leftmost_edge=leftmost_edge,
			rightmost_edge=rightmost_edge,
			round_to_base=round_to_base)
		if is_modified:
			modified_bin_edges = np.array([
				modified_leftmost_edge,
				modified_rightmost_edge])
		else:
			modified_bin_edges = np.arange(
				modified_leftmost_edge,
				modified_rightmost_edge + bin_widths,
				bin_widths)
		return modified_bin_edges

	def get_bins_by_midpoints(self, bin_midpoints, bin_widths):
		modified_bin_midpoints = self.get_autocorrected_array(
			values=bin_midpoints,
			is_increasing=True)
		modified_bin_widths = self.get_autocorrected_array(
			values=bin_widths,
			number_values=modified_bin_midpoints.size,
			is_strictly_positive=True)
		leftmost_edge = modified_bin_midpoints[0] - modified_bin_widths[0]
		modified_bin_edges = list()
		modified_bin_edges.append(
			leftmost_edge)
		for midpoint, width in zip(modified_bin_midpoints, modified_bin_widths):
			right_edge = midpoint + width
			modified_bin_edges.append(
				right_edge)
		modified_bin_edges = np.array(
			modified_bin_edges)
		return modified_bin_edges

	def get_bin_counts_by_left_side_bias(self, bin_edges):
		bin_counts, _ = np.histogram(
			self.distribution_values,
			bins=bin_edges)
		return bin_counts

	def get_bin_counts_by_right_side_bias(self, bin_edges):
		bin_counts = np.full(
			fill_value=0,
			shape=bin_edges.size - 1,
			dtype=int)
		count_value_indices, count_values = np.unique(
			np.searchsorted(
				bin_edges,
				self.distribution_values,
				side="left"),
			return_counts=True)
		for index_at_count_value, count_value in zip(count_value_indices, count_values):
			bin_counts[index_at_count_value - 1] = count_value
		return bin_counts

class HistogramBinsConfiguration(BaseHistogramBinsConfiguration):

	def __init__(self):
		super().__init__()

	def initialize_distribution_values(self, distribution_values):
		self.verify_container_is_flat_numerical_array(
			container=distribution_values)
		self._distribution_values = distribution_values

	def initialize_bin_locations(self, bin_selection_method, *args, **kwargs):
		is_bin_locations_modified = False
		mapping_at_bin_selection = {
			"number bins" : self.get_bins_by_number,
			"bin edges" : self.get_bins_by_edges,
			"equivalent bin widths" : self.get_bins_by_equivalent_width,
			"bin midpoints" : self.get_bins_by_midpoints}
		if bin_selection_method not in mapping_at_bin_selection.keys():
			raise ValueError("invalid bin_selection_method: {}".format(bin_selection_method))
		get_bin_edges = mapping_at_bin_selection[bin_selection_method]
		bin_edges = get_bin_edges(
			*args,
			**kwargs)
		number_bins = bin_edges.size - 1
		if number_bins == 0:
			raise ValueError("invalid len(bin_edges): {}".format(bin_edges.size))
			# coordinate_at_singular_edge = bin_edges[0]
			# bin_edges = np.array([
			# 	coordinate_at_singular_edge - 1,
			# 	coordinate_at_singular_edge + 1])
			# number_bins = bin_edges.size - 1
			# is_bin_locations_modified = True
		bin_widths = np.diff(
			bin_edges)
		bin_midpoints = self.get_midpoints(
			bin_edges=bin_edges)
		is_bins_equivalent_widths = np.all(
			bin_widths == bin_widths[0])
		self._number_bins = number_bins
		self._bin_edges = bin_edges
		self._bin_widths = bin_widths
		self._bin_midpoints = bin_midpoints
		self._is_bins_equivalent_widths = is_bins_equivalent_widths
		self._is_bin_locations_modified = is_bin_locations_modified

	def initialize_bin_counts(self, side_bias, bin_counts=None):
		mapping_at_side_bias = {
			"left" : self.get_bin_counts_by_left_side_bias,
			"right" : self.get_bin_counts_by_right_side_bias}
		if side_bias not in mapping_at_side_bias.keys():
			raise ValueError("invalid side_bias: {}".format(side_bias))
		if bin_counts is None:
			get_bin_counts = mapping_at_side_bias[side_bias]
			bin_counts = get_bin_counts(
				bin_edges=self.bin_edges)
		else:
			self.verify_container_is_flat_numerical_array(
				container=bin_counts)
			if self.number_bins != bin_counts.size:
				raise ValueError("{} bins and {} bin-counts are not compatible".format(self.number_bins, bin_counts))
		cumulative_bin_counts = np.cumsum(
			bin_counts)
		self._side_bias = side_bias
		self._bin_counts = bin_counts
		self._cumulative_bin_counts = cumulative_bin_counts

class HistogramConfiguration(HistogramBinsConfiguration):

	def __init__(self):
		super().__init__()

	def initialize_histogram(self, distribution_values, bin_selection_method, *args, side_bias="left", **kwargs):
		self.initialize_distribution_values(
			distribution_values=distribution_values)
		self.initialize_bin_locations(
			bin_selection_method,
			*args,
			**kwargs)
		self.initialize_bin_counts(
			side_bias=side_bias)

	def transform_frequency_data(self, frequency_data, distribution_values=None, side_bias="left"):
		if not isinstance(frequency_data, dict):
			raise ValueError("invalid type(frequency_data): {}".format(type(frequency_data)))
		bin_counts = np.array(
			list(
				frequency_data.values()))
		self.verify_container_is_flat_numerical_array(
			container=bin_counts)
		number_bins = bin_counts.size
		bin_edges = np.arange(
			number_bins + 1,
			dtype=int)
		if distribution_values is not None:
			self.initialize_distribution_values(
				distribution_values=distribution_values)
		self.initialize_bin_locations(
			bin_selection_method="bin edges",
			bin_edges=bin_edges)
		self.initialize_bin_counts(
			side_bias=side_bias,
			bin_counts=bin_counts)

##