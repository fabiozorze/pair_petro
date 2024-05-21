import MetaTrader5 as mt5
import pandas as pd
import numpy as np

def get_ohlc(ativo, timeframe, n=None):
    ativo = mt5.copy_rates_from_pos(ativo, timeframe, 0, n)
    ativo = pd.DataFrame(ativo)
    ativo = ativo.rename(columns={'time': 'date', 'open': 'open', 'high': 'high', 'low': 'low', 'close': 'close'})
    ativo['date'] = pd.to_datetime(ativo['date'], unit='s')
    ativo.set_index('date', inplace=True)

    return ativo

def BB (df, lookback, std_dev):

    # Moving Average
    df['moving_average'] = df.spread.rolling(lookback).mean()
    # Moving Standard Deviation
    df['moving_std_dev'] = df.spread.rolling(lookback).std()

    # Upper band and lower band
    df['upper_band'] = df.moving_average + std_dev*df.moving_std_dev
    df['lower_band'] = df.moving_average - std_dev*df.moving_std_dev

    # Long positions
    df['long_entry'] = df.spread < df.lower_band
    df['long_exit'] = df.spread >= df.moving_average

    df['positions_long'] = np.nan
    df.loc[df.long_entry, 'positions_long'] = 1
    df.loc[df.long_exit, 'positions_long'] = 0
    df.positions_long = df.positions_long.fillna(method='ffill')

    # Short positions
    df['short_entry'] = df.spread > df.upper_band
    df['short_exit'] = df.spread <= df.moving_average

    df['positions_short'] = np.nan
    df.loc[df.short_entry, 'positions_short'] = -1
    df.loc[df.short_exit, 'positions_short'] = 0

    df.positions_short = df.positions_short.fillna(method='ffill')

    # Positions
    df['positions'] = df.positions_long + df.positions_short

    return df


