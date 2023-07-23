import src.dependency.algorithm_bers as algorithm_bers

import json
import pandas as pd

def get_estimation_config(building_config_file):

	# Read the JSON file as a dictionary
	with open('input/building_config/{file}'.format(file=building_config_file), 'r') as f: json_data = json.load(f)

	# Extract variables from the dictionary
	dict_building_config = {i: json_data[i][0] for i in list(json_data.keys()) if i in ['building_name', 'estimation_system', 'building_type', 'building_address_county', 'building_address_town', 'building_coordinate_longitude', 'building_coordinate_latitude', 'building_n_stories_above_ground', 'building_n_stories_below_ground', 'ec', 'ec_other', 'est_q_rw', 'ec_heating_comm', 'height_watertower']}

	return

def main_script(**kwargs):
	
	"""
	The main script of the estimation system.
	=========================================================================================

	Arguments:

		**kwargs (dict): The input data.

	Returns:

		est_result (dict): The estimation result.
	"""

	building_config_file = kwargs.get('file', None)
	get_estimation_config(building_config_file)
	
	"""
	# Read section tables
	df_es      = pd.read_csv('input/building_config/energysection.test.ver1.csv')
	df_es_comm = df_es[df_es['Section_Type']=='common']
	df_es_exc  = df_es[df_es['Section_Type']=='exclusive']
	"""

	# Get input data
	
	# Convert number-like strings to numbers
	dict_building_config = {i: float(dict_building_config[i]) if (dict_building_config[i].replace('.', '', 1).isdigit()) else dict_building_config[i] for i in dict_building_config.keys()}

	print(dict_building_config)

	# Create a building object
	building_1 = algorithm_bers.Building(**dict_building_config)

	# Create elevator
	building_1.create_elevator(
		elevator_bottom_floor=-2,
		elevator_top_floor=3,
		elevator_es=['B3', 'B3', 'B3', 'B3', 'B3'],
		coef_people_per_elevator=20,
		coef_load_per_elevator=1350,
		coef_speed=45,
	)

	# Create exhibition area
	building_1.create_exhibitionarea(
		a=121.1,
		coef_usage_d=320,
	)

	# Create performance area
	building_1.create_performancearea(
		a=676.53,
		coef_usage_d=20,
	)

	building_1.create_performancearea(
		a=521.62,
		coef_usage_d=59,
	)

	est_result = building_1.estimate()
	
	return est_result

if (__name__ == '__main__'):
	
	# Read section tables
	df_es      = pd.read_csv('input/building_config/energysection.test.ver1.csv')
	df_es_comm = df_es[df_es['Section_Type']=='common']
	df_es_exc  = df_es[df_es['Section_Type']=='exclusive']
	
	building_1 = algorithm_bers.Building(
		estimation_system='BERSe',
		building_type='B2',
		building_es_comm=df_es_comm,
		building_es_exc=df_es_exc,
		building_n_stories_above_ground=15,
		building_n_stories_below_ground=3,
		building_coordinate=(120.21668276114208, 23.00121344494166),
		height_watertower=14,
		ec=95169,
		ec_other=0,
	)
	
	# Create elevator
	building_1.create_elevator(
		elevator_bottom_floor=-2,
		elevator_top_floor=3,
		elevator_es=['B3', 'B3', 'B3', 'B3', 'B3'],
		coef_people_per_elevator=20,
		coef_load_per_elevator=1350,
		coef_speed=45,
	)

	# Create exhibition area
	building_1.create_exhibitionarea(
		a=121.1,
		coef_usage_d=320,
	)

	# Create performance area
	building_1.create_performancearea(
		a=676.53,
		coef_usage_d=20,
	)

	building_1.create_performancearea(
		a=521.62,
		coef_usage_d=59,
	)

	est_result = building_1.estimate()