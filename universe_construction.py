import pandas as pd
import datetime
import os
import pickle
import csv_file_manipulations as cfm


def get_universe(start_year, end_year, exchcd_folder_path, exchange_code):
    # Iterate over all the permnos (files in the folder)
    universe = {}
    all_months = set(cfm.get_all_months_in_year_range(start_year, end_year))

    for file in os.listdir(exchcd_folder_path):
        df = pd.read_csv(exchcd_folder_path+'/'+file, header=None, names=['date', 'exchcd'])
        trunc_mos = [str(elem)[:-2] for elem in df['date']]
        df['date'] = trunc_mos
        df.set_index('date', inplace=True)

        for yyyymm in df.index:
            if yyyymm in all_months and df.loc[yyyymm, 'exchcd'] == exchange_code:
                if yyyymm not in universe.keys():
                    universe[yyyymm] = []

                universe[yyyymm].append(file.split('.')[0])  # Only take the permno into the dict
    return universe

def make_crsp_txt_file(permno_dict_file, desired_filename):
    universe = pickle.load(open(permno_dict_file, 'rb'))

    unique_permnos = set()

    for value in universe.values():
        unique_permnos.update(value)

    unique_permnos = sorted(list(unique_permnos))

    file = open(desired_filename, 'w+')
    file.writelines([str(elem) + '\n' for elem in unique_permnos])
    file.close()

if __name__ == '__main__':
    # exchcd_folder_path = "C:/Users/Luv Iyer/Documents/Simon Data/permno_monthly_192601_201612_exchcds"
    #
    # # No data from 2017 is included. Only goes up to 2016-12. NYSE Exchange Code is 1.
    # universe = get_universe(1973, 2017, permno_folder_path, exchange_code=1)


    # The following code makes the .txt file of permnos that are uploaded to crsp
    make_crsp_txt_file('permnos_dict_nyse_197301_201612.txt', 'nyse_crsp_permnos_197301_201612.txt')

    # with open('permnos_dict_nyse_197301_201612.txt', 'wb+') as f:
    #     pickle.dump(universe, f, pickle.HIGHEST_PROTOCOL)

    # with open('permnos_dict_nyse_197301_201612.txt', 'rb') as f:
    #     nyse = pickle.load(f)
    #     print(sorted(nyse.keys()))
