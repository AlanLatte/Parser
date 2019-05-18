from flask          import (Blueprint, render_template, request, redirect,
                                url_for, send_from_directory)
from flask          import current_app as app

from app.parser     import get_data as parser

bp  =   Blueprint('main', __name__, url_prefix='/', static_folder='/static')

@bp.route('/')
def index_page():
    return render_template('index.html')

@bp.route('/search', methods=["GET"])
def search_page():
    return render_template('search.html')

# TODO: изменить POST на GET
# request.args.get flask в помощь.
@bp.route('/request-result', methods=["POST"])
def request_result():
    """
        request_data : list()
        name         : str()
    """
    request_data     = request.json
    name             =  '_'.join(sub_name for sub_name in request_data)
    parser  (
                search_data     =   request_data,
                name            =   name
            )
    return redirect(url_for('main.download_page', file_name=name, _method="GET"))

@bp.route('/download-result/<path:file_name>', methods=["GET"])
def download_page(file_name):
    if request.method == "GET":
        return send_from_directory(app.config['DATA_BASE_STORAGE'], f'{file_name}.txt', as_attachment=False)

@bp.route('/team', methods=["GET"])
def team_page():
    return render_template('team.html')

if __name__ == '__main__':
    app.run()
