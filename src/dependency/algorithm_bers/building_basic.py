"""
Abbreviation:
 - a: Area
 - coef: Coefficient
 - eff: Efficiency
 - es: Energy Section
 - n: Number
 - ec: Energy Consumption
 - wc: Water Consumption
"""

from . import building_facility
from . import read_eui_criteria
from . import constant
from . import tool

import numpy as np
import pandas as pd
import geopandas as gpd
import os

__path__ = os.path.dirname(__file__).replace('\\', '/').replace('C:/', '/') + '/'

class EnergySection():

	"""
	This class is used to create an energy section object for building object in BERSe and R-BERS.
	"""

	def __init__(self, **kwargs):
		
		# Add all key-value pairs to the object attribute
		for key, value in kwargs.items():

			setattr(self, key, value)

class ExclusiveEnergySection():

	"""
	This class is used to create an energy section object for building object in BERSe.
	"""

	def __init__(self, **kwargs):

		# Add all key-value pairs to the object attribute
		for key, value in kwargs.items():

			setattr(self, key, value)

class NonResidentialEnergySection():

	"""
	This class is used to create an energy section object for building object in R-BERS.
	"""

	def __init__(self, nonresidential_energy_section_type: str, **kwargs):


		"""
		This method is used to initialize a building object.
		===========================================================================================

		Arguments:

			nonresidential_energy_section_type (str): The type of non-residential energy section. It can be one of the following:

				- office

				- bank

				- government agency

				- hospital-advanced

				- hospital-intermediate

				- hospital-general

				- temple

				- church

				- theater

				- cinema

				- mall

				- retail store

				- restaurant

				- town house

				- house

				- apartment

				- dormitory

				- hotel

				- junior high school

				- elementary school

				- senior high school

				- university

				- graduate school

				- library

				- factory
				
		Output:

			None
		"""

		# Add all key-value pairs to the object attribute
		for key, value in kwargs.items():

			setattr(self, key, value)
		
		self.nonresidential_energy_section_type = nonresidential_energy_section_type
		self.a                                  = kwargs.get('a', 0)

		# =========================================================================================
		#
		# Initialize the non-residential energy section object
		#
		# =========================================================================================

		# Get water consumption coefficients
		self.coef_effective_a, self.coef_people_density, self.coef_water_density = self._calc_water_consumption_coef()

	def _calc_water_consumption_coef(self) -> tuple:

		"""
		This method is used to calculate the water consumption coefficients.
		===========================================================================================

		Arguments:

			None

		Output:

			coef_effective_a (float): The coefficient of effective area.

			coef_people_density (float): The coefficient of people density.

			coef_water_density (float): The coefficient of water density.
		"""
		
		# Read the file for water consumption coefficients
		df_coef = pd.read_csv(__path__ + 'data/water_consumption_coef.csv', index_col = 0)
		df_coef = df_coef[df_coef['Section_Type']==self.nonresidential_energy_section_type]

		# Fill the missing values with default values
		df_coef['Coef_Effective_Area'] = df_coef['Coef_Effective_Area'].fillna(50)
		df_coef['Coef_People_Density'] = df_coef['Coef_People_Density'].fillna(0.2)
		df_coef['Qdp']                 = df_coef['Qdp'].fillna(0.1)

		# Get the water consumption coefficients
		coef_effective_a    = df_coef.loc['Coef_Effective_Area'].values[0] / 100
		coef_people_density = df_coef.loc['Coef_People_Density'].values[0]
		coef_water_density  = df_coef.loc['Qdp'].values[0]

		return coef_effective_a, coef_people_density, coef_water_density

