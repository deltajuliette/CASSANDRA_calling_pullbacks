# Create custom functions for SIREN
import numpy as np
import pandas as pd
import datetime

# Creating a custom function to kick-start the EDA process
def eda_clean(df):
    print('Dataset Statistics:')
    print(f'Shape of dataframe: {df.shape}')
    print(f'% of Null values in dataframe: {round(((df.isna().sum().sum())/(df.shape[0]*df.shape[1])) * 100, 2)}%')
    print(f"% duplicate rows: {round(df[df.duplicated()].shape[0] / df.shape[0] * 100, 2)}%")
    print(f'\nColumn names: {df.columns}')
    print(f"Columns Count: \n{df.dtypes.value_counts()}")

# Converting Eurodollar futures
def derive_eurodollar_pricing(df):
    df_tidied = df.set_index('date').apply(lambda x: 100-x).drop(columns=['ed1', 'ed2']).reset_index()

    return df_tidied

# Creation of yield curve(s)
def derive_yield_curves(df):
    df_tidied = df.copy()
    if sum(df_tidied.columns.str.startswith('us_')) > 0:
        # df_tidied['us_30y10ys'] = df_tidied.iloc[:, 5] - df_tidied.iloc[:, 4]
        # df_tidied['us_30y5ys'] = df_tidied.iloc[:, 5] - df_tidied.iloc[:, 3]
        # df_tidied['us_30y2ys'] = df_tidied.iloc[:, 5] - df_tidied.iloc[:, 2]
        # df_tidied['us_30y3ms'] = df_tidied.iloc[:, 5] - df_tidied.iloc[:, 1]
        # df_tidied['us_10y5ys'] = df_tidied.iloc[:, 4] - df_tidied.iloc[:, 3]
        df_tidied['us_10y2ys'] = df_tidied.iloc[:, 2] - df_tidied.iloc[:, 1]
        # df_tidied['us_10y3ms'] = df_tidied.iloc[:, 4] - df_tidied.iloc[:, 1]
        # df_tidied['us_5y2ys'] = df_tidied.iloc[:, 3] - df_tidied.iloc[:, 2]
        # df_tidied['us_5y3ms'] = df_tidied.iloc[:, 3] - df_tidied.iloc[:, 1]
        # df_tidied['us_2y3ms'] = df_tidied.iloc[:, 2] - df_tidied.iloc[:, 1]
        
    if sum(df_tidied.columns.str.startswith('eu_')) > 0:
        # df_tidied['eu_30y10ys'] = df_tidied.iloc[:, 5] - df_tidied.iloc[:, 4]
        # df_tidied['eu_30y5ys'] = df_tidied.iloc[:, 5] - df_tidied.iloc[:, 3]
        # df_tidied['eu_30y2ys'] = df_tidied.iloc[:, 5] - df_tidied.iloc[:, 2]
        # df_tidied['eu_30y3ms'] = df_tidied.iloc[:, 5] - df_tidied.iloc[:, 1]
        # df_tidied['eu_10y5ys'] = df_tidied.iloc[:, 4] - df_tidied.iloc[:, 3]
        df_tidied['eu_10y2ys'] = df_tidied.iloc[:, 2] - df_tidied.iloc[:, 1]
        # df_tidied['eu_10y3ms'] = df_tidied.iloc[:, 4] - df_tidied.iloc[:, 1]
        # df_tidied['eu_5y2ys'] = df_tidied.iloc[:, 3] - df_tidied.iloc[:, 2]
        # df_tidied['eu_5y3ms'] = df_tidied.iloc[:, 3] - df_tidied.iloc[:, 1]
        # df_tidied['eu_2y3ms'] = df_tidied.iloc[:, 2] - df_tidied.iloc[:, 1]   

    else: pass
    return df_tidied

# Calculate calendar spreads for commodities
def derive_cal_spreads(df):
    df_tidied = df.copy()
    if sum(df_tidied.columns.str.startswith('brent')) > 0:
        df_tidied['brent_13m1m'] = df_tidied.iloc[:, 4] - df_tidied.iloc[:, 6]
        
    if sum(df_tidied.columns.str.startswith('wti')) > 0:
        df_tidied['wti_13m1m'] = df_tidied.iloc[:, 5] - df_tidied.iloc[:, 7]

    else: pass
    return df_tidied

