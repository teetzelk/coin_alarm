from time import sleep
from coinmarketcap import Market
import requests

#Initialize and set initial variables
oldBTC = .01
oldETH = .01
oldLTC = .01
uppT = 5.1
lowT = -4.5

#Define the alert to Telegram
def telegram_alert(coin, cost, perChange):
    report = {}
    report["value1"] = coin
    report["value2"] = cost
    report["value3"] = perChange
    requests.post("https://maker.ifttt.com/trigger/coin_alert/with/key/dmvKd4MLi_KFy1YAPbk65G", data=report)

#Define standard messaging to Telegram for information purposes
def telegram_msg(message):
    report = {}
    report["value1"] = message
    requests.post("https://maker.ifttt.com/trigger/ca_message_system/with/key/dmvKd4MLi_KFy1YAPbk65G", data=report)

telegram_msg("Reinitializing program")
sleep(2)

tmsg = f'Threshold: {uppT:0.2f}% to {lowT:0.2f}%'
telegram_msg(tmsg)

while True:
    #pull out the data from Coin Market Cap site
    cmc = Market()
    dataBTC = cmc.ticker('bitcoin')
    dataETH = cmc.ticker('ethereum')
    dataLTC = cmc.ticker('litecoin')
    BTC = dataBTC[0]
    ETH = dataETH[0]
    LTC = dataLTC[0]

    #Convert the current price from string to number
    BTCCurrent = float(BTC['price_usd'])
    ETHCurrent = float(ETH['price_usd'])
    LTCCurrent = float(LTC['price_usd'])

    #Calculate the change from the previously gathered price
    #Turn it into a "whole" number for readability
    BTCChange = ((BTCCurrent - oldBTC) / oldBTC) * 100
    ETHChange = ((ETHCurrent - oldETH) / oldETH) * 100
    LTCChange = ((LTCCurrent - oldLTC) / oldLTC) * 100
    sLTCChange = str(LTCChange)

    #If the change is outside the threshold, send notification and print it
    if (BTCChange >= uppT) or (BTCChange <= lowT) :
        telegram_alert("BTC", str(BTCCurrent), str(BTCChange))
        print("----->ALERT SENT<-----")
        print(f"Old: ${oldBTC:0.2f}-New: ${BTCCurrent:0.2f}-Change: {BTCChange:0.2f}%")

    if (ETHChange >= uppT) or (ETHChange <= lowT) :
        telegram_alert("ETH", str(ETHCurrent), str(ETHChange))
        print("----->ALERT SENT<-----")
        print(f"Old: ${oldETH:0.2f}-New: ${ETHCurrent:0.2f}-Change: {ETHChange:0.2f}%")

    if (LTCChange >= uppT) or (LTCChange <= lowT) :
        telegram_alert("LTC", str(LTCCurrent), str(LTCChange))
        print("----->ALERT SENT<-----")
        print(f"Old: ${oldLTC:0.2f}-New: ${LTCCurrent:0.2f}-Change: {LTCChange:0.2f}%")

    #Set the new "old" price
    oldBTC = float(BTC['price_usd'])
    oldETH = float(ETH['price_usd'])
    oldLTC = float(LTC['price_usd'])

    #telegram_msg("Completed cycle - this is a test")

    #wait 1 minute to avoid calling the request too often
    sleep(60)
