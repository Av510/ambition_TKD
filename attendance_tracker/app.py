import re #python -m flask run and ctrl c to quit work

from flask import Flask, g, render_template, request

import sqlite3

app = Flask(__name__)
DATABASE = "TKD - Copy.db"
