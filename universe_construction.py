import pandas as pd
import datetime
import os
import pickle

def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)


def get_all_months_in_year_range(start_year, end_year):
    month_range = []
    for year in range(start_year, end_year):
        for month in range(1, 13):
            month_to_add = last_day_of_month(datetime.date(year, month, 1))
            month_range.append(month_to_add.strftime('%Y%m'))
    return month_range

'''Now assume that we have our date range, we need to know if the current permno is in our universe'''
def get_universe(start_year, end_year, permno_folder_path, exchange_code):
    # Iterate over all the permnos (files in the folder)
    universe = {}
    all_months = set(get_all_months_in_year_range(start_year, end_year))

    for file in os.listdir(permno_folder_path):
        df = pd.read_csv(permno_folder_path+'/'+file, header=None, names=['date', 'exchcd'])
        trunc_mos = [str(elem)[:-2] for elem in df['date']]
        df['date'] = trunc_mos
        df.set_index('date', inplace=True)

        for yyyymm in df.index:
            if yyyymm in all_months and df.loc[yyyymm, 'exchcd'] == exchange_code:
                if yyyymm not in universe.keys():
                    universe[yyyymm] = []

                universe[yyyymm].append(file.split('.')[0])  # Only take the permno into the dict
    return universe

if __name__ == '__main__':
    # permno_folder_path = "C:/Users/Luv Iyer/Documents/Simon Data/permno_monthly_192601_201612_exchcds"
    #
    # # No data from 2017 is included. Only goes up to 2016-12. NYSE Exchange Code is 1.
    # universe = get_universe(1973, 2017, permno_folder_path, exchange_code=1)

    universe = pickle.load(open('permnos_dict_nyse_197301_201612.txt', 'rb'))

    unique_permnos = set()

    for value in universe.values():
        unique_permnos.update(value)
    unique_permnos = sorted(list(unique_permnos))

    file = open('nyse_crsp_permnos_197301_201612.txt', 'w+')
    file.writelines([str(elem) + '\n' for elem in unique_permnos])
    file.close()

    # with open('permnos_dict_nyse_197301_201612.txt', 'wb+') as f:
    #     pickle.dump(universe, f, pickle.HIGHEST_PROTOCOL)

    # with open('permnos_dict_nyse_197301_201612.txt', 'rb') as f:
    #     nyse = pickle.load(f)
    #     print(sorted(nyse.keys()))
