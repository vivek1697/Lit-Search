import sqlite3
from flask import Flask, render_template
from webforms import SearchForm
import sqlalchemy as db





app = Flask(__name__)
app.config["SECRET_KEY"] = "12345678"

@app.route('/')
def index():
    engine = db.create_engine('sqlite:///Article.db')
    connection = engine.connect()
    metadata = db.MetaData()
    articles = db.Table('Article', metadata, autoload=True, autoload_with=engine)
    query = db.select([articles])
    result_proxy = connection.execute(query)
    
    result_set = result_proxy.fetchall()
    return render_template('index.html', articles = result_set)

@app.context_processor
def base():
    form = SearchForm()
    return dict(form = form)

# Create a search functionality
@app.route('/search', methods=["POST"])
def search():
    form  = SearchForm()
    engine = db.create_engine('sqlite:///Article.db')
    connection = engine.connect()
    metadata = db.MetaData()
    articles = db.Table('Article', metadata, autoload=True, autoload_with=engine)
    query = db.select([articles])
    result_proxy = connection.execute(query)
    articles = result_proxy.fetchall()
    

    if form.validate_on_submit():
        
        article_searched = form.searched.data
        # Query the Database
        articles = articles.filter(Article.heading.like('%' + article_searched + '%'))
		

        return render_template("search.html", form = form, searched = article_searched, articles = articles)
        
        
        


@app.route("/about")
def about():
    return render_template('about.html')