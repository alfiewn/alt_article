from aan import load_article_df, get_by_index, get_by_title

from flask import Flask

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.before_first_request
def load_articles():
    load_article_df()

@app.route('/by_index/<int:index>')
def get_article_by_index(index):
    success, response = get_by_index(index)
    if success:
        return(response, 200)
    else:
        return(response, 400)
    
@app.route('/by_title/<string:title>')
def get_article_by_title(title):
    success, response = get_by_title(title)
    if success:
        return(response, 200)
    else:
        return(response, 400)

if __name__ == '__main__':
    app.run(threaded=True, port=5000)