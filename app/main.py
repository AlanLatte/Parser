from flask import (Blueprint, render_template, request, g, redirect)
from flask import current_app as app

import app.parser as parser


bp = Blueprint('main', __name__, url_prefix='/', static_folder='/static')

@bp.route('/')
def index():
    try:
        return render_template('index.html')
    except AttributeError:
        g.error = None
        return redirect('/')

@bp.route('/search', methods=["GET", "POST"])
def search_page():
    if request.method == 'POST':
        data = request.json
        print(data)
        for item in data:
            parser.get_data(search_data=item)

    return render_template('search.html')
@bp.route('/team')
def render_team():
    return render_template('team.html')

if __name__ == '__main__':
    app.run()