class Building():

	def __init__(self, **kwargs):
		
		# Add all key-value pairs to the object attribute
		for key, value in kwargs.items(): setattr(self, key, value)

		# =========================================================================================
		# Energy section information
		# Common energy section information
		self.energy_section                  = kwargs.get('energy_section', [])
		self.n_energy_section                = len(self.energy_section)

		# Exclusive energy section information
		self.exclusive_energy_section        = kwargs.get('exclusive_energy_section', [])
		self.n_exclusive_energy_section      = len(self.exclusive_energy_section)

		# Non-residential energy section information
		self.nonresidential_energy_section   = kwargs.get('nonresidential_energy_section', [])
		self.n_nonresidential_energy_section = len(self.nonresidential_energy_section)
		
		# =========================================================================================
		# Building facility information
		# Elevator information
		self.elevator                        = kwargs.get('elevator', [])
		self.n_elevator                      = len(self.elevator)

		# Escalator information
		self.escalator                       = kwargs.get('escalator', [])
		self.n_escalator                     = len(self.escalator)

		# Water tower information
		self.watertower                      = kwargs.get('watertower', [])
		self.n_watertower                    = len(self.watertower)

		# Hotel information
		self.hotel                           = kwargs.get('hotel', [])
		self.n_hotel                         = len(self.hotel)

		# Hospital information
		self.hospital                        = kwargs.get('hospital', [])
		self.n_hospital                      = len(self.hospital)

		# Sport bathroom information
		self.sportbathroom                   = kwargs.get('sportbathroom', [])
		self.n_sportbathroom                 = len(self.sportbathroom)

		# Swimming pool information
		self.swimmingpool                    = kwargs.get('swimmingpool', [])
		self.n_swimmingpool                  = len(self.swimmingpool)

		# Spa information
		self.spa                             = kwargs.get('spa', [])
		self.n_spa                           = len(self.spa)

		# Dining area information
		self.diningarea                      = kwargs.get('diningarea', [])
		self.n_diningarea                    = len(self.diningarea)

		# Exhibition area information
		self.exhibitionarea                  = kwargs.get('exhibitionarea', [])
		self.n_exhibitionarea                = len(self.exhibitionarea)

		# Performance area information
		self.performancearea                 = kwargs.get('performancearea', [])
		self.n_performancearea               = len(self.performancearea)

		# Data center information
		self.datacenter                      = kwargs.get('datacenter', [])
		self.n_datacenter                    = len(self.datacenter)

		# Heater
		self.heater                          = kwargs.get('heater', [])
		self.n_heater                        = len(self.heater)

		# Parking garage information
		self.parkinggarage                   = kwargs.get('parkinggarage', [])
		self.n_parkinggarage                 = len(self.parkinggarage)

	def create_energy_section(self, **kwargs):

		"""
		This method is used to create an energy section object and append it to the building object.
		===========================================================================================

		Arguments:

			None

		Output:

			None
		"""

		new_energy_section = EnergySection(**kwargs)

		self.energy_section.append(new_energy_section)
		self.n_energy_section = len(self.energy_section)

		return
	
	def create_exclusive_energy_section(self, **kwargs):

		"""
		This method is used to create an exclusive energy section object and append it to the building object.
		===========================================================================================

		Arguments:

			None

		Output:

			None
		"""

		# If building_class is not 'general', raise error
		if (self.building_class != 'general'): raise ValueError('The building class is not general, cannot create exclusive energy section.')

		new_exclusive_energy_section = ExclusiveEnergySection(**kwargs)

		self.exclusive_energy_section.append(new_exclusive_energy_section)
		self.n_exclusive_energy_section = len(self.exclusive_energy_section)

		return
	
	def create_nonresidential_energy_section(self, **kwargs):

		"""
		This method is used to create a non-residential energy section object and append it to the building object.
		===========================================================================================

		Arguments:

			None

		Output:

			None
		"""

		# If building_class is not 'residential', raise error
		if (self.building_class != 'residential'): raise ValueError('The building class is not residential, cannot create non-residential energy section.')

		new_nonresidential_energy_section = NonResidentialEnergySection(**kwargs)

		self.nonresidential_energy_section.append(new_nonresidential_energy_section)
		self.n_nonresidential_energy_section = len(self.nonresidential_energy_section)

		return

	def create_elevator(self, **kwargs):

		"""
		This method is used to create an elevator object and append it to the building object.
		===========================================================================================
		
		Arguments:

			None

		Output:

			None
		"""

		# Remove building_type in kwargs avoiding repetition
		if ('building_type' in kwargs): kwargs.pop('building_type')

		new_elevator = building_facility.Elevator(
			estimation_system=self.estimation_system,
			building_class=self.building_class,
			building_type=self.building_type,
			**kwargs,
		)
		self.elevator.append(new_elevator)
		self.n_elevator = len(self.elevator)

		return
	
	def create_escalator(self, **kwargs):

		"""
		This method is used to create an escalator object and append it to the building object.
		===========================================================================================
		
		Arguments:

			None

		Output:

			None
		"""

		# Remove building_type in kwargs avoiding repetition
		if ('building_type' in kwargs): kwargs.pop('building_type')

		new_escalator = building_facility.Escalator(
			estimation_system=self.estimation_system,
			building_class=self.building_class,
			building_type=self.building_type,
			**kwargs,
		)
		self.escalator.append(new_escalator)
		self.n_escalator = len(self.escalator)

		return
	
	def create_watertower(self, **kwargs):

		"""
		This method is used to create a watertower object and append it to the building object.
		===========================================================================================
		
		Arguments:

			None

		Output:

			None
		"""

		# Remove building_type in kwargs avoiding repetition
		if ('building_type' in kwargs): kwargs.pop('building_type')

		new_watertower = building_facility.WaterTower(
			estimation_system=self.estimation_system,
			building_class=self.building_class,
			building_type=self.building_type,
			building_address_county=self.building_address_county,
			**kwargs,
		)
		self.watertower.append(new_watertower)
		self.n_watertower = len(self.watertower)

		return
	
	def create_hotel(self, **kwargs):

		"""
		This method is used to create a hotel object and append it to the building object.
		===========================================================================================

		Arguments:

			None

		Output:

			None
		"""

		# Remove building_type in kwargs avoiding repetition
		if ('building_type' in kwargs): kwargs.pop('building_type')
		if ('building_cz' in kwargs): kwargs.pop('building_cz')

		new_hotel = building_facility.Hotel(
			estimation_system=self.estimation_system,
			building_class=self.building_class,
			building_type=self.building_type,
			building_cz=self.building_cz,
			**kwargs,
		)
		self.hotel.append(new_hotel)
		self.n_hotel = len(self.hotel)

		return
	
	def create_hospital(self, **kwargs):

		"""
		This method is used to create a hospital object and append it to the building object.
		===========================================================================================

		Arguments:

			None

		Output:

			None
		"""

		# Remove building_type in kwargs avoiding repetition
		if ('building_type' in kwargs): kwargs.pop('building_type')
		if ('building_cz' in kwargs): kwargs.pop('building_cz')

		new_hospital = building_facility.Hospital(
			estimation_system=self.estimation_system,
			building_class=self.building_class,
			building_type=self.building_type,
			building_cz=self.building_cz,
			**kwargs,
		)
		self.hospital.append(new_hospital)
		self.n_hospital = len(self.hospital)

		return
	
	def create_sportbathroom(self, **kwargs):

		"""
		This method is used to create a sportbathroom object and append it to the building object.
		===========================================================================================

		Arguments:

			None

		Output:

			None
		"""

		# Remove building_type in kwargs avoiding repetition
		if ('building_type' in kwargs): kwargs.pop('building_type')
		if ('building_cz' in kwargs): kwargs.pop('building_cz')

		new_sportbathroom = building_facility.SportBathroom(
			estimation_system=self.estimation_system,
			building_class=self.building_class,
			building_type=self.building_type,
			building_cz=self.building_cz,
			**kwargs,
		)
		self.sportbathroom.append(new_sportbathroom)
		self.n_sportbathroom = len(self.sportbathroom)

		return
	
	def create_swimmingpool(self, **kwargs):

		"""
		This method is used to create a swimmingpool object and append it to the building object.
		===========================================================================================

		Arguments:

			None

		Output:

			None
		"""

		# Remove building_type in kwargs avoiding repetition
		if ('building_type' in kwargs): kwargs.pop('building_type')
		if ('building_cz' in kwargs): kwargs.pop('building_cz')

		new_swimmingpool = building_facility.SwimmingPool(
			estimation_system=self.estimation_system,
			building_class=self.building_class,
			building_type=self.building_type,
			building_cz=self.building_cz,
			**kwargs,
		)
		self.swimmingpool.append(new_swimmingpool)
		self.n_swimmingpool = len(self.swimmingpool)

		return
	
	def create_spa(self, **kwargs):
		
		"""
		This method is used to create a spa object and append it to the building object.
		===========================================================================================

		Arguments:

			None

		Output:

			None
		"""

		# Remove building_type in kwargs avoiding repetition
		if ('building_type' in kwargs): kwargs.pop('building_type')
		if ('building_cz' in kwargs): kwargs.pop('building_cz')

		new_spa = building_facility.Spa(
			estimation_system=self.estimation_system,
			building_class=self.building_class,
			building_type=self.building_type,
			building_cz=self.building_cz,
			**kwargs,
		)
		self.spa.append(new_spa)
		self.n_spa = len(self.spa)

		return
	
	def create_diningarea(self, **kwargs):

		"""
		This method is used to create a diningarea object and append it to the building object.
		===========================================================================================

		Arguments:

			None

		Output:

			None
		"""

		# Remove building_type in kwargs avoiding repetition
		if ('building_type' in kwargs): kwargs.pop('building_type')
		if ('building_cz' in kwargs): kwargs.pop('building_cz')

		new_diningarea = building_facility.DiningArea(
			estimation_system=self.estimation_system,
			building_class=self.building_class,
			building_type=self.building_type,
			building_cz=self.building_cz,
			**kwargs,
		)
		self.diningarea.append(new_diningarea)
		self.n_diningarea = len(self.diningarea)

		return
	
	def create_exhibitionarea(self, **kwargs):

		"""
		This method is used to create a exhibitionarea object and append it to the building object.
		===========================================================================================

		Arguments:

			None

		Output:

			None
		"""

		# Remove building_type in kwargs avoiding repetition
		if ('building_type' in kwargs): kwargs.pop('building_type')
		if ('building_cz' in kwargs): kwargs.pop('building_cz')

		new_exhibitionarea = building_facility.ExhibitionArea(
			estimation_system=self.estimation_system,
			building_class=self.building_class,
			building_type=self.building_type,
			building_cz=self.building_cz,
			**kwargs,
		)
		self.exhibitionarea.append(new_exhibitionarea)
		self.n_exhibitionarea = len(self.exhibitionarea)

		return
	
	def create_performancearea(self, **kwargs):

		"""
		This method is used to create a performancearea object and append it to the building object.
		===========================================================================================

		Arguments:

			None

		Output:

			None
		"""

		# Remove building_type in kwargs avoiding repetition
		if ('building_type' in kwargs): kwargs.pop('building_type')
		if ('building_cz' in kwargs): kwargs.pop('building_cz')

		new_performancearea = building_facility.PerformanceArea(
			estimation_system=self.estimation_system,
			building_class=self.building_class,
			building_type=self.building_type,
			building_cz=self.building_cz,
			**kwargs,
		)
		self.performancearea.append(new_performancearea)
		self.n_performancearea = len(self.performancearea)

		return
	
	def create_datacenter(self, **kwargs):

		"""
		This method is used to create a datacenter object and append it to the building object.
		===========================================================================================

		Arguments:

			None

		Output:

			None
		"""
		
		# Remove building_type in kwargs avoiding repetition
		if ('building_type' in kwargs): kwargs.pop('building_type')

		new_datacenter = building_facility.DataCenter(
			estimation_system=self.estimation_system,
			building_class=self.building_class,
			building_type=self.building_type,
			**kwargs,
		)
		self.datacenter.append(new_datacenter)
		self.n_datacenter = len(self.datacenter)

		return
	
	def create_heater(self, **kwargs):

		"""
		This method is used to create a heater object and append it to the building object.
		===========================================================================================

		Arguments:

			None

		Output:

			None
		"""
		
		# Remove building_type in kwargs avoiding repetition
		if ('building_type' in kwargs): kwargs.pop('building_type')

		new_heater = building_facility.Heater(
			estimation_system=self.estimation_system,
			building_class=self.building_class,
			building_type=self.building_type,
			**kwargs,
		)
		self.heater.append(new_heater)
		self.n_heater = len(self.heater)

		return
	
	def create_parkinggarage(self, **kwargs):

		"""
		This method is used to create a parking garage object and append it to the building object.
		===========================================================================================

		Arguments:

			None

		Output:

			None
		"""
		
		# Remove building_type in kwargs avoiding repetition
		if ('building_type' in kwargs): kwargs.pop('building_type')

		new_parkinggarage = building_facility.ParkingGarage(
			estimation_system=self.estimation_system,
			building_class=self.building_class,
			building_type=self.building_type,
			**kwargs,
		)
		self.parkinggarage.append(new_parkinggarage)
		self.n_parkinggarage = len(self.parkinggarage)

		return

