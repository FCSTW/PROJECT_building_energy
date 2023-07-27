import json
import os
import pandas as pd

def get_estimation_config(file_name):

	"""
	Get the building configuration from the JSON file.
	===========================================================================================

	Arguments:

		file_name (str): The name of the building configuration file.

	Output:

		dict_building_config (dict): The building configuration for estimation, basic information and energy consumption.

		dict_es_comm_config_nested (dict): The energy section configuration.

		dict_es_exclusive_config_nested (dict): The exclusive energy section configuration.

		dict_elevator_config_nested (dict): The elevator configuration.

		dict_escalator_config_nested (dict): The escalator configuration.
	"""

	# Read the JSON file as a dictionary
	with open('input/building_config/{file}'.format(file=file_name), 'r') as f: json_data = json.load(f)
	
	# Convert all values in the dictionary to float if possible
	for i in json_data.keys():

		for j in range(len(json_data[i])):

			try: json_data[i][j] = float(json_data[i][j])

			except: pass
	
	# =========================================================================================
	# Estimation information / Basic information / nergy consumption
	# Extract all variables for building basic configuration from the dictionary
	dict_building_config            = {i: json_data[i][0] for i in list(json_data.keys()) if i in ['building_name', 'estimation_system', 'building_type', 'building_address_county', 'building_address_town', 'building_coordinate_longitude', 'building_coordinate_latitude', 'building_n_stories_above_ground', 'building_n_stories_below_ground', 'ec', 'ec_other', 'est_q_rw', 'ec_heating_comm', 'height_watertower']}

	# =========================================================================================
	# Energy section / Exclusive section
	# Extract all varialbes starts with 'es-' from the dictionary
	dict_es_comm_config             = {i: json_data[i][0] for i in list(json_data.keys()) if i.startswith('es-') and not i.startswith('es-exclusive-')}
	dict_es_exclusive_config        = {i: json_data[i][0] for i in list(json_data.keys()) if i.startswith('es-exclusive-')}
	list_es_comm_id                 = [int(i.split('-')[2]) for i in list(dict_es_comm_config.keys()) if i.startswith('es-id') and i.split('-')[2].isdigit()]
	list_es_exclusive_id            = [int(i.split('-')[3]) for i in list(dict_es_exclusive_config.keys()) if i.startswith('es-exclusive-id') and i.split('-')[3].isdigit()]

	dict_es_comm_config_nested      = {i: {j: dict_es_comm_config[j] for j in list(dict_es_comm_config.keys()) if j.startswith('es-attr-' + str(i)) or j.startswith('es-id-' + str(i))} for i in list_es_comm_id}
	dict_es_exclusive_config_nested = {i: {j: dict_es_exclusive_config[j] for j in list(dict_es_exclusive_config.keys()) if j.startswith('es-exclusive-attr-' + str(i)) or j.startswith('es-exclusive-id-' + str(i))} for i in list_es_exclusive_id}

	# Fill 'es-exclusive-attr-{i}-a': 0 for each exclusive section if the key 'es-exclusive-attr-{i}-a' does not exist
	for i in list_es_exclusive_id:

		if ('es-exclusive-attr-{i}-a'.format(i=i) not in dict_es_exclusive_config_nested[i].keys()): dict_es_exclusive_config_nested[i]['es-exclusive-attr-{i}-a'.format(i=i)] = 0


	# =========================================================================================
	# Elevator / Escalator
	# Extract all varialbes starts with 'elevator-' from the dictionary
	dict_elevator_config            = {i: json_data[i] for i in list(json_data.keys()) if i.startswith('elevator-')}
	dict_escalator_config           = {i: json_data[i] for i in list(json_data.keys()) if i.startswith('escalator-')}

	# Convert the list to a single value if the length of the list is 1
	for i in dict_elevator_config.keys():
		
		if len(dict_elevator_config[i]) == 1: dict_elevator_config[i] = dict_elevator_config[i][0]
	
	for i in dict_escalator_config.keys():
		
		if len(dict_escalator_config[i]) == 1: dict_escalator_config[i] = dict_escalator_config[i][0]

	list_elevator_id                = [int(i.split('-')[2]) for i in list(dict_elevator_config.keys()) if i.startswith('elevator-attr') and i.split('-')[2].isdigit()]
	list_escalator_id               = [int(i.split('-')[2]) for i in list(dict_escalator_config.keys()) if i.startswith('escalator-attr') and i.split('-')[2].isdigit()]

	list_elevator_id                = list(set(list_elevator_id))
	list_escalator_id               = list(set(list_escalator_id))

	dict_elevator_config_nested     = {i: {j: dict_elevator_config[j] for j in list(dict_elevator_config.keys()) if j.startswith('elevator-attr-' + str(i))} for i in list_elevator_id}
	dict_escalator_config_nested    = {i: {j: dict_escalator_config[j] for j in list(dict_escalator_config.keys()) if j.startswith('escalator-attr-' + str(i))} for i in list_escalator_id}

	return dict_building_config, \
		dict_es_comm_config_nested, dict_es_exclusive_config_nested, \
		dict_elevator_config_nested, dict_escalator_config_nested \

