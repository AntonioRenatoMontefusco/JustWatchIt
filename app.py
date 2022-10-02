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


@app.route("/query/find_by_year", methods=['POST'])
def find_by_year():
    if request.method == 'POST':
        year = request.form['year']
        results = query.find_by_year(year)
        return render_template('/query.html', results=results, size=len(results), title="Ricerca per anno: " + year)
    return json.dumps({"ok": True})


@app.route("/query/show_update", methods=['POST'])
def show_update():
    title = request.form["title"]
    year = request.form["year"]

    res = query.find_by_title_and_year(title=title, year=year)
    return render_template('/update.html', element=res)


if __name__ == '__main__':
    app.run()
