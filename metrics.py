import pandas as pd

'''Metrics used for quality portfolios are described below'''

def return_on_equity(df):
    '''

    :param df: (pandas dataframe) dataframe with the columns used below
    :return: (pandas dataframe) dataframe with added roe column

    '''

    df['bvps'] = (df['atq']-df['ltq'])/(df['cshoq']*df['mkvaltq'])
    df['roe'] = df['epsx12']/df['bvps']

    return df


def debt_to_equity(df):
    '''

    :param df: (pandas dataframe) dataframe with the columns used below
    :return: (pandas dataframe) dataframe with added dte column

    '''

    df['bv'] = (df['atq']-df['ltq'])/df['mkvaltq']
    df['dte'] = df['ltq']/df['bv']

    return df


if __name__ == '__main__':
    test = return_on_equity()