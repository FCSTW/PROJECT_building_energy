import dependency.algorithm_bers as algorithm_bers

if (__name__ == '__main__'):

	# Create a building object
	building_1 = algorithm_bers.building(
		estimation_system='BERSe',
		building_type='B2',
		building_n_stories_above_ground=15,
		building_n_stories_below_ground=3,
		building_coordinate=(121.53811771789655, 25.027638292217627),
	)

	# Create elevator
	building_1.create_elevator(
		elevator_bottom_floor=-2,
		elevator_top_floor=4,
		elevator_es=['NB13', 'NB13', 'J1', 'J1', 'J1', 'J1'],
		coef_people_per_elevator=8,
		coef_load_per_elevator=1010,
		coef_speed=105,
	)

	building_1.estimate()