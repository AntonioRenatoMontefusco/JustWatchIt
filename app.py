from flask import Flask

from dataCleaning import main_proc

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return main_proc()


if __name__ == '__main__':
    app.run()
