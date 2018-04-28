#This is the minitwit web api i.e. mt_api.py

import click
from flask import Flask, jsonify, request, abort
from sqlite3 import dbapi2 as sqlite3
from minitwit import *
#from flask_basicauth import BasicAuth

app = Flask(__name__)

def populate_db():
    # Populates the database
    db = get_db()
    with app.open_resource('population.sql', mode = 'r') as f:
        db.cursor().executescript(f.read())
    db.commit()

@app.cli.command('populatedb')
def populatedb_command():
    #Populates the database
    populate_db()
    print('Populated the database.')

@app.route('/api/v1.0/mt', methods=['GET'])
def get_tasks():
    return jsonify({'task': "hello world!!!"})

@app.route('/api/v1.0/register', methods=['POST'])
def register():
    """Registers the user."""
    if not request.json or not 'username' in request.json or not 'email' in request.json or not 'pw_hash' in request.json:
        abort(400)

    db = get_db()
    entry = {

        'username': request.json.get('username'),
        'email': request.json.get('email'),
        'pw_hash': request.json.get('pw_hash')
    }

    db.execute('''insert into user (
              username, email, pw_hash) values (?, ?, ?)''',(entry['username'], entry['email'],entry['pw_hash']))
    db.commit()
   # flash('Your have been registered')

   # return jsonify({'mt':entry}), 201
    return jsonify("its success"), 201

if __name__=='__main__':
    app.run(debug=true)
    #app.run(host='127.0.0.1',port=5001,debug=True)
