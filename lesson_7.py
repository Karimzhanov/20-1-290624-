import schedule
import time
import requests

# def test():
#     print("Hello Geeks")
#     print(time.ctime())


def get_btc_price():
    print("=======BTC======")
    url = 'https://api.binance.com/api/v3/avgPrice?symbol=BTCUSDT'
    response = requests.get(url=url).json()
    price = response.get('price')

    print(f'Стоимость биткоина {price}, {time.ctime()}')

# get_btc_price()


# schedule.every(2).seconds.do(get_btc_price)
# # schedule.every(2).seconds.do(get_btc_price)
# # schedule.every(1).minutes.do(get_btc_price)
# # schedule.every().day.at('19:27').do(get_btc_price)
# # schedule.every().thursday.at("19:28").do(get_btc_price)
# # schedule.every().day.at("19:30", "Europe/London").do(get_btc_price)
# # schedule.every().hour.at(':25').do(get_btc_price)
schedule.every(2).seconds.do(get_btc_price)
    
while True:
    schedule.run_pending()  
    time.sleep(1)