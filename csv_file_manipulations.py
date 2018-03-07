import pandas as pd
import os
import datetime

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

def csv_separate_permnos(csv_file, folder_name, make_monthly_data):
    '''

    :param csv_file: (str) filename for csv
    :param folder_name: (str) folder where all the separated files should be saved
    :param make_monthly_data: (boolean) forward fills quarterly data into monthly data
    :return: None

    '''

    df = pd.read_csv(csv_file)

    list_of_permnos = list(df['LPERMNO'].unique())

    for permno in list_of_permnos:
        permno_df = df[df['LPERMNO'] == permno]

        truncated_months = [str(elem)[:-2] for elem in permno_df['datadate']]
        permno_df.set_index(pd.Series(truncated_months), inplace=True)

        if make_monthly_data:
            permno_df = make_monthly_time_series(permno_df)

        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        permno_df.to_csv('{}/{}.csv'.format(folder_name, permno))


def make_monthly_time_series(df):
    start_month = last_day_of_month(datetime.datetime.strptime(df.index[0], '%Y%m'))
    end_month = last_day_of_month(datetime.datetime.strptime(df.index[-1], '%Y%m'))

    monthly_dt_index = pd.date_range(start_month, end_month, freq='M')
    monthly_str_index = [elem.strftime('%Y%m') for elem in monthly_dt_index]

    empty_monthly_df = pd.DataFrame(index=monthly_str_index)
    monthly_df = empty_monthly_df.join(df)
    monthly_df.fillna(method='pad', inplace=True)

    return monthly_df


if __name__ == '__main__':
    csv_separate_permnos('roe_test.csv', 'Quality Permnos', make_monthly_data=True)
