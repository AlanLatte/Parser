# -*- coding: utf-8 -*-
import requests, json, os, time
from bs4 import BeautifulSoup
from urllib.parse import quote

""" Change directory to current """
os.chdir(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))))

def hh_parser(url: str, headers: dict, nums_of_answer: int):
    """
        type url        ==  string
        type headers    ==  dict
        type data       ==  dict
        type divs       ==  list
    """
    #Открываем сессию.
    with requests.Session() as Session:
        #Отправляем запрос, получаем ответ в виде html
        request = Session.get(url, headers=headers)
        data =  {
                'status_request':   str()   ,
                'timestamp'     :   int()   ,
                'data_response' :   list()  ,
                'quantity'      :   int()   ,
                }
        data['timestamp'] = int(time.time())
        # Проверяем ответ сервера
        if request.status_code==200:
            data['status_request'] = 'ok'
            # Извлекаем контент из request ответа
            soup = BeautifulSoup(request.content, 'html.parser')
            # Извлекаем из контента блок 'div' с артибутами attrs
            # TODO: Добавить поиск по divs_premium.
            divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
            # range_pages = soup.find_all('a', attrs={'class' : 'bloko-button HH-Pager-Control'})
            # for page in range_pages:
            #     print(page.get('data-page'))
            for raw_data in divs:
                # Извлекаем из пресонализированного тега данные, преобразуем в текст
                title = raw_data.find('a',attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                #Извлекаем зп из html
                wage = raw_data.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
                # Если зп не указанна, так и выводим
                if wage:
                    """
                        type wage   ==  bytes
                    """
                    #Преобразуем wage в utf-8
                    # TODO: В случае записи в БД, переделать.
                    wage = wage.text
                else:
                    wage='Не указанно'
                # Извлекаем контент
                # TODO: Переработать сбор информации.
                href = raw_data.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).get('href')
                company = raw_data.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                short_responsibility = raw_data.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
                requirement = raw_data.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
                publication_date = raw_data.find('span', attrs={'class' : "vacancy-serp-item__publication-date"})
                if publication_date:

                    publication_date = publication_date.text

                else:
                    publication_date = 'Не указанно'
                procces_data =  {
                                'publication_date'      : publication_date,
                                'title'                 : title,
                                'wage'                  : wage,
                                'company'               : company,
                                'short_responsibility'  : short_responsibility,
                                'url'                   : href
                                }
                # Добавляем в json
                data['data_response'].append(procces_data)
        else:
            data['status_request'] = 'false'
    data['quantity'] = len(data['data_response'])
    write_json('data', data)


def write_json(file_name: str, data: dict):
    with open(f'{file_name}.json', mode='w', encoding='utf8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=2)
def main():
    """
        Структура url:
        https://hh.ru/search/vacancy    --  дефолт
        order_by={order_by}             --  сортировка ответа
        area={area}                     --  Размер ответа (0 -- максимум)
        search_period={period}          --  Период поиска
        text={search}                   --  текст поиска
    """
    #Формируем запрос, преобразуем его в url-подобный тип
    search = quote(input('Search: '))

    area        =   1
    period      =   7
    order_by    =   'publication_time'

    hh_parser  (
                url=f'https://hh.ru/search/vacancy?order_by={order_by}&area={area}&search_period={period}&text={search}',
                headers={
                    'accept'     : '*/*',
                    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
                        },
                nums_of_answer=40
            )
if __name__ == '__main__':
    #   Вызываем main
    main()
