import pandas as pd
import numpy as np
from scipy.stats.mstats import winsorize
import os
import pickle

import csv_file_manipulations as cfm
import metrics

def quality_score(csv_file, separate_csv_folder_name, permnos_dict_file, desired_output_filename):
    permnos_dict = pickle.load(open(permnos_dict_file, 'rb'))
    year_range = list(permnos_dict.keys())

    # Make a separate csv file for each permno
    # cfm.csv_separate_permnos(csv_file, separate_csv_folder_name, make_monthly_data=True)

    print('Permnos have been put into separate files')
    permno_directory_list = os.listdir(separate_csv_folder_name)
    unique_permnos = [elem.split('.')[0] for elem in permno_directory_list]

    list_of_nan = [np.nan for i in range(len(unique_permnos))]

    empty_df = pd.DataFrame({year: list_of_nan for year in year_range}, index=unique_permnos)
    print('Empty dataframe successfully created')
    i = 1
    roe_scores = empty_df.copy()
    for permno_file in permno_directory_list:
        permno = permno_file.split('.')[0]
        df = pd.read_csv('{}/{}'.format(separate_csv_folder_name, permno_file), index_col=0)

        # Compute the first metric
        df_roe = metrics.return_on_equity(df)

        fill_in_values = {str(col): df_roe.T.loc['roe'][col] for col in df_roe.T.columns}
        roe_scores.loc[permno].fillna(fill_in_values, inplace=True)

    return roe_scores


if __name__ == '__main__':
    print('Starting Score Calculation')
    df = quality_score('roe_test.csv', 'Quality Permnos', 'permnos_dict_nyse_197301_201612.txt', 'quality_scores.csv')
    print(df.loc[['10071', '10092'], ['200001', '198603', '199705']])
