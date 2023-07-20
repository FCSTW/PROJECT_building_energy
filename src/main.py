import dependency.algorithm_bers as algorithm_bers

import pandas as pd

if (__name__ == '__main__'):

	# Read section tables
	df_es      = pd.read_csv('../input/building_config/energysection.test.ver1.csv')
	df_es_comm = df_es[df_es['Section_Type']=='common']
	df_es_exc  = df_es[df_es['Section_Type']=='exclusive']

	# Create a building object
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

	building_1.estimate()