import yfinance as yf


class Stock:
    state = 0  # state: 0-normal 1-no such stock 2-fetch info failed
    code = ''
    name = ''
    price = 0.0
    ask = 0.0
    bid = 0.0
    previous_open = 0.0
    previous_close = 0.0
    float_range = 0.0
    volume = 0
    day_low = 0.0
    day_high = 0.0
    weeks_low = 0.0
    weeks_high = 0.0
    earnings_date = ''
    earnings_ave = 0.0
    earnings_low = 0.0
    earnings_high = 0.0
    site = ''
    pic_url = ''
    news = []

    def message(self):
        if(self.state == 0):
            message = '<a href="{}">[{}] {}</a>\n'.format(self.site, self.code, self.name)
            message += 'Price: <b>{:.2f} ({:+.2%})</b>\n'.format(self.price, self.float_range)
            message += 'Open: <b>{:.2f}</b>\n'.format(self.previous_open)
            message += 'Close: <b>{:.2f}</b>\n'.format(self.previous_close)
            message += 'Day Range: <b>{:.2f} - {:.2f}</b>\n'.format(self.day_low, self.day_high)
            message += '52 Weeks Range: <b>{:.2f} - {:.2f}</b>\n'.format(self.weeks_low, self.weeks_high)
            message += 'Volume: <b>{:d}</b>\n\n'.format(self.volume)

            message += 'Earnings Date: <b>{:s}</b>\n'.format(self.earnings_date)
            message += 'Earnings Averange: <b>{:.2f}</b>\n'.format(self.earnings_ave)
            message += 'Earnings Range: <b>{:.2f} - {:.2f}</b>\n'.format(self.earnings_low, self.earnings_high)
        elif(self.state == 1):
            message = 'No Such Stock Code [{:s}]'.format(self.code)
        elif(self.state == 2):
            message = 'Yahoo Server Connect Failed'
        else:
            message = 'Unknown Error'
        return message

    @staticmethod
    def Create(code):
        stock = Stock()
        stock.code = code.upper()
        try:
            yfstock = yf.Ticker(code)
            info = yfstock.info
            calendar = yfstock.calendar
        except KeyError:
            stock.state = 1
            return
        except Exception:
            stock.state = 2
            return
        # import info to stock object
        stock.name = info['shortName']
        stock.price = info['regularMarketPrice']
        stock.ask = info['ask']
        stock.bid = info['bid']
        stock.previous_open = info['open']
        stock.previous_close = info['previousClose']
        stock.float_range = (stock.price - stock.previous_close) / stock.previous_close
        stock.volume = info['volume']
        stock.day_low = info['dayLow']
        stock.day_high = info['dayHigh']
        stock.weeks_low = info['fiftyTwoWeekLow']
        stock.weeks_high = info['fiftyTwoWeekHigh']
        # earnings from calendar
        stock.earnings_date = str(calendar.values[0][0])[0:10]
        stock.earnings_ave = calendar.values[1][0]
        stock.earnings_low = calendar.values[2][0]
        stock.earnings_high = calendar.values[3][0]
        stock.site = 'https://finance.yahoo.com/quote/' + stock.code
        stock.pic_url = 'http://image.sinajs.cn/newchartv5/usstock/min/{}.gif'.format(stock.code)
        stock.state = 0
        return stock
