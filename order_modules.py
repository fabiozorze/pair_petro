import MetaTrader5 as mt5


def Long(Y_symbol, X_symbol, y_size=None, x_size=None):


    Y_price = mt5.symbol_info_tick(Y_symbol).last# GET PRICE POSITION CALCULATION
    X_price = mt5.symbol_info_tick(X_symbol).last# GET PRICE POSITION CALCULATION

    Y_SIZE = y_size
    X_SIZE = x_size


    ylot = Y_SIZE
    requestBuy = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": Y_symbol,
        "volume": float(ylot),
        "type": mt5.ORDER_TYPE_BUY,
        "price": Y_price,
        "magic": 10,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_TYPE_BUY_LIMIT,
    }


    xlot = X_SIZE
    requestSell = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": X_symbol,
        "volume": float(xlot),
        "type": mt5.ORDER_TYPE_SELL,
        "price": X_price,
        "magic": 10,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_TYPE_BUY_LIMIT,
    }

    return (requestBuy,requestSell)


def Short(Y_symbol, X_symbol, y_size=None, x_size=None):


    Y_price = mt5.symbol_info_tick(Y_symbol).last# GET PRICE POSITION CALCULATION
    X_price = mt5.symbol_info_tick(X_symbol).last# GET PRICE POSITION CALCULATION

    Y_SIZE = y_size
    X_SIZE = x_size

    ylot = Y_SIZE
    requestSell = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": Y_symbol,
        "volume": float(ylot),
        "type": mt5.ORDER_TYPE_SELL,
        "price": Y_price,
        "magic": 10,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_TYPE_BUY_LIMIT,
    }



    xlot = X_SIZE
    requestBuy = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": X_symbol,
        "volume": float(xlot),
        "type": mt5.ORDER_TYPE_BUY,
        "price": X_price,
        "magic": 10,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_TYPE_BUY_LIMIT,
    }

    return (requestSell, requestBuy)


def Close_Long(Y_symbol, X_symbol, y_volume, x_volume):


    Y_price = mt5.symbol_info_tick(Y_symbol).last# GET PRICE POSITION CALCULATION
    X_price = mt5.symbol_info_tick(X_symbol).last# GET PRICE POSITION CALCULATION

    requestBuy = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": Y_symbol,
        "volume": float(y_volume),
        "type": mt5.ORDER_TYPE_SELL,
        "price": Y_price,
        "magic": 10,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_TYPE_BUY_LIMIT,
    }

    requestSell = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": X_symbol,
        "volume": float(x_volume),
        "type": mt5.ORDER_TYPE_BUY,
        "price": X_price,
        "magic": 10,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_TYPE_BUY_LIMIT,
    }

    return (requestSell, requestBuy)


def Close_Short(Y_symbol, X_symbol, y_volume, x_volume):

    Y_price = mt5.symbol_info_tick(Y_symbol).last# GET PRICE POSITION CALCULATION
    X_price = mt5.symbol_info_tick(X_symbol).last# GET PRICE POSITION CALCULATION

    requestBuy = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": Y_symbol,
        "volume": float(y_volume),
        "type": mt5.ORDER_TYPE_BUY,
        "price": Y_price,
        "magic": 10,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_TYPE_BUY_LIMIT,
    }


    requestSell = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": X_symbol,
        "volume": float(x_volume),
        "type": mt5.ORDER_TYPE_SELL,
        "price": X_price,
        "magic": 10,
        "comment": "python script open",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_TYPE_BUY_LIMIT,
    }


    return (requestBuy, requestSell)


def close_position(position, symbol=None):
    position_id = position[0].ticket
    lot_size = position[0].volume
    price = mt5.symbol_info_tick(symbol).bid if position[0].type == mt5.ORDER_TYPE_BUY else mt5.symbol_info_tick(symbol).ask
    order_type = mt5.ORDER_TYPE_SELL if position[0].type == mt5.ORDER_TYPE_BUY else mt5.ORDER_TYPE_BUY

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": position[0].symbol,
        "volume": lot_size,
        "type": order_type,
        "position": position_id,
        "price": price,
        "deviation": 20,
        "magic": 234000,
        "comment": "Close position",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_RETURN,
    }

    return request