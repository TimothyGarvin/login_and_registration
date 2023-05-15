from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
import re
regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
bcrypt = Bcrypt(app)


class Users:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_user_by_email(cls,data):
        query = """
            SELECT * FROM users
            WHERE email = %(email)s
        """
        result = connectToMySQL('login_registration').query_db(query,data)
        return cls(result[0])

    @classmethod
    def show(cls,data):
        query = """
            SELECT * FROM users
            WHERE first_name = %(first_name)s
        """
        result = connectToMySQL('login_registration').query_db(query,data)
        return cls(result[0])


    @staticmethod
    def validate_user(user):
        is_valid = True
        if user['first_name'].isalpha() == False or user['last_name'].isalpha() == False:
            flash("Names must use characters A-Z only.")
            is_valid = False
        if len(user['first_name']) < 1 or len(user['last_name']) < 1:
            flash("Name fields cannot be blank")
            is_valid = False
        if len(user['first_name']) < 2 and len(user['first_name']) > 0 or len(user['last_name']) < 2 and len(user['last_name']) > 0:
            flash("Name must be at least 2 characters.")
            is_valid = False
        if len(user['email']) < 1:
            flash("Email cannot be blank.")
            is_valid = False
        if not regex.match(user['email']):
            flash("Invalid email address.")
            is_valid = False
        if len(user['password']) < 1:
            flash("Password cannot be blank.")
            is_valid = False
        if len(user['password']) < 8 and len(user['password']) > 0:
            flash("Password must be 8 characters minimum.")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords do not match.")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_login(user):
        is_valid = True
        if len(user['password']) < 1:
            flash("Password cannot be blank.")
            is_valid = False
        query = """
            SELECT * FROM users 
            WHERE email = %(email)s
        """
        data = {
            "email" : user['email']
        }
        print(data)
        result = connectToMySQL('login_registration').query_db(query,data)
        print(result)
        if len(result) == 0:
            flash("Email or password is incorrect")
            is_valid = False
        return is_valid

    @classmethod
    def register_user(cls, data):
        query = """
            INSERT INTO users (first_name, last_name, email, password, created_at, updated_at)
            VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())
        """
        return connectToMySQL("login_registration").query_db(query, data)