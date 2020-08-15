# import requests
# from bs4 import BeautifulSoup
# url = 'https://finance.yahoo.com/quote/MSFT'

# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'lxml')
# base_url = 'https://finance.yahoo.com'

# news1 = soup.select('.StretchedBox')[0].parent
# print(base_url + news1.attrs['href'])
# print(news1.text)
# print(news1.parent.next_sibling.text)

# news2 = soup.select('.StretchedBox')[1].parent
# print(base_url + news2.attrs['href'])
# print(news2.text)
# print(news2.parent.next_sibling.text)

# news3 = soup.select('.StretchedBox')[2].parent
# print(base_url + news3.attrs['href'])
# print(news3.text)
# print(news3.parent.next_sibling.text)