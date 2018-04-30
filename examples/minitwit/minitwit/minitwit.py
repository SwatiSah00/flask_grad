# -*- coding: utf-8 -*-
"""
    MiniTwit
    ~~~~~~~~

    A microblogging application written with Flask and sqlite3.

    :copyright: © 2010 by the Pallets team.
    :license: BSD, see LICENSE for more details.
"""

import time
import requests
import json
#from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash, _app_ctx_stack
from werkzeug import check_password_hash, generate_password_hash
#from mt_api import query_db, get_db


API_BASE_URL = 'http://localhost:5100'
#DATABASE = '/tmp/minitwit.db'
#PER_PAGE = 30
DEBUG = True
SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'

app = Flask('minitwit')
app.config.from_object(__name__)
app.config.from_envvar('MINITWIT_SETTINGS', silent=True)

def get_user_id(username):
    """Convenience method to look up the id for a username."""
    rv = requests.get(API_BASE_URL + '/api/v1.0/resources/users/{}'.format(username))
    return rv.json()['uID']
    #return rv.text


def format_datetime(timestamp):
    """Format a timestamp for display."""
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d @ %H:%M')


def gravatar_url(email, size=80):
    """Return the gravatar image for the given email address."""
    return 'https://www.gravatar.com/avatar/%s?d=identicon&s=%d' % \
        (md5(email.strip().lower().encode('utf-8')).hexdigest(), size)


@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        print('*****************')
        #g.user = query_db('select * from user where user_id = ?',
                          #[session['user_id']], one=True)
        payload={'user_id': session['user_id']}
        print('payload: {}'.format(payload))
        rv = requests.post(API_BASE_URL +'/api/v1.0/resources/user', json=payload)
        g.user= rv.json().get('g.user')
        print('g.user:{}'.format(g.user))


@app.route('/')
def timeline():
    """Shows a users timeline or if no user is logged in it will
    redirect to the public timeline.  This timeline shows the user's
    messages as well as all the messages of followed users.
    """
    if not g.user:
        return redirect(url_for('public_timeline'))
    #return render_template('timeline.html', messages=query_db('''
        #select message.*, user.* from message, user
        #where message.author_id = user.user_id and (
            #user.user_id = ? or
            #user.user_id in (select whom_id from follower
                                    #where who_id = ?))
        #order by message.pub_date desc limit ?''',
        #[session['user_id'], session['user_id'], PER_PAGE]))
    user_id = session['user_id']
    print('user_id:{}'.format(user_id))
    payload={'user_id' : user_id}
    rv = requests.post(API_BASE_URL +'/api/v1.0/resources/', json=payload)
    response = rv.json()
    return render_template('timeline.html', messages=response.get('messages')) 


@app.route('/public')
def public_timeline():
    """Displays the latest messages of all users."""
    rv = requests.get(API_BASE_URL +'/api/v1.0/resources/timeline/public')
    #print('rv.text():{}'.format(rv.text()))
    print('rv.json():{}'.format(rv.json()))
    response = rv.json()
    return render_template('timeline.html',  messages=response.get('messages'))
    #return render_template('timeline.html', messages=query_db('''select message.*, user.* from message, user where message.author_id = user.user_id order by message.pub_date desc limit ?''', [PER_PAGE]))



@app.route('/<username>/follow')
def follow_user(username):
    """Adds the current user as follower of the given user."""
    if not g.user:
        abort(401)
    whom_id = get_user_id(username)
    if whom_id is None:
        abort(404)
    user_id = session['user_id']
    payload = {'whom_id': whom_id}
    rv = requests.post(API_BASE_URL +'/api/v1.0/resources/users/{}/follow'.format(user_id), json=payload)
    return redirect(url_for('user_timeline', username=username))


@app.route('/favicon.ico')
def empty_response():
    return '' 

