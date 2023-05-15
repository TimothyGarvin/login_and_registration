from flask_app import app
from flask import render_template,redirect,request,session,flash
from flask_bcrypt import Bcrypt
from flask_app.models.users import Users
from flask import flash
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/register', methods=['POST'])
def register():
    if not Users.validate_user(request.form):
        return redirect('/')
    else:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password": pw_hash
        }
        user_id = Users.register_user(data)
        session['user_id'] = user_id
        return redirect(f'/welcome/{data["first_name"]}')

@app.route('/welcome/<string:first_name>')
def welcome(first_name):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'first_name' : first_name
    }
    return render_template('welcome.html', user=Users.show(data))

@app.route('/login',methods = ['POST'])
def login():
    if not Users.validate_login(request.form):
        return redirect('/')
    data = {
        "password" : request.form['password'],
        "email" : request.form['email'] 
    }
    user_in_db = Users.get_user_by_email(data)
    session['user_id'] = user_in_db.id
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        print("bcrypt error")
        print(user_in_db.password)
        print(request.form['password'])
        flash("Email or password is incorrect.")
        return redirect('/')
    return redirect(f'/welcome/{user_in_db.first_name}')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')