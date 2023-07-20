import pandas as pd
import os

__path__ = os.path.dirname(__file__).replace('\\', '/').replace('C:/', '/') + '/'

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

def get_coef_usage_d(es, es_sub=1):

	"""
	This method is used to get YOD (operation days per year) of the given es.
	===========================================================================================

	Arguments:

		es (str): Energy section

		es_sub (str): Sub-energy section. Default is 1 and only available for J4

	Output:

		coef_usage_d (float): YOD of the given es
	"""

	# Read the file for YOD
	df_coef = pd.read_csv(__path__ + '../data/coef_es_operation/coef_es_operation.csv')

	# Modify es if the section is special
	if (es == 'N7'):
		
		es = 'L6-1'

	# Get YOD from the dataframe
	if (es != 'J4'):
		
		df_coef = df_coef.loc[df_coef['Energy_Section'].str.split('. ').str[0]==es, 'YOD']
	
	else:
		
		df_coef = df_coef.loc[(df_coef['Energy_Section'].str.split('. ').str[0]==es)&(df_coef['Sub-section'].str.split('. ').str[0]==str(es_sub)), 'YOD']
	
	# Raise error if no YOD is found (the given es is not defined)
	if (df_coef.empty): raise ValueError('YOD is not defined for es {}.'.format(es))

	# Get YOD
	coef_usage_d =  df_coef.values[0]

	return coef_usage_d

def get_coef_usage_i_water(es, es_sub=1):

	"""
	This method is used to get Qw (water usage intensity) [m3 / (m2 * year)] of the given es.
	===========================================================================================

	Arguments:

		es (str): Energy section

		es_sub (str): Sub-energy section. Default is 1 and only available for J4

	Output:

		coef_usage_i_water (float): Water usage intensity [m3 / (m2 * year)] of the given es
	"""

	# Read the file for Qw
	df_coef = pd.read_csv(__path__ + '../data/coef_es_operation/coef_es_operation.csv')
	
	# Modify es if the section is special
	if (es == 'N7'):
		
		es = 'L6-1'

	# Get YOH from the dataframe
	if (es != 'J4'):
		
		df_coef = df_coef.loc[df_coef['Energy_Section'].str.split('. ').str[0]==es, 'Qw']
	
	else:
		
		df_coef = df_coef.loc[(df_coef['Energy_Section'].str.split('. ').str[0]==es)&(df_coef['Sub-section'].str.split('. ').str[0]==str(es_sub)), 'Qw']
	
	# Raise error if no Qw is found (the given es is not defined)
	if (df_coef.empty): raise ValueError('Qw is not defined for es {}.'.format(es))

	# Get Qw
	coef_usage_i_water =  df_coef.values[0]

	return coef_usage_i_water

def get_coef_usage_h_ac(es, cz, ac_type, es_sub=1):

	"""
	This method is used to get YAH (AC operation hours per year) of the given es.
	===========================================================================================

	Arguments:

		es (str): Energy section

		cz (str): Climate zone (N, C, S)

		ac_type (str): AC type (CONTINUE, INTERVAL)

		es_sub (str): Sub-energy section. Default is 1 and only available for J4

	Output:

		coef_usage_h (float): YAH of the given es
	"""

	# Read the file for YAH
	df_coef = pd.read_csv(__path__ + '../data/coef_es_operation/coef_es_operation.csv')

	# Modify es if the section is special
	if (es == 'N7'):
		
		es = 'L6-1'

	# Get YAH from the dataframe
	if (es != 'J4'):
		
		df_coef = df_coef.loc[df_coef['Energy_Section'].str.split('. ').str[0]==es, 'YAH_{}_{}'.format(cz, ac_type.upper())]
	
	else:
		
		df_coef = df_coef.loc[(df_coef['Energy_Section'].str.split('. ').str[0]==es)&(df_coef['Sub-section'].str.split('. ').str[0]==str(es_sub)), 'YAH_{}_{}'.format(cz, ac_type)]
	
	# Raise error if no YAH is found (the given es is not defined)
	if (df_coef.empty): raise ValueError('YAH is not defined for es {}.'.format(es))

	# Get YAH
	coef_usage_h_ac =  df_coef.values[0]

	return coef_usage_h_ac