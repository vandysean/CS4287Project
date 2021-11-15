from flask import Flask, render_template, session, redirect, request
from flask.helpers import url_for
from stream2fa import stream2fa
from functools import wraps

app = Flask(__name__)
app.secret_key = b'\xcc^\x91\xea\x17-\xd0W\x03\xa7\xf8J0\xac8\xc5'

# Decorators
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session.values():
            return f(*args, **kwargs)
        else:
            return redirect('/')

    return wrap


# Routes
@app.route('/')
def home():
    # delete session variables if they exist    
    session.pop("username", None)
    session.pop("logged_in", None)
    
    return render_template('home.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/set-user-reg-details', methods=['POST'])
def set_user_reg_details():
    data = request.get_json()
 
    session['reg_username'] = data.get('username')
    session['reg_password'] = data.get('password')
    
    return 'User registration details set'

@app.route('/register')
def register():
    print(session)
    username, password = session['reg_username'], session['reg_password']
    del session['reg_username']
    del session['reg_password']
    
    session['logged_in'] = 'logged_in'
    session['username'] = username
    
    success_url = url_for('dashboard')
    failure_url = url_for('back_to_signup')
    
    return stream2fa.register_user(username=username, password=password,
                                   success_url=success_url, failure_url=failure_url)
    
@app.route('/back-to-signup')
def back_to_signup():
    session.pop("username", None)
    session.pop("logged_in", None)
    
    return redirect('/signup')
    
@app.route('/set-user-auth-details', methods=['POST'])
def set_user_auth_details():
    data = request.get_json()
    
    session['auth_username'] = data.get('username')
    session['auth_password'] = data.get('password')
    
    return 'User authorization details set'

@app.route('/authorize')
def authorize():
    username, password = session['auth_username'], session['auth_password']
    del session['auth_username']
    del session['auth_password']
    
    session['logged_in'] = 'logged_in'
    session['username'] = username

    success_url = url_for('dashboard')
    failure_url = url_for('back_to_login')
        
    return stream2fa.authorize_user(username=username, password=password,
                                   success_url=success_url, failure_url=failure_url)
    
@app.route('/back-to-login')
def back_to_login():
    session.pop("username", None)
    session.pop("logged_in", None)
    
    return redirect('/login')

@app.route('/logout')
@login_required
def logout():
    return redirect('/')

@app.route('/delete')
@login_required
def delete():
    stream2fa.delete_user(username=session['username'])
    
    return redirect('/')
    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True)
