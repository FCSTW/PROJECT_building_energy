import numpy as np
import json
import os
import src.dependency.algorithm_bers as algorithm_bers

def get_estimation_config(file_name: str) -> tuple:

	"""
	Get the building configuration from the JSON file.
	Parse the building configuration to the dictionaries.
	===========================================================================================

	Arguments:

		file_name (str): The name of the building configuration file.

	Output:

		dict_config (tuple): The tuple of the dictionaries for the building configuration.
	"""

	# Read the JSON file as a dictionary
	with open('input/building_config/{file}'.format(file=file_name), 'r') as f: json_data = json.load(f)
	
	# Convert all values in the dictionary to float if possible
	for i in json_data.keys():

		# If the key contains "type", "name", "address", or "energy_rating", do not convert the value to float
		if (i.endswith('type') or i.endswith('name') or i.endswith('address') or i.endswith('energy_rating')):

			continue

		for j in range(len(json_data[i])):

			try: json_data[i][j] = float(json_data[i][j])

			except: pass
	
	# =========================================================================================
	#
	# Estimation information / Basic information / Energy consumption
	#
	# =========================================================================================

	# Extract all variables for building basic configuration from the dictionary
	list_building_attributes        = [
		# The attributes for all estimation systems
		'building_name',
		'estimation_system',
		'building_class',
		'building_type',
		'building_address_county',
		'building_address_town',
		'building_coordinate_longitude',
		'building_coordinate_latitude',
		'building_n_stories_above_ground',
		'building_n_stories_below_ground',
		# The attributes for only the estimation system 'BERSe'
		'ec_other',
		'est_q_rw',
		'ec_heating_comm',
		'height_watertower',
		# The attributes for only the estimation system 'R-BERS'
		'n_suite',
		'n_household_big',
		'coef_eff_ac_residential',
		'coef_eff_ac_nonresidential',
		'coef_eff_envelope',
		'coef_eff_lighting_residential',
		'coef_eff_lighting_nonresidential',
	]
	dict_building_config            = {i: json_data[i][0] for i in list(json_data.keys()) if i in list_building_attributes}

	# Add ec data to the dictionary if available (BERSe... etc.)
	if ('ec_input_type' in json_data.keys()):

		if (json_data['ec_input_type'][0] == 'direct'):
			# If the input type is direct, add the ec data to the dictionary directly

			dict_building_config['ec'] = json_data['ec'][0]

		elif (json_data['ec_input_type'][0] == 'monthly'):
			# If the input type is monthly, calculate the summation of all values that the keys start with 'ec_monthly_'

			dict_building_config['ec'] = np.nansum([json_data[i][0] for i in list(json_data.keys()) if i.startswith('ec_monthly_')]) / 2

		elif (json_data['ec_input_type'][0] == 'bimonthly'):
			# If the input type is bimonthly, calculate the summation of all values that the keys start with 'ec_bimonthly_'

			dict_building_config['ec'] = np.nansum([json_data[i][0] for i in list(json_data.keys()) if i.startswith('ec_bimonthly_')]) / 2
	
	# =========================================================================================
	#
	# Energy section / Exclusive section / Non-residential section
	#
	# =========================================================================================

	# Extract all varialbes starts with 'es-' from the dictionary
	dict_es_comm_config                  = {i: json_data[i][0] for i in list(json_data.keys()) if i.startswith('es-') and not i.startswith('es-exclusive-') and not i.startswith('es-nonresidential-')}
	dict_es_exclusive_config             = {i: json_data[i][0] for i in list(json_data.keys()) if i.startswith('es-exclusive-')}
	dict_es_nonresidential_config        = {i: json_data[i][0] for i in list(json_data.keys()) if i.startswith('es-nonresidential-')}

	# Get the lists of unique ids
	list_es_comm_id                      = [int(i.split('-')[2]) for i in list(dict_es_comm_config.keys()) if i.startswith('es-id') and i.split('-')[2].isdigit()]
	list_es_exclusive_id                 = [int(i.split('-')[3]) for i in list(dict_es_exclusive_config.keys()) if i.startswith('es-exclusive-id') and i.split('-')[3].isdigit()]
	list_es_nonresidential_id            = [int(i.split('-')[3]) for i in list(dict_es_nonresidential_config.keys()) if i.startswith('es-nonresidential-id') and i.split('-')[3].isdigit()]

	# Create nested dictionaries containing the attributes for each section according to their ids
	dict_es_comm_config_nested           = {i: {j: dict_es_comm_config[j] for j in list(dict_es_comm_config.keys()) if j.startswith('es-attr-' + str(i)) or j.startswith('es-id-' + str(i))} for i in list_es_comm_id}
	dict_es_exclusive_config_nested      = {i: {j: dict_es_exclusive_config[j] for j in list(dict_es_exclusive_config.keys()) if j.startswith('es-exclusive-attr-' + str(i)) or j.startswith('es-exclusive-id-' + str(i))} for i in list_es_exclusive_id}
	dict_es_nonresidential_config_nested = {i: {j: dict_es_nonresidential_config[j] for j in list(dict_es_nonresidential_config.keys()) if j.startswith('es-nonresidential-attr-' + str(i)) or j.startswith('es-nonresidential-id-' + str(i))} for i in list_es_nonresidential_id}

	# Fill 'es-exclusive-attr-{i}-a': 0 for each exclusive section if the key 'es-exclusive-attr-{i}-a' does not exist
	for i in list_es_exclusive_id:

		if ('es-exclusive-attr-{i}-a'.format(i=i) not in dict_es_exclusive_config_nested[i].keys()): dict_es_exclusive_config_nested[i]['es-exclusive-attr-{i}-a'.format(i=i)] = 0

	# =========================================================================================
	#
	# Facility
	#
	# =========================================================================================

	# Extract all varialbes starts with '${FAILITY_NAME}-' from the dictionary
	dict_elevator_config             = {i: json_data[i] for i in list(json_data.keys()) if i.startswith('elevator-')}
	dict_escalator_config            = {i: json_data[i] for i in list(json_data.keys()) if i.startswith('escalator-')}
	dict_watertower_config           = {i: json_data[i] for i in list(json_data.keys()) if i.startswith('watertower-')}
	dict_heater_config               = {i: json_data[i] for i in list(json_data.keys()) if i.startswith('heater-')}
	dict_parkinggarage_config        = {i: json_data[i] for i in list(json_data.keys()) if i.startswith('parkinggarage-')}

	# Convert the list to a single value if the length of the list is 1
	for i in dict_elevator_config.keys():
		
		if len(dict_elevator_config[i]) == 1: dict_elevator_config[i] = dict_elevator_config[i][0]
	
	for i in dict_escalator_config.keys():
		
		if len(dict_escalator_config[i]) == 1: dict_escalator_config[i] = dict_escalator_config[i][0]

	for i in dict_watertower_config.keys():

		if len(dict_watertower_config[i]) == 1: dict_watertower_config[i] = dict_watertower_config[i][0]

	for i in dict_heater_config.keys():

		if len(dict_heater_config[i]) == 1: dict_heater_config[i] = dict_heater_config[i][0]

	for i in dict_parkinggarage_config.keys():

		if len(dict_parkinggarage_config[i]) == 1: dict_parkinggarage_config[i] = dict_parkinggarage_config[i][0]

	# Get the lists of unique ids
	list_elevator_id                 = [int(i.split('-')[2]) for i in list(dict_elevator_config.keys()) if i.startswith('elevator-attr') and i.split('-')[2].isdigit()]
	list_escalator_id                = [int(i.split('-')[2]) for i in list(dict_escalator_config.keys()) if i.startswith('escalator-attr') and i.split('-')[2].isdigit()]
	list_watertower_id               = [int(i.split('-')[2]) for i in list(dict_watertower_config.keys()) if i.startswith('watertower-attr') and i.split('-')[2].isdigit()]
	list_heater_id                   = [int(i.split('-')[2]) for i in list(dict_heater_config.keys()) if i.startswith('heater-attr') and i.split('-')[2].isdigit()]
	list_parkinggarage_id            = [int(i.split('-')[2]) for i in list(dict_parkinggarage_config.keys()) if i.startswith('parkinggarage-attr') and i.split('-')[2].isdigit()]

	list_elevator_id                 = list(set(list_elevator_id))
	list_escalator_id                = list(set(list_escalator_id))
	list_watertower_id               = list(set(list_watertower_id))
	list_heater_id                   = list(set(list_heater_id))
	list_parkinggarage_id            = list(set(list_parkinggarage_id))

	# Create nested dictionaries containing the attributes for each facility according to their ids
	dict_elevator_config_nested      = {i: {j: dict_elevator_config[j] for j in list(dict_elevator_config.keys()) if j.startswith('elevator-attr-' + str(i))} for i in list_elevator_id}
	dict_escalator_config_nested     = {i: {j: dict_escalator_config[j] for j in list(dict_escalator_config.keys()) if j.startswith('escalator-attr-' + str(i))} for i in list_escalator_id}
	dict_watertower_config_nested    = {i: {j: dict_watertower_config[j] for j in list(dict_watertower_config.keys()) if j.startswith('watertower-attr-' + str(i))} for i in list_watertower_id}
	dict_heater_config_nested        = {i: {j: dict_heater_config[j] for j in list(dict_heater_config.keys()) if j.startswith('heater-attr-' + str(i))} for i in list_heater_id}
	dict_parkinggarage_config_nested = {i: {j: dict_parkinggarage_config[j] for j in list(dict_parkinggarage_config.keys()) if j.startswith('parkinggarage-attr-' + str(i))} for i in list_parkinggarage_id}

	# =========================================================================================
	#
	# Collect all dictionaries that are created above
	#
	# =========================================================================================

	dict_config = (
		dict_building_config,
		dict_es_comm_config_nested,
		dict_es_exclusive_config_nested,
		dict_es_nonresidential_config_nested,
		dict_elevator_config_nested,
		dict_escalator_config_nested,
		dict_watertower_config_nested,
		dict_heater_config_nested,
		dict_parkinggarage_config_nested
	)

	return dict_config

