import numpy as np
import pandas as pd
import os

__path__ = os.path.dirname(__file__).replace('\\', '/').replace('C:/', '/') + '/'

class EuiCriteria:

    def __init__(self, building_climate_zone: str = None, building_address_county: str = None, building_address_town: str = None, climate_adjustment: bool = False) -> None:

        """
        Initial an EUI criteria object, and read the EUI criteria from the input file.
        If climate_adjustment is True, the EUI criteria will be adjusted based on the building address county and town.
        If climate_adjustment is False, the EUI criteria will be obtained based on building climate zone directly.
        ===========================================================================================

        Arguments:

            building_climate_zone (str): Optional. Building climate zone. "N", "C", and "S" are the options.

            building_address_county (str): Optional.Building address county.

            building_address_town (str): Optional. Building address town.

            climate_adjustment (bool): Optional. If True, the EUI criteria will be adjusted based on the climate zone.

        Output:

            None
        """

        # =========================================================================================
        # 
        # Error handling
        # 
        # =========================================================================================

        # building_cliamte zone is not given and climate_adjustment is False
        if building_climate_zone is None and not climate_adjustment:
            
            raise ValueError('building_climate_zone is not given and climate_adjustment is False.')

        # building_cliamte zone is not given and building_address_county & building_address_town are not given simultaneously
        if building_climate_zone is None and (building_address_county is None or building_address_town is None):
            
            raise ValueError('building_cliamte zone is given and building_address_county and building_address_town are not given simultaneously.')

        # =========================================================================================
        # 
        # Initialize the climate adjustment parameters
        # 
        # =========================================================================================

        if not hasattr(self, 'df_cdd'): self._init_climate_adjustment()

        # =========================================================================================
        # 
        # Read the EUI criteria files
        # 
        # =========================================================================================

        for i_eui_parameter in ['min', 'm', 'max']:

            # Read the file for EUI score
            df_eui = pd.read_csv(__path__ + '../data/eui_criteria/eui_criteria.{}.csv'.format(i_eui_parameter))
            df_eui['Energy_Section_ID'] = df_eui['Energy_Section'].str.split('. ').str[0]

            # Select the AEUI columns based on the building climate zone
            for i_ac_operation in ['CONTINUE', 'INTERVAL']:
                
                df_eui = self._calc_eui(
                    df_eui,
                    climate_adjustment,
                    i_ac_operation,
                    building_climate_zone,
                    building_address_county,
                    building_address_town,
                )
                    
            # Remove all columns that start with "AEUI_" but contain two "_"
            df_eui = df_eui[df_eui.columns.drop(list(df_eui.filter(regex='AEUI_.*_.*')))]

            # Set df_eui as an attribute of the class
            setattr(self, 'df_eui_{}'.format(i_eui_parameter), df_eui)

        return

    def get_eui_criteria(self, energy_section, eui_parameter: str, eui_component: str) -> float:

        """
        This method reads the EUI criteria from the input file.
        Select the AEUI columns based on the building climate zone and air-conditioning operation.
        ===========================================================================================

        Arguments:

            energy_section (algorithm_bers.building_basic.EnergySection): Energy section object.

            eui_parameter (str): EUI parameter. "min", "m", "max" are the options.

            eui_component (str): EUI component. "leui", "aeui", "eeui" are the options.

        Output:

            eui_criteria (float): the value of the EUI criteria with the given EUI parameter and air-conditioning operation.
        """

        # =========================================================================================
        # 
        # Error handling
        # 
        # =========================================================================================

        # Invalid EUI parameter
        if eui_parameter not in ['min', 'm', 'max']: raise ValueError('Invalid EUI parameter. "min", "m", "max" are the options.')

        # =========================================================================================
        # 
        # Get the EUI criteria
        # 
        # =========================================================================================

        # Get EUI criteria dataframe
        df_eui_criteria = getattr(self, 'df_eui_{}'.format(eui_parameter))

        # Get the name of EUI column
        if (eui_component == 'aeui'):

            eui_column = 'AEUI_{}'.format(energy_section.ac_operation.upper())

        else:

            eui_column = eui_component.upper()
        
        # Get the EUI criteria
        eui_criteria = df_eui_criteria.loc[df_eui_criteria['Energy_Section_ID']==energy_section.id, eui_column].values[0]

        return eui_criteria
    
    def _init_climate_adjustment(self) -> None:

        """
        This method reads the cooling degree days from the input file.
        Calculate the ratio between each town and 臺北市中正區.
        ===========================================================================================

        Arguments:

            None

        Output:

            None
        """

        # Read the file for cooling degree days
        df_cdd = pd.read_csv(__path__ + '../data/climate_data_cdd/climate_data_cdd_town.csv')
        df_cdd = df_cdd[['TOWNCODE', 'COUNTYNAME', 'TOWNNAME', 'baseline']]

        # Calculate CDD ratio relative to 臺北市中正區
        df_cdd['cdd_ratio'] = df_cdd['baseline'] / df_cdd.loc[(df_cdd['COUNTYNAME']=='臺北市')&(df_cdd['TOWNNAME']=='中正區'), 'baseline'].values[0]
        df_cdd = df_cdd.set_index('TOWNCODE')

        # Set df_cdd as an attribute of the class
        self.df_cdd = df_cdd

        return
    
    def _calc_eui(self, df_eui, climate_adjustment, ac_operation, building_climate_zone=None, building_address_county=None, building_address_town=None) -> float:

        """
        This method calculates the AEUI either based on the building climate zone or the building address county and town.
        ===========================================================================================

        Arguments:

            None

        Output:

            None
        """

        def _calc_linear_regression(series_):

            """
            The process of calculating the AEUI by linear regression.
            """

            # Create regressor (X: cooling degree days) and response variables (Y: AEUI)
            regression_x = np.array(self.df_cdd.loc[[63000050, 66000050, 64000090], 'cdd_ratio'])
            regression_y = np.array([series_['AEUI_{}_{}'.format(i, ac_operation.upper())] for i in ['N', 'C', 'S']])

            # Get the predict X (cooling degree days) based on the building address county and town
            predict_x    = self.df_cdd[(self.df_cdd['COUNTYNAME']==building_address_county)&(self.df_cdd['TOWNNAME']==building_address_town)][['cdd_ratio']].values[0]

            # Create a degree 1 polynomial interpolation function
            poly = np.poly1d(np.polyfit(regression_x, regression_y, 1))

            # Predict the AEUI
            return poly(predict_x)[0]

        # =========================================================================================
        #
        # Calculate the AEUI
        #
        # =========================================================================================
        
        if climate_adjustment:
            # If climate_adjustment is True, the EUI criteria will be adjusted based on the building address county and town.
            
            df_eui['AEUI_{}'.format(ac_operation.upper())] = df_eui.apply(_calc_linear_regression, axis=1)

        else:
            # If climate_adjustment is False, the EUI criteria will be obtained based on building climate zone directly.

            df_eui['AEUI_{}'.format(ac_operation.upper())] = df_eui['AEUI_{}_{}'.format(building_climate_zone, ac_operation.upper())]

        return df_eui