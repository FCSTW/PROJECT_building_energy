import numpy as np
import pandas as pd
import os
from typing import Union
from . import tool
from . import constant

__path__ = os.path.dirname(__file__).replace('\\', '/').replace('C:/', '/') + '/'

class Elevator:

	def __init__(self, **kwargs):

		"""
		This method is used to initialize an elevator object.
		===========================================================================================

		Arguments:

			None
		"""

		# Get the arguments
		self.building_class                  = kwargs.get('building_class', None)
		self.building_type                   = kwargs.get('building_type', None)
		self.elevator_bottom_floor           = kwargs.get('elevator_bottom_floor', None)
		self.elevator_top_floor              = kwargs.get('elevator_top_floor', None)
		self.elevator_floor_offset           = kwargs.get('elevator_floor_offset', 0)
		self.coef_people_per_elevator        = kwargs.get('coef_people_per_elevator', None)
		self.coef_load_per_elevator          = kwargs.get('coef_load_per_elevator', None)
		self.coef_speed                      = kwargs.get('coef_speed', None)
		self.coef_eff	                     = kwargs.get('coef_eff', 1.0)

		if (self.building_class == 'general'):
			# If the building class is general, then collect the following arguments

			self.elevator_type                   = kwargs.get('elevator_type', 'common')
			self.elevator_es 				     = kwargs.get('elevator_es', [])
		
		elif (self.building_class == 'residential'):
			# If the building class is residential, then collect the following arguments

			pass
			# No more arguments are needed now

		else:

			raise ValueError('The building class ({}) is not defined for elevator.'.format(self.building_class))
		
		# =========================================================================================
		#
		# Initialize the elevator object
		#
		# =========================================================================================

		# Basic information: building class
		if (self.building_class is None):

			raise ValueError('The building class is not set.')
		
		# Basic information: building floor
		if (self.elevator_top_floor > 0) and (self.elevator_bottom_floor < 0):

			self.elevator_n_stories_total = self.elevator_top_floor - self.elevator_bottom_floor - 1

		elif ((self.elevator_top_floor > 0) and (self.elevator_bottom_floor > 0)) or \
			 ((self.elevator_top_floor < 0) and (self.elevator_bottom_floor < 0)):
			
			self.elevator_n_stories_total = self.elevator_top_floor - self.elevator_bottom_floor

		else:

			raise ValueError('The elevator bottom floor ({}) and top floor ({}) are not set correctly.'.format(self.elevator_bottom_floor, self.elevator_top_floor))
		
		self.elevator_n_stories_total  += self.elevator_floor_offset

		# Coefficient of usage ratio of elevator
		self.coef_usage_r               = self._get_coef_usage_r_elevator()
		self.coef_ec                    = self._get_coef_ec_elevator()

		# Energy consumption of elevator
		self.coef_usage_h               = self._get_coef_usage_h_elevator()
	
	def _get_coef_usage_r_elevator(self) -> float:

		"""
		This method is used to get the coefficient of usage ratio of elevator by building class and building type.
		===========================================================================================
		
		Arguments:

			building_type (str): Building type

		Output:

			coef_usage_r_elevator (float): Coefficient of usage ratio of elevator
		"""

		if (self.building_class == 'general'):

			# Read the file for coefficient of usage ratio of elevator
			df_coef = pd.read_csv(__path__ + '../data/coef_facility/coef_facility_usage_elevator_escalator.csv')

			# Get the coefficient of usage ratio of elevator
			coef_usage_r_elevator  = df_coef.loc[df_coef['Section_ID']==self.building_type, 'Or'].values[0]

		elif (self.building_class == 'residential'):

			coef_usage_r_elevator = None

		return coef_usage_r_elevator
	
	def _get_coef_ec_elevator(self) -> float:

		"""
		This method is used to get the coefficient of EC of elevator by building type.
		===========================================================================================
		
		Arguments:
		
			None

		Output:

			coef_ec_elevator (float): Coefficient of EC of elevator (FLE)
		"""

		if (self.building_class == 'general'):

			if (self.elevator_type == 'common'):

				# Read the file for coefficient of EC of elevator
				df_coef = pd.read_csv(__path__ + '../data/coef_facility/coef_facility_ec_elevator.csv')

				# Filter the range of stories
				df_coef = df_coef.loc[\
					(df_coef['Stories_min']<=self.elevator_n_stories_total) &
					(df_coef['Stories_max']>=self.elevator_n_stories_total)
				]

				# Create a key for sorting
				df_coef['key_sorting'] = \
					(np.array(df_coef['n_People'])-self.coef_people_per_elevator)**2 + \
					1e-2*(np.array(df_coef['n_Load'])-self.coef_load_per_elevator)**2 + \
					0.5*(np.array(df_coef['Speed'])-self.coef_speed)**2
			
			elif (self.elevator_type == 'freight'):

				# Read the file for coefficient of EC of elevator
				df_coef = pd.read_csv(__path__ + '../data/coef_facility/coef_facility_ec_elevator_industrial.csv')

				# Create a key for sorting
				df_coef['key_sorting'] = \
					1e-2*(np.array(df_coef['n_Load'])-self.coef_load_per_elevator)**2 + \
					0.5*(np.array(df_coef['Speed'])-self.coef_speed)**2
			
			else:

				raise ValueError('The elevator type is not supported.')

			# Get the coefficient of EC of elevator
			coef_ec_elevator = df_coef.loc[df_coef['key_sorting']==df_coef['key_sorting'].min(), 'FLE'].values[0]

		elif (self.building_class == 'residential'):

			# Read the file for coefficient of EC of elevator
			df_coef = pd.read_csv(__path__ + '../data/coef_facility_residential/coef_facility_ec_elevator.csv')

			# Filter the range of stories
			df_coef = df_coef.loc[\
				(df_coef['Stories_min']<=self.elevator_n_stories_total) &
				(df_coef['Stories_max']>=self.elevator_n_stories_total) &
				(df_coef['Building_Type']>=self.building_type)
			]

			# Create a key for sorting
			df_coef['key_sorting'] = \
				(np.array(df_coef['n_People'])-self.coef_people_per_elevator)**2 + \
				1e-2*(np.array(df_coef['n_Load'])-self.coef_load_per_elevator)**2 + \
				0.5*(np.array(df_coef['Speed'])-self.coef_speed)**2
			
			# Get the coefficient of EC of elevator
			coef_ec_elevator = df_coef.loc[df_coef['key_sorting']==df_coef['key_sorting'].min(), 'FLE'].values[0]

		return coef_ec_elevator

	def _get_coef_usage_h_elevator(self):

		"""
		This method is used to get YOH (operation hours per year) of elevator by building class and building type.
		===========================================================================================
		
		Arguments:

			None

		Output:

			coef_usage_h_elevator (float): Coefficient of usage ratio of elevator
		"""

		if (self.building_class == 'general'):

			# Get the coefficient of usage ratio of elevator by finding the maximum value of YOH of all energy sections that elevator goes through
			coef_usage_h = np.nanmax([tool.get_coef_usage_h(i) for i in self.elevator_es])
		
		elif (self.building_class == 'residential'):

			# Set default value
			coef_usage_h = 0.2 * 8760
		
		return coef_usage_h

