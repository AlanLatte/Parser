import requests, sys
from bs4 import BeautifulSoup as bs


def parcer(url, headers):
    with requests.Session() as Session:
        request = Session.get(url, headers=headers)
        if request.status_code==200:
            soup = bs(request.content,'html.parser')
            # div = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
            # ans = soup.find('div', class_='answercell post-layout--right')
            # print(len(div))
            # print(div)
            # print(soup.encode(encoding=))
        else:
            print('server error')


def main():
    url = "https://hh.ru/"
    headers={
                'accept'     : '*/*',
                'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
            }
    parcer(url, headers)
if __name__ == '__main__':
    main()