class ExistingBuilding(Building):

	"""
	This class is used to create a building object
	"""

	def __init__(self, estimation_system: str, building_type: str, **kwargs):

		"""
		This method is used to initialize a building object.
		===========================================================================================

		Arguments:

			estimation_system (str): Estimation system. Only BERSe is available now.

			building_type (str): Building type. A-1, B-1, ..., etc.

		Output:

			None
		"""

		# Initialize the building object
		super().__init__(
			**dict(
				kwargs,
				estimation_system=estimation_system,
				building_class='general',
				building_type=building_type,
			)
		)

		# 1. Building information
		# 1-a. Estimation information
		self.building_name                   = kwargs.get('building_name', None)
		self.estimation_system               = estimation_system
		self.building_class                  = 'general'
		self.building_type                   = building_type

		# 1-b. Basic information
		self.building_coordinate             = kwargs.get('building_coordinate', None)
		self.building_address_county         = kwargs.get('building_address_county', None)
		self.building_address_town           = kwargs.get('building_address_town', None)
		self.building_n_stories_above_ground = kwargs.get('building_n_stories_above_ground', None)
		self.building_n_stories_below_ground = kwargs.get('building_n_stories_below_ground', None)
		self.building_floor_offset           = kwargs.get('building_floor_offset', 0)

		self.energy_section                  = kwargs.get('energy_section', [])
		self.n_energy_section                = len(self.energy_section)
		self.exclusive_energy_section        = kwargs.get('exclusive_energy_section', [])
		self.n_exclusive_energy_section      = len(self.exclusive_energy_section)

		# 1-c. Energy consumption
		self.ec                              = kwargs.get('ec', None)
		self.ec_other                        = kwargs.get('ec_other', None)
		self.est_q_rw                        = kwargs.get('est_q_rw', 0)
		self.ec_heating_comm                 = kwargs.get('ec_heating_comm', 'HE')

		# =========================================================================================
		#
		# Error handling
		#
		# =========================================================================================

		# Building location is not defined
		if (self.building_coordinate is None) and ((self.building_address_county is None) and (self.building_address_town is None)): raise ValueError('Building location is not defined.')

		# Building system is not available
		if (self.estimation_system not in ['BERSe']): raise ValueError('Building system is not available. Only BERSe is available now.')

		# =========================================================================================
		#
		# Initialize the building object
		#
		# =========================================================================================

		# Basic information
		self.building_n_stories_total = self.building_n_stories_above_ground + self.building_n_stories_below_ground + self.building_floor_offset

		# =========================================================================================

		# Climate zone and urban coefficient
		if (self.building_coordinate is not None): self.building_address_county, self.building_address_town = self._get_address_coordinate(*self.building_coordinate)
		
		self.building_cz = tool.get_climatezone(self.building_address_county, self.building_address_town)
		self.building_ur = tool.get_urbanregion(self.building_address_county, self.building_address_town)

		# =========================================================================================
		
		# Heating ec
		if (self.ec_heating_comm == 'HE'): self.ec_heating_comm = 45.1
		elif (self.ec_heating_comm == 'HPE'): self.ec_heating_comm = 13.2
		else: self.ec_heating_comm = 0.0

	def estimate(self):

		"""
		This method is used to estimate the EUI score of a building
		===========================================================================================

		Arguments:

			None

		Output:

			None
		"""

		# =========================================================================================
		#
		# Check for energy section and exclusive energy section
		#
		# =========================================================================================

		# Energy section and exclusive energy section are not defined
		if (self.n_energy_section == 0) and (self.n_exclusive_energy_section == 0): raise ValueError('Energy section and exclusive energy section are not defined.')

		# ac_operation syntax error: attribute ac_operation in energy sections contain the string except CONTINUE and INTERVAL (case insensitive)
		if not all([i.ac_operation.upper() in ['CONTINUE', 'INTERVAL'] for i in self.energy_section]): raise ValueError('ac_operation syntax error: attribute ac_operation in energy sections contain the string except CONTINUE and INTERVAL (case insensitive).')

		# =========================================================================================
		#
		# Get SO_r (ratio of operation) for specific energy sections
		#
		# =========================================================================================

		for i_es in self.energy_section: i_es.SO_r = self._get_coef_usage_r_operation(i_es)

		# =========================================================================================
		# 
		# Calculate EUI score scale
		# 
		# =========================================================================================

		# Read the files for EUI score
		eui_criteria = read_eui_criteria.EuiCriteria(
			building_climate_zone=self.building_cz,
			building_address_county=self.building_address_county,
			building_address_town=self.building_address_town,
		)

		# Extract EUI values from EUI score tables
		for i_es in self.energy_section:

			i_es.eeui_m     = eui_criteria.get_eui_criteria(i_es, 'm', 'eeui')
			i_es.leui_min   = eui_criteria.get_eui_criteria(i_es, 'min', 'leui')
			i_es.leui_m     = eui_criteria.get_eui_criteria(i_es, 'm', 'leui')
			i_es.leui_max   = eui_criteria.get_eui_criteria(i_es, 'max', 'leui')
			i_es.aeui_min   = eui_criteria.get_eui_criteria(i_es, 'min', 'aeui')
			i_es.aeui_m     = eui_criteria.get_eui_criteria(i_es, 'm', 'aeui')
			i_es.aeui_max   = eui_criteria.get_eui_criteria(i_es, 'max', 'aeui')

		# Error handling
		# aeui_min, aeui_m, or aeui_max include NaN
		if ([i.aeui_min for i in self.energy_section] + [i.aeui_m for i in self.energy_section] + [i.aeui_max for i in self.energy_section]).count(np.nan) > 0: raise ValueError('aeui_min, aeui_m, or aeui_max include NaN.')

		# Calculate area, EUI for common energy sections
		self.est_a_es_comm   = np.nansum([i.a for i in self.energy_section])
		self.est_aeui_min    = np.nansum([i.a * i.aeui_min for i in self.energy_section]) / self.est_a_es_comm
		self.est_aeui_m      = np.nansum([i.a * i.aeui_m for i in self.energy_section]) / self.est_a_es_comm
		self.est_aeui_max    = np.nansum([i.a * i.aeui_max for i in self.energy_section]) / self.est_a_es_comm
		self.est_leui_min    = np.nansum([i.a * i.leui_min for i in self.energy_section]) / self.est_a_es_comm
		self.est_leui_m      = np.nansum([i.a * i.leui_m for i in self.energy_section]) / self.est_a_es_comm
		self.est_leui_max    = np.nansum([i.a * i.leui_max for i in self.energy_section]) / self.est_a_es_comm
		self.est_eeui_m      = np.nansum([i.a * i.eeui_m for i in self.energy_section]) / self.est_a_es_comm

		self.est_eui_g       = self.building_ur * (0.8 * self.est_aeui_m + 0.8 * self.est_leui_m + self.est_eeui_m)
		self.est_eui_min     = self.building_ur * (self.est_aeui_min + self.est_leui_min + self.est_eeui_m)
		self.est_eui_m       = self.building_ur * (self.est_aeui_m + self.est_leui_m + self.est_eeui_m)
		self.est_eui_max     = self.building_ur * (self.est_aeui_max + self.est_leui_max + self.est_eeui_m)

		# Calculate the properties for exclusive energy sections
		if (self.n_exclusive_energy_section > 0):
			
			for i_es in self.exclusive_energy_section: i_es.e_n = self._calc_e_n(i_es)

			self.est_e_n = np.nansum([i.e_n for i in self.exclusive_energy_section])

		else:

			self.est_e_n = 0.0
		
		self.est_a_es_exclusive = np.nansum([i.a for i in self.exclusive_energy_section])
		

		# =========================================================================================
		# 
		# Calculate adjusted EC
		# 
		# =========================================================================================

		# Error handling
		# n_elevator/n_escalator is not equal to the length of elevator/escalator list
		if (self.n_elevator != len(self.elevator)): raise ValueError('n_elevator is not equal to the length of elevator list.')
		if (self.n_escalator != len(self.escalator)): raise ValueError('n_escalator is not equal to the length of escalator list.')

		# Calculate ec for transportation
		self.est_e_t         = self._calc_ec_total_elevator() + self._calc_ec_total_escalator()

		# Calculate ec for pump
		self.hydraulic_head_total = self._calc_average_hydraulic_head_watertower()

		self.est_q_w         = \
			self._calc_water_total_comm() + \
			self._calc_water_total_hotel() + \
			self._calc_water_total_hospital() + \
			self._calc_water_total_sportbathroom() + \
			self._calc_water_total_swimmingpool() + \
			self._calc_water_total_spa()
		
		self.est_q_aw        = \
			self._calc_water_total_watercooled()

		self.est_e_p         = \
			self._calc_ec_water_pumping_total_comm() + \
			self._calc_ec_water_pumping_total_swimmingpool() + \
			self._calc_ec_water_pumping_total_spa() + \
			self._calc_ec_water_process_total_swimmingpool() + \
			self._calc_ec_water_process_total_spa() + \
			self._calc_ec_water_nozzle_total_spa()
		
		# Calculate ec for heating
		self.est_q_hw        = \
			self._calc_hotwater_total_hotel() + \
			self._calc_hotwater_total_hospital() + \
			self._calc_hotwater_total_diningarea() + \
			self._calc_hotwater_total_sportbathroom()
		
		self.est_e_h         = \
			self._calc_es_water_heating_total_comm() + \
			self._calc_es_water_heating_total_swimmingpool() + \
			self._calc_es_water_heating_total_spa()
		
		# Calculate main eui
		self.est_eui_main    = (self.ec - self.building_ur * (self.est_e_n + self.est_e_t + self.est_e_p + self.est_e_h) - self.ec_other) / self.est_a_es_comm

		# =========================================================================================
		# 
		# Bias-correction for EC
		# 
		# =========================================================================================

		# Calculate adjusted eui_m
		self.est_aeui_m_adj  = np.nansum([i.a * i.aeui_m * i.SO_r for i in self.energy_section]) / self.est_a_es_comm
		self.est_leui_m_adj  = np.nansum([i.a * i.leui_m * i.SO_r for i in self.energy_section]) / self.est_a_es_comm
		self.est_eeui_m_adj  = np.nansum([i.a * i.eeui_m * i.SO_r for i in self.energy_section]) / self.est_a_es_comm
		
		self.est_eui_m_adj   = self.building_ur * (self.est_aeui_m_adj + self.est_leui_m_adj + self.est_eeui_m_adj)

		# Calculate unbiased eui
		self.est_eui         = self.est_eui_m + self.est_eui_main - self.est_eui_m_adj
		
		# Calculate total eui
		self.est_eui_total   = self.ec / (self.est_a_es_comm + self.est_a_es_exclusive)
		
		# =========================================================================================
		# 
		# Calculate cei
		# 
		# =========================================================================================

		# Calculate cei
		self.est_cei		 = self.est_eui * constant.coef_ece

		# =========================================================================================
		# 
		# Calculate score
		# 
		# =========================================================================================

		print()

		# Calculate score
		if (self.est_eui <= self.est_eui_g):

			self.est_score = 50 + 50 * (self.est_eui_g - self.est_eui) / (self.est_eui_g - self.est_eui_min)
		
		elif (self.est_eui > self.est_eui_g):
			self.est_score = 50 * (self.est_eui_max - self.est_eui) / (self.est_eui_max - self.est_eui_g)

		# Compress the score to 0-100
		self.est_score = min(max(self.est_score, 0), 100)

		# Caclulate score level
		if (self.est_score >= 90): self.est_score_level = '1+'
		elif (self.est_score >= 80): self.est_score_level = '1'
		elif (self.est_score >= 70): self.est_score_level = '2'
		elif (self.est_score >= 60): self.est_score_level = '3'
		elif (self.est_score >= 50): self.est_score_level = '4'
		elif (self.est_score >= 40): self.est_score_level = '5'
		elif (self.est_score >= 20): self.est_score_level = '6'
		elif (self.est_score >= 0): self.est_score_level = '7'

		# =========================================================================================
		# 
		# Finish estimation
		# 
		# =========================================================================================

		return

	def _calc_ec_total_elevator(self):

		"""
		This method is used to calculate the energy consumption of elevators.
		If no elevator is created, 0 is returned.
		===========================================================================================

		Arguments:

			None

		Output:

			ec_total_elevator (float): Energy consumption of all elevators
		"""
		
		# No elevator is created
		if (self.n_elevator == 0):
			
			ec_total_elevator = 0
		
		else:
			
			ec_total_elevator = np.nansum([i.coef_usage_r * i.coef_ec * i.coef_eff * i.coef_usage_h for i in self.elevator])

		return ec_total_elevator
	
	def _calc_ec_total_escalator(self):

		"""
		This method is used to calculate the energy consumption of escalators.
		If no escalator is created, 0 is returned.
		===========================================================================================

		Arguments:

			None

		Output:

			ec_total_escalator (float): Energy consumption of all escalators
		"""
		
		# No escalator is created
		if (self.n_escalator == 0):
			
			ec_total_escalator = 0
		
		else:
			
			ec_total_escalator = np.nansum([i.coef_usage_r * i.coef_power * i.coef_eff * i.coef_usage_h for i in self.escalator])

		return ec_total_escalator
	
	def _calc_average_hydraulic_head_watertower(self):

		"""
		This method is used to calculate the average hydraulic head of all water towers.
		If the number of water towers is larger than 1, the volumes (v) will be used as weights.
		If no water tower is created, 0 is returned.
		===========================================================================================

		Arguments:

			None

		Output:

			average_hydraulic_head_watertower (float): Average hydraulic head of all water towers
		"""
		
		# No water tower is created
		if (self.n_watertower == 0):
			
			average_hydraulic_head_watertower = 0

		elif (self.n_watertower == 1):

			average_hydraulic_head_watertower = self.watertower[0].standard_hydraulic_head_total
		
		else:
			
			average_hydraulic_head_watertower = np.average([i.standard_hydraulic_head_total for i in self.watertower], weights=[i.v for i in self.watertower])

		return average_hydraulic_head_watertower
	
	def _calc_water_total_comm(self):

		"""
		This method is used to calculate the water consumption of all common energy sections.
		The function tool.get_coef_usage_i_water return m^3/(room*year). Therefore, if the energy section is hotel (id = H1 or H2), the water consumption will be divided by the number of rooms.
		===========================================================================================

		Arguments:

			None

		Output:

			water_total_comm (float): Water consumption of all common energy sections
		"""

		water_total_comm = \
			np.nansum([i.a * tool.get_coef_usage_i_water(i.id) for i in self.energy_section if not i.id in ['H1', 'H2']]) + \
			np.nansum([i.a * tool.get_coef_usage_i_water(i.id) / getattr(i, 'hotel-n_room') for i in self.energy_section if i.id in ['H1', 'H2']])
		
		return water_total_comm
	
	def _calc_water_total_hotel(self):

		"""
		This method is used to calculate the water consumption of all hotel.
		===========================================================================================

		Arguments:

			None
		
		Output:

			water_total_hotel (float): Water consumption of all hotel
		"""
		
		# No hotel is created
		if (self.n_hotel == 0):
			
			water_total_hotel = 0
		
		else:
			
			water_total_hotel = 73.0 * np.nansum([i.n_room * i.coef_usage_r_room for i in self.hotel])

		return water_total_hotel
	
	def _calc_water_total_hospital(self):

		"""
		This method is used to calculate the water consumption of all hospital.
		===========================================================================================

		Arguments:

			None
		
		Output:

			water_total_hospital (float): Water consumption of all hospital
		"""
		
		# No hospital is created
		if (self.n_hospital == 0):
			
			water_total_hospital = 0
		
		else:
			
			water_total_hospital = 91.3 * np.nansum([i.n_hospitalbed * i.coef_usage_r_hospitalbed for i in self.hospital])

		return water_total_hospital

	def _calc_water_total_sportbathroom(self):

		"""
		This method is used to calculate the water consumption of all sport bathroom.
		===========================================================================================

		Arguments:

			None
		
		Output:

			water_total_sportbathroom (float): Water consumption of all sport bathroom
		"""
		
		# No sportbathroom is created
		if (self.n_sportbathroom == 0):
			
			water_total_sportbathroom = 0
		
		else:
			
			water_total_sportbathroom = 0.046 * np.nansum([i.a * i.coef_usage_h for i in self.sportbathroom])

		return water_total_sportbathroom

	def _calc_water_total_swimmingpool(self):

		"""
		This method is used to calculate the water consumption of all swimming pool.
		===========================================================================================

		Arguments:

			None
		
		Output:

			water_total_swimmingpool (float): Water consumption of all swimming pool
		"""
		
		# No swimmingpool is created
		if (self.n_swimmingpool == 0):
			
			water_total_swimmingpool = 0
		
		else:
			
			water_total_swimmingpool = 0.01 * np.nansum([i.v * i.coef_usage_h for i in self.swimmingpool])

		return water_total_swimmingpool
	
	def _calc_water_total_spa(self):

		"""
		This method is used to calculate the water consumption of all spa.
		===========================================================================================

		Arguments:

			None
		
		Output:

			water_total_spa (float): Water consumption of all spa
		"""

		# No spa is created
		if (self.n_spa == 0):
			
			water_total_spa = 0
		
		else:
			
			water_total_spa = 0.01 * np.nansum([i.v * i.coef_usage_h for i in self.spa])

		return water_total_spa
	
	def _calc_water_total_watercooled(self):

		"""
		This method is used to calculate the water consumption of all watercooled AC energy sections.
		===========================================================================================

		Arguments:

			None
		
		Output:

			water_total_watercooled (float): Water consumption of all watercooled AC energy sections
		"""

		# No spa is created
		"""
		if (self.building_es_comm[self.building_es_comm['AC_Type'].str.upper()=='WATERCOOLED'].empty):
			
			water_total_watercooled = 0
		
		else:
			
			water_total_watercooled = np.nansum([(0.00036 * tool.get_coef_usage_h_ac(i['Section_ID'], self.building_cz, i['AC_Operation']) + 0.32) * i['Area'] for _, i in self.building_es_comm.iterrows() if str(i['AC_Type']).upper()=='WATERCOOLED'])
		"""
		if (len([i for i in self.energy_section if i.ac_type.upper()=='WATERCOOLED']) == 0):

			water_total_watercooled = 0
		
		else:
			
			water_total_watercooled = np.nansum([(0.00036 * tool.get_coef_usage_h_ac(i.id, self.building_cz, i.ac_operation) + 0.32) * i.a for i in self.energy_section if i.ac_type.upper()=='WATERCOOLED'])


		return water_total_watercooled
	
	def _calc_ec_water_pumping_total_comm(self):

		"""
		This method is used to calculate the ec of water pumping consumption of all common energy sections.
		===========================================================================================

		Arguments:

			None
		
		Output:

			ec_water_pumping_total_comm (float): Energy consumption of water pumping consumption of all common energy sections
		"""
		
		ec_water_pumping_total_comm = 0.02 * self.hydraulic_head_total * (self.est_q_w + self.est_q_aw - self.est_q_rw)

		return ec_water_pumping_total_comm
	
	def _calc_ec_water_pumping_total_swimmingpool(self):

		"""
		This method is used to calculate the ec of water pumping consumption of all swimming pool.
		===========================================================================================

		Arguments:

			None
		
		Output:

			ec_water_pumping_total_swimmingpool (float): Energy consumption of water pumping consumption of all swimming pool
		"""
		
		# No swimmingpool is created
		if (self.n_swimmingpool == 0):
			
			ec_water_pumping_total_swimmingpool = 0
		
		else:
			
			ec_water_pumping_total_swimmingpool = np.nansum([0.02 * (i.height_watertower + 6.0) * 0.01 * i.v * i.coef_usage_h for i in self.swimmingpool])

		return ec_water_pumping_total_swimmingpool
	
	def _calc_ec_water_pumping_total_spa(self):
		
		"""
		This method is used to calculate the ec of water pumping consumption of all spa.
		===========================================================================================

		Arguments:

			None
		
		Output:

			ec_water_pumping_total_spa (float): Energy consumption of water pumping consumption of all spa
		"""
		
		# No spa is created
		if (self.n_spa == 0):
			
			ec_water_pumping_total_spa = 0
		
		else:
			
			ec_water_pumping_total_spa = np.nansum([0.02 * (i.height_watertower + 6.0) * 0.01 * i.v * i.coef_usage_h for i in self.spa])

		return ec_water_pumping_total_spa
	
	def _calc_ec_water_process_total_swimmingpool(self):

		"""
		This method is used to calculate the ec of water process consumption of all swimming pool.
		===========================================================================================

		Arguments:

			None
		
		Output:

			ec_water_process_total_swimmingpool (float): Energy consumption of water process consumption of all swimming pool
		"""
		
		# No swimmingpool is created
		if (self.n_swimmingpool == 0):
			
			ec_water_process_total_swimmingpool = 0
		
		else:
			
			ec_water_process_total_swimmingpool = np.nansum([0.016 * i.v * i.coef_usage_h for i in self.swimmingpool])

		return ec_water_process_total_swimmingpool
	
	def _calc_ec_water_process_total_spa(self):

		"""
		This method is used to calculate the ec of water process consumption of all spa.
		===========================================================================================

		Arguments:

			None
		
		Output:

			ec_water_process_total_spa (float): Energy consumption of water process consumption of all spa
		"""
		
		# No spa is created
		if (self.n_spa == 0):
			
			ec_water_process_total_spa = 0
		
		else:
			
			ec_water_process_total_spa = np.nansum([0.16 * i.v * i.coef_usage_h for i in self.spa])

		return ec_water_process_total_spa
	
	def _calc_ec_water_nozzle_total_spa(self):

		"""
		This method is used to calculate the ec of water nozzle consumption of all spa.
		===========================================================================================

		Arguments:

			None

		Output:

			ec_water_nozzle_total_spa (float): Energy consumption of water nozzle consumption of all spa
		"""

		# No spa is created
		if (self.n_spa == 0):
			
			ec_water_nozzle_total_spa = 0
		
		else:
			
			ec_water_nozzle_total_spa = np.nansum([0.064 * i.v * i.coef_usage_h for i in self.spa])

		return ec_water_nozzle_total_spa
	
	def _calc_hotwater_total_hotel(self):

		"""
		This method is used to calculate the hotwater consumption of all hotel.
		===========================================================================================

		Arguments:

			None

		Output:

			hotwater_total_hotel (float): Hotwater consumption of all hotel
		"""

		# No hotel is created
		if (self.n_hotel == 0):
			
			hotwater_total_hotel = 0
		
		else:
			
			hotwater_total_hotel = 10.2 * np.nansum([i.n_room * i.coef_usage_r_room for i in self.hotel])

		return hotwater_total_hotel
	
	def _calc_hotwater_total_hospital(self):

		"""
		This method is used to calculate the hotwater consumption of all hospital.
		===========================================================================================

		Arguments:

			None

		Output:

			hotwater_total_hospital (float): Hotwater consumption of all hospital
		"""

		# No hospital is created
		if (self.n_hospital == 0):
			
			hotwater_total_hospital = 0
		
		else:
			
			hotwater_total_hospital = 12.8 * np.nansum([i.n_hospitalbed * i.coef_usage_r_hospitalbed for i in self.hospital])

		return hotwater_total_hospital
	
	def _calc_hotwater_total_diningarea(self):

		"""
		This method is used to calculate the hotwater consumption of all dining area.
		===========================================================================================

		Arguments:

			None

		Output:

			hotwater_total_diningarea (float): Hotwater consumption of all dining area
		"""

		# No diningarea is created
		if (self.n_diningarea == 0):
			
			hotwater_total_diningarea = 0
		
		else:
			
			hotwater_total_diningarea = np.nansum([i.coef_usage_i_hotwater * i.a * i.coef_usage_d for i in self.diningarea])

		return hotwater_total_diningarea
	
	def _calc_hotwater_total_sportbathroom(self):

		"""
		This method is used to calculate the hotwater consumption of all sport bathroom.
		===========================================================================================

		Arguments:

			None

		Output:

			hotwater_total_sportbathroom (float): Hotwater consumption of all sport bathroom
		"""

		# No sportbathroom is created
		if (self.n_sportbathroom == 0):
			
			hotwater_total_sportbathroom = 0
		
		else:
			
			hotwater_total_sportbathroom = 0.023 * np.nansum([i.a * i.coef_usage_h for i in self.sportbathroom])

		return hotwater_total_sportbathroom
	
	def _calc_hotwater_total_swimmingpool(self):

		"""
		This method is used to calculate the hotwater consumption of all swimming pool.
		===========================================================================================

		Arguments:

			None

		Output:

			hotwater_total_swimmingpool (float): Hotwater consumption of all swimming pool
		"""

		# No swimmingpool is created
		if (self.n_swimmingpool == 0):
			
			hotwater_total_swimmingpool = 0
		
		else:
			
			hotwater_total_swimmingpool = 0.16 * np.nansum([i.v * i.coef_usage_d_hotwater for i in self.swimmingpool])

		return hotwater_total_swimmingpool
	
	def _calc_hotwater_total_spa(self):

		"""
		This method is used to calculate the hotwater consumption of all spa.
		===========================================================================================

		Arguments:

			None

		Output:

			hotwater_total_spa (float): Hotwater consumption of all spa
		"""

		# No spa is created
		if (self.n_spa == 0):
			
			hotwater_total_spa = 0
		
		else:
			
			hotwater_total_spa = 0.16 * np.nansum([i.v * i.coef_usage_d_hotwater for i in self.spa])

		return hotwater_total_spa
	
	def _calc_es_water_heating_total_comm(self):

		"""
		This method is used to calculate the energy consumption of water heating of all common energy sections.
		===========================================================================================

		Arguments:

			None

		Output:

			es_water_heating_total_comm (float): Energy consumption of water heating of all common energy sections
		"""

		es_water_heating_total_comm = self.ec_heating_comm * self.est_q_hw 

		return es_water_heating_total_comm
	
	def _calc_es_water_heating_total_swimmingpool(self):

		"""
		This method is used to calculate the energy consumption of water heating of all swimming pool.
		===========================================================================================

		Arguments:

			None

		Output:

			es_water_heating_total_swimmingpool (float): Energy consumption of water heating of all swimming pool
		"""

		# No swimmingpool is created
		if (self.n_swimmingpool == 0):
			
			es_water_heating_total_swimmingpool = 0
		
		else:
			
			# Weighted average of heating ec
			es_water_heating_total_swimmingpool = np.average([i.ec_heating for i in self.swimmingpool], weights=[i.v for i in self.swimmingpool]) * self._calc_hotwater_total_swimmingpool()

		return es_water_heating_total_swimmingpool

	def _calc_es_water_heating_total_spa(self):
		
		"""
		This method is used to calculate the energy consumption of water heating of all spa.
		===========================================================================================

		Arguments:

			None

		Output:

			es_water_heating_total_spa (float): Energy consumption of water heating of all spa
		"""

		# No spa is created
		if (self.n_spa == 0):
			
			es_water_heating_total_spa = 0
		
		else:
			
			# Weighted average of heating ec
			es_water_heating_total_spa = np.average([i.ec_heating for i in self.spa], weights=[i.v for i in self.spa]) * self._calc_hotwater_total_spa()

		return es_water_heating_total_spa

	def _get_address_coordinate(self, lon, lat):

		"""
		This method is used to get the county and town of a building by latitude and longitude.
		===========================================================================================
		
		Arguments:

			lon (float): Longitude of the building

			lat (float): Latitude of the building

		Output:

			county (str): County of the building

			town (str): Town of the building
		"""

		# Read the shapefile
		df_town = gpd.read_file(__path__ + '../data/gis_layer/layer_taiwan_town/TOWN_MOI_1120317.shp', encoding='utf-8')

		# Get the county and town by latitude and longitude
		county = df_town.loc[df_town['geometry'].contains(gpd.points_from_xy([lon], [lat])[0]), 'COUNTYNAME'].values[0]
		town   = df_town.loc[df_town['geometry'].contains(gpd.points_from_xy([lon], [lat])[0]), 'TOWNNAME'].values[0]

		return county, town
	
	def _calc_e_n(self, es):

		"""
		This method is used to calculate the energy consumption of exclusive sections.
		===========================================================================================

		Arguments:

			es (ExclusiveEnergySection): Exclusive energy section
		
		Output:

			en (float): Energy consumption of exclusive sections
		"""

		# =========================================================================================
		# 
		# Class 1: EUI + area
		# 
		# =========================================================================================
		
		# N1-1-1
		if (es.id == 'N1-1-1'): en = 330 * es.a

		# N1-1-2
		if (es.id == 'N1-1-2'): en = 250 * es.a

		# N1-2-1
		if (es.id == 'N1-2-1'): en = 665 * es.a

		# N1-2-2
		if (es.id == 'N1-2-2'): en = 530 * es.a

		# N1-3-1
		if (es.id == 'N1-3-1'): en = 1318 * es.a

		# N1-3-2
		if (es.id == 'N1-3-2'): en = 900 * es.a

		# N1-4-1
		if (es.id == 'N1-4-1'): en = 989 * es.a

		# N1-4-2
		if (es.id == 'N1-4-2'): en = 675 * es.a

		# N1-5
		if (es.id == 'N1-5'): en = 387 * es.a

		# N1-6
		if (es.id == 'N1-6'): en = 1500 * es.a

		# N1-7
		if (es.id == 'N1-7'): en = 530 * es.a

		# N3-1-1
		if (es.id == 'N3-1-1'): en = 26.7 * es.a

		# N3-1-2
		if (es.id == 'N3-1-2'): en = 35.3 * es.a

		# N3-2-1
		if (es.id == 'N3-2-1'): en = 21.3 * es.a

		# N3-2-2
		if (es.id == 'N3-2-1'): en = 29.9 * es.a

		# N3-3-1
		if (es.id == 'N3-3-1'): en = 41.9 * es.a

		# N4-1
		if (es.id == 'N4-1'): en = 3.2 * es.a

		# N4-2
		if (es.id == 'N4-2'): en = 6.1 * es.a

		# N4-3
		if (es.id == 'N4-3'): en = 80.0 * es.a

		# N5
		if (es.id == 'N5'): en = 545 * es.a

		# N6
		if (es.id == 'N6'): en = 910 * es.a

		# =========================================================================================
		# 
		# Class 2: usage
		# 
		# =========================================================================================

		# N2-1-1
		if (es.id == 'N2-1-1'):

			if (self.n_hotel == 0): raise ValueError('Please create hotel first.')

			# Calculate the summation of hotel room and weighted average of coef_usage_r_hotelroom
			sum_n_hotelroom             = np.nansum([i.n_room for i in self.hotel])
			mean_coef_usage_r_hotelroom = np.average([i.coef_usage_r_room for i in self.hotel], weights=[i.n_room for i in self.hotel])
			
			en = sum_n_hotelroom * 5.85 * 365 * mean_coef_usage_r_hotelroom * 2.0
		
		# N2-1-2
		if (es.id == 'N2-1-2'):
			
			if (self.n_hotel == 0): raise ValueError('Please create hotel first.')

			# Calculate the summation of hotel room and weighted average of coef_usage_r_hotelroom
			sum_n_hotelroom             = np.nansum([i.n_room for i in self.hotel])
			mean_coef_usage_r_hotelroom = np.average([i.coef_usage_r_room for i in self.hotel], weights=[i.n_room for i in self.hotel])
			
			en = sum_n_hotelroom * 3.85 * 365 * mean_coef_usage_r_hotelroom * 1.5

		# N2-2
		if (es.id == 'N2-2'):
			
			if (self.n_hospital == 0): raise ValueError('Please create hospital first.')

			# Calculate the summation of hospital room and weighted average of coef_usage_r_hospitalbed
			sum_n_hospitalbed             = np.nansum([i.n_hospitalbed for i in self.hospital])
			mean_coef_usage_r_hospitalbed = np.average([i.coef_usage_r_hospitalbed for i in self.hospital], weights=[i.n_hospitalbed for i in self.hospital])
			
			en = sum_n_hospitalbed * 0.93 * 365 * mean_coef_usage_r_hospitalbed * 1.5

		# =========================================================================================
		# 
		# Class 3: usage + area
		# 
		# =========================================================================================

		# N2-1-3
		if (es.id == 'N2-1-3'):

			if (self.n_diningarea == 0): raise ValueError('Please create diningarea first.')
			
			# Calculate summation of dining area and weighted average of n_meal_per_day
			sum_a_dining        = np.nansum([i.a for i in self.diningarea])
			mean_n_meal_per_day = np.average([i.n_meal_per_day for i in self.diningarea], weights=[i.a for i in self.diningarea])

			# Calculate es
			en = sum_a_dining * 0.09 * mean_n_meal_per_day * 365 * 0.7 * 1.5

		# =========================================================================================
		# 
		# Class 4: EUI + usage + area
		# 
		# =========================================================================================

		# N7
		if (es.id == 'N7'): en = 0.124 * es.a * es.coef_usage_h

		# N8
		if (es.id == 'N8'):
			
			if (self.n_datacenter == 0): raise ValueError('Please create data center first.')
			
			# Calculate es
			en = np.nansum([i.a * (2630 * i.coef_power_cabinetrack + 51) for i in self.datacenter])

		# =========================================================================================
		# 
		# Class 5: other
		# 
		# =========================================================================================

		# N9, N10, N12
		if (es.id in ['N9', 'N10', 'N12']): en = 0.0

		# N11: raise error. Please use the other es
		if (es.id == 'N11'): raise ValueError('Please avoid using N11. Use the other es instead.')

		# =========================================================================================
		#
		# Summation
		#
		# =========================================================================================

		return en
	
	def _get_coef_usage_r_operation(self, es):

		"""
		This method is used to get the coefficient of actual operation for usage ratio.
		===========================================================================================

		Arguments:

			es (EnergySection): Energy section object

		Output:

			coef_usage_r_operation (float): Coefficient of operation for usage ratio
		"""

		# Default value
		coef_usage_r_operation = 1.0

		# Exhibition area
		if (self.n_exhibitionarea != 0):

			if (es.id in ['D1', 'D2', 'D3', 'E1']):

				coef_usage_r_operation = 0.52 + 0.45 * np.nansum([i.a * i.coef_usage_d for i in self.exhibitionarea]) / np.nansum([i.a * 273 for i in self.exhibitionarea])

		# Performance area
		if (self.n_performancearea != 0):

			if (es.id in ['F1']):
				
				coef_usage_r_operation = 0.17 + 0.83 * np.average([i.coef_usage_d / tool.get_coef_usage_d('F1') for i in self.performancearea], weights=[i.a for i in self.performancearea])

			elif (es.id in ['F2']):

				coef_usage_r_operation = 0.21 + 0.77 * np.average([i.coef_usage_d / tool.get_coef_usage_d('F2') for i in self.performancearea], weights=[i.a for i in self.performancearea])

			elif (es.id in ['G1']):

				coef_usage_r_operation = 0.39 + 0.60 * np.average([i.coef_usage_d / tool.get_coef_usage_d('G1') for i in self.performancearea], weights=[i.a for i in self.performancearea])

			elif (es.id in ['G2']):

				coef_usage_r_operation = 0.31 + 0.67 * np.average([i.coef_usage_d / tool.get_coef_usage_d('G2') for i in self.performancearea], weights=[i.a for i in self.performancearea])
		
		# Hotel
		if (self.n_hotel != 0):

			if (es.id in ['H1']):

				coef_usage_r_operation = 0.58 + 0.571 * np.average([i.coef_usage_r_room for i in self.hotel], weights=[i.n_room for i in self.hotel])

		# Hospital
		if (self.n_hospital != 0):

			if (es.id in ['H2']):

				coef_usage_r_operation = 0.25 + 0.94 * np.average([i.coef_usage_r_hospitalbed for i in self.hospital], weights=[i.n_hospitalbed for i in self.hospital])
		
		return coef_usage_r_operation

