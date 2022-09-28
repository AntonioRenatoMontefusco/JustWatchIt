from flask import Flask, render_template, request
from dataCleaning import main_proc
import query_manager as query
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    # return main_proc()
    return render_template('/index.html')


@app.route("/query/find_by_type", methods=['POST'])
def find_by_type():
    if request.method == 'POST':
        name = request.form['type']
        results = query.filter_by_type(name)
        return render_template('/query.html', results=results, size=len(results),
                               title="Ricerca per tipologia: " + name)
    return json.dumps({"ok": True})


@app.route("/query/find_by_genre", methods=['POST'])
def find_by_genre():
    if request.method == 'POST':
        genre = request.form['genre']
        results = query.find_by_genres(genre)
        return render_template('/query.html', results=results, size=len(results),
                               title="Ricerca per genere: " + genre)
    return json.dumps({"ok": True})


@app.route("/query/find_by_title_and_year", methods=['POST'])
def find_by_title_and_year():
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        results = query.find_by_title_and_year(title, year)
        return render_template('/query.html', results=results, size=len(results),
                               title="Ricerca per titolo e anno di uscita: " + title + "uscito nel " + year)
    return json.dumps({"ok": True})


@app.route("/query/find_by_title", methods=['POST'])
def find_by_year():
    if request.method == 'POST':
        title = request.form['title']
        results = query.find_by_title(title)
        return render_template('/query.html', results=results, size=len(results), title="Ricerca per titolo: " + title)
    return json.dumps({"ok": True})


@app.route("/query/find_by_year", methods=['POST'])
def find_by_title():
    if request.method == 'POST':
        year = request.form['year']
        results = query.find_by_year(year)
        return render_template('/query.html', results=results, size=len(results), title="Ricerca per anno: " + year)
    return json.dumps({"ok": True})


if __name__ == '__main__':
    app.run()
