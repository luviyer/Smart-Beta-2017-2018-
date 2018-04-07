import pandas as pd
import numpy as np
from scipy.stats.mstats import winsorize
import os
import pickle
import timeit

import csv_file_manipulations as cfm
import metrics


def quality_score(csv_file, separate_csv_folder_name, permnos_dict_file, desired_output_filename):
    '''

    :param csv_file: (str) filename for csv downloaded from CRSP with all permnos' data. This
                        csv file will be separated by permno into individual csvs
    :param separate_csv_folder_name: (str) folder name for where separate csvs should be stored
    :param permnos_dict_file: (str) name of .txt file that contains the universe for each month
    :param desired_output_filename: (str) name of the score file
    :return: None

    '''

    permnos_dict = pickle.load(open(permnos_dict_file, 'rb'))

    # Make a separate csv file for each permno (only necessary if data has just been downloaded from CRSP,
    # and not been pre-processed yet. This will add at least a minute to the run time.)
    # cfm.csv_separate_permnos(csv_file, separate_csv_folder_name, make_monthly_data=True)

    permno_directory_list = os.listdir(separate_csv_folder_name)
    unique_permnos = [elem.split('.')[0] for elem in permno_directory_list]

    roe_data = []
    dte_data = []

    for permno_file in permno_directory_list:
        permno = permno_file.split('.')[0]
        df = pd.read_csv('{}/{}'.format(separate_csv_folder_name, permno_file), index_col=0)

        # Compute the metrics and transpose the dataframes to get the years as the columns
        df_roe = metrics.return_on_equity(df)
        df_dte = metrics.debt_to_equity(df)
        df_roe = df_roe.T
        df_dte = df_dte.T

        # Need to make sure that the date range for the CRSP data matches the date range in the permnos_dict file.
        condition = np.array([[permno in permnos_dict[str(yyyymm)]] for yyyymm in df_roe.columns]).T

        try:
            df_roe.where(condition, inplace=True)
            df_dte.where(condition, inplace=True)
        except ValueError:
            # This error will happen if the condition array ends up being empty....
            # Not sure why since all these stocks should have at least 1 month in the NYSE because
            # that's what we sorted for during the universe construction.
            pass
        # Make a dict {'yyyymm': metric_result} for each permno. All this will be put into the dataframe at the end.
        roe_fill_in = df_roe.loc['roe'].to_dict()
        dte_fill_in = df_dte.loc['dte'].to_dict()

        try:
            # Making a dataframe with all NaN's and then filling it when the metric is calculated is less efficient
            # than making a dataframe with all the data in hand.
            # roe_scores.loc[permno].fillna(fill_in_values, inplace=True)
            roe_data.append(roe_fill_in)
            dte_data.append(dte_fill_in)
        except TypeError:
            continue

    roe = pd.DataFrame(roe_data, index=unique_permnos)
    dte = pd.DataFrame(dte_data, index=unique_permnos)

    def standardize(df):
        '''

        :param df: (pandas dataframe) dataframe with columns: years, index: permnos, entries: metric_results
        :return: (pandas dataframe) winsorized dataframe of z_scores

        '''
        # Keep the middle 95% of data. Clip the rest. NaN's in data will change percentiles.
        winsorize(df, (0.025, 0.025), inplace=True)
        z_score = (df-df.mean())/df.std()
        return z_score

    avg_z_score = (standardize(roe) + standardize(dte))/2.0  # Probably shouldn't hard code this...
    for_neg_z_score = 1 - avg_z_score
    for_pos_z_score = 1 + avg_z_score
    quality_score = for_pos_z_score.where(avg_z_score >= 0, np.power(for_neg_z_score, -1))

    quality_score.to_csv(desired_output_filename)
    print('Quality score file has been created.')