class NewBuilding(Building):

	"""
	# ===========================================================================================
	#
	# New residential building object
	#
	# ===========================================================================================

	The new residential building object is used in R-BERS to calculate the energy consumption of residential buildings.
	The primary components of a new residential building object are as follows:
		- Energy section
		- Non-residential energy section (optional)
		- Parking garage (optional)
		- Elevator (optional)
	"""

	def __init__(self, estimation_system: str, building_type: str, **kwargs):

		"""
		This method is used to initialize a new residential building object.
		===========================================================================================

		Arguments:

			estimation_system (str): Estimation system. Only R-BERS is available.

			building_type (str): Building type. Only 'appartment' and 'house' are available.

		Output:

			None
		"""

		# Initialize the building object
		super().__init__(
			**dict(
				kwargs,
				estimation_system=estimation_system,
				building_class='residential',
				building_type=building_type,
			)
		)

		# Initialize the building object
		# 1. Building information
		# 1-a. Estimation information
		self.estimation_system                = estimation_system
		self.building_class                   = 'residential'
		self.building_type                    = building_type

		# 1-b. Basic information
		self.building_coordinate              = kwargs.get('building_coordinate', None)
		self.building_address_county          = kwargs.get('building_address_county', None)
		self.building_address_town            = kwargs.get('building_address_town', None)
		self.building_n_stories_above_ground  = kwargs.get('building_n_stories_above_ground', None)
		self.building_n_stories_below_ground  = kwargs.get('building_n_stories_below_ground', None)
		self.building_floor_offset            = kwargs.get('building_floor_offset', 0)

		self.energy_section                   = kwargs.get('energy_section', [])
		self.n_energy_section                 = len(self.energy_section)
		self.exclusive_energy_section         = kwargs.get('exclusive_energy_section', [])
		self.n_exclusive_energy_section       = len(self.exclusive_energy_section)

		# 2. Building simulation information
		self.coef_eff_ac_residential          = kwargs.get('coef_eff_ac_residential', 0.9)
		self.coef_eff_ac_nonresidential       = kwargs.get('coef_eff_ac_nonresidential', 0.9)
		self.coef_eff_envelope                = kwargs.get('coef_eff_envelope', 0.9)
		self.coef_eff_lighting_residential    = kwargs.get('coef_eff_lighting_residential', 0.9)
		self.coef_eff_lighting_nonresidential = kwargs.get('coef_eff_lighting_nonresidential', 0.9)

		# Numbers of suites and rooms
		if (self.building_class == 'apartment'):

			self.n_suite         = kwargs.get('n_suite', None)
			self.n_household_big = kwargs.get('n_household_big', None)

			if (self.n_suite is None): raise ValueError('Numbers of suites are not defined.')
			if (self.n_household_big is None): raise ValueError('Numbers of households with more than two rooms are not defined.')

		# =========================================================================================
		#
		# Error handling
		#
		# =========================================================================================

		# Building location is not defined
		if (self.building_coordinate is None) and ((self.building_address_county is None) and (self.building_address_town is None)): raise ValueError('Building location is not defined.')

		# Building system is not available
		if (self.estimation_system not in ['R-BERS']): raise ValueError('Building system is not available. Only BERSe is available now.')

		# =========================================================================================
		#
		# Initialize the building object
		#
		# =========================================================================================

		# Basic information
		self.building_n_stories_total = self.building_n_stories_above_ground + self.building_n_stories_below_ground + self.building_floor_offset

		# =========================================================================================

		# Climate zone and urban coefficient
		if (self.building_coordinate is not None): self.building_address_county, self.building_address_town = self._get_address_coordinate(*self.building_coordinate)
		
		self.building_cz = tool.get_climatezone(self.building_address_county, self.building_address_town)
		self.building_ur = tool.get_urbanregion(self.building_address_county, self.building_address_town)

	def estimate(self) -> tuple:

		"""
		This method is used to estimate the EUI score of a building.
		The primary target for estimation in R-BERS is CEI. Therefore, the EUIs outputed by this method is for reference only.
		===========================================================================================

		Arguments:

			None

		Output:

			None
		"""

		# Calculate average hydraulic head of water tower
		self.hydraulic_head_total = self._calc_average_hydraulic_head_watertower()

		# =========================================================================================
		#
		# Error handling
		#
		# =========================================================================================

		# n_elevator/n_escalator is not equal to the length of elevator/escalator list
		if (self.n_elevator != len(self.elevator)): raise ValueError('n_elevator is not equal to the length of elevator list.')

		# =========================================================================================
		#
		# Check for energy section and exclusive energy section
		#
		# =========================================================================================

		# Energy section and exclusive energy section are not defined
		if (self.n_energy_section == 0) and (self.n_exclusive_energy_section == 0): raise ValueError('Energy section and exclusive energy section are not defined.')

		# Change all ac_operation to 'INTERVAL' in all energy section (the ac_operation in R-BERS is not used)
		for i_es in self.energy_section: i_es.ac_operation = 'INTERVAL'

		# =========================================================================================
		# 
		# Calculate CEI score scale
		# 
		# =========================================================================================

		# Read the files for EUI score: EUI median, maximum, and minimum
		df_eui_m                        = pd.read_csv(__path__ + '../data/eui_criteria/eui_criteria.m.csv')
		df_eui_max                      = pd.read_csv(__path__ + '../data/eui_criteria/eui_criteria.max.csv')
		df_eui_min                      = pd.read_csv(__path__ + '../data/eui_criteria/eui_criteria.min.csv')

		df_eui_m['Energy_Section_ID']   = df_eui_m['Energy_Section'].str.split('. ').str[0]
		df_eui_max['Energy_Section_ID'] = df_eui_max['Energy_Section'].str.split('. ').str[0]
		df_eui_min['Energy_Section_ID'] = df_eui_min['Energy_Section'].str.split('. ').str[0]

		# Extract EUI values from EUI score tables
		for i_es in self.energy_section:

			i_es.leui_min   = df_eui_min.loc[df_eui_min['Energy_Section_ID']==i_es.id, 'LEUI'].values[0]
			i_es.leui_m     = df_eui_m.loc[df_eui_m['Energy_Section_ID']==i_es.id, 'LEUI'].values[0]
			i_es.leui_max   = df_eui_max.loc[df_eui_max['Energy_Section_ID']==i_es.id, 'LEUI'].values[0]
			i_es.aeui_min   = df_eui_min.loc[df_eui_min['Energy_Section_ID']==i_es.id, 'AEUI_{}_{}'.format(self.building_cz, i_es.ac_operation.upper())].values[0]
			i_es.aeui_m     = df_eui_m.loc[df_eui_m['Energy_Section_ID']==i_es.id, 'AEUI_{}_{}'.format(self.building_cz, i_es.ac_operation.upper())].values[0]
			i_es.aeui_max   = df_eui_max.loc[df_eui_max['Energy_Section_ID']==i_es.id, 'AEUI_{}_{}'.format(self.building_cz, i_es.ac_operation.upper())].values[0]

		# Error handling
		# aeui_min, aeui_m, or aeui_max include NaN
		if ([i.aeui_min for i in self.energy_section] + [i.aeui_m for i in self.energy_section] + [i.aeui_max for i in self.energy_section]).count(np.nan) > 0: raise ValueError('aeui_min, aeui_m, or aeui_max include NaN.')

		# Calculate area, EUI for common energy sections
		self.est_a_es_comm   = np.nansum([i.a for i in self.energy_section])

		if (self.building_type == 'house'):
			
			# Fixed equipment carbon emission
			self.est_fce                    = 4.0 * np.nansum([i.quantity * i.coef_emission_intensity for i in self.heater])

			# Calculate CEI for energy sections
			self.est_cei_g                  = 0.9 * np.nansum([(i.aeui_m + i.leui_m) * i.a * constant.coef_ece for i in self.energy_section] + self.est_fce) / self.est_a_es_comm
			self.est_cei_n                  = 0.7 * np.nansum([(i.aeui_m + i.leui_m) * i.a * constant.coef_ece for i in self.energy_section] + self.est_fce) / self.est_a_es_comm
			self.est_cei_m                  = np.nansum([(i.aeui_m + i.leui_m) * i.a * constant.coef_ece for i in self.energy_section] + self.est_fce) / self.est_a_es_comm
			self.est_cei_max                = np.nansum([(i.aeui_max + i.leui_max) * i.a * constant.coef_ece for i in self.energy_section] + self.est_fce) / self.est_a_es_comm

		elif (self.building_type == 'apartment'):

			# Total number of households (suite + household with more than 2 rooms)
			self.est_n_household            = self.n_suite + self.n_household_big

			# Mean number of people per household
			self.est_n_people_per_household = (2 * self.n_suite + 3 * self.n_household_big) / (self.n_suite + self.n_household_big)

			# Fixed equipment carbon emission
			self.est_fce                    = self.est_n_people_per_household * np.nansum([i.quantity * i.coef_emission_intensity for i in self.heater])

			# Public equipment carbon emission
			self.est_mce                    = (self._calc_ec_ventilation_total_parking() + self._calc_ec_total_elevator() + self._calc_ec_water_pumping_total()) * constant.coef_ece
			
			# Calculate CEI for energy sections
			self.est_cei_g                  = 0.9 * (np.nansum([(i.aeui_m + i.leui_m) * i.a * constant.coef_ece for i in self.energy_section]) + self.est_fce + self.est_mce) / self.est_a_es_comm
			self.est_cei_n                  = 0.7 * (np.nansum([(i.aeui_m + i.leui_m) * i.a * constant.coef_ece for i in self.energy_section]) + self.est_fce + self.est_mce) / self.est_a_es_comm
			self.est_cei_m                  = (np.nansum([(i.aeui_m + i.leui_m) * i.a * constant.coef_ece for i in self.energy_section]) + self.est_fce + self.est_mce) / self.est_a_es_comm
			self.est_cei_max                = (np.nansum([(i.aeui_max + i.leui_max) * i.a * constant.coef_ece for i in self.energy_section]) + self.est_fce + self.est_mce) / self.est_a_es_comm
		
		# =========================================================================================
		# 
		# Calculate simulated CEI
		# 
		# =========================================================================================

		if (self.building_type == 'house'):
			
			# Calculate total carbon emission
			self.est_total_simulated_carbon_emission = \
				self._calc_ace_total_simulated() + \
				self._calc_lce_total_simulated() + \
				self._calc_fce_total_simulated()
		
		elif (self.building_type == 'apartment'):

			# Calculate total carbon emission
			self.est_total_simulated_carbon_emission = \
				self._calc_ace_total_simulated() + \
				self._calc_lce_total_simulated() + \
				self._calc_fce_total_simulated() + \
				self._calc_mce_total_simulated()
		
		# Calculate simulated CEI
		self.est_cei = self.est_total_simulated_carbon_emission / self.est_a_es_comm

		# =========================================================================================
		# 
		# Calculate score
		# 
		# =========================================================================================

		# Calculate score
		if (self.est_cei <= self.est_cei_g):

			self.est_score = 50 + 40 * (self.est_cei_g - self.est_cei) / (self.est_cei_g - self.est_cei_n)
		
		elif (self.est_cei > self.est_cei_g):

			self.est_score = 50 * (self.est_cei_max - self.est_cei) / (self.est_cei_max - self.est_cei_g)

		# Compress the score to 0-100
		self.est_score = min(max(self.est_score, 0), 100)

		# Caclulate score level
		if (self.est_score >= 90): self.est_score_level = '1+'
		elif (self.est_score >= 80): self.est_score_level = '1'
		elif (self.est_score >= 70): self.est_score_level = '2'
		elif (self.est_score >= 60): self.est_score_level = '3'
		elif (self.est_score >= 50): self.est_score_level = '4'
		elif (self.est_score >= 40): self.est_score_level = '5'
		elif (self.est_score >= 20): self.est_score_level = '6'
		elif (self.est_score >= 0): self.est_score_level = '7'

		# =========================================================================================
		# 
		# Finish estimation
		# 
		# =========================================================================================

		# Calculate EUI for reference
		self.est_eui     = self.est_cei / constant.coef_ece
		self.est_eui_max = self.est_cei_max / constant.coef_ece
		self.est_eui_m   = self.est_cei_m   / constant.coef_ece
		self.est_eui_n   = self.est_cei_n   / constant.coef_ece
		self.est_eui_g   = self.est_cei_g   / constant.coef_ece

		return
		
	def _calc_average_hydraulic_head_watertower(self):

		"""
		This method is used to calculate the average hydraulic head of all water towers.
		If the number of water towers is larger than 1, the water pumping capacity (water_pumping_capacity) will be used as weights.
		If no water tower is created, 0 is returned.
		===========================================================================================

		Arguments:

			None

		Output:

			average_hydraulic_head_watertower (float): Average hydraulic head of all water towers
		"""
		
		# No water tower is created
		if (self.n_watertower == 0):
			
			average_hydraulic_head_watertower = 0
		
		elif (self.n_watertower == 1):

			average_hydraulic_head_watertower = self.watertower[0].standard_hydraulic_head_total

		else:
			
			average_hydraulic_head_watertower = np.average([i.standard_hydraulic_head_total for i in self.watertower], weights=[i.water_pumping_capacity for i in self.watertower])

		return average_hydraulic_head_watertower
	
	def _calc_ec_ventilation_total_parking(self) -> float:

		"""
		This method is used to calculate the total ec of ventilation in underground parking garage.
		===========================================================================================

		Arguments:

			None

		Output:

			ec_ventilation_parking (float): The energy consumption for ventilation in parking.
		"""

		# Add up the ec of ventilation in parking for all parking garage objects
		ec_ventilation_total_parking = np.nansum([i.a * i.ec_ventilation for i in self.parkinggarage])

		return ec_ventilation_total_parking
	
	def _calc_ec_ventilation_total_simulated_parking(self) -> float:

		"""
		This method is used to calculate the total simulated ec of ventilation in underground parking garage.
		===========================================================================================

		Arguments:

			None

		Output:

			ec_ventilation_parking (float): The simulated energy consumption for ventilation in parking.
		"""

		# Add up the ec of ventilation in parking for all parking garage objects
		ec_ventilation_total_simulated_parking = np.nansum([i.a * i.ec_ventilation * i.coef_eff_powersaving_ventilation for i in self.parkinggarage])

		return ec_ventilation_total_simulated_parking
	
	def _calc_ec_total_elevator(self) -> float:

		"""
		This method is used to calculate the energy consumption of elevators.
		If no elevator is created, 0 is returned.
		===========================================================================================

		Arguments:

			None

		Output:

			ec_total_elevator (float): The total energy consumption of all elevators
		"""
		
		# No elevator is created
		if (self.n_elevator == 0):
			
			ec_total_elevator = 0
		
		else:
			
			ec_total_elevator = np.nansum([i.coef_ec * i.coef_usage_h for i in self.elevator])

		return ec_total_elevator
	
	def _calc_ec_total_simulated_elevator(self) -> float:

		"""
		This method is used to calculate the simulated energy consumption of elevators.
		If no elevator is created, 0 is returned.
		===========================================================================================

		Arguments:

			None

		Output:

			ec_total_elevator (float): The simulated energy consumption of all elevators
		"""
		
		# No elevator is created
		if (self.n_elevator == 0):
			
			ec_total_simulated_elevator = 0
		
		else:
			
			ec_total_simulated_elevator = np.nansum([i.coef_ec * i.coef_usage_h * i.coef_eff for i in self.elevator])

		return ec_total_simulated_elevator
	
	def _calc_ec_water_pumping_total(self) -> float:

		"""
		This method is used to calculate the energy consumption of water pumping.
		===========================================================================================

		Arguments:

			None

		Output:

			ec_water_pumping_total (float): The total energy consumption of water pumping.
		"""

		# Water consumption for residential usage
		water_residential    = 0.6 * (225/1000) * 365 * self.est_n_people_per_household * self.est_n_household

		# Water consumption for non-residential usage
		if (self.n_nonresidential_energy_section == 0):

			water_nonresidential = 0

		else:

			water_nonresidential = 0.6 * 365 * np.nansum([i.a * i.coef_effective_area * i.coef_people_density * i.coef_water_density for i in self.nonresidential_energy_section]) * (1/1000)

		# Calculate the total water consumption
		ec_water_pumping_total = 0.0183 * (water_residential + water_nonresidential) * self.hydraulic_head_total

		return ec_water_pumping_total
	
	def _calc_ec_water_pumping_total_simulated(self) -> float:

		"""
		This method is used to calculate the simulated energy consumption of water pumping.
		===========================================================================================

		Arguments:

			None

		Output:

			ec_water_pumping_total (float): The simulated energy consumption of water pumping.
		"""

		# Water consumption for residential usage
		water_residential    = 0.6 * (225/1000) * 365 * self.est_n_people_per_household * self.est_n_household

		# Water consumption for non-residential usage
		if (self.n_nonresidential_energy_section == 0):

			water_nonresidential = 0

		else:

			water_nonresidential = 0.6 * 365 * np.nansum([i.a * i.coef_effective_area * i.coef_people_density * i.coef_water_density for i in self.nonresidential_energy_section]) * (1/1000)

		# Calculate the total water consumption
		ec_water_pumping_total_simulated = 0.0183 * (water_residential + water_nonresidential) * self.hydraulic_head_total * self._calc_coef_eff_ec_water_pumping()

		return ec_water_pumping_total_simulated
	
	def _calc_ace_total_simulated(self) -> float:

		"""
		This method is used to calculate the total simulated carbon emission of air conditioning.
		===========================================================================================

		Arguments:

			None

		Output:

			ace_total_simulated (float): The total simulated carbon emission of air conditioning.
		"""

		# Calculate the total carbon emission of air conditioning
		ace_total_simulated = \
			np.nansum([i.aeui_m * i.a * constant.coef_ece * (self.coef_eff_ac_residential - 0.12 * self.coef_eff_envelope) for i in self.energy_section if i.id.startswith('R')]) + \
			np.nansum([i.aeui_m * i.a * constant.coef_ece * (self.coef_eff_ac_nonresidential - 0.12 * self.coef_eff_envelope) for i in self.energy_section if i.id.startswith('P')])
		
		return ace_total_simulated
	
	def _calc_lce_total_simulated(self) -> float:

		"""
		This method is used to calculate the total simulated carbon emission of lighting.
		===========================================================================================

		Arguments:

			None

		Output:

			lce_total_simulated (float): The total simulated carbon emission of lighting.
		"""

		# Calculate the total carbon emission of lighting
		lce_total_simulated = \
			np.nansum([i.leui_m * i.a * constant.coef_ece * self.coef_eff_lighting_residential for i in self.energy_section if i.id.startswith('R')]) + \
			np.nansum([i.leui_m * i.a * constant.coef_ece * self.coef_eff_lighting_nonresidential for i in self.energy_section if i.id.startswith('P')])

		return lce_total_simulated
	
	def _calc_fce_total_simulated(self) -> float:

		"""
		This method is used to calculate the total simulated carbon emission of fixed equipment.
		===========================================================================================

		Arguments:

			None

		Output:

			fce_total_simulated (float): The total simulated carbon emission of fixed equipment.
		"""

		# Calculate the total carbon emission of fixed equipment
		fce_total_simulated = \
			self.est_n_people_per_household * (
				np.nansum([i.quantity * i.coef_emission_intensity * i.coef_eff * i.coef_eff_powersaving_hotwater_pipeline for i in self.heater if i.type in ['1', '2.1', '2.2', '2.3']]) + \
				np.nansum([i.quantity * i.coef_emission_intensity * i.coef_eff for i in self.heater if i.type in ['3', '4.1', '4.2']])
			)

		return fce_total_simulated
	
	def _calc_mce_total_simulated(self) -> float:

		"""
		This method is used to calculate the total simulated carbon emission of public equipment.
		===========================================================================================

		Arguments:

			None

		Output:

			mce_total_simulated (float): The total simulated carbon emission of public equipment.
		"""

		# Calculate the total carbon emission of public equipment
		mce_total_simulated = (self._calc_ec_ventilation_total_simulated_parking() + self._calc_ec_total_simulated_elevator() + self._calc_ec_water_pumping_total_simulated()) * constant.coef_ece

		return mce_total_simulated
	
	def _calc_coef_eff_ec_water_pumping(self) -> float:

		"""
		This method is used to calculate the coefficient of energy consumption of water pumping (PEB).
		PEB has minimum value of 0.5, indicating that the energy consumption of water pumping is just enough to pump water to the top of the building.
		If PEB is 1 (reference value), it means that the energy consumption of water pumping is two times of the standard value.

				  Qd * PHd
		PEB = ----------------
		        2 * Qc * PHc
		
		Qd: Design water pumping capacity [volume per time; CMH or LPM]
		Qc: Standard water pumping capacity [volume per time; CMH or LPM]
		PHd: Design total hydraulic head [m]
		PHc: Standard total hydraulic head [m]
		===========================================================================================

		Arguments:

			None

		Output:

			coef_eff_ec_water_pumping (float): The coefficient of energy consumption of water pumping.
		"""

		# Calculate the coefficient of energy consumption of water pumping for every water towers
		for i in self.watertower:
			
			# Calculate standard daily water consumption
			if (self.building_address_county == '臺北市'):

				standard_daily_water_consumption = 3 * 225 * self.est_n_household * (1/1000)

			else:

				standard_daily_water_consumption = 4 * 250 * self.est_n_household * (1/1000)
			
			# Safety factor
			standard_daily_water_consumption *= 1.2

			# Calculate standard water pumping capacity
			standard_water_pumping_capacity   = standard_daily_water_consumption / 10

			# Convert the unit of standard water pumping capacity from m3/h to LPM
			standard_water_pumping_capacity  *= 1000 / 60

			# Calculate PEB
			i.coef_eff_ec_water_pumping = (i.water_pumping_capacity * i.hydraulic_head_total) / (2 * standard_water_pumping_capacity * i.standard_hydraulic_head_total)

		if (self.n_watertower == 1):
			
			coef_eff_ec_water_pumping = self.watertower[0].coef_eff_ec_water_pumping

		else:

			coef_eff_ec_water_pumping = np.average([i.coef_eff_ec_water_pumping for i in self.watertower], weights=[i.water_pumping_capacity for i in self.watertower])

		return coef_eff_ec_water_pumping