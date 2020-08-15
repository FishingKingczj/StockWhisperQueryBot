import yfinance as yf
import requests
from bs4 import BeautifulSoup


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
    ave_volume = 0
    ave_10d_volume = 0
    day_low = 0.0
    day_high = 0.0
    weeks_low = 0.0
    weeks_high = 0.0
    earnings_date = ''
    industry = ''
    sector = ''
    market_cap = ''
    PE = 0.0
    # fPE = 0.0
    PS = 0.0
    EVS = 0.0
    EPS = 0.0
    # fEPS = 0.0
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
            message += '52 Weeks Range:\n<b>{:.2f} - {:.2f}</b>\n'.format(self.weeks_low, self.weeks_high)
            message += 'Volume: <b>{:d}</b>\n'.format(self.volume)
            message += 'AVG Volume: <b>{:d}</b>\n'.format(self.ave_volume)
            message += 'AVG Volume 10 days: <b>{:d}</b>\n\n'.format(self.ave_10d_volume)
            # analysis target
            message += 'Earnings Date: <b>{:s}</b>\n'.format(self.earnings_date)
            message += 'Industry: <b>{:s}</b>\n'.format(self.industry)
            message += 'Sector: <b>{:s}</b>\n'.format(self.sector)
            message += 'Market Cap: <b>{:s}</b>\n'.format(self.market_cap)
            message += 'P/E: <b>{:.2f}</b>  P/S: <b>{:.2f}</b>\n'.format(self.PE, self.PS)
            message += 'EV/S: <b>{:.2f}</b>  EPS: <b>{:.2f}</b>\n'.format(self.EVS, self.EPS)
            # news
            for n in self.news:
                message += '<a href="{:s}">{:s}</a>\n'.format(n['url'], n['title'])
                message += '{:s}\n\n'.format(n['context'])
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
        # print('Search Stock Code {}'.format(stock.code))
        try:
            yfstock = yf.Ticker(code)
            info = yfstock.info
            calendar = yfstock.calendar
        except KeyError:
            print('No Such Stock Code [{:s}]'.format(stock.code))
            stock.state = 1
            return stock
        except Exception:
            print('Yahoo Server Connect Failed')
            stock.state = 2
            return stock
        # import info to stock object
        stock.name = info['shortName']
        stock.price = info['regularMarketPrice']
        stock.ask = info['ask']
        stock.bid = info['bid']
        stock.previous_open = info['open']
        stock.previous_close = info['previousClose']
        stock.float_range = (stock.price - stock.previous_close) / stock.previous_close
        stock.volume = info['volume']
        stock.ave_volume = info['averageVolume']
        stock.ave_10d_volume = info['averageDailyVolume10Day']
        stock.day_low = info['dayLow']
        stock.day_high = info['dayHigh']
        stock.weeks_low = info['fiftyTwoWeekLow']
        stock.weeks_high = info['fiftyTwoWeekHigh']
        # earnings from calendar
        stock.earnings_date = str(calendar.values[0][0])[0:10]
        stock.industry = info['industry']
        stock.sector = info['sector']
        market_cap_number = info['marketCap'] / 1000000000
        if market_cap_number > 1000:
            stock.market_cap = '{:.2f}T'.format(market_cap_number / 1000)
        else:
            stock.market_cap = '{:.2f}B'.format(market_cap_number)
        stock.PE = info['trailingPE']
        stock.PS = info['priceToSalesTrailing12Months']
        stock.EVS = info['enterpriseToRevenue']
        stock.EPS = info['trailingEps']
        # websites and news sites
        stock.site = 'https://finance.yahoo.com/quote/' + stock.code
        stock.pic_url = 'http://image.sinajs.cn/newchartv5/usstock/min/{}.gif'.format(stock.code)
        try:
            stock.news = Stock.GetNews(stock.code)
        except Exception:
            print('Get News of [{:s}] Error'.format(stock.code))
        stock.state = 0
        return stock

    @staticmethod
    def GetNews(code):
        url = 'https://finance.yahoo.com/quote/{}'.format(code)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        base_url = 'https://finance.yahoo.com'

        array = []
        for i in range(0, 3):
            news = soup.select('.StretchedBox')[i].parent
            array.append(
                {
                    'url': base_url + news.attrs['href'],
                    'title': news.text,
                    'context': news.parent.next_sibling.text
                }
            )
        return array