def output_estimation_result(file_name, est_eui, est_eui_min, est_eui_g, est_eui_m, est_eui_max, est_score, est_score_level):

	"""
	Ouptut the estimation result to a JSON file and diagram.
	=========================================================================================

	Arguments:

		file_name (str): The name of the building configuration file.

		est_eui (float): The estimated EUI of a building.

		est_eui_min (float): The minimum estimated EUI of a building.

		est_eui_g (float): The green building criteria estimated EUI of a building.

		est_eui_m (float): The median estimated EUI of a building.

		est_eui_max (float): The maximum estimated EUI of a building.

		est_score (float): The estimated score of a building.

		est_score_level (str): The estimated score level of a building.
	"""

	# Set output directory
	output_path = './output/{file}/'.format(file='.'.join(file_name.split('.')[1:-1]))
	if (not os.path.exists(output_path)): os.makedirs(output_path)

	# Output to JSON file
	with open(output_path + 'estimation_result.json', 'w') as outfile:

		json.dump({
			'est_eui': est_eui,
			'est_eui_min': est_eui_min,
			'est_eui_g': est_eui_g,
			'est_eui_m': est_eui_m,
			'est_eui_max': est_eui_max,
			'est_score': est_score,
			'est_score_level': est_score_level,
		}, outfile, indent=4)

	# Output diagram

	return True