def min_vol_score(csv_file, separate_csv_folder_name, permnos_dict_file, desired_output_filename):
    '''

    :param csv_file: (str) filename for csv downloaded from CRSP with all permnos' data. This
                        csv file will be separated by permno into individual csvs
    :param separate_csv_folder_name: (str) folder name for where separate csvs should be stored
    :param permnos_dict_file: (str) name of .txt file that contains the universe for each month
    :param desired_output_filename: (str) name of the score file
    :return: None

    '''

    permnos_dict = pickle.load(open(permnos_dict_file, 'rb'))

    # Make a separate csv file for each permno (only necessary if data has just been downloaded from CRSP,
    # and not been pre-processed yet. This will add at least a minute to the run time.)
    # cfm.csv_separate_permnos(csv_file, separate_csv_folder_name, make_monthly_data=True)

    permno_directory_list = os.listdir(separate_csv_folder_name)
    unique_permnos = [elem.split('.')[0] for elem in permno_directory_list]

    trailing_12mo_vol_data = []

    for permno_file in permno_directory_list:
        permno = permno_file.split('.')[0]
        df = pd.read_csv('{}/{}'.format(separate_csv_folder_name, permno_file), index_col=0)

        # Compute the metrics and transpose the dataframes to get the years as the columns
        df_12mo_vol = metrics.trailing_12mo_vol(df)
        df_12mo_vol = df_12mo_vol.T


        # Need to make sure that the date range for the CRSP data matches the date range in the permnos_dict file.

        list_of_bools = []
        for yyyymm in df_12mo_vol.columns:
            try:
                is_in_universe = permno in permnos_dict[str(yyyymm)]
                list_of_bools.append([is_in_universe])
            except KeyError:
                list_of_bools.append([False])

        condition = np.array(list_of_bools).T

        try:
            df_12mo_vol.where(condition, inplace=True)

        except ValueError:
            # This error will happen if the condition array ends up being empty....
            # Not sure why since all these stocks should have at least 1 month in the NYSE because
            # that's what we sorted for during the universe construction.
            pass
        # Make a dict {'yyyymm': metric_result} for each permno. All this will be put into the dataframe at the end.
        trailing_12mo_vol_fill_in = df_12mo_vol.loc['12mo_vol'].to_dict()

        try:
            # Making a dataframe with all NaN's and then filling it when the metric is calculated is less efficient
            # than making a dataframe with all the data in hand.
            # roe_scores.loc[permno].fillna(fill_in_values, inplace=True)
            trailing_12mo_vol_data.append(trailing_12mo_vol_fill_in)
        except TypeError:
            continue

    trailing_12mo_vol = pd.DataFrame(trailing_12mo_vol_data, index=unique_permnos)

    def standardize(df):
        '''

        :param df: (pandas dataframe) dataframe with columns: years, index: permnos, entries: metric_results
        :return: (pandas dataframe) winsorized dataframe of z_scores

        '''
        # Keep the middle 95% of data. Clip the rest. NaN's in data will change percentiles.
        winsorize(df, (0.025, 0.025), inplace=True)
        z_score = (df-df.mean())/df.std()
        return z_score

    avg_z_score = standardize(trailing_12mo_vol)  # Probably shouldn't hard code this...

    # Producing score greater than 0. Less than 1 is stuff to short...Need to see whether this is compatible
    # with Simon's optimizer (like whether he needs negative scores or not...probably not...just top and bottom deciles)
    for_neg_z_score = 1 - avg_z_score
    for_pos_z_score = 1 + avg_z_score
    min_vol_score = for_pos_z_score.where(avg_z_score >= 0, np.power(for_neg_z_score, -1))

    min_vol_score.to_csv(desired_output_filename)
    print('Min Vol score file has been created.')

if __name__ == '__main__':
    print('Starting Score Calculation')
    min_vol_score("minvol_test.csv", "Min Vol Permnos", "permnos_dict_nyse_197301_201612.txt", "min_vol_scores.csv")
    # print(timeit.timeit(stmt='sc.quality_score("roe_test.csv", "Quality Permnos", '
    #                          '"permnos_dict_nyse_197301_201612.txt", "quality_scores.csv")',
    #                     setup='import score_calculation as sc', number=2)/2)

