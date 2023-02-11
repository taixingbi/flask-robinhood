from math import ceil
import yfinance as yf
from datetime import datetime
import pytz

try:
    from robin.credential import rbCredential
except:
    from credential import rbCredential

rs = rbCredential().login()

class robintrade:
    def __init__(self, symbol, quantity, key):
        print("robintrade init")
        self.ESTTime = self.ESTTime()
        self.symbol = symbol
        self.quantity = quantity
        self.key = key
        self.symbol = symbol
        self.strike = self.getCurrentPrice()
        self.expirationDate = self.getTomorrowDate()
        self.call_debit = self.getBestDebit("call")
        self.put_debit = self.getBestDebit("put")

    def ESTTime(self):
        newYorkTz = pytz.timezone("America/New_York") 
        timeInNewYork = datetime.now(newYorkTz)
        return timeInNewYork.strftime("%Y-%m-%d %H:%M:%S")

    def getTomorrowDate(self):
        # return "2023-02-10"
        tk = yf.Ticker("SPY")
        exps = tk.options
        return exps[1]

    def getCurrentPrice(self):
        price = rs.stocks.get_latest_price(self.symbol, includeExtendedHours=True)
        price = int(float(price[0]))
        # print(self.symbol, price)
        return price

    def getBestDebit(self, optionType):
        best_bid = rs.options.find_options_by_expiration_and_strike(self.symbol,
                                                 self.expirationDate,
                                                 self.strike,
                                                 optionType= optionType,
                                                 info='bid_price')
        best_ask = rs.options.find_options_by_expiration_and_strike(self.symbol,
                                                 self.expirationDate,
                                                 self.strike,
                                                 optionType= optionType,
                                                 info='ask_price')
        best_bid, best_ask = float(best_bid[0]), float(best_ask[0])
        best_debit = float((best_bid + best_ask)/2)
        best_debit = ceil(best_debit * 100) / 100.0
        print(self.symbol, self.expirationDate, optionType, best_debit, "(",best_bid,best_ask,")")
        dic_debit = {"symbol": "SPY", "symbol": self.symbol,  "expirationDate": self.expirationDate, "optionType": optionType, "best_debit": best_debit, "best_bid": best_bid, "best_ask": best_ask} 
        return dic_debit

    def order(self, optionType):
        print(optionType)
        debit = self.call_debit["best_debit"] if optionType == "call" else self.put_debit["best_debit"]
        res = rs.orders.order_buy_option_limit(positionEffect = 'open', 
                                        creditOrDebit = 'debit', 
                                        price= debit,  # option price of debit
                                        symbol= self.symbol,
                                        quantity= self.quantity,
                                        expirationDate= self.expirationDate, 
                                        strike=  self.strike, 
                                        optionType= optionType, 
                                        timeInForce='gtc')
        # print(res)
        return res

    def straddle(self, order):
        order_call_robinhood, order_put_robinhood = None, None
        if self.key == "abcd":  
            order_call_robinhood = self.order("call")
            order_put_robinhood =  self.order("put")
        # print(self.symbol, self.expirationDate, "$"+str(self.strike), "$"+str(round(self.call_debit + self.put_debit,2)))
        debit = "$"+str(round(self.call_debit["best_debit"] + self.put_debit["best_debit"],2))
        summary = {"symbol": self.symbol, "type": "straddle", "expirationDate": self.expirationDate, "debit": debit, "estTime": self.ESTTime}
        response = {"summary": summary , "call_debit": self.call_debit, "put_debit": self.put_debit, "order_call_robinhood": order_call_robinhood, "order_put_robinhood": order_put_robinhood}
        print(response)
        return response

    def cancelAllOrders(self):
        rs.orders.cancel_all_option_orders()

if __name__ == '__main__':
    robintrade(quantity=1).straddle(order = False)


