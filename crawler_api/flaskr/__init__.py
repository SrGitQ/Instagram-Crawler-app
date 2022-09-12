from flask import Flask

app = Flask(__name__)

#routes
from .routes import home

@app.route("/")
def hello():
    return home