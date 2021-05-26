import time
import pybithumb
import pyupbit

access = "H41UV5OVGzq3sQg2EKRY3NsnxUeTEd0vGFK75qw4"
seBTCt = "2r5P2ObcCHI2HFW1NF8Yza1S2Q70xPuOAQCy4J4P"


def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time


def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]


# 로그인
upbit = pyupbit.Upbit(access, seBTCt)
print("autotrade start")

# 자동매매 시작

ap = pyupbit.get_current_price("KRW-BTC")
bp = pyupbit.get_current_price("KRW-BTC")


while True:
    try:
        time.sleep(1)
        current_price = get_current_price("KRW-BTC")
        if ap > current_price:
            ap = current_price

        if bp < current_price:
            bp = current_price

        sp = ap * 1.01
        xp = bp * 0.995

        # 매수
        if sp < current_price:
            krw = get_balance("KRW")
            if krw > 5000:
                ap = pyupbit.get_current_price("KRW-BTC")
                bp = pyupbit.get_current_price("KRW-BTC")
                upbit.buy_market_order("KRW-BTC", krw*0.9995)
                # print("매수주문: ", int(krw*0.9995))

                time.sleep(5)
        #매도
        if xp > current_price:
            btc = get_balance("BTC")
            if btc > 0.00008:
                ap = pyupbit.get_current_price("KRW-BTC")
                bp = pyupbit.get_current_price("KRW-BTC")
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
                # print("매도주문: ", int(btc*0.9995))
                time.sleep(5)

    except Exception as e:
        print(e)
        time.sleep(1)
