import pandas as pd

'''Metrics used for quality portfolios are described below'''

def return_on_equity(filename):
    '''
    :param filename:
    :return:
    '''

    df = pd.read_csv(filename, usecols=['LPERMNO', 'datadate', 'atq', 'ltq', 'mkvaltq', 'cshoq', 'epsx12'])

    df['bvps'] = (df['atq']-df['ltq'])/(df['cshoq']*df['mkvaltq'])
    df['roe'] = df['epsx12']/df['bvps']

    return df['roe']

if __name__ == '__main__':
    test = return_on_equity()