def fix_credit(df):
    
    # Standardise credit spreads as pp
    df['em_usd'] = df['em_usd']/100
    
    # Calculating spreads between US high-yield and US investment-grade bonds (Not adjusted for duration)
    df['us_hy_baa_spread'] = df['us_hy'] - df['us_baa']

    return df

def fix_cftc(df):

    #Standardise dates
    df['date'] = [(i - datetime.timedelta(days=i.weekday()) + datetime.timedelta(days=4)) for i in df['date']]
    df.set_index('date', inplace=True)
    # Calculating net positioning as a % of OI
    df['cftc_nc_net_pct_oi'] = df['cftc_nc_net'] / df['cftc_oi'] * 100

    return df

# Creating a custom function to calculate rolling differences
def roll_diff(df):
    
    # Standardize dates (End-of-week) for merge later
    df['date'] = [(i - datetime.timedelta(days=i.weekday()) + datetime.timedelta(days=4)) for i in df['date']]
    df.set_index('date', inplace=True)

    # Calculate rolling differences
    df_diff_1w = df.diff(1)
    df_diff_4w = df.diff(4)
    df_diff_13w = df.diff(13)
    df_diff_26w = df.diff(26)

    #Concat dataset
    df_tidied = pd.concat([df_diff_1w.add_suffix("_1w_chg"), df_diff_4w.add_suffix("_4w_chg"), 
                         df_diff_13w.add_suffix("_13w_chg"), df_diff_26w.add_suffix("_26w_chg")], axis=1)

    return df_tidied

def eri_diff(df, n1, n2):
    df['date'] = [(i - datetime.timedelta(days=i.weekday()) + datetime.timedelta(days=4)) for i in df['date']]
    df.set_index('date', inplace=True)

    # Computing upgrade / downgrade ratios
    df['net'] = df['upgrades'] / df['downgrades'] - 1

    # Calculate 3-month rolling average (This will be our ERI)
    df['eri'] = df['net'].rolling(13).mean()

    # Calculate 1-month change
    df['eri_1m_chg'] = df['eri'].diff(n1)

    # Calculate 3-month change
    df['eri_3m_chg'] = df['eri'].diff(n2)

    # Preparing dataset to be merged
    df_tidied = df[['eri', 'eri_1m_chg', 'eri_3m_chg']]

    return df_tidied

def lag_roll_pct_chg(df, n):
    df['date'] = [(i - datetime.timedelta(days=i.weekday()) + datetime.timedelta(days=4)) for i in df['date']]
    df.set_index('date', inplace=True)
    df_lagged = df.pct_change(n).shift(-n)*100

    return df_lagged

# Creating a custom function to calculate rolling differences
def roll_pct_chg(df):
    
    # Standardize dates (End-of-week) for merge later
    df['date'] = [(i - datetime.timedelta(days=i.weekday()) + datetime.timedelta(days=4)) for i in df['date']]
    df.set_index('date', inplace=True)

    # Calculate rolling differences
    df_pctchg_1w = df.pct_change(1)
    df_pctchg_4w = df.pct_change(4)
    df_pctchg_13w = df.pct_change(13)
    df_pctchg_26w = df.pct_change(26)

    #Concat dataset
    df_tidied = pd.concat([df_pctchg_1w.add_suffix("_1w_pctchg"), df_pctchg_4w.add_suffix("_4w_pctchg"), 
                         df_pctchg_13w.add_suffix("_13w_pctchg"), df_pctchg_26w.add_suffix("_26w_pctchg")], axis=1)

    return df_tidied

def log_transform_adjust_dates(df):
    df['date'] = [(i - datetime.timedelta(days=i.weekday()) + datetime.timedelta(days=4)) for i in df['date']]
    df.set_index('date', inplace=True)
    df_log = np.log1p(df)

    return df_log

def adjust_dates_only(df):
    df['date'] = [(i - datetime.timedelta(days=i.weekday()) + datetime.timedelta(days=4)) for i in df['date']]
    df.set_index('date', inplace=True)

    return df