class Escalator:

	def __init__(self, **kwargs):

		"""
		This method is used to initialize an escalator object.
		===========================================================================================

		Arguments:

			None
		"""

		# Get the arguments
		self.building_type                   = kwargs.get('building_type', None)
		self.escalator_elevate_height        = kwargs.get('escalator_elevate_height', None)
		self.escalator_width                 = kwargs.get('escalator_width', None)
		self.escalator_es                    = kwargs.get('escalator_es', [])
		self.coef_eff	                     = kwargs.get('coef_eff', 1.0)

		# =========================================================================================
		#
		# Initialize the escalator object
		#
		# =========================================================================================

		# Coefficient of usage ratio of escalator
		self.coef_usage_r               = self._get_coef_usage_r_escalator()
		self.coef_power                 = self._get_coef_power_escalator()

		# Energy consumption of escalator
		self.coef_usage_h               = np.nanmax([tool.get_coef_usage_h(i) for i in self.escalator_es])

	def _get_coef_usage_r_escalator(self):

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
	
	def _get_coef_power_escalator(self):

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

class WaterTower:

	def __init__(self, **kwargs):

		"""
		This method is used to initialize a water tower object.
		
		                            -- water tower  ->      <||>                              -- 
		                            |                     ||===============||                  |  
		                            |                     || [ ]  [ ]  [ ] ||                  |  
		                            |                     ||               ||                  |  
		                            |                     || [ ]  [ ]  [ ] ||                  |  
		[static hydraulic head] ->  |                     ||               ||                  |  <- [height]
		                            |                     || [ ]  [ ]  [ ] ||                  |  
		                            |                     ||               ||                  |  
		                            |                     ||      /-\      ||                  |  
		                            |              -------||======| |======||-----     ground --  
		                            -- pump         ->     {o}
		
		Total hydraulic head = static hydraulic head + friction hydraulic head
								 (potential energy)        (friction energy)
		
		===========================================================================================

		Arguments:

			None
		"""

		# Get the arguments
		self.estimation_system               = kwargs.get('estimation_system', None)
		self.building_address_county         = kwargs.get('building_address_county', None)

		if (self.estimation_system == 'BERSe'):
			# In case of BERSe
			# Static hydraulic head: equal to the water tower height + 6m
			# Friction hydraulic head: unavailable. the effect is adjusted by the power intensity of the pump (0.0183 * 1.1 = 0.2)
			# When calculate average hydraulic head, the volumes (v) will be used as weights

			if (kwargs.get('height', None) == None): raise ValueError('The height of water tower is required for BERSe estimation system')

			self.height                           = kwargs.get('height', None)
			self.v                                = kwargs.get('v', 1)
			self.standard_hydraulic_head_static   = self.height + 6
			self.standard_hydraulic_head_friction = 0
		
		elif (self.estimation_system == 'R-BERS'):
			# In case of R-BERS
			# Static hydraulic head and friction hydraulic head are both needed. If the friction hydraulic head is unavailable, it will be estimated by the static hydraulic head
			# When calculate average hydraulic head, the water pumping capacity (water_pumping_capacity) will be used as weights

			if (kwargs.get('standard_hydraulic_head_static', None) == None): raise ValueError('The standard hydraulic head static of water tower is required for R-BERS estimation system')

			self.water_pumping_capacity           = kwargs.get('water_pumping_capacity', None)
			self.standard_hydraulic_head_static   = kwargs.get('standard_hydraulic_head_static', None)
			self.standard_hydraulic_head_friction = kwargs.get('standard_hydraulic_head_friction', self.standard_hydraulic_head_static * 0.1)
		
		# Set the standard and actual hydraulic head
		self.standard_hydraulic_head_total   = self.standard_hydraulic_head_static + self.standard_hydraulic_head_friction
		self.hydraulic_head_total            = kwargs.get('hydraulic_head_total', self.standard_hydraulic_head_total * 1.05)

