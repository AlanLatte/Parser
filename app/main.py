from flask          import (Blueprint, render_template, request, redirect,
                            url_for, send_from_directory)
from flask          import current_app  as app

from app.parser     import get_data     as parser
from app.all_tags   import all_tags


bp  =   Blueprint('main', __name__, url_prefix='/', static_folder='/static')

@bp.route('/')
def index_page():
    return render_template('index.html')

@bp.route('/search', methods=["GET"])
def search_page():
    return render_template('search.html')

@bp.route('/team', methods=["GET"])
def team_page():
    return render_template('team.html')

@bp.route('/how', methods=["GET"])
def how_page():
    return render_template('how_to_use.html')

@bp.route('/features', methods=["GET"])
def features_page():
    return render_template('features.html')

@bp.route('/about', methods=["GET"])
def about_page():
    return render_template('about.html')

@bp.route('/contacts', methods=["GET"])
def contacts_page():
    return render_template('contacts.html')

@bp.route('/request-result', methods=["GET"])
def request_result():
    """
        request_data : list()
        name         : str()
    """
    request_data     =  request.args.get('data').split(',')
    name             =  '_'.join(sub_name for sub_name in request_data)
    parser  (
                search_data     =   request_data,
                name            =   name
            )
    return redirect(url_for('main.download_page', file_name=name, _method="GET"))

@bp.route('/download-result/<path:file_name>', methods=["GET"])
def download_page(file_name):
    if request.method == "GET":
        try:
            return send_from_directory(app.config['DATA_BASE_STORAGE'], f'{file_name}.txt', as_attachment=True)
        except:
            return redirect(url_for('.main.search_page'))

@bp.route('/search/all_tags', methods=["GET"])
def all_tags_page():
    name            = 'DATA_OF_ALL_TAGS'
    FILE_OF_TAGS    = 'TAGS'
    all_tags(
                file_name = name,
                FILE_OF_TAGS = FILE_OF_TAGS
            )
    return redirect(url_for('main.download_page', file_name=name, _method="GET"))


if __name__ == '__main__':
    app.run()
