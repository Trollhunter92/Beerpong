import websocket, json ,pprint ,talib,numpy

RSI_PERIOD = 14 
RSI_OVERBOUGHT = 70
RSI_OVERSOLD   = 30
TRADE_SYMBOL   = 'ETHUSD'
TRADE_QUANTITY = 0.05
in_position = False

closes = []
SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
def on_open(ws):
    print('opened connection')

def on_close(ws):
    print('cloesed connection')
 
def on_message(ws,message):
    print('recieved message')
    #print(message)
    json_message = json.loads(message)
    pprint.pprint(json_message)  # key(key รอง)(value) เลยเชียน pprint.pprint()

    candle = json_message['k']
    is_candle_close =  candle['x']
    close = candle['c']

    if is_candle_close:
        print("candle close at{}".format(close))
        global closes 
        closes.append(float(close))
        print("closes")
        print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes,RSI_PERIOD)
            print("all rsi callculated so far ")
            print(rsi)
            last_rsi = rsi[-1]
            print("the current rsi is{}".format(last_rsi))

            if last_rsi > RSI_OVERBOUGHT:
                if in_position:
                     print("================== Sell! Sell! Sell!====================")
                else:                        
                    print("it's overbought but you r already in position, Nothing to do")
 
                            
            if last_rsi < RSI_OVERSOLD:
                if in_position: 
                    print("it's oversold but you r already in position,Nothing to do")
                else:
                    print("================= Buy! Buy! Buy!=======================")     
        #else: print("RSI is not yet completed  RSI_PERIOD")


ws  = websocket.WebSocketApp(SOCKET,
                               on_open = on_open,
                              on_message = on_message,
                              #on_error = on_error,
                              on_close= on_close)
ws.run_forever()
