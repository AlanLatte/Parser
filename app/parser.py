# -*- coding: utf-8 -*-
from flask import current_app as app
from bs4 import BeautifulSoup
from urllib.parse import quote
import os
import requests
import json
import time


def main(url: str, headers: dict):
    """
        type url        ==  string
        type headers    ==  dict
        type divs       ==  list
        type data       ==  dict
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
            # TODO: Добавить поиск по divs_premium. [+]
            divs_premium = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy vacancy-serp__vacancy_premium'})
            divs         = soup.find_all('div', attrs={'data-qa': 'vacancy-serp__vacancy'})
            # TODO: Привести все к DRY.
            if divs_premium:
                hh_parser(divs = divs_premium)
            if divs:
                hh_parser(divs = divs        )

def hh_parser(divs):
    global long_data
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
            wage = wage.text
        else:
            wage="45000-90000 руб."
        # Извлекаем контент
        # TODO: Переработать сбор информации.
        href = raw_data.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).get('href')
        short_responsibility = raw_data.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
        requirement = raw_data.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
        all_data = f'\n{title}\n{wage}\nОбязанности:{short_responsibility}\nТребования к кандидату:{requirement}\n\n'
        long_data += all_data

def write_file(file_name: str, data: str):
    """
        Сохранение данных
    """
    with open(os.path.join(app.config['DATA_BASE_STORAGE'], f'{file_name}.txt'), mode='w', encoding='utf8') as outfile:
        outfile.write(data)

def get_data(search_data, name, get_all_tags=False):
    global long_data
    """
        Структура url:
        https://hh.ru/search/vacancy    --  дефолт
        order_by={order_by}             --  сортировка ответа
        area={area}                     --  Размер ответа (0 -- максимум)
        text={search}                   --  текст поиска
        items_on_page={nums_of_answer}  --  количество ответов
    """

    #Генерируем все необходимые данные для создания ссылки

    long_data       =   str()
    base            =   'https://hh.ru/search/vacancy?'
    area            =   1
    order_by        =   'publication_time'
    nums_of_answer  =   100
    headers = {
        'User-Agent': "PostmanRuntime/7.11.0",
        'Accept': "*/*",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }
    #создаем вспомогательные данные
    for search_item in search_data:
        long_data += f'------{search_item}------\n'
        search      =   quote(search_item)
        main    (
                    url    =f'{base}order_by={order_by}&area={area}&text={search}&items_on_page={nums_of_answer}',
                    headers = headers
                    )
    if get_all_tags == True:
        return long_data
    else:
        write_file(file_name=name, data=long_data)

if __name__ == '__main__':
    get_data(search_data='c++', name = '', get_all_tags=False)
