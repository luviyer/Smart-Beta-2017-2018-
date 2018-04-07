import pandas as pd

'''Metrics used for quality portfolios are described below'''

def return_on_equity(df):
    '''

    :param df: (pandas dataframe) dataframe with the columns used below
    :return: (pandas dataframe) dataframe with added roe column

    '''

    df['bvps'] = (df['atq']-df['ltq'])/df['cshoq']
    df['roe'] = df['epsx12']/df['bvps']

    return df[['roe']]


def debt_to_equity(df):
    '''

    :param df: (pandas dataframe) dataframe with the columns used below
    :return: (pandas dataframe) dataframe with only one column: dte

    '''

    df['bv'] = df['atq']-df['ltq']
    df['dte'] = df['ltq']/df['bv']

    return df[['dte']]


'''Metrics used for min vol portfolios are described below'''
def trailing_12mo_vol(df):
    '''

    :param df: (pandas dataframe) dataframe with the columns used below. Make sure has data for 12 mos before start date
    :return: (pandas dataframe) dataframe with only one column: invvol

    '''

    # We'll use trailing 12 month volatility of monthly returns.
    df['12mo_vol'] = df['trt1m'].rolling(window=12).std()

    return df[['12mo_vol']]

if __name__ == '__main__':
    pass