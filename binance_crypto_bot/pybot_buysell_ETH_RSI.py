# Author : Yogesh K

# Trading logic 2: 
# Relative Strength Index (RSI) is a type of momentum indicator that looks at the pace of recent price 
# changes so as to determine whether a stock is ripe for a rally or a selloff.
# When an asset is overbought, it means the price is in bullish momentum for an extended period. 
# Therefore, it’s trading at a higher price than its inherent value
# When an asset is oversold, it indicates that an asset is trading below what it is worth at its current price. 
# This happens when the asset is sold at an undervalued price over an extended period, signaling that
# it is already at its all-time low.
# The RSI overbought and oversold readings are as follow:
# A level above 70 is considered an overbought reading.
# At levels below 30, prices are considered to be in oversold territory.
# The rules are simple: Enter(buy) if the RSI crosses below 30, and exit(Sell) when it crosses above 70

########################################################
# Formula to calculate RSI =  100 – 100 / ( 1 + RS )
# where RS = Relative Strength = AvgU / AvgD
# AvgU = average of all up moves in the last N intervals
# AvgD = average of all down moves in the last N intervals
# N = the period of RSI (usually 14)
#########################################################



##################### Disclaimer!! ####################candle_msgor any losses 
#incurred if you choose to use the code developed here on Binance.
####################################################################

'''
{
  "e": "kline",     // Event type
  "E": 123456789,   // Event time
  "s": "BTCUSDT",    // Symbol
  "k": {
    "t": 123400000, // Kline start time
    "T": 123460000, // Kline close time
    "s": "BTCUSDT",  // Symbol
    "i": "1m",      // Interval
    "f": 100,       // First trade ID
    "L": 200,       // Last trade ID
    "o": "0.0010",  // Open price
    "c": "0.0020",  // Close price
    "h": "0.0025",  // High price
    "l": "0.0015",  // Low price
    "v": "1000",    // Base asset volume
    "n": 100,       // Number of trades
    "x": false,     // Is this kline closed?
    "q": "1.0000",  // Quote asset volume
    "V": "500",     // Taker buy base asset volume
    "Q": "0.500",   // Taker buy quote asset volume
    "B": "123456"   // Ignore
  }
}
'''

import os
from binance.client import Client
from binance import ThreadedWebsocketManager
import pprint
from time import sleep

import talib
import numpy

TEST_NET = True
RSI_MIN_PERIOD  = 2 # usually it is 14, but to test lets use 2 ,else we need to wait for a lot of time
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
kline_closed_values = []


# RSI logic to trade
def rsi_trading_logic(last_rsi):
    if last_rsi > RSI_OVERBOUGHT:
        try:
            print(" Sell Sell Sell...")
            order = client.order_market_sell(symbol=symbol, quantity=1)
            pprint.pprint(order)
            return True
        except Exception as e:
            print(e)
            return False
    elif last_rsi < RSI_OVERSOLD:
        try:
            print("Buy Buy Buy...")
            order = client.order_market_buy(symbol=symbol, quantity=1)
            pprint.pprint(order)
            return True
        except Exception as e:
            print(e)
            return False
    else:
        print("Do nothing.. Just Wait and Watch !!")
        # Add more code here such that if nothing happens, continue running instead of stopping






def handle_kline_message(candle_msg):
    pprint.pprint(f"kline message type: {candle_msg['e']}")
    pprint.pprint(candle_msg)
    kline = candle_msg['k']   # access the key 'k'
    is_kline_closed = kline['x']   # if true, then its end of current kline
    kline_close_value = kline['c']  # last or closing ETH value

    if is_kline_closed:
        print("kline closed at: {}".format(kline_close_value))
        kline_closed_values.append(float(kline_close_value))
        print(kline_closed_values)

        ## trading logic.
        if len(kline_closed_values) > RSI_MIN_PERIOD:
            kline_np_closed_values = numpy.array(kline_closed_values)
            rsi = talib.RSI(kline_np_closed_values, RSI_MIN_PERIOD)
            print("RSI values:", rsi)
            last_calc_rsi = rsi[-1]
            print("RSI for trading caldculations: {}".format(last_calc_rsi))
            success = rsi_trading_logic(last_calc_rsi)
            print("trading was:",success)
            twm.stop()


def main():
    twm.start()

    twm.start_kline_socket(callback=handle_kline_message, symbol=symbol, interval='1m')

    twm.join()  # main will exit if no join added




if __name__ == "__main__":
    if TEST_NET:
        api_key = os.environ.get('BINANCE_TESTNET_KEY')     # passkey (saved in bashrc for linux)
        api_secret = os.environ.get('BINANCE_TESTNET_PASSWORD')  # secret (saved in bashrc for linux)
        
        client = Client(api_key, api_secret, testnet=True)
        print("Using Binance TestNet server")
    
    twm = ThreadedWebsocketManager()
    symbol = 'ETHUSDT' #'ETHUSDT' can be changed say to say (BNBUSDT)
    main()
