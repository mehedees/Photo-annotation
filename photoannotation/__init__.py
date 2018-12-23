from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'edfaf0ea54d28cf8d331d4f951fbfdbe'

from photoannotation import routes