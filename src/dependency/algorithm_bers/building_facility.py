from . import tool

import numpy as np
import pandas as pd
import os

__path__ = os.path.dirname(__file__).replace('\\', '/').replace('C:/', '/') + '/'

class Elevator():

	def __init__(self, **kwargs):

		"""
		This method is used to initialize an elevator object.
		===========================================================================================

		Arguments:

			None
		"""

		# Initialize the elevator object
		self.building_type                   = kwargs.get('building_type', None)
		self.elevator_bottom_floor           = kwargs.get('elevator_bottom_floor', None)
		self.elevator_top_floor              = kwargs.get('elevator_top_floor', None)
		self.elevator_floor_offset           = kwargs.get('elevator_floor_offset', 0)
		self.elevator_es 				     = kwargs.get('elevator_es', [])
		self.coef_eff	                     = kwargs.get('coef_eff', 1.0)
		self.coef_people_per_elevator        = kwargs.get('coef_people_per_elevator', None)
		self.coef_load_per_elevator          = kwargs.get('coef_load_per_elevator', None)
		self.coef_speed                      = kwargs.get('coef_speed', None)

		# =========================================================================================
		#
		# Initialize the elevator object
		#
		# =========================================================================================

		# Basic information
		self.elevator_n_stories_total   = self.elevator_top_floor - self.elevator_bottom_floor + self.elevator_floor_offset

		# Coefficient of usage ratio of elevator
		self.coef_usage_r               = self._get_coef_facility_usage_r_elevator()
		self.coef_facility_ec           = self._get_coef_facility_ec_elevator()

		# Energy consumption of elevator
		self.coef_usage_h               = np.nanmax([tool.get_coef_usage_h(i) for i in self.elevator_es])
	
	def _get_coef_facility_usage_r_elevator(self):

		"""
		This method is used to get the coefficient of usage ratio of elevator by building type.
		===========================================================================================
		
		Arguments:

			building_type (str): Building type

		Output:

			coef_usage_r_elevator (float): Coefficient of usage ratio of elevator
		"""

		# Read the file for coefficient of usage ratio of elevator
		df_coef = pd.read_csv(__path__ + '../data/coef_facility/coef_facility_usage_elevator_escalator.csv')

		# Get the coefficient of usage ratio of elevator
		coef_usage_r_elevator  = df_coef.loc[df_coef['Section_ID']==self.building_type, 'Or'].values[0]

		return coef_usage_r_elevator
	
	def _get_coef_facility_ec_elevator(self):

		"""
		This method is used to get the coefficient of EC of elevator by building type.
		===========================================================================================
		
		Arguments:
		
			None

		Output:

			coef_ec_elevator (float): Coefficient of EC of elevator
		"""

		# Read the file for coefficient of EC of elevator
		df_coef = pd.read_csv(__path__ + '../data/coef_facility/coef_facility_ec_elevator.csv')

		# Get the coefficient of EC of elevator
		df_coef = df_coef.loc[\
			(df_coef['Stories_min']<=self.elevator_n_stories_total) &
			(df_coef['Stories_max']>=self.elevator_n_stories_total)
		]

		# Create a key for sorting
		df_coef['key_sorting'] = \
			(np.array(df_coef['n_People'])-self.coef_people_per_elevator)**2 + \
			1e-2*(np.array(df_coef['n_Load'])-self.coef_load_per_elevator)**2 + \
			0.5*(np.array(df_coef['Speed'])-self.coef_speed)**2

		# Get the coefficient of EC of elevator
		coef_ec_elevator = df_coef.loc[df_coef['key_sorting']==df_coef['key_sorting'].min(), 'FLE'].values[0]

		return coef_ec_elevator

class Escalator():

	def __init__(self, **kwargs):

		"""
		This method is used to initialize an escalator object.
		===========================================================================================

		Arguments:

			None
		"""

		# Initialize the escalator object
		self.building_type                   = kwargs.get('building_type', None)
		self.escalator_elevate_height        = kwargs.get('escalator_elevate_height', None)
		self.escalator_width                 = kwargs.get('escalator_width', None)
		self.escalator_es                    = kwargs.get('escalator_es', [])
		self.coef_eff	                     = kwargs.get('coef_eff', 1.0)
		self.coef_people_per_escalator       = kwargs.get('coef_people_per_escalator', None)
		self.coef_load_per_escalator         = kwargs.get('coef_load_per_escalator', None)
		self.coef_speed                      = kwargs.get('coef_speed', None)

		# =========================================================================================
		#
		# Initialize the escalator object
		#
		# =========================================================================================

		# Basic information
		self.escalator_n_stories_total  = self.escalator_top_floor - self.escalator_bottom_floor + self.escalator_floor_offset

		# Coefficient of usage ratio of escalator
		self.coef_usage_r               = self._get_coef_facility_usage_r_escalator()
		self.coef_facility_power        = self._get_coef_facility_power_escalator()

		# Energy consumption of escalator
		self.coef_usage_h               = np.nanmax([tool.get_coef_usage_h(i) for i in self.escalator_es])

	def _get_coef_facility_usage_r_escalator(self):

		"""
		This method is used to get the coefficient of usage ratio of escalator by building type.
		===========================================================================================
		
		Arguments:

			building_type (str): Building type

		Output:

			coef_usage_r_escalator (float): Coefficient of usage ratio of escalator
		"""

		# Read the file for coefficient of usage ratio of scalator
		df_coef = pd.read_csv(__path__ + '../data/coef_facility/coef_facility_usage_elevator_escalator.csv')

		# Get the coefficient of usage ratio of escalator
		coef_usage_r_escalator = df_coef.loc[df_coef['Section_ID']==self.building_type, 'Osr'].values[0]

		return coef_usage_r_escalator
	
	def _get_coef_facility_power_escalator(self):

		"""
		This method is used to get the coefficient of power of escalator by building type.
		===========================================================================================
		
		Arguments:
		
			None

		Output:

			coef_ec_escalator (float): Coefficient of power of escalator
		"""

		# Read the file for coefficient of EC of escalator
		df_coef = pd.read_csv(__path__ + '../data/coef_facility/coef_facility_power_escalator.csv')

		# Get the coefficient of EC of escalator
		df_coef = df_coef.loc[\
			(df_coef['Elevate_min']<=self.escalator_elevate_height)&\
			(df_coef['Elevate_max']>self.escalator_elevate_height)
		]

		# Create a key for sorting
		df_coef['key_sorting'] = (np.array(df_coef['Width'])-self.escalator_width)

		# Get the coefficient of power of escalator
		coef_ec_escalator = df_coef.loc[df_coef['key_sorting']==df_coef['key_sorting'].min(), 'Power'].values[0]

		return coef_ec_escalator

class Hotel():

	def __init__(self, **kwargs):

		# Initialize the hotel object
		self.building_type                   = kwargs.get('building_type', None)
		self.n_room                          = kwargs.get('n_room', 0)
		self.coef_usage_r_room               = kwargs.get('coef_usage_room', 1)

class Hospital():

	def __init__(self, **kwargs):

		# Initialize the hospital object
		self.building_type                   = kwargs.get('building_type', None)
		self.n_hospitalbed                   = kwargs.get('n_hospitalbed', 0)
		self.coef_usage_r_hospitalbed        = kwargs.get('coef_usage_hospitalbed', 1)

class SportBathroom():
	
	def __init__(self, **kwargs):
		
		# Initialize the sport bathroom object
		self.building_type                   = kwargs.get('building_type', None)
		self.ec_heating                      = kwargs.get('ec_heating', 'BHPE')
		self.a                               = kwargs.get('a', 0)
		self.coef_usage_h                    = kwargs.get('coef_usage_h', tool.get_coef_usage_h('L3'))

		# =========================================================================================
		# Get the ec of heating
		if (self.ec_heating == 'BHPE'): self.ec_heating = 6.5
		else: self.ec_heating = 0.0
	
class SwimmingPool():

	def __init__(self, **kwargs):

		# Initialize the swimming pool object
		self.building_type                   = kwargs.get('building_type', None)
		self.building_cz                     = kwargs.get('building_cz', None)
		self.ec_heating                      = kwargs.get('ec_heating', 'BHPE')
		self.v                               = kwargs.get('v', 0)
		self.coef_usage_h                    = kwargs.get('coef_usage_h', tool.get_coef_usage_h('L6-2'))
		self.height_watertower               = kwargs.get('height_watertower', 30)
		self.constant_temperature            = kwargs.get('constant_temperature', True)
		
		# =========================================================================================
		# Get the days of hot water usage
		self.coef_usage_d_hotwater           = self._get_coef_usage_d_hotwater()
		
		# Get the ec of heating
		if (self.ec_heating == 'BHPE'): self.ec_heating = 6.5
		else: self.ec_heating = 0.0

	def _get_coef_usage_d_hotwater(self):

		"""
		This method is used to get the day of hot water usage for swimming pool
		===========================================================================================
		
		Arguments:

			None
		
		Output:

			coef_usage_d_hotwater (float): Day of hot water usage for swimming pool
		"""

		# Get day of hot water usage based on whether the swimming pool is constant temperature throughout the year or not
		if (self.constant_temperature):
			
			coef_usage_d_hotwater = 365
		
		else:
			
			if (self.building_cz == 'N'):

				coef_usage_d_hotwater = 181

			elif (self.building_cz == 'C'):

				coef_usage_d_hotwater = 151

			elif (self.building_cz == 'S'):

				coef_usage_d_hotwater = 121

		return coef_usage_d_hotwater

