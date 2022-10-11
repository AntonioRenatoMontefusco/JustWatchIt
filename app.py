from flask import Flask, render_template, request
from dataCleaning import main_proc
import query_manager as query
import json
import global_param

app = Flask(__name__)


@app.route('/')
def hello_world():
    # return main_proc()
    return render_template('/index.html')


@app.route("/query/find_by_type", methods=['POST'])
def find_by_type():
    if request.method == 'POST':
        name = request.form['type']
        global_param.query_result = query.filter_by_type(name)
        global_param.number_of_pages = int(len(global_param.query_result) / global_param.limit) + 1
        return render_template('/query.html', results=global_param.query_result[0:11],
                               size=len(global_param.query_result), title=global_param.title, page=1,
                               max_pages=global_param.number_of_pages)
    return json.dumps({"ok": True})


@app.route("/query/show_update", methods=['POST'])
def show_update():
    title = request.form["title"]

    res = query.find_by_title_equals(title=title)
    return render_template('/update.html', element=res)


@app.route("/query/find_by_genre", methods=['POST'])
def find_by_genre():
    if request.method == 'POST':
        genre = request.form['genre']
        global_param.query_result = query.find_by_genres(genre)
        global_param.number_of_pages = int(len(global_param.query_result) / global_param.limit) + 1
        return render_template('/query.html', results=global_param.query_result[0:11],
                               size=len(global_param.query_result), title=global_param.title, page=1,
                               max_pages=global_param.number_of_pages)
    return json.dumps({"ok": True})


@app.route("/query/find_by_title", methods=['POST'])
def find_by_title():
    if request.method == 'POST':
        title = request.form['title']
        global_param.query_result = query.find_by_title(title)
        global_param.title= "Ricerca per titolo:" + title
        global_param.number_of_pages = int(len(global_param.query_result) / global_param.limit) + 1
        return render_template('/query.html', results=global_param.query_result[0:11],
                               size=len(global_param.query_result), title=global_param.title, page=1,
                               max_pages=global_param.number_of_pages)
    return json.dumps({"ok": True})


@app.route("/query/find_by_year", methods=['POST'])
def find_by_year():
    if request.method == 'POST':
        year = request.form['year']
        global_param.query_result = query.find_by_year(year)
        global_param.title = "Ricerca per anno: " + year
        global_param.number_of_pages = int(len(global_param.query_result) / global_param.limit) +1
        return render_template('/query.html', results=global_param.query_result[0:11],
                               size=len(global_param.query_result), title=global_param.title, page=1,
                               max_pages=global_param.number_of_pages)
    return json.dumps({"ok": True})


@app.route("/query/change_page", methods=['POST'])
def change_page():
    if request.method == 'POST':
        page = int(request.form['page'])
        modifier = int(request.form['modifier'])

        start = 0
        end = 0
        if modifier == -1:
            start = global_param.limit * (page - 1)
            end = global_param.limit * page
        else:
            start = global_param.limit * page
            end = global_param.limit * (page + 1)

        return render_template('/query.html',
                               results=global_param.query_result[
                                       start: end + 1],
                               size=len(global_param.query_result), title=global_param.title, page=page + modifier,
                               max_pages=global_param.number_of_pages)
    return json.dumps({"ok": True})


@app.route("/query/find_by_year_range", methods=['POST'])
def find_by_year_range():
    if request.method == 'POST':
        min = request.form['min_year']
        max = request.form['max_year']
        global_param.title = "Ricerca tra il: " + min + "e il "+max
        global_param.query_result = query.find_by_year_range(min, max)
        global_param.number_of_pages = int(len(global_param.query_result) / global_param.limit) + 1
        return render_template('/query.html', results=global_param.query_result[0:11],
                               size=len(global_param.query_result), title=global_param.title, page=1,
                               max_pages=global_param.number_of_pages)
    return json.dumps({"ok": True})


@app.route("/query/find_by_director", methods=['POST'])
def find_by_director():
    if request.method == 'POST':
        director = request.form['director']
        global_param.title = "Ricerca per regista:"+director
        global_param.query_result = query.find_by_director(director)
        global_param.number_of_pages = int(len(global_param.query_result) / global_param.limit) + 1
        return render_template('/query.html', results=global_param.query_result[0:11],
                               size=len(global_param.query_result), title=global_param.title, page=1,
                               max_pages=global_param.number_of_pages)
    return json.dumps({"ok": True})


@app.route("/query/find_series_by_at_least_season_count", methods=['POST'])
def find_series_by_at_least_season_count():
    if request.method == 'POST':
        seasons = request.form['seasons']
        global_param.title = "Ricerca per numero di stagioni:" + seasons
        global_param.query_result = query.find_series_by_at_least_season_count(seasons)
        global_param.number_of_pages = int(len(global_param.query_result) / global_param.limit) + 1
        return render_template('/query.html', results=global_param.query_result[0:11],
                               size=len(global_param.query_result), title=global_param.title, page=1,
                               max_pages=global_param.number_of_pages)
    return json.dumps({"ok": True})


@app.route("/query/find_by_rating", methods=['POST'])
def find_by_rating():
    if request.method == 'POST':
        rating = request.form['rating']
        global_param.title = "Ricerca per rating:" + rating
        global_param.query_result = query.find_by_rating(rating)
        global_param.number_of_pages = int(len(global_param.query_result) / global_param.limit) + 1
        return render_template('/query.html', results=global_param.query_result[0:11],
                               size=len(global_param.query_result), title=global_param.title, page=1,
                               max_pages=global_param.number_of_pages)
    return json.dumps({"ok": True})


@app.route("/query/find_orderby_date", methods=['POST'])
def find_orderby_date():
    if request.method == 'POST':
        order = request.form['order']
        global_param.title = "Ricerca ordinata per data:" + "decrescente" if order==1 else "ascendente"
        global_param.query_result = query.find_orderby_date(order)
        global_param.number_of_pages = int(len(global_param.query_result) / global_param.limit) + 1
        return render_template('/query.html', results=global_param.query_result[0:11],
                               size=len(global_param.query_result), title=global_param.title, page=1,
                               max_pages=global_param.number_of_pages)
    return json.dumps({"ok": True})


if __name__ == '__main__':
    app.run()
