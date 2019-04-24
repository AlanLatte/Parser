from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def create_app():
    return render_template('index.html')

@app.route('/search', methods=["GET", "POST"])
def search_page():
    if request.method == 'POST':
        data = request.json
        
    return render_template('search.html')

if __name__ == '__main__':
    app.run()