class Spa():

	def __init__(self, **kwargs):

		# Initialize the SPA object
		self.building_type                   = kwargs.get('building_type', None)
		self.building_cz                     = kwargs.get('building_cz', None)
		self.ec_heating                      = kwargs.get('ec_heating', 'BHPE')
		self.v                               = kwargs.get('v', 0)
		self.coef_usage_h                    = kwargs.get('coef_usage_h', tool.get_coef_usage_h('L6-2'))
		self.height_watertower               = kwargs.get('height_watertower', 30)
		self.constant_temperature            = kwargs.get('constant_temperature', True)

		# =========================================================================================
		# Get the days of hot water usage
		self.coef_usage_d_hotwater           = self._get_coef_usage_d_hotwater()
		
		# Get the ec of heating
		if (self.ec_heating == 'BHPE'): self.ec_heating = 6.5
		else: self.ec_heating = 0.0

	def _get_coef_usage_d_hotwater(self):

		"""
		This method is used to get the day of hot water usage for spa
		===========================================================================================
		
		Arguments:

			None
		
		Output:

			coef_usage_d_hotwater (float): Day of hot water usage for spa
		"""

		# Get day of hot water usage based on whether the spa is constant temperature throughout the year or not
		if (self.constant_temperature):
			
			coef_usage_d_hotwater = 365
		
		else:
			
			if (self.building_cz == 'N'):

				coef_usage_d_hotwater = 181

			elif (self.building_cz == 'C'):

				coef_usage_d_hotwater = 151

			elif (self.building_cz == 'S'):

				coef_usage_d_hotwater = 121

		return coef_usage_d_hotwater

class DiningArea():

	def __init__(self, **kwargs):

		# Initialize the dining area object
		self.building_type                   = kwargs.get('building_type', None)
		self.a                               = kwargs.get('a', 0)
		self.n_meal_per_day                  = kwargs.get('n_meal_per_day', 2)
		self.washdishes_by_hand              = kwargs.get('washdishes_by_hand', False)
		self.coef_usage_d                    = kwargs.get('coef_usage_d', self._get_coef_usage_d())

		# =========================================================================================
		# Get the hot water usage intensity
		self.coef_usage_i_hotwater           = self._get_coef_usage_i_hotwater()

	def _get_coef_usage_i_hotwater(self):

		"""
		This method is used to get Wh (hot water usage intensity) [m3 / (m2 * day)].
		===========================================================================================

		Arguments:

			None
		
		Output:

			coef_usage_i_hotwater (float): Wh hot water usage intensity [m3 / (m2 * day)]
		"""

		# Get the hot water usage intensity based on the number of meal per day
		if (self.n_meal_per_day == 1): coef_usage_i_hotwater = 0.00284
		elif (self.n_meal_per_day == 2): coef_usage_i_hotwater = 0.00568
		elif (self.n_meal_per_day == 3): coef_usage_i_hotwater = 0.00852
		elif (self.n_meal_per_day == 4): coef_usage_i_hotwater = 0.02840

		# Multiply the hot water usage intensity by 0.283 if the dishes are washed by hand
		if (self.washdishes_by_hand): coef_usage_i_hotwater *= 0.283

		return coef_usage_i_hotwater
	
	def _get_coef_usage_d(self):

		"""
		This method is used to get the coefficient of usage ratio of dining area
		===========================================================================================
		
		Arguments:

			None
		
		Output:

			coef_usage_d (float): Coefficient of usage ratio of dining area
		"""

		# Get the coefficient of usage ratio based on the number of meal per day
		if (self.n_meal_per_day == 1): coef_usage_d = tool.get_coef_usage_d('I1')
		elif (self.n_meal_per_day == 2): coef_usage_d = tool.get_coef_usage_d('I2')
		elif (self.n_meal_per_day == 3): coef_usage_d = tool.get_coef_usage_d('I3')
		elif (self.n_meal_per_day == 4): coef_usage_d = tool.get_coef_usage_d('I5')

		return coef_usage_d

class ExhibitionArea():

	def __init__(self, **kwargs):

		# Initialize the exhibition area object
		self.building_type                   = kwargs.get('building_type', None)
		self.a                               = kwargs.get('a', 0)
		self.coef_usage_d                    = kwargs.get('coef_usage_d', tool.get_coef_usage_d('D1'))

class PerformanceArea():

	def __init__(self, **kwargs):

		# Initialize the performance area object
		self.building_type                   = kwargs.get('building_type', None)
		self.a                               = kwargs.get('a', 0)
		self.coef_usage_d                    = kwargs.get('coef_usage_d', tool.get_coef_usage_d('F1'))