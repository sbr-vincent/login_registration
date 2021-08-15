from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
import re	

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Login:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM logins;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('login_schema').query_db(query)
        # Create an empty list to append our instances of logins
        logins = []
        # Iterate over the db results and create instances of logins with cls.
        for login in results:
            logins.append( cls(login) )
        return logins

    @classmethod
    def save(cls,data):
        query = "INSERT INTO logins (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s,  %(password)s, NOW(), NOW());"
        return connectToMySQL("login_schema").query_db(query, data)

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM logins WHERE email = %(email_login)s;"
        result = connectToMySQL("login_schema").query_db(query,data)
        # Didn't find a matching user
        if len(result) < 1:
            return False
        return cls(result[0])
    

    @staticmethod
    def validate_user( login ):
        is_valid = True

        if not str.isalpha(login['first_name']):
            flash("Please use letters only!")
            is_valid = False

        if len(login['first_name']) < 3:
            flash("First name is too short!")
            is_valid = False
        
        if not str.isalpha(login['last_name']):
            flash("Please use letters only!")
            is_valid = False

        if len(login['last_name']) < 3:
            flash("Last name is too short!")
            is_valid = False

        # test whether a field matches the pattern
        if not EMAIL_REGEX.match(login['email']): 
            flash("Invalid email address!")
            is_valid = False
        
        if len(login['password']) < 7:
            flash("Password is too short!")
            is_valid = False

        if login['password']  != login['password_confirm']:
            flash("Passwords do not match!")
            is_valid = False

        return is_valid