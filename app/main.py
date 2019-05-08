from flask          import  (Blueprint, render_template, request, g, redirect,
                            url_for, make_response, Response, session)
from flask          import current_app as app

from app.parser     import get_data as parser

from json           import load
from os             import listdir
from time           import time

bp  =   Blueprint('main', __name__, url_prefix='/', static_folder='/static')

@bp.route('/')
def index_page():

    return render_template('index.html')

@bp.route('/search', methods=["GET", "POST"])
def search_page():
    response                     = make_response(redirect(url_for('main.result_page')))
    # TODO: c++_java != java_c++ // NEED FIX
    if request.method == 'POST':
        request_data             = request.json
        if request_data:
            name                 =  '_'.join(sub_name for sub_name in request_data)
            DATA_BASE_STORAGE    = app.config['DATA_BASE_STORAGE']
            list_of_dir_DBS      = tuple(listdir(DATA_BASE_STORAGE))
            response.set_cookie(key = "name", value = name)
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
                        return response
                    else:
                        return response
            else:
                parser  (
                            search_data     =   request_data,
                            name            =   name
                        )
                return response
    return render_template('search.html', result_url='/search/result')

@bp.route('/search/result')
def result_page():
    # TODO: Work with POST api
    name = request.cookies.get("name")
    # if (name != None) and (name != ''):
    return f'<h1>{name}</h1>'
    # return redirect('/search'

@bp.route('/team')
def team_page():
    return render_template('team.html')

if __name__ == '__main__':
    app.run()
