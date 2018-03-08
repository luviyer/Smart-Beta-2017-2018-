import pandas as pd
import numpy as np
from scipy.stats.mstats import winsorize
import os
import pickle
import timeit

import csv_file_manipulations as cfm
import metrics

def quality_score(csv_file, separate_csv_folder_name, permnos_dict_file, desired_output_filename):
    permnos_dict = pickle.load(open(permnos_dict_file, 'rb'))
    year_range = [int(elem) for elem in permnos_dict.keys()]

    # Make a separate csv file for each permno
    # cfm.csv_separate_permnos(csv_file, separate_csv_folder_name, make_monthly_data=True)

    # print('Permnos have been put into separate files')
    permno_directory_list = os.listdir(separate_csv_folder_name)
    # print(len(permno_directory_list))
    unique_permnos = [elem.split('.')[0] for elem in permno_directory_list]

    empty_df = pd.DataFrame(columns=year_range, index=unique_permnos)
    roe_scores = empty_df.copy()
    dte_scores = empty_df.copy()

    # , '10092.csv', '10006.csv', '10014.csv', '10051.csv', '10064.csv', '10085.csv'
    for permno_file in ['10071.csv']:
        permno = permno_file.split('.')[0]
        df = pd.read_csv('{}/{}'.format(separate_csv_folder_name, permno_file), index_col=0)

        # Compute the first metric
        df_roe = metrics.return_on_equity(df)

        fill_in_values = df_roe.T.loc['roe'].to_dict()

        try:
            roe_scores.loc[permno].fillna(fill_in_values, inplace=True)
        except TypeError as err:
            print(err)
            continue

    return roe_scores


if __name__ == '__main__':
    print('Starting Score Calculation')
    df = quality_score("roe_test.csv", "Quality Permnos", "permnos_dict_nyse_197301_201612.txt", "quality_scores.csv")
    print(df.loc[['10071', '10092', '10006']][199705])
    print(timeit.timeit(stmt='sc.quality_score("roe_test.csv", "Quality Permnos", '
                             '"permnos_dict_nyse_197301_201612.txt", "quality_scores.csv")',
                        setup='import score_calculation as sc', number=10)/10)