def main_script(**kwargs):

	"""
	The main script of the estimation system.
	=========================================================================================

	Arguments:

		**kwargs (dict): The input data.

	Returns:

		est_result (dict): The estimation result.
	"""

	import src.dependency.algorithm_bers as algorithm_bers

	file_name = kwargs.get('file', None)

	# Get the building configuration file
	building_config, es_comm_config, es_exclusive_config, elevator_config, escalator_config = get_estimation_config(file_name)
	
	# Create dataframes for es_comm_config and es_exclusive_config
	df_es_comm                 = {}
	df_es_comm['Section_Type'] = ['common'] * len(es_comm_config.keys())
	df_es_comm['Section_ID']   = [es_comm_config[i]['es-id-{i}'.format(i=i)] for i in es_comm_config.keys()]
	df_es_comm['Area']         = [es_comm_config[i]['es-attr-{i}-a'.format(i=i)] for i in es_comm_config.keys()]
	df_es_comm['AC_Operation'] = [es_comm_config[i]['es-attr-{i}-ac_operation'.format(i=i)] for i in es_comm_config.keys()]
	df_es_comm['AC_Type']      = [es_comm_config[i]['es-attr-{i}-ac_type'.format(i=i)] for i in es_comm_config.keys()]
	df_es_comm                 = pd.DataFrame(df_es_comm)

	df_es_exclusive                 = {}
	df_es_exclusive['Section_Type'] = ['exclusive'] * len(es_exclusive_config.keys())
	df_es_exclusive['Section_ID']   = [es_exclusive_config[i]['es-exclusive-id-{i}'.format(i=i)] for i in es_exclusive_config.keys()]
	df_es_exclusive['Area']         = [es_exclusive_config[i]['es-exclusive-attr-{i}-a'.format(i=i)] for i in es_exclusive_config.keys()]
	df_es_exclusive['AC_Operation'] = [''] * len(es_exclusive_config.keys())
	df_es_exclusive['AC_Type']      = [''] * len(es_exclusive_config.keys())
	df_es_exclusive                 = pd.DataFrame(df_es_exclusive)

	# =========================================================================================

	# Create a building object
	building_1 = algorithm_bers.Building(
		**building_config,
		building_es_comm=df_es_comm,
		building_es_exc=df_es_exclusive
	)

	# Create elevator
	for i_elevator in elevator_config.keys():

		building_1.create_elevator(
			**{k.split('-')[-1]: v for k, v in elevator_config[i_elevator].items()}
		)
	
	# Create escalator
	for i_escalator in escalator_config.keys():

		building_1.create_escalator(
			**{k.split('-')[-1]: v for k, v in escalator_config[i_escalator].items()}
		)
	
	# Create hotel if there is any H1, H2 es-comm
	for i_key in [i for i in es_comm_config.keys() if es_comm_config[i]['es-id-' + str(i)] in ['H1', 'H2']]:

		building_1.create_hotel(
			n_room=es_comm_config[i_key]['es-attr-{i}-hotel-n_room'.format(i=i_key)],
			coef_usage_r_room=es_comm_config[i_key]['es-attr-{i}-hotel-coef_usage_r_room'.format(i=i_key)],
		)
	
	# Create hospital if there is any A1, A2, K1, K3, K8, K9 es-comm
	for i_key in [i for i in es_comm_config.keys() if es_comm_config[i]['es-id-' + str(i)] in ['A1', 'A2', 'K1', 'K3', 'K8', 'K9']]:

		building_1.create_hospital(
			n_hospitalbed=es_comm_config[i_key]['es-attr-{i}-hospital-n_hospitalbed'.format(i=i_key)],
			coef_usage_r_hospitalbed=es_comm_config[i_key]['es-attr-{i}-hospital-coef_usage_r_hospitalbed'.format(i=i_key)],
		)
	
	# Create sport bathroom if there is any H7, H9, L2, L3, L4-2 es-comm
	for i_key in [i for i in es_comm_config.keys() if es_comm_config[i]['es-id-' + str(i)] in ['H7', 'H9', 'L2', 'L3', 'L4-2']]:

		building_1.create_sportbathroom(
			a=es_comm_config[i_key]['es-attr-{i}-sportbathroom-a'.format(i=i_key)],
			coef_usage_h=es_comm_config[i_key]['es-attr-{i}-sportbathroom-coef_usage_h'.format(i=i_key)],
		)
	
	# Create swimming pool, SPA, and sport bathroom if there is any H8, L6-1, L6-2, L6-3 es-comm
	for i_key in [i for i in es_comm_config.keys() if es_comm_config[i]['es-id-' + str(i)] in ['H8', 'L6-1', 'L6-2', 'L6-3']]:

		building_1.create_swimmingpool(
			ec_heating=es_comm_config[i_key]['es-attr-{i}-swimmingpool-ec_heating'.format(i=i_key)],
			v=es_comm_config[i_key]['es-attr-{i}-swimmingpool-v'.format(i=i_key)],
			coef_usage_h=es_comm_config[i_key]['es-attr-{i}-swimmingpool-coef_usage_h'.format(i=i_key)],
			height_watertower=es_comm_config[i_key]['es-attr-{i}-swimmingpool-height_watertower'.format(i=i_key)],
			constant_temperature=es_comm_config[i_key]['es-attr-{i}-swimmingpool-constant_temperature'.format(i=i_key)],
		)

		building_1.create_spa(
			ec_heating=es_comm_config[i_key]['es-attr-{i}-spa-ec_heating'.format(i=i_key)],
			v=es_comm_config[i_key]['es-attr-{i}-spa-v'.format(i=i_key)],
			coef_usage_h=es_comm_config[i_key]['es-attr-{i}-spa-coef_usage_h'.format(i=i_key)],
			height_watertower=es_comm_config[i_key]['es-attr-{i}-spa-height_watertower'.format(i=i_key)],
			constant_temperature=es_comm_config[i_key]['es-attr-{i}-spa-constant_temperature'.format(i=i_key)],
		)

		building_1.create_sportbathroom(
			a=es_comm_config[i_key]['es-attr-{i}-sportbathroom-a'.format(i=i_key)],
			coef_usage_h=es_comm_config[i_key]['es-attr-{i}-sportbathroom-coef_usage_h'.format(i=i_key)],
		)
	
	# Create dining area if there is any H10, I1, I2, I3, I4, I5, I6, I7 es-comm
	for i_key in [i for i in es_comm_config.keys() if es_comm_config[i]['es-id-' + str(i)] in ['H10', 'I1', 'I2', 'I3', 'I4', 'I5', 'I6', 'I7']]:

		building_1.create_diningarea(
			a=es_comm_config[i_key]['es-attr-{i}-diningarea-a'.format(i=i_key)],
			n_meal_per_day=es_comm_config[i_key]['es-attr-{i}-diningarea-n_meal_per_day'.format(i=i_key)],
			washdishes_by_hand=es_comm_config[i_key]['es-attr-{i}-diningarea-washdishes_by_hand'.format(i=i_key)],
			coef_usage_d=es_comm_config[i_key]['es-attr-{i}-diningarea-coef_usage_d'.format(i=i_key)],
		)

	# Create exhibition area if there is any D1, D2, D3, E1 es-comm
	for i_key in [i for i in es_comm_config.keys() if es_comm_config[i]['es-id-' + str(i)] in ['D1', 'D2', 'D3', 'E1']]:
		
		building_1.create_exhibitionarea(
			a=es_comm_config[i_key]['es-attr-{i}-a'.format(i=i_key)],
			coef_usage_d=es_comm_config[i_key]['es-attr-{i}-exhibitionarea-coef_usage_d'.format(i=i_key)],
		)
	
	# Create performance area if there is any F1, F2, G1, G2 es-comm
	for i_key in [i for i in es_comm_config.keys() if es_comm_config[i]['es-id-' + str(i)] in ['F1', 'F2', 'G1', 'G2']]:

		building_1.create_performancearea(
			a=es_comm_config[i_key]['es-attr-{i}-a'.format(i=i_key)],
			coef_usage_d=es_comm_config[i_key]['es-attr-{i}-performancearea-coef_usage_d'.format(i=i_key)],
		)
	
	# Create data center if there is any N8 es-exclusive
	for i_key in [i for i in es_exclusive_config.keys() if es_exclusive_config[i]['es-exclusive-id-' + str(i)] in ['N8']]:

		building_1.create_datacenter(
			a=es_exclusive_config[i_key]['es-exclusive-attr-{i}-a'.format(i=i_key)],
			coef_power_cabinetrack=es_exclusive_config[i_key]['es-exclusive-attr-{i}-datacenter-coef_power_cabinetrack'.format(i=i_key)],
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

	est_eui, est_eui_min, est_eui_g, est_eui_m, est_eui_max, est_score, est_score_level = building_1.estimate()

	estimation_result = output_estimation_result(file_name, est_eui, est_eui_min, est_eui_g, est_eui_m, est_eui_max, est_score, est_score_level)

	return estimation_result

"""
if (__name__ == '__main__'):

	import dependency.algorithm_bers as algorithm_bers
	
	# Read section tables
	df_es      = pd.read_csv('../input/building_config/energysection.test.ver1.csv')
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
		elevator_type='freight',
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

	est_eui, est_score, est_score_level = building_1.estimate()

	print('Estimated EUI: {eui:.2f} kWh/m2. SCORE={score} ({score_level})'.format(eui=est_eui, score=est_score, score_level=est_score_level))
"""
