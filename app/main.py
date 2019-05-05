from flask import  (Blueprint, render_template, request, g, redirect, jsonify,
                    url_for, make_response, Response)
from flask import current_app as app

from app.parser import get_data as parser

from json import (load, dumps, loads)
from os import listdir
from time import time

bp          =   Blueprint('main', __name__, url_prefix='/', static_folder='/static')

urls        =   {
                    'index'     :   '/',
                    'search'    :   '/search',
                    'result'    :   '/search/result',
                    'team'      :   '/team'
                }

@bp.route(urls['index'])
def index_page():

    return render_template('index.html')

@bp.route(urls['search'], methods=["GET", "POST"])
def search_page():
    response                 = make_response(redirect(url_for('.result_page')))
    # TODO: c++_java != java_c++ // NEED FIX
    if request.method == 'POST':
        request_data         = request.json
        if request_data:
            name                 =  '_'.join(sub_name for sub_name in request_data)
            DATA_BASE_STORAGE    = app.config['DATA_BASE_STORAGE']
            list_of_dir_DBS      = tuple(listdir(DATA_BASE_STORAGE))
            if f'{name}.json' in list_of_dir_DBS:
                with open(f'{DATA_BASE_STORAGE}/{name}.json', encoding='utf8') as json_file:
                    data         = load(json_file)
                    current_time = int(time())
                    timestamp    = data['timestamp']
                    if current_time - timestamp > 7200:
                        parser  (
                                    search_data     =   request_data,
                                    name            =   name
                                )
                        response.set_cookie(key = "name", value = name)
                        return response
                    else:
                        response.set_cookie(key = "name", value = name)
                        return response
            else:
                parser  (
                            search_data     =   request_data,
                            name            =   name
                        )
                response.set_cookie(key = "name", value = name)
                return response
    return render_template('search.html', result_url=urls['result'])

@bp.route(urls['result'], methods=["GET", "POST"])
def result_page():
    # TODO: Work with POST api
    name = request.cookies.get("name")
    # if (name != None) and (name != ''):
    return f'<h1>{name}</h1>'
    # return redirect('/search'



@bp.route(urls['team'])
def team_page():
    return render_template('team.html')

if __name__ == '__main__':
    app.run()
