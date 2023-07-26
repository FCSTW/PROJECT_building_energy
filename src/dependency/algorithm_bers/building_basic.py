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
from . import tool

import numpy as np
import pandas as pd
import geopandas as gpd
import os

__path__ = os.path.dirname(__file__).replace('\\', '/').replace('C:/', '/') + '/'

class Building():

	"""
	This class is used to create a building object
	"""

	def __init__(self, **kwargs):

		"""
		This method is used to initialize a building object.
		===========================================================================================

		Arguments:

			None

		Output:

			None
		"""

		# Initialize the building object
		# 1. Building information
		# 1-a. Estimation information
		self.estimation_system               = kwargs.get('estimation_system', None)
		self.building_type                   = kwargs.get('building_type', None)

		# 1-b. Basic information
		self.building_coordinate             = kwargs.get('building_coordinate', None)
		self.building_address_county         = kwargs.get('building_address_county', None)
		self.building_address_town           = kwargs.get('building_address_town', None)
		self.building_es_comm                = kwargs.get('building_es_comm', None)
		self.building_es_exc                 = kwargs.get('building_es_exc', None)
		self.building_n_stories_above_ground = kwargs.get('building_n_stories_above_ground', None)
		self.building_n_stories_below_ground = kwargs.get('building_n_stories_below_ground', None)
		self.building_floor_offset           = kwargs.get('building_floor_offset', 0)

		# 1-c. Energy consumption
		self.ec                              = kwargs.get('ec', None)
		self.ec_other                        = kwargs.get('ec_other', None)
		self.est_q_rw                        = kwargs.get('est_q_rw', 0)
		self.ec_heating_comm                 = kwargs.get('ec_heating_comm', 'HE')
		self.height_watertower	             = kwargs.get('height_watertower', None)

		# 2. Building information
		# Elevator information
		self.elevator                        = kwargs.get('elevator', [])
		self.n_elevator                      = len(self.elevator)

		# Escalator information
		self.escalator                       = kwargs.get('escalator', [])
		self.n_escalator                     = len(self.escalator)

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

		# =========================================================================================
		# Error handling
		# Building information for estimation is not defined
		if (self.estimation_system is None): raise ValueError('Estimation system is not defined.')
		if (self.building_type is None): raise ValueError('Building type is not defined.')

		# Building location is not defined
		if (self.building_coordinate is None) and ((self.building_address_county is None) and (self.building_address_town is None)): raise ValueError('Building location is not defined.')

		# building_es_comm syntax error: AC_Operation contain the string except 'CONTINUE' and 'INTERVAL' (case insensitive)
		if not (self.building_es_comm['AC_Operation'].str.contains('CONTINUE|INTERVAL', case=False).all()): raise ValueError('building_es_comm syntax error: AC_Operation contain the string except CONTINUE and INTERVAL (case insensitive).')

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
		
		self.building_cz = self._get_climatezone(self.building_address_county, self.building_address_town)
		self.building_ur = self._get_urbanregion(self.building_address_county, self.building_address_town)

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

			est_eui (float): The estimated EUI of a building.

			est_eui_min (float): The minimum estimated EUI of a building.

			est_eui_g (float): The green building criteria estimated EUI of a building.

			est_eui_m (float): The median estimated EUI of a building.

			est_eui_max (float): The maximum estimated EUI of a building.

			est_score (float): The estimated score of a building.

			est_score_level (str): The estimated score level of a building.
		"""

		# =========================================================================================
		#
		# Get SO_r (ratio of operation) for specific energy sections
		#
		# =========================================================================================

		df_es_comm_temp                 = self.building_es_comm.copy()
		df_es_comm_temp['SO_r']         = self.building_es_comm.apply(self._get_coef_usage_r_operation, axis=1)
		self.building_es_comm           = df_es_comm_temp.copy()
		del df_es_comm_temp

		# =========================================================================================
		# 
		# Calculate EUI score scale
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
		df_es_comm_temp                 = self.building_es_comm.copy()
		df_es_comm_temp['eeui_m']       = self.building_es_comm.apply(lambda x: df_eui_m.loc[df_eui_m['Energy_Section_ID']==x['Section_ID'], 'EEUI'].values[0], axis=1)
		df_es_comm_temp['leui_min']     = self.building_es_comm.apply(lambda x: df_eui_min.loc[df_eui_min['Energy_Section_ID']==x['Section_ID'], 'LEUI'].values[0], axis=1)
		df_es_comm_temp['leui_m']       = self.building_es_comm.apply(lambda x: df_eui_m.loc[df_eui_m['Energy_Section_ID']==x['Section_ID'], 'LEUI'].values[0], axis=1)
		df_es_comm_temp['leui_max']     = self.building_es_comm.apply(lambda x: df_eui_max.loc[df_eui_max['Energy_Section_ID']==x['Section_ID'], 'LEUI'].values[0], axis=1)
		df_es_comm_temp['aeui_min']     = self.building_es_comm.apply(lambda x: df_eui_min.loc[df_eui_min['Energy_Section_ID']==x['Section_ID'], 'AEUI_{}_{}'.format(self.building_cz, x['AC_Operation'].upper())].values[0], axis=1)
		df_es_comm_temp['aeui_m']       = self.building_es_comm.apply(lambda x: df_eui_m.loc[df_eui_m['Energy_Section_ID']==x['Section_ID'], 'AEUI_{}_{}'.format(self.building_cz, x['AC_Operation'].upper())].values[0], axis=1)
		df_es_comm_temp['aeui_max']     = self.building_es_comm.apply(lambda x: df_eui_max.loc[df_eui_max['Energy_Section_ID']==x['Section_ID'], 'AEUI_{}_{}'.format(self.building_cz, x['AC_Operation'].upper())].values[0], axis=1)
		df_es_comm_temp['meaneui_m']    = self.building_es_comm.apply(lambda x: df_eui_m.loc[df_eui_m['Energy_Section_ID']==x['Section_ID'], 'EUI_Mean'].values[0], axis=1)
		df_es_comm_temp['totaleui_m']   = self.building_es_comm.apply(lambda x: df_eui_m.loc[df_eui_m['Energy_Section_ID']==x['Section_ID'], 'TotalEUI'].values[0], axis=1)
		self.building_es_comm = df_es_comm_temp.copy()
		del df_es_comm_temp

		# Error handling
		# aeui_min, aeui_m, or aeui_max include NaN
		if (self.building_es_comm[['aeui_min', 'aeui_m', 'aeui_max']].isna().values.any()): raise ValueError('aeui_min, aeui_m, or aeui_max include NaN.')

		# Calculate area, EUI for common energy sections
		self.est_a_es_comm   = self.building_es_comm['Area'].sum().round(2)
		self.est_aeui_min    = self.building_es_comm['Area'].dot(self.building_es_comm['aeui_min']) / self.est_a_es_comm
		self.est_aeui_m      = self.building_es_comm['Area'].dot(self.building_es_comm['aeui_m']) / self.est_a_es_comm
		self.est_aeui_max    = self.building_es_comm['Area'].dot(self.building_es_comm['aeui_max']) / self.est_a_es_comm
		self.est_leui_min    = self.building_es_comm['Area'].dot(self.building_es_comm['leui_min']) / self.est_a_es_comm
		self.est_leui_m      = self.building_es_comm['Area'].dot(self.building_es_comm['leui_m']) / self.est_a_es_comm
		self.est_leui_max    = self.building_es_comm['Area'].dot(self.building_es_comm['leui_max']) / self.est_a_es_comm
		self.est_eeui_m      = self.building_es_comm['Area'].dot(self.building_es_comm['eeui_m']) / self.est_a_es_comm

		self.est_eui_g       = self.building_ur * (0.8 * self.est_aeui_m + 0.8 * self.est_leui_m + self.est_eeui_m)
		self.est_eui_min     = self.building_ur * (self.est_aeui_min + self.est_leui_min + self.est_eeui_m)
		self.est_eui_m       = self.building_ur * (self.est_aeui_m + self.est_leui_m + self.est_eeui_m)
		self.est_eui_max     = self.building_ur * (self.est_aeui_max + self.est_leui_max + self.est_eeui_m)

		# Calculate area, EUI for exclusive energy sections
		self.est_a_es_exc    = self.building_es_exc['Area'].sum().round(2)
		self.est_e_n         = self._calc_e_n(self.building_es_exc)

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
		
		self.est_q_shw       = \
			self._calc_hotwater_total_swimmingpool() + \
			self._calc_hotwater_total_spa()
		
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
		self.est_aeui_m_adj  = (self.building_es_comm['Area']*self.building_es_comm['SO_r']).dot(self.building_es_comm['aeui_m']) / self.est_a_es_comm
		self.est_leui_m_adj  = (self.building_es_comm['Area']*self.building_es_comm['SO_r']).dot(self.building_es_comm['leui_m']) / self.est_a_es_comm
		self.est_eeui_m_adj  = (self.building_es_comm['Area']*self.building_es_comm['SO_r']).dot(self.building_es_comm['eeui_m']) / self.est_a_es_comm
		
		self.est_eui_m_adj   = self.building_ur * (self.est_aeui_m_adj + self.est_leui_m_adj + self.est_eeui_m_adj)

		# Calculate unbiased eui
		self.est_eui         = self.est_eui_m + self.est_eui_main - self.est_eui_m_adj

		# =========================================================================================
		# 
		# Calculate score
		# 
		# =========================================================================================

		# Calculate score
		if (self.est_eui <= self.est_eui_g):

			self.est_score = min(50 + 50 * (self.est_eui_g - self.est_eui) / (self.est_eui_g - self.est_eui_min), 100)
		
		elif (self.est_eui > self.est_eui_g):

			self.est_score = max(50 * (self.est_eui_max - self.est_eui) / (self.est_eui_max - self.est_eui_g), 0)

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

		return \
			self.est_eui, \
			self.est_eui_min, self.est_eui_g, self.est_eui_m, self.est_eui_max, \
			self.est_score, self.est_score_level

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

		new_elevator = building_facility.Elevator(building_type=self.building_type, **kwargs)
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

		new_escalator = building_facility.Escalator(building_type=self.building_type, **kwargs)
		self.escalator.append(new_escalator)
		self.n_escalator = len(self.escalator)

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
			building_type=self.building_type,
			building_cz=self.building_cz,
			**kwargs
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
			building_type=self.building_type,
			building_cz=self.building_cz,
			**kwargs
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

		new_sportbathroom = building_facility.Sportbathroom(
			building_type=self.building_type,
			building_cz=self.building_cz,
			**kwargs
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
			building_type=self.building_type,
			building_cz=self.building_cz,
			**kwargs
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
			building_type=self.building_type,
			building_cz=self.building_cz,
			**kwargs
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
			building_type=self.building_type,
			building_cz=self.building_cz,
			**kwargs
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
			building_type=self.building_type,
			building_cz=self.building_cz,
			**kwargs
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
			building_type=self.building_type,
			building_cz=self.building_cz,
			**kwargs
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

		new_datacenter = building_facility.DataCenter(building_type=self.building_type, **kwargs)
		self.datacenter.append(new_datacenter)
		self.n_datacenter = len(self.datacenter)

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
	
	def _calc_water_total_comm(self):

		"""
		This method is used to calculate the water consumption of all common energy sections.
		===========================================================================================

		Arguments:

			None

		Output:

			water_total_comm (float): Water consumption of all common energy sections
		"""
		
		water_total_comm = np.nansum([i['Area'] * tool.get_coef_usage_i_water(i['Section_ID']) for _, i in self.building_es_comm.iterrows()])

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
			
			water_total_hospital = 73.0 * np.nansum([i.n_hospitalbed * i.coef_usage_r_hospitalbed for i in self.hospital])

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
			
			water_total_sportbathroom = 0.00036 * np.nansum([i.a * i.coef_usage_h for i in self.sportbathroom])

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
		if (self.building_es_comm[self.building_es_comm['AC_Type'].str.upper()=='WATERCOOLED'].empty):
			
			water_total_watercooled = 0
		
		else:
			
			water_total_watercooled = np.nansum([(0.00036 * tool.get_coef_usage_h_ac(i['Section_ID'], self.building_cz, i['AC_Operation']) + 0.32) * i['Area'] for _, i in self.building_es_comm.iterrows() if str(i['AC_Type']).upper()=='WATERCOOLED'])

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
		
		ec_water_pumping_total_comm = 0.02 * (self.height_watertower + 6.0) * (self.est_q_w + self.est_q_aw - self.est_q_rw)

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
			es_water_heating_total_swimmingpool = np.average([i.ec_heating for i in self.swimmingpool], weights=[i.v for i in self.swimmingpool]) * self.est_q_shw

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
			es_water_heating_total_spa = np.average([i.ec_heating for i in self.spa], weights=[i.v for i in self.spa]) * self.est_q_shw

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
	
	def _get_climatezone(self, county, town):

		"""
		This method is used to get the climate zone of a building by address.
		===========================================================================================
		
		Arguments:

			county (str): County of the building

			town (str): Town of the building

		Output:

			climatezone (str): Climate zone of the building. N, C, or S.
		"""

		# Read the file for climate zone
		df_town_climatezone = pd.read_csv(__path__ + '../data/coef_climatezone/coef_climatezone.csv')

		# Get the climate zone
		climatezone         = df_town_climatezone.loc[(df_town_climatezone['COUNTYNAME']==county)&(df_town_climatezone['TOWNNAME']==town), 'Climate_Zone'].values[0]

		return climatezone

	def _get_urbanregion(self, county, town):

		"""
		This method is used to get the urban region of a building by address.
		===========================================================================================
		
		Arguments:

			county (str): County of the building

			town (str): Town of the building

		Output:

			urbanregion (str): Urban region of the building. N, C, or S.
		"""

		# Read the file for urban region
		df_town_urbanregion = pd.read_csv(__path__ + '../data/coef_urbanregion/coef_urbanregion.csv')

		# Get the urban region
		urbanregion         = df_town_urbanregion.loc[(df_town_urbanregion['COUNTYNAME']==county)&(df_town_urbanregion['TOWNNAME']==town), 'Urban_Region'].values[0]

		if (urbanregion == 'A'): urbanregion = 1.0
		elif (urbanregion == 'B'): urbanregion = 0.95
		elif (urbanregion == 'C'): urbanregion = 0.8
		else: urbanregion = 0.7

		return urbanregion
	
	def _calc_e_n(self, df_es_exc):

		"""
		This method is used to calculate the energy consumption of exclusive sections.
		===========================================================================================

		Arguments:

			df_es_exc (pandas.DataFrame): DataFrame of exclusive sections

		Output:

			en (float): Energy consumption of exclusive sections
		"""

		# Define masking function
		mask_section = lambda x: df_es_exc['Section_ID']==x

		# Deep copy
		df_es_exc_temp = df_es_exc.copy()

		# =========================================================================================
		# 
		# Class 1: EUI + area
		# 
		# =========================================================================================
		
		# N1-1-1
		if (mask_section('N1-1-1').any()): df_es_exc_temp.loc[mask_section('N1-1-1'), 'en'] = 330 * df_es_exc.loc[mask_section('N1-1-1'), 'Area'].values[0]

		# N1-1-2
		if (mask_section('N1-1-2').any()): df_es_exc_temp.loc[mask_section('N1-1-2'), 'en'] = 250 * df_es_exc.loc[mask_section('N1-1-2'), 'Area'].values[0]

		# N1-2-1
		if (mask_section('N1-2-1').any()): df_es_exc_temp.loc[mask_section('N1-2-1'), 'en'] = 665 * df_es_exc.loc[mask_section('N1-2-1'), 'Area'].values[0]

		# N1-2-2
		if (mask_section('N1-2-2').any()): df_es_exc_temp.loc[mask_section('N1-2-2'), 'en'] = 530 * df_es_exc.loc[mask_section('N1-2-2'), 'Area'].values[0]

		# N1-3-1
		if (mask_section('N1-3-1').any()): df_es_exc_temp.loc[mask_section('N1-3-1'), 'en'] = 1318 * df_es_exc.loc[mask_section('N1-3-1'), 'Area'].values[0]

		# N1-3-2
		if (mask_section('N1-3-2').any()): df_es_exc_temp.loc[mask_section('N1-3-2'), 'en'] = 900 * df_es_exc.loc[mask_section('N1-3-2'), 'Area'].values[0]

		# N1-4-1
		if (mask_section('N1-4-1').any()): df_es_exc_temp.loc[mask_section('N1-4-1'), 'en'] = 989 * df_es_exc.loc[mask_section('N1-4-1'), 'Area'].values[0]

		# N1-4-2
		if (mask_section('N1-4-2').any()): df_es_exc_temp.loc[mask_section('N1-4-2'), 'en'] = 675 * df_es_exc.loc[mask_section('N1-4-2'), 'Area'].values[0]

		# N1-5
		if (mask_section('N1-5').any()): df_es_exc_temp.loc[mask_section('N1-5'), 'en'] = 387 * df_es_exc.loc[mask_section('N1-5'), 'Area'].values[0]

		# N1-6
		if (mask_section('N1-6').any()): df_es_exc_temp.loc[mask_section('N1-6'), 'en'] = 1500 * df_es_exc.loc[mask_section('N1-6'), 'Area'].values[0]

		# N1-7
		if (mask_section('N1-7').any()): df_es_exc_temp.loc[mask_section('N1-7'), 'en'] = 530 * df_es_exc.loc[mask_section('N1-7'), 'Area'].values[0]

		# N3-1-1
		if (mask_section('N3-1-1').any()): df_es_exc_temp.loc[mask_section('N3-1-1'), 'en'] = 26.7 * df_es_exc.loc[mask_section('N3-1-1'), 'Area'].values[0]

		# N3-1-2
		if (mask_section('N3-1-2').any()): df_es_exc_temp.loc[mask_section('N3-1-2'), 'en'] = 35.3 * df_es_exc.loc[mask_section('N3-1-2'), 'Area'].values[0]

		# N3-2-1
		if (mask_section('N3-2-1').any()): df_es_exc_temp.loc[mask_section('N3-2-1'), 'en'] = 21.3 * df_es_exc.loc[mask_section('N3-2-1'), 'Area'].values[0]

		# N3-2-2
		if (mask_section('N3-2-2').any()): df_es_exc_temp.loc[mask_section('N3-2-2'), 'en'] = 29.9 * df_es_exc.loc[mask_section('N3-2-2'), 'Area'].values[0]

		# N3-3-1
		if (mask_section('N3-3-1').any()): df_es_exc_temp.loc[mask_section('N3-3-1'), 'en'] = 41.9 * df_es_exc.loc[mask_section('N3-3-1'), 'Area'].values[0]

		# N4-1
		if (mask_section('N4-1').any()): df_es_exc_temp.loc[mask_section('N4-1'), 'en'] = 3.2 * df_es_exc.loc[mask_section('N4-1'), 'Area'].values[0]

		# N4-2
		if (mask_section('N4-2').any()): df_es_exc_temp.loc[mask_section('N4-2'), 'en'] = 6.1 * df_es_exc.loc[mask_section('N4-2'), 'Area'].values[0]

		# N4-3
		if (mask_section('N4-3').any()): df_es_exc_temp.loc[mask_section('N4-3'), 'en'] = 80.0 * df_es_exc.loc[mask_section('N4-3'), 'Area'].values[0]

		# N5
		if (mask_section('N5').any()): df_es_exc_temp.loc[mask_section('N5'), 'en'] = 545 * df_es_exc.loc[mask_section('N5'), 'Area'].values[0]

		# N6
		if (mask_section('N6').any()): df_es_exc_temp.loc[mask_section('N6'), 'en'] = 910 * df_es_exc.loc[mask_section('N6'), 'Area'].values[0]

		# =========================================================================================
		# 
		# Class 2: usage
		# 
		# =========================================================================================

		# N2-1-1
		if (mask_section('N2-1-1').any()): df_es_exc_temp.loc[mask_section('N2-1-1'), 'en'] = self.n_hotelroom * 5.85 * 365 * self.coef_usage_r_hotelroom * 2.0
		
		# N2-1-2
		if (mask_section('N2-1-2').any()): df_es_exc_temp.loc[mask_section('N2-1-2'), 'en'] = self.n_hotelroom * 3.85 * 365 * self.coef_usage_r_hotelroom * 1.5

		# N2-2
		if (mask_section('N2-2').any()): df_es_exc_temp.loc[mask_section('N2-2'), 'en'] = self.n_hospitalbed * 0.93 * 365 * self.coef_usage_r_hospitalbed * 1.5

		# =========================================================================================
		# 
		# Class 3: usage + area
		# 
		# =========================================================================================

		# N2-1-3
		if (mask_section('N2-1-3').any()):

			if (self.n_diningarea == 0): raise ValueError('Please create diningarea first.')
			
			# Calculate summation of dining area and weighted average of n_meal_per_day
			sum_a_dining        = np.nansum([i.a for i in self.diningarea])
			mean_n_meal_per_day = np.average([i.n_meal_per_day for i in self.diningarea], weights=[i.a for i in self.diningarea])

			# Calculate es
			df_es_exc_temp.loc[mask_section('N2-1-3'), 'en'] = sum_a_dining * 0.09 * mean_n_meal_per_day * 365 * 0.7 * 1.5

		# =========================================================================================
		# 
		# Class 4: EUI + usage + area
		# 
		# =========================================================================================

		# N7
		if (mask_section('N7').any()): df_es_exc_temp.loc[mask_section('N7'), 'en'] = 0.124 * df_es_exc.loc[mask_section('N7'), 'Area'].values[0] * self.get_coef_usage_h('N7') * 1.5 

		# N8
		if (mask_section('N8').any()):
			
			if (self.n_datacenter == 0): raise ValueError('Please create data center first.')
			
			# Calculate es
			df_es_exc_temp.loc[mask_section('N8'), 'en'] = np.nansum([i.a * (2630 * i.coef_power_cabinetrack + 51) for i in self.datacenter])

		# =========================================================================================
		# 
		# Class 5: other
		# 
		# =========================================================================================

		# N9, N10, N12
		if (mask_section('N9').any()): df_es_exc_temp.loc[mask_section('N9'), 'en'] = 0
		if (mask_section('N10').any()): df_es_exc_temp.loc[mask_section('N10'), 'en'] = 0
		if (mask_section('N12').any()): df_es_exc_temp.loc[mask_section('N12'), 'en'] = 0

		# N11: raise error. Please use the other es
		if (mask_section('N11').any()): raise ValueError('Please avoid using N11. Use the other es instead.')

		# =========================================================================================
		#
		# Summation
		#
		# =========================================================================================

		# Rename variables
		df_es_exc = df_es_exc_temp.copy()
		del df_es_exc_temp

		# Calculate en
		en = df_es_exc['en'].sum()

		return en
	
	def _get_coef_usage_r_operation(self, row):

		"""
		This method is used to get the coefficient of actual operation for usage ratio.
		===========================================================================================

		Arguments:

			row (pandas.Series): Row of the DataFrame

		Output:

			coef_usage_r_operation (float): Coefficient of operation for usage ratio
		"""

		# Get variables
		section_id   = row['Section_ID']

		# Get coefficient of operation for usage ratio based on section id

		# Default value
		coef_usage_r_operation = 1.0

		# Exhibition area
		if (self.n_exhibitionarea != 0):

			if (section_id in ['D1', 'D2', 'D3', 'E1']):

				coef_usage_r_operation = 0.52 + 0.45 * np.nansum([i.a * i.coef_usage_d for i in self.exhibitionarea]) / np.nansum([i.a * 273 for i in self.exhibitionarea])

		# Performance area
		if (self.n_performancearea != 0):

			if (section_id in ['F1']):
				
				coef_usage_r_operation = 0.17 + 0.83 * np.average([i.coef_usage_d / tool.get_coef_usage_d('F1') for i in self.performancearea], weights=[i.a for i in self.performancearea])

			elif (section_id in ['F2']):

				coef_usage_r_operation = 0.21 + 0.77 * np.average([i.coef_usage_d / tool.get_coef_usage_d('F2') for i in self.performancearea], weights=[i.a for i in self.performancearea])

			elif (section_id in ['G1']):

				coef_usage_r_operation = 0.39 + 0.60 * np.average([i.coef_usage_d / tool.get_coef_usage_d('G1') for i in self.performancearea], weights=[i.a for i in self.performancearea])

			elif (section_id in ['G2']):

				coef_usage_r_operation = 0.31 + 0.67 * np.average([i.coef_usage_d / tool.get_coef_usage_d('G2') for i in self.performancearea], weights=[i.a for i in self.performancearea])
		
		# Hotel
		if (self.n_hotel != 0):

			if (section_id in ['H1']):

				coef_usage_r_operation = 0.58 + 0.571 * np.average([i.coef_usage_r_room for i in self.hotel], weights=[i.a for i in self.hotel])

		# Hospital
		if (self.n_hospital != 0):

			if (section_id in ['H2']):

				coef_usage_r_operation = 0.25 + 0.94 * np.average([i.coef_usage_r_hospitalbed for i in self.hospital], weights=[i.a for i in self.hospital])
		
		return coef_usage_r_operation