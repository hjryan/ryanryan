import sqlite3
from flask import g, session, redirect, url_for
import requests

DATABASE = 'ryanryan_db.db'

def get_db():
    db = getattr(g, '_database', None)
    if not db:
        db = g._database = sqlite3.connect(DATABASE)

    return db
    