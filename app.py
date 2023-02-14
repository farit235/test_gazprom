import data_init
from flask import Flask
from wiki.view import wiki_blueprint

app = Flask(__name__)

data_init.init_db()

app.register_blueprint(wiki_blueprint, url_prefix="/wiki/")

app.run()