class Hotel:

	"""
	This class is used in existing building in BERSe.
	"""

	def __init__(self, **kwargs):

		# Get the arguments
		self.building_type                   = kwargs.get('building_type', None)
		self.n_room                          = kwargs.get('n_room', 0)
		self.coef_usage_r_room               = kwargs.get('coef_usage_r_room', 1)

class Hospital:

	"""
	This class is used in existing building in BERSe.
	"""

	def __init__(self, **kwargs):

		# Get the arguments
		self.building_type                   = kwargs.get('building_type', None)
		self.n_hospitalbed                   = kwargs.get('n_hospitalbed', 0)
		self.coef_usage_r_hospitalbed        = kwargs.get('coef_usage_r_hospitalbed', 1)

class SportBathroom:
	
	"""
	This class is used in existing building in BERSe.
	"""

	def __init__(self, **kwargs):
		
		# Get the arguments
		self.building_type                   = kwargs.get('building_type', None)
		self.a                               = kwargs.get('a', 0)
		self.coef_usage_h                    = kwargs.get('coef_usage_h', tool.get_coef_usage_h('L3'))
	
class SwimmingPool:

	"""
	This class is used in existing building in BERSe.
	"""

	def __init__(self, **kwargs):

		# Get the arguments
		self.building_type                   = kwargs.get('building_type', None)
		self.building_cz                     = kwargs.get('building_cz', None)
		self.ec_heating                      = kwargs.get('ec_heating', 'BHPE')
		self.v                               = kwargs.get('v', 0)
		self.coef_usage_h                    = kwargs.get('coef_usage_h', tool.get_coef_usage_h('L6-2'))
		self.height_watertower               = kwargs.get('height_watertower', 30)
		self.constant_temperature            = kwargs.get('constant_temperature', True)
		
		# =========================================================================================
		#
		# Initialize the swimming pool object
		#
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

class Spa:

	"""
	This class is used in existing building in BERSe.
	"""

	def __init__(self, **kwargs):

		# Get the arguments
		self.building_type                   = kwargs.get('building_type', None)
		self.building_cz                     = kwargs.get('building_cz', None)
		self.ec_heating                      = kwargs.get('ec_heating', 'BHPE')
		self.v                               = kwargs.get('v', 0)
		self.coef_usage_h                    = kwargs.get('coef_usage_h', tool.get_coef_usage_h('L6-2'))
		self.height_watertower               = kwargs.get('height_watertower', 30)
		self.constant_temperature            = kwargs.get('constant_temperature', True)

		# =========================================================================================
		#
		# Initialize the spa object
		#
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

