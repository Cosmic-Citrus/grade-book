from plotter_configuration import GradeBookPlotterConfiguration


class BaseGradeBookEmailConfiguration(GradeBookPlotterConfiguration):

	def __init__(self):
		super().__init__()


class GradeBookEmailConfiguration(BaseGradeBookEmailConfiguration):

	def __init__(self):
		super().__init__()

	def initialize_email_functionality(self, ):
		...

##