from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def create_app():
    return render_template('index.html')

@app.route('/search')
def search_page():
    return render_template('search.html')

def search():
    if request.method == 'POST':
        if request.form['submit_button'] == 'submit':
            print(request.args.get('data'))

if __name__ == '__main__':
    app.run()
