import pandas as pd
import numpy as np
import MetaTrader5 as mt5
import time
from datetime import datetime
import warnings

import modules as mo
import order_modules as order

import logging_module as log

# Suppress specific RuntimeWarnings
warnings.filterwarnings("ignore", category=RuntimeWarning, message="Degrees of freedom <= 0 for slice")

logger = log.logger_online()

global connection
connection = False
if not mt5.initialize():
    connection = False
    print("initialize() fail")
    mt5.shutdown()
connection = True
print(connection)


if __name__ == '__main__':

    on = True
    dt_minut_old = datetime.now().minute - 5

    while on == True:

        dt = datetime.now()
        if (dt.hour >= 18) & (dt.minute >= 24):

            if (dt.minute != dt_minut_old) & (dt.minute % 5 == 0):
                dt_minut_old = dt_minut_old = datetime.now().minute
                dt = datetime.now()
                print(dt)
                logger.info('Started cycle')

                y = 'PETR3'
                x = 'PETR4'

                data_y = mo.get_ohlc(y, mt5.TIMEFRAME_M5, n=240)['close']
                data_x = mo.get_ohlc(x, mt5.TIMEFRAME_M5, n=240)['close']

                pair_data = pd.concat([data_y,data_x],axis=1)
                pair_data.columns = [y,x]

                pair_data['spread'] = pair_data[y] - pair_data[x]

                pair_data = mo.BB(pair_data, 20, 2)


                print(str(datetime.now()) + '  RODOU TUDO')
                print(pair_data.positions[-1])
                logger.info('Finished cycle')
                logger.info(f'Old: {pair_data.positions.iloc[-2]} - New: {pair_data.positions.iloc[-1]}')

                if pair_data.positions.iloc[-1] != pair_data.positions.iloc[-2]:

                    try:
                        positions_y = mt5.positions_get(symbol=y)[0][9]
                        positions_x = mt5.positions_get(symbol=y)[0][9]
                    except:
                        positions_y = 0
                        positions_x = 0

                    ### OPEN POSITION BLOCK
                    if (positions_y == 0) & (positions_x == 0):

                        if (pair_data.positions.iloc[-2] == 0) & (pair_data.positions.iloc[-1] == 1): ### LONG SPREAD
                            print('----LONG SPREAD----')
                            logger.info('----LONG SPREAD----')

                            y_buy, x_sell = order.Long(y, x, y_size=100, x_size=100)
                            mt5.order_send(y_buy)
                            mt5.order_send(x_sell)

                        elif (pair_data.positions.iloc[-2] == 0) & (pair_data.positions.iloc[-1] == -1): ### SELL SPREAD
                            print('----SELL SPREAD----')
                            logger.info('----SELL SPREAD----')

                            y_sell, x_buy = order.Short(y, x, y_size=100, x_size=100)
                            mt5.order_send(y_sell)
                            mt5.order_send(x_buy)

                    ### CLOSE POSITION BLOCK
                    elif (positions_y != 0) & (positions_x != 0):

                        ### CLOSE LONG SPREAD
                        if (pair_data.positions.iloc[-2] == 1) & (pair_data.positions.iloc[-1] == 0):

                            try:
                                y_volume = mt5.positions_get(symbol=y)[0][9]  # GET Y VOLUME
                                x_volume = mt5.positions_get(symbol=x)[0][9]  # GET X VOLUME
                            except:
                                y_volume = 0
                                x_volume = 0
                                continue
                            print('----CLOSE LONG SPREAD----')
                            logger.info('----CLOSE LONG SPREAD----')

                            y_sell, x_buy = order.Close_Long(y, x, y_volume, x_volume)
                            mt5.order_send(y_sell)
                            mt5.order_send(x_buy)

                        ### CLOSE SHORT SPREAD
                        elif (pair_data.positions.iloc[-2] == -1) & (pair_data.positions.iloc[-1] == 0):
                            try:
                                y_volume = mt5.positions_get(symbol=y)[0][9]  # GET Y VOLUME
                                x_volume = mt5.positions_get(symbol=x)[0][9]  # GET X VOLUME
                            except:
                                y_volume = 0
                                x_volume = 0
                                continue
                            print('----CLOSE SHORT SPREAD----')
                            logger.info('----CLOSE SHORT SPREAD----')

                            y_sell, x_buy = order.Close_Short(y, x, y_volume, x_volume)
                            mt5.order_send(y_sell)
                            mt5.order_send(x_buy)

                else:
                    print('----FAZER NADA----')
                    logger.info('----FAZER NADA----')

        elif (dt.hour >= 20) & (dt.minute >= 45):
            if (positions_y != 0) & (positions_x != 0):

                positions_y = mt5.positions_get(symbol=y)
                positions_x = mt5.positions_get(symbol=x)

                close_y = order.close_position(positions_y, symbol=y)
                mt5.order_send(close_y)

                close_x = order.close_position(positions_x, symbol=x)
                mt5.order_send(close_x)

        print('----STOP STRATEGY----')
        logger.info('----STOP STRATEGY----')

        formatted_date = dt.strftime('%Y-%m-%d')
        pair_data.to_csv(rf'C:\Users\Fabio\PycharmProjects\pair_petro\data_save\{formatted_date}')

        break

