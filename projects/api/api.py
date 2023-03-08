import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
        d = {}
        
        for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
        return d

@app.route('/', methods=['GET'])
def home():
        return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"

@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('books.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM books;').fetchall()
    
    return jsonify(all_books)

@app.route('/api/v1/resources/books', methods=['GET'])
def api_id():
        print("@@@@@@@@@@@@@@@@@@@@@@@@@ " + str(request.args))
        
        if 'id' in request.args:
                id = int(request.args['id'])
        else:
                return "Error: No id field provided. Please specify an id."
        
        results = []
        
        for book in books:
                if book['id'] == id:
                        results.append(book)
                        
        return jsonify(results)

app.run()