def output_estimation_result(file_name, **kwargs):

	"""
	Ouptut the estimation result to a JSON file and diagram.
	=========================================================================================

	Arguments:

		file_name (str): The name of the building configuration file.

		kwarg (dict): The dictionary containing the estimation result.
	"""

	# Set output directory
	output_path = './output/{file}/'.format(file='.'.join(file_name.split('.')[1:-1]))
	if (not os.path.exists(output_path)): os.makedirs(output_path)

	# Output to JSON file
	with open(output_path + 'estimation_result.json', 'w') as outfile:

		json.dump({
			'est_eui': kwargs.get('est_eui', None),
			'est_eui_min': kwargs.get('est_eui_min', None),
			'est_eui_g': kwargs.get('est_eui_g', None),
			'est_eui_m': kwargs.get('est_eui_m', None),
			'est_eui_max': kwargs.get('est_eui_max', None),
			'est_cei': kwargs.get('est_cei', None),
			'est_score': kwargs.get('est_score', None),
			'est_score_level': kwargs.get('est_score_level', None),
		}, outfile, indent=4)

	# Output diagram
	algorithm_bers.plot.plot_eui_diagram(
		output_path,
		**kwargs,
	)

	return True

def run_estimate_berse(file: str, **kwargs):

	"""
	The main script of the BERSe estimation.
	=========================================================================================

	Arguments:

		file (str): The name of the building configuration file.

		**kwargs (dict): The input data.

	Returns:

		None
	"""
	
	# Get the building configuration file
	dict_config = get_estimation_config(file)
	building_config, es_comm_config, es_exclusive_config, _, elevator_config, escalator_config, _, _, _ = dict_config
	
	# =========================================================================================
	#
	# Create a building object
	#
	# =========================================================================================

	building_1 = algorithm_bers.ExistingBuilding(
		**building_config,
	)

	# =========================================================================================
	#
	# Create energy section
	#
	# =========================================================================================

	# Create common energy section
	for i_es in es_comm_config.keys():

		building_1.create_energy_section(
			id=es_comm_config[i_es]['es-id-' + str(i_es)],
			**{'-'.join(k.split('-')[3:]): v for k, v in es_comm_config[i_es].items() if k.startswith('es-attr-')},
		)

	# Create exclusive energy section
	for i_es in es_exclusive_config.keys():

		building_1.create_exclusive_energy_section(
			id=es_exclusive_config[i_es]['es-exclusive-id-' + str(i_es)],
			**{'-'.join(k.split('-')[4:]): v for k, v in es_exclusive_config[i_es].items() if k.startswith('es-exclusive-attr-')},
		)
	
	# =========================================================================================
	#
	# Create facility
	#
	# =========================================================================================

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
	
	# Create water tower
	building_1.create_watertower(
		height=building_config['height_watertower'],
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

	# =========================================================================================
	#
	# Estimate in BERSe system
	#
	# =========================================================================================

	est_result = building_1.estimate()
	
	est_eui, \
	est_eui_min, est_eui_g, est_eui_m, est_eui_max, \
	est_cei, \
	est_score, est_score_level \
	= est_result
	
	# =========================================================================================
	#
	# Output the estimation result to ./output/ directory
	#
	# =========================================================================================

	output_estimation_result(
		file,
		est_eui=est_eui,
		est_eui_min=est_eui_min,
		est_eui_g=est_eui_g,
		est_eui_m=est_eui_m,
		est_eui_max=est_eui_max,
		est_cei=est_cei,
		est_score=est_score,
		est_score_level=est_score_level,
	)

	return

def run_estimate_rbers(file: str, **kwargs):

	"""
	The main script of the BERSe estimation.
	=========================================================================================

	Arguments:

		file (str): The name of the building configuration file.

		**kwargs (dict): The input data.

	Returns:

		None
	"""

	# Get the building configuration file
	dict_config = get_estimation_config(file)
	building_config, es_comm_config, _, es_nonresidential_config, elevator_config, _, watertower_config, heater_config, parkinggarage_config = dict_config
	
	# =========================================================================================
	#
	# Create a building object
	#
	# =========================================================================================

	building_1 = algorithm_bers.NewBuilding(
		**building_config,
	)

	# =========================================================================================
	#
	# Create energy section
	#
	# =========================================================================================

	# Create common energy section
	for i_es in es_comm_config.keys():

		building_1.create_energy_section(
			id=es_comm_config[i_es]['es-id-' + str(i_es)],
			**{'-'.join(k.split('-')[3:]): v for k, v in es_comm_config[i_es].items() if k.startswith('es-attr-')},
		)

	# Create non-residential energy section
	for i_es in es_nonresidential_config.keys():

		building_1.create_exclusive_energy_section(
			id=es_nonresidential_config[i_es]['es-nonresidential-id-' + str(i_es)],
			**{'-'.join(k.split('-')[4:]): v for k, v in es_nonresidential_config[i_es].items() if k.startswith('es-nonresidential-attr-')},
		)
	
	# =========================================================================================
	#
	# Create facility
	#
	# =========================================================================================

	# Create elevator
	for i_elevator in elevator_config.keys():
		building_1.create_elevator(
			**{k.split('-')[-1]: v for k, v in elevator_config[i_elevator].items()}
		)
	
	# Create water tower
	for i_watertower in watertower_config.keys():
		building_1.create_watertower(
			**{k.split('-')[-1]: v for k, v in watertower_config[i_watertower].items()}
		)

	# Create heater
	for i_heater in heater_config.keys():
		building_1.create_heater(
			**{k.split('-')[-1]: v for k, v in heater_config[i_heater].items()}
		)
	
	# Create parking garage
	for i_parkinggarage in parkinggarage_config.keys():
		building_1.create_parkinggarage(
			**{k.split('-')[-1]: v for k, v in parkinggarage_config[i_parkinggarage].items()}
		)
	
	# =========================================================================================
	#
	# Estimate in R-BERS system
	#
	# =========================================================================================

	est_result = building_1.estimate()

	est_eui_simulated, \
	est_eui_n, est_eui_g, est_eui_m, est_eui_max, \
	est_cei_simulated, \
	est_cei_n, est_cei_g, est_cei_m, est_cei_max, \
	est_score, est_score_level \
	= est_result
	
	# =========================================================================================
	#
	# Output the estimation result to ./output/ directory
	#
	# =========================================================================================

	output_estimation_result(
		file,
		est_eui=est_eui_simulated,
		est_eui_min=est_eui_n,
		est_eui_g=est_eui_g,
		est_eui_m=est_eui_m,
		est_eui_max=est_eui_max,
		est_cei=est_cei_simulated,
		est_cei_min=est_cei_n,
		est_cei_g=est_cei_g,
		est_cei_m=est_cei_m,
		est_cei_max=est_cei_max,
		est_score=est_score,
		est_score_level=est_score_level,
	)