class DiningArea:

	"""
	This class is used in existing building in BERSe.
	"""

	def __init__(self, **kwargs):

		# Initialize the dining area object
		self.building_type                   = kwargs.get('building_type', None)
		self.a                               = kwargs.get('a', 0)
		self.n_meal_per_day                  = kwargs.get('n_meal_per_day', 2)
		self.washdishes_by_hand              = kwargs.get('washdishes_by_hand', False)
		self.coef_usage_d                    = kwargs.get('coef_usage_d', self._get_coef_usage_d())

		# =========================================================================================
		#
		# Initialize the dining area object
		#
		# =========================================================================================

		# Convert washdishes_by_hand to boolean
		if (self.washdishes_by_hand == 'True'): self.washdishes_by_hand = True
		else: self.washdishes_by_hand = False

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

class ExhibitionArea:

	"""
	This class is used in existing building in BERSe.
	"""

	def __init__(self, **kwargs):

		# Initialize the exhibition area object
		self.building_type                   = kwargs.get('building_type', None)
		self.a                               = kwargs.get('a', 0)
		self.coef_usage_d                    = kwargs.get('coef_usage_d', tool.get_coef_usage_d('D1'))

class PerformanceArea:

	"""
	This class is used in existing building in BERSe.
	"""

	def __init__(self, **kwargs):

		# Initialize the performance area object
		self.building_type                   = kwargs.get('building_type', None)
		self.a                               = kwargs.get('a', 0)
		self.coef_usage_d                    = kwargs.get('coef_usage_d', tool.get_coef_usage_d('F1'))

class DataCenter:

	"""
	This class is used in existing building in BERSe (for only exclusive energy section).
	"""

	def __init__(self, **kwargs):

		# Initialize the data center object
		self.building_type                   = kwargs.get('building_type', None)
		self.a                               = kwargs.get('a', 0)
		self.coef_power_cabinetrack          = kwargs.get('coef_power_cabinetrack', 3)

class Heater:

	"""
	This class is used in new residential building in R-BERS.
	"""

	def __init__(self, type: str, energy_rating: str = 'none', quantity: int = 1, **kwargs):

		"""
		Arguments:

			type (str): Type of heater.

				- 1: Gas water heater

				- 2.1: Electric (storage) water heater

				- 2.2: Electric (terminal storage) water heater

				- 2.3: Electric (heat pump) water heater

				- 3: Gas stove

				- 4.1: Induction heating stove

				- 4.2: Halogen or ceramic heating stove
			
			energy_rating (str["1", "2", "3", "4", "5", "no"]): Energy rating of heater.

			quantity (int): Quantity of heater.
		"""

		# Get the arguments
		self.type                            = type
		self.energy_rating                   = energy_rating
		self.quantity                        = quantity

		# =========================================================================================
		#
		# Initialize the heater object
		#
		# =========================================================================================

		# Check type
		if (self.type not in ['1', '2.1', '2.2', '2.3', '3', '4.1', '4.2']):

			raise ValueError('Invalid type of heater. Please set the type of heater correctly.')
				
		# Get the coefficient of efficiency
		self.coef_eff                        = self._get_coef_eff_heater()
		
		# Get the coefficient of emission intensity
		self.coef_emission_intensity         = self._get_coef_emission_intensity_heater()

		# =========================================================================================
		#
		# Hotwater pipeline attributes
		#
		# =========================================================================================

		if (self.type in ['1', '2.1', '2.2', '2.3']):
			
			# Hotwater pipeline thermal conductivity
			self.coef_pipe_thermal_conductivity         = kwargs.get('coef_pipe_thermal_conductivity', 4.5)

			# Hotwater pipeline energy saving efficiency
			self.coef_eff_powersaving_hotwater_pipeline = self._get_coef_eff_powersaving_hotwater_pipeline()

	def _get_coef_eff_heater(self) -> float:

		"""
		This method is used to get the coefficient of efficiency of heater.
		===========================================================================================

		Arguments:

			None

		Output:

			coef_eff (float): Coefficient of efficiency of heater
		"""

		# Read the file for coefficient of efficiency of heater
		df_coef = pd.read_csv(__path__ + '../data/coef_facility_residential/coef_facility_heater.csv', dtype={'Facility_Type': str})

		# Set the column name based on the energy rating
		if (self.energy_rating in ['1', '2', '3', '4', '5']):
			
			column_name = 'Em_{}'.format(self.energy_rating)

		elif (self.energy_rating == 'no'):

			column_name = 'Em_none'

		else:

			raise ValueError('Invalid energy rating. If the energy rating is not available, please set it to "no".')
		
		# Get the coefficient of efficiency of heater
		coef_eff_heater = df_coef.loc[(df_coef['Facility_Type'].astype(str)==self.type), column_name].values[0]

		return coef_eff_heater
	
	def _get_coef_emission_intensity_heater(self) -> float:

		"""
		This method is used to get the coefficient of emission intensity of heater.

		The coefficient of emission intensity of heater is calculated as follows:
		             kWh
		coef = ----------------
		        person * year
		===========================================================================================

		Arguments:

			None

		Output:

			coef_emission_intensity_heater (float): Coefficient of emission intensity of heater
		"""

		# Read the file for coefficient of emission intensity of heater
		df_coef = pd.read_csv(__path__ + '../data/coef_facility_residential/coef_facility_heater.csv', dtype={'Facility_Type': str})

		# Get the coefficient of emission intensity of heater (YCE * Multiplier)
		coef_yce        = df_coef.loc[(df_coef['Facility_Type']==self.type), 'YCE'].values[0]
		coef_multiplier = df_coef.loc[(df_coef['Facility_Type']==self.type), 'YCE_Multiplier'].values[0]
		coef_emission_intensity_heater = coef_yce * getattr(constant, coef_multiplier)

		return coef_emission_intensity_heater

	def _get_coef_eff_powersaving_hotwater_pipeline(self) -> float:

		"""
		This method is used to get the coefficient of power saving efficiency of hot water pipeline.
		===========================================================================================

		Arguments:

			None

		Output:

			coef_eff_powersaving_hotwater_pipeline (float): The coefficient of power saving efficiency of hot water pipeline.
		"""

		# The coefficient of efficiency of hot water pipeline
		if (self.coef_pipe_thermal_conductivity < 4.1):

			coef_eff_powersaving_hotwater_pipeline = 0.97

		else:

			coef_eff_powersaving_hotwater_pipeline = 1

		return coef_eff_powersaving_hotwater_pipeline
	
