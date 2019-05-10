from flask          import (Blueprint, render_template, request, redirect,
                                url_for, send_from_directory)
from flask          import current_app as app

from app.parser     import get_data as parser

from os import mkdir
bp  =   Blueprint('main', __name__, url_prefix='/', static_folder='/static')



@bp.route('/')
def index_page():
    return render_template('index.html')

@bp.route('/search', methods=["GET"])
def search_page():
    return render_template('search.html')

@bp.route('/request-result', methods=['POST'])
def request_result():
    request_data     = request.json
    name             =  '_'.join(sub_name for sub_name in request_data)
    parser  (
                search_data     =   request_data,
                name            =   name
            )
    # return redirect(f'/download-result/{name}.txt')
    return redirect("https://google.com")

@bp.route('/download-result/<path:file_name>')
def result_page(file_name):
    return send_from_directory(app.config['DATA_BASE_STORAGE'], file_name, as_attachment=True)


if __name__ == '__main__':
    app.run()
