import time
import logging
import random
import decimal
import requests
import json

SRC_URL='https://finance.yahoo.com/currencies/'
SOI=[	('ETHUSD=X','Ethereum-USD'),
		('BTC-USD','Bitcoin-USD'),
		('GBPUSD=X','GBP-USD'),
		('^DJI','Dow Jones Industrial Avg'),
		('^VIX','VIX Volatility Index'),
		('^GSPC','S&P 500'),
		('EURUSD=X','EUR-USD')
		]
#KAFKA_TOPIC='prices'


#PX_SIMULATED={}

# Grab actual market prices from Yahoo Finance
def getMarketPrices():
	TO_RET={}
	url = requests.get(SRC_URL)
	htmltext = url.text
	STRING_INDEX_PX_JSON_START=htmltext.find("root.App.main =")
	STRING_INDEX_PX_JSON_END=htmltext.find("}(this));")
	STRING_PX_JSON = htmltext[STRING_INDEX_PX_JSON_START+16:STRING_INDEX_PX_JSON_END-2]
	j=json.loads(STRING_PX_JSON)
	for (ticker,desc) in SOI:
		TO_RET[ticker]=j['context']['dispatcher']['stores']['StreamDataStore']['quoteData'][ticker]['regularMarketPrice']['raw']
	return TO_RET

def main():
	logging.basicConfig(format='%(asctime)s  %(levelname)s:%(message)s', level=logging.INFO)
	#logging.info("Writing to topic %s " % KAFKA_TOPIC)

	#producer = KafkaProducer()

	tick_id=100000
	while True:
		PX_MARKET_ACTUAL=getMarketPrices()
		PX_SIMULATED=PX_MARKET_ACTUAL

		logging.info("Actual Market Price Obtained as seed")

		for _ in range(100000):

			for (ticker,desc) in SOI:
				tick_id = tick_id + 1
				if tick_id%5000==0:
					logging.debug("Produced item " + str(tick_id))

				# fuzzer str(round(answer, 2))
				PX_SIMULATED[ticker]=PX_SIMULATED[ticker]*random.uniform(.999,1.001)

				tick = {}
				tick['tickid'] = tick_id
				tick['ticker'] = ticker
				tick['desc'] = desc
				tick['pxlast'] = round(float(PX_SIMULATED[ticker]),2)

				tickOnWire=str(json.dumps(tick))
				#future = producer.send(KAFKA_TOPIC, tickOnWire.encode())
				#result = future.get(timeout=60)
				logging.info("Fuzzed Price Mumble " + tickOnWire)
				time.sleep(1) # slow down the production so i can actually follow it on the screen

if __name__ == '__main__':
    main()			