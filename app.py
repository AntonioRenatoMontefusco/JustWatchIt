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
def find_by_name():
    if request.method == 'POST':
        name = request.form['name']
        results = query.filter_by_type(name)
        return render_template('/query.html', results=results, size=len(results), title="Ricerca per nome: " + name)
    return json.dumps({"ok": True})


if __name__ == '__main__':
    app.run()
