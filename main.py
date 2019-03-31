# -*- coding: utf-8 -*-
import requests, sys
from bs4 import BeautifulSoup
from urllib.parse import quote

def hh_parser(url, headers):
    """
        type url        ==  string
        type headers    ==  dict
    """
    #Открываем сессию.
    with requests.Session() as Session:
        #Отправляем запрос, получаем ответ в виде html
        request = Session.get(url, headers=headers)
        # Проверяем ответ сервера
        if request.status_code==200:
            # Извлекаем контент из request ответа
            soup = BeautifulSoup(request.content, 'html.parser')
            # Извлекаем из контента блок 'div' с артибутами attrs
            divs = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
            """
                type divs   ==  list
            """
            for data in divs:
                # Извлекаем из пресонализированного тега данные, преобразуем в текст
                title = data.find('a',attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                #Извлекаем зп из html
                wage = data.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'})
                # Если зп не указанна, так и выводим
                if wage != None:
                    """
                        type wage   ==  bytes
                    """
                    # Преобразуем wage в utf-8
                    # TODO: В случае записи в БД, переделать.
                    wage = wage.renderContents().decode('utf-8')
                    # Извлекаем контент
                    href = data.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).get('href')
                    company = data.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                    responsibility = data.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
                    requirement = data.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
                    #Создаем общую информацию
                    all_data = f'{title}\t{wage}\n{company}\n{responsibility}\n{requirement}\nurl: {href}\n'
                    print("------------Result------------")
                    print(all_data)
                else:
                    wage='Не указанно'
        else:
            print('server error')

def main():
    """
        Структура url:
        https://hh.ru/search/vacancy    --  дефолт
        area={area}                     --  Размер ответа (0 -- максимум)
        search_period={period}          --  Период поиска
        text={search}                   --  текст поиска
    """
    #Формируем запрос, преобразуем его в url-подобный тип
    search = quote(input('Search: '))
    area = 0
    period = 3
    hh_parser  (
                url=f'https://hh.ru/search/vacancy?area={area}&search_period={period}&text={search}',
                headers={
                    'accept'     : '*/*',
                    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
                        }
            )
if __name__ == '__main__':
    #   Вызываем main
    main()
