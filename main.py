import requests, sys
from bs4 import BeautifulSoup as bs
from urllib.parse import quote
def parser(url, headers):
    with requests.Session() as Session:
        request = Session.get(url, headers=headers)
        if request.status_code==200:
            urls = get_urls(request, url, attrs={'data-qa': 'vacancy-serp__vacancy'}, tag='div')
        else:
            print('server error')

def get_urls(request, url, tag, attrs):
    soup = bs(request.content,'html.parser')
    div = soup.find_all(tag, attrs)
    for i in range(len(div)):
        print(div[i].find('a').get('href'))

def main():
    search = quote(input('Search: '))
    parser  (
                url=f'https://hh.ru/search/vacancy?text={search}&area=1',
                headers={
                    'accept'     : '*/*',
                    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
                        }
            )
if __name__ == '__main__':
    main()