@app.route('/<username>')
def user_timeline(username):
    """Display's a users tweets."""
    #profile_user = query_db('select * from user where username = ?',
                            #[username], one=True)
    #print(username)
    #print(session['user_id'])
    #print(profile_user['user_id'])
    #if profile_user is None:
        #abort(404)
    #followed = False
    payload = {}
    if g.user:
        payload = {'user_id': session['user_id']}
        print('payload:{}'.format(payload))
    print('payload out of if:{}'.format(payload))
    print('username:{}'.format(username))
    rv = requests.post(API_BASE_URL +'/api/v1.0/resources/timeline/{}'.format(username), json=payload)
    
    response = rv.json()
    profile_user = response['profile_user']
    #profile_user = rv.json()['profile_user']
    if profile_user is None:
        abort(404)
        #followed = query_db('''select 1 from follower where
            #follower.who_id = ? and follower.whom_id = ?''',
            #[session['user_id'], profile_user['user_id']],
            #one=True) is not None
        #print('followed')
        #print(followed)
    #return render_template('timeline.html', messages=query_db('''
            #select message.*, user.* from message, user where
            #user.user_id = message.author_id and user.user_id = ?
            #order by message.pub_date desc limit ?''',
            #[profile_user['user_id'], PER_PAGE]), followed=followed,
            #profile_user=profile_user)

    #return render_template('timeline.html', messages=rv.json()['messages'], followed=rv.json()['followed'], profile_user=profile_user)
    return render_template('timeline.html', messages=response.get('messages'), followed=response.get('followed'), profile_user=profile_user) 
@app.route('/<username>/unfollow')
def unfollow_user(username):
    """Removes the current user as follower of the given user."""
    #if not g.user:
    #    abort(401)
    whom_id = get_user_id(username)
    print (whom_id)
    if whom_id is None:
        abort(404)
    user_id = session['user_id']
    payload = {'whom_id': whom_id}
    rv = requests.post(API_BASE_URL +'/api/v1.0/resources/users/{}/unfollow'.format(user_id), json=payload)
    return redirect(url_for('user_timeline', username=username))



@app.route('/add_message', methods=['POST'])
def add_message():
    """Registers a new message for the user."""
    print('WWWWWWWWWWWWWWWWWWWWWWWWW')
    if 'user_id' not in session:
        abort(401)
    if request.form['text']:
    	author_id = session['user_id']
    	text = request.form['text']
        #print(author_id)
        #print(text)
        payload={'text':text}
        rv = requests.post(API_BASE_URL +'/api/v1.0/resources/messages_add/{}'.format(author_id), json=payload)
    return redirect(url_for('timeline'))
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Logs the user in."""
    if g.user:
        return redirect(url_for('timeline'))
    error = None
    if request.method == 'POST':
        username = request.form['username']
        rv = requests.get(API_BASE_URL + '/api/v1.0/resources/users/login/{}'.format(username))
        user = rv.json()['user']
        #user = query_db('''select * from user where
            #username = ?''', [request.form['username']], one=True)
        if user is None:
            error = 'Invalid username'
        elif not check_password_hash(user[0]['pw_hash'],
                                     request.form['password']):
            error = 'Invalid password'
        else:
            flash('You were logged in')
            session['user_id'] = user[0]['user_id']
            return redirect(url_for('timeline'))
    return render_template('login.html', error=error)

@app.route('/mostviewed')
def mostviewed():
    print('qqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqq')
    rv = requests.get(API_BASE_URL +'/api/v1.0/resources/mostviewed')
    response = rv.json()
    print('rv.json():{}'.format(rv.json()))
    return render_template('mostviewed.html',data=response['data'])
    #return render_template('timeline.html',  messages=response.get('messa
    #return str(response['data'])

@app.route('/mostfollowed')
def mostfollowed():
    print('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
    rv = requests.get(API_BASE_URL +'/api/v1.0/resources/mostfollowed')
    print('rv.json():{}'.format(rv.json()))
    return render_template('most-followed.html',data=rv.json()['data'])

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registers the user."""
    if g.user:
        return redirect(url_for('timeline'))
    error = None
    if request.method == 'POST':
        if not request.form['username']:
            error = 'You have to enter a username'
        elif not request.form['email'] or \
                '@' not in request.form['email']:
            error = 'You have to enter a valid email address'
        elif not request.form['password']:
            error = 'You have to enter a password'
        elif request.form['password'] != request.form['password2']:
            error = 'The two passwords do not match'
        elif get_user_id(request.form['username']) is not None:
            error = 'The username is already taken'
        else:
            payload={'username':request.form['username'], 'email':request.form['email'], 'pw_hash':generate_password_hash(request.form['password'])}
            rv = requests.post(API_BASE_URL +'/api/v1.0/register', json=payload)
            return redirect(url_for('login'))
    return render_template('register.html', error=error)


@app.route('/logout')
def logout():
    """Logs the user out."""
    flash('You were logged out')
    session.pop('user_id', None)
    return redirect(url_for('public_timeline'))

@app.route('/test')
def hellow():
    print('here')

# add some filters to jinja
app.jinja_env.filters['datetimeformat'] = format_datetime
app.jinja_env.filters['gravatar'] = gravatar_url
