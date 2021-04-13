from aan import get_alternative_article, load_article_df

from flask import Flask

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.before_first_request
def load_articles():
    load_article_df()

@app.route('/by_index/<int:index>')
def get_article_by_index(index):
    alternative_article = get_alternative_article(index)
    if alternative_article:
        return (get_alternative_article(index), 200)
    else:
        return({"error": "Failed to find a valid article"}, 400)
    
@app.route('/by_title/title')
def get_article_by_title(title):
    index = index_from_title(title)
    return get_alternative_article(index)

if __name__ == '__main__':
    app.run(threaded=True, port=5000)