class ParkingGarage:

	"""
	This class is used in new residential building in R-BERS.
	Only underground parking garage is considered.
	"""

	def __init__(self, a: float, floor: int, **kwargs):

		"""
		Arguments:

			a (float): Area of parking garage (m2).

			floor (int): The floor of parking garage.
		"""

		# Initialize the parking garage object
		self.a                               = a
		self.floor                           = floor
		self.energy_rating                   = kwargs.get('energy_rating', False)
		self.co2_variable_frequency          = kwargs.get('co2_variable_frequency', False)

		# =========================================================================================
		#
		# Initialize the parking garage object
		#
		# =========================================================================================

		# Get the ec of ventilation in underground parking garage
		self.ec_ventilation                   = self._get_ec_ventilation()

		# Get the 
		self.coef_eff_powersaving_ventilation = self._get_coef_eff_powersaving_ventilation()
	
	def _get_ec_ventilation(self) -> float:

		"""
		This method is used to get the ec of ventilation in underground parking garage.
		===========================================================================================

		Arguments:

			None

		Output:

			ec_ventilation (float): The ec of ventilation in underground parking garage
		"""

		# Read the file for ec of ventilation in underground parking garage
		df_coef = pd.read_csv(__path__ + '../data/coef_facility_residential/coef_facility_ec_ventilation_parking.csv')

		# Get the ec of ventilation in underground parking garage
		ec_ventilation = df_coef.loc[(df_coef['Stories_min']<=self.floor)&(df_coef['Stories_max']>=self.floor), 'VEc'].values[0]

		return ec_ventilation
	
	def _get_coef_eff_powersaving_ventilation(self) -> float:

		"""
		This method is used to get the coefficient of power saving efficiency of ventilation in underground parking garage.
		===========================================================================================

		Arguments:

			None

		Output:

			coef_eff_powersaving_ventilation (float): The coefficient of power saving efficiency of ventilation in underground parking garage.
		"""

		# The coefficient of efficiency of ventilation in underground parking garage
		if (self.co2_variable_frequency):

			coef_eff_powersaving_ventilation = 0.70

		elif (self.energy_rating):

			coef_eff_powersaving_ventilation = 0.80

		else:

			coef_eff_powersaving_ventilation = 1

		return coef_eff_powersaving_ventilation