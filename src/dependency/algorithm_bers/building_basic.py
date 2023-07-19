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

import numpy as np
import pandas as pd
import geopandas as gpd
import os

__path__ = os.path.dirname(__file__).replace('\\', '/').replace('C:/', '/') + '/'

class Building():

	"""
	This class is used to create a building object
	"""

	#__path__ = os.path.dirname(__file__).replace('\\', '/').replace('C:/', '/') + '/'

	def __init__(self, **kwargs):

		"""
		This method is used to initialize a building object.
		===========================================================================================

		Arguments:

			estimation_system (str): The estimation system used to estimate the EUI score of a building.

			building_type (str): The type of a building.
		"""

		# Initialize the building object
		# 0. Building information for estimation
		self.estimation_system               = kwargs.get('estimation_system', None)
		self.building_type                   = kwargs.get('building_type', None)

		# 1. Building basic information
		self.building_coordinate             = kwargs.get('building_coordinate', None)
		self.building_address_county         = kwargs.get('building_address_county', None)
		self.building_address_town           = kwargs.get('building_address_town', None)
		self.building_n_stories_above_ground = kwargs.get('building_n_stories_above_ground', None)
		self.building_n_stories_below_ground = kwargs.get('building_n_stories_below_ground', None)
		self.ec_annual                       = kwargs.get('ec_annual', None)
		self.ec_other                        = kwargs.get('ec_other', None)
		self.wc_annual_rainfall	             = kwargs.get('wc_annual_rainfall', None)

		# 3. Building information for energy consumption sections
		self.energysection                   = kwargs.get('energysection', None)
		self.a_recreation                    = kwargs.get('a_recreation', None)
		self.a_dining                        = kwargs.get('a_dining', None)
		self.a_watercooledac                 = kwargs.get('a_watercooledac', None)
		self.a_exhibition                    = kwargs.get('a_exhibition', None)
		self.n_escalator                     = kwargs.get('n_escalator', None)
		self.coef_power_cabinetrack	         = kwargs.get('coef_power_cabinetrack', None)
		self.ec_heating_normal	             = kwargs.get('ec_heating_normal', None)
		self.ec_heating_recreation           = kwargs.get('ec_heating_recreation', None)
		self.height_watertower	             = kwargs.get('height_watertower', None)
		self.volume_swimmingpool             = kwargs.get('volume_swimmingpool', None)
		self.volume_spapool                  = kwargs.get('volume_spapool', None)
		self.coef_usage_r_swimmingpool       = kwargs.get('coef_usage_swimmingpool', None)
		self.coef_usage_r_spapool	         = kwargs.get('coef_usage_spapool', None)
		self.coef_usage_r_hospitalbed        = kwargs.get('coef_usage_hospitalbed', None)
		self.coef_usage_r_hotelroom          = kwargs.get('coef_usage_hotelroom', None)
		self.coef_usage_d_exhibition         = kwargs.get('coef_usage_d_exhibition', None)
		self.n_hospitalbed                   = kwargs.get('n_hospitalbed', None)
		self.n_hotelroom                     = kwargs.get('n_hotelroom', None)
		self.n_dining_meal_per_day           = kwargs.get('n_dining_meal_per_day', None)

		# 4. Elevator information
		self.elevator                        = kwargs.get('elevator', [])
		self.n_elevator                      = len(self.elevator)

		# 5. Escalator information
		self.escalator                       = kwargs.get('escalator', [])
		self.n_escalator                     = len(self.escalator)

		# Other information
		self.floor_offset                    = kwargs.get('floor_offset', 0)

		# Error handling
		# Building information for estimation is not defined
		if (self.estimation_system is None) or (self.building_type is None): raise ValueError('Building information for estimation is not defined.')

		# Building location is not defined
		if (self.building_coordinate is None) and ((self.building_address_county is None) and (self.building_address_town is None)): raise ValueError('Building location is not defined.')

		# =========================================================================================
		#
		# Initialize the building object
		#
		# =========================================================================================

		# Basic information
		self.building_n_stories_total = self.building_n_stories_above_ground + self.building_n_stories_below_ground + self.floor_offset

		# =========================================================================================

		# Climate zone and urban coefficient
		if (self.building_coordinate is not None): self.building_address_county, self.building_address_town = self._get_address_coordinate(*self.building_coordinate)
		
		self.building_cz = self._get_climatezone(self.building_address_county, self.building_address_town)
		self.building_uc = self._get_urbanregion(self.building_address_county, self.building_address_town)

		# =========================================================================================
		
		# Elevator

	def estimate(self):

		"""
		This method is used to estimate the EUI score of a building
		"""

		# =========================================================================================
		# 
		# Calculate EUI score scale
		# 
		# =========================================================================================

		# Read the files for EUI score: EUI median, maximum, and minimum
		df_eui_m                        = pd.read_csv(__path__ + '../data/eui_criteria/eui_criteria.m.csv')
		df_eui_max                      = pd.read_csv(__path__ + '../data/eui_criteria/eui_criteria.max.csv')
		df_eui_min                      = pd.read_csv(__path__ + '../data/eui_criteria/eui_criteria.m.csv')

		df_eui_m['Energy_Section_ID']   = df_eui_m['Energy_Section'].str.split('. ').str[0]
		df_eui_max['Energy_Section_ID'] = df_eui_max['Energy_Section'].str.split('. ').str[0]
		df_eui_min['Energy_Section_ID'] = df_eui_min['Energy_Section'].str.split('. ').str[0]

		# Read section tables
		df_es                          = pd.read_csv(__path__ + '../../../input/building_config/energysection.test.ver1.csv')
		df_es_comm                     = df_es[df_es['Section_Type']=='common']
		df_es_exc                      = df_es[df_es['Section_Type']=='exclusive']

		# Extract EUI values from EUI score tables
		df_es_comm_temp                = df_es_comm.copy()
		df_es_comm_temp['eeui_m']      = df_es_comm.apply(lambda x: df_eui_m.loc[df_eui_m['Energy_Section_ID']==x['Section_ID'], 'EEUI'].values[0], axis=1)
		df_es_comm_temp['leui_min']    = df_es_comm.apply(lambda x: df_eui_min.loc[df_eui_min['Energy_Section_ID']==x['Section_ID'], 'LEUI'].values[0], axis=1)
		df_es_comm_temp['leui_m']      = df_es_comm.apply(lambda x: df_eui_m.loc[df_eui_m['Energy_Section_ID']==x['Section_ID'], 'LEUI'].values[0], axis=1)
		df_es_comm_temp['leui_max']    = df_es_comm.apply(lambda x: df_eui_max.loc[df_eui_max['Energy_Section_ID']==x['Section_ID'], 'LEUI'].values[0], axis=1)
		df_es_comm_temp['aeui_min']    = df_es_comm.apply(lambda x: df_eui_min.loc[df_eui_min['Energy_Section_ID']==x['Section_ID'], 'AEUI_{}_{}'.format(self.building_cz, x['AC_Type'].upper())].values[0], axis=1)
		df_es_comm_temp['aeui_m']      = df_es_comm.apply(lambda x: df_eui_m.loc[df_eui_m['Energy_Section_ID']==x['Section_ID'], 'AEUI_{}_{}'.format(self.building_cz, x['AC_Type'].upper())].values[0], axis=1)
		df_es_comm_temp['aeui_max']    = df_es_comm.apply(lambda x: df_eui_max.loc[df_eui_max['Energy_Section_ID']==x['Section_ID'], 'AEUI_{}_{}'.format(self.building_cz, x['AC_Type'].upper())].values[0], axis=1)
		df_es_comm_temp['meaneui_m']   = df_es_comm.apply(lambda x: df_eui_m.loc[df_eui_m['Energy_Section_ID']==x['Section_ID'], 'EUI_Mean'].values[0], axis=1)
		df_es_comm_temp['totaleui_m']  = df_es_comm.apply(lambda x: df_eui_m.loc[df_eui_m['Energy_Section_ID']==x['Section_ID'], 'TotalEUI'].values[0], axis=1)
		df_es_comm = df_es_comm_temp.copy()
		del df_es_comm_temp

		# Error handling
		# aeui_min, aeui_m, or aeui_max include NaN
		if (df_es_comm[['aeui_min', 'aeui_m', 'aeui_max']].isna().values.any()): raise ValueError('aeui_min, aeui_m, or aeui_max include NaN.')

		# Calculate area and EUIs
		self.est_a_es_comm   = df_es_comm['Area'].sum().round(2)
		self.est_a_es_exc    = df_es_exc['Area'].sum().round(2)
		self.est_aeui_min    = (df_es_comm['Area'].dot(df_es_comm['aeui_min'])) / self.est_a_es_comm
		self.est_aeui_m      = (df_es_comm['Area'].dot(df_es_comm['aeui_m'])) / self.est_a_es_comm
		self.est_aeui_max    = (df_es_comm['Area'].dot(df_es_comm['aeui_max'])) / self.est_a_es_comm
		self.est_leui_min    = (df_es_comm['Area'].dot(df_es_comm['leui_min'])) / self.est_a_es_comm
		self.est_leui_m      = (df_es_comm['Area'].dot(df_es_comm['leui_m'])) / self.est_a_es_comm
		self.est_leui_max    = (df_es_comm['Area'].dot(df_es_comm['leui_max'])) / self.est_a_es_comm
		self.est_eeui_m      = (df_es_comm['Area'].dot(df_es_comm['eeui_m'])) / self.est_a_es_comm
		self.est_e_n         = self._calc_e_n(df_es_exc)

		# =========================================================================================
		# 
		# Calculate adjusted EC
		# 
		# =========================================================================================

		# Error handling
		# n_elevator/n_escalator is not equal to the length of elevator/escalator list
		if (self.n_elevator != len(self.elevator)): raise ValueError('n_elevator is not equal to the length of elevator list.')
		if (self.n_escalator != len(self.escalator)): raise ValueError('n_escalator is not equal to the length of escalator list.')

		# Get coefficient for special EC
		self.est_e_t         = \
			np.nansum([i.coef_usage_r * i.coef_facility_ec * i.coef_eff * i.coef_usage_h for i in self.elevator]) + \
			np.nansum([i.coef_usage_r * i.coef_facility_power * i.coef_eff * i.coef_usage_h for i in self.escalator])
		
		#self.est_e_p        = 
		

		# =========================================================================================
		# 
		# Bias-correction for EC
		# 
		# =========================================================================================



		# =========================================================================================
		# 
		# Calculate score
		# 
		# =========================================================================================

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

		new_elevator = FacilityElevator(building_type=self.building_type, **kwargs)
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

		new_escalator = FacilityEscalator(building_type=self.building_type, **kwargs)
		self.escalator.append(new_escalator)
		self.n_escalator = len(self.escalator)

		return

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
		if (mask_section('N2-1-3').any()): df_es_exc_temp.loc[mask_section('N2-1-3'), 'en'] = self.a_dining * 0.09 * self.n_dining_meal_per_day * 365 * 0.7 * 1.5

		# =========================================================================================
		# 
		# Class 4: EUI + usage + area
		# 
		# =========================================================================================

		# N7
		if (mask_section('N7').any()): df_es_exc_temp.loc[mask_section('N7'), 'en'] = 0.124 * df_es_exc.loc[mask_section('N7'), 'Area'].values[0] * self.get_coef_usage_h('N7') * 1.5 

		# N8
		if (mask_section('N8').any()): df_es_exc_temp.loc[mask_section('N8'), 'en'] = (2630 * self.coef_power_cabinetrack + 51) * df_es_exc.loc[mask_section('N8'), 'Area'].values[0]

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

class FacilityElevator():

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
		self.coef_usage_h               = np.nanmax([get_coef_usage_h(i) for i in self.elevator_es])
	
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

class FacilityEscalator():

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
		self.coef_usage_h               = np.nanmax([get_coef_usage_h(i) for i in self.escalator_es])

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

class FacilitySwimmingpool():

	def __init__(self, **kwargs):

		pass

class FacilitySpa():

	def __init__(self, **kwargs):

		pass

class FacilityHospital():

	def __init__(self, **kwargs):

		pass

class FacilityHotel():

	def __init__(self, **kwargs):

		pass

def get_coef_usage_h(es, es_sub=1):

	"""
	This method is used to get YOH (operation hours per year) of the given es.
	===========================================================================================

	Arguments:

		es (str): Energy section

		es_sub (str): Sub-energy section. Default is 1 and only available for J4

	Output:

		coef_usage_h (float): YOH of the given es
	"""

	# Read the file for YOH
	df_coef = pd.read_csv(__path__ + '../data/coef_es_operation/coef_es_operation.csv')

	# Modify es if the section is special
	if (es == 'N7'):
		
		es = 'L6-1'

	# Get YOH from the dataframe
	if (es != 'J4'):
		
		df_coef = df_coef.loc[df_coef['Energy_Section'].str.split('. ').str[0]==es, 'YOH']
	
	else:
		
		df_coef = df_coef.loc[(df_coef['Energy_Section'].str.split('. ').str[0]==es)&(df_coef['Sub-section'].str.split('. ').str[0]==str(es_sub)), 'YOH']
	
	# Raise error if no YOH is found (the given es is not defined)
	if (df_coef.empty): raise ValueError('YOH is not defined for es {}.'.format(es))

	# Get YOH
	coef_usage_h =  df_coef.values[0]

	return coef_usage_h