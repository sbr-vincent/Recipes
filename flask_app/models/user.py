from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_bcrypt import Bcrypt
import re	

bcrypt = Bcrypt(app)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
# model the class after the friend table from our database
class User:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    # Now we use class methods to query our database


    def fullname(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('recipes').query_db(query)

        users = []
        for user in results:
            users.append( cls(user) )
        return users

    @classmethod
    def get_one(cls, user_id):
        query = "SELECT * FROM users WHERE id = %(id)s;"

        results = connectToMySQL('recipes').query_db(query, user_id)
        users = []
        for user in results:    
            users.append( cls(user) )
        return users[0]

    @classmethod
    def get_id(cls, data):
        results = 0
        query = "SELECT * FROM users WHERE first_name = %(fname)s AND last_name = %(lname)s;"

        results = connectToMySQL('recipes').query_db(query, data)
        return results[0]['id']
            
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( first_name , last_name , email , password, created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , %(password)s, NOW() , NOW() );"
        return connectToMySQL('recipes').query_db( query, data )
    
    @classmethod
    def delete(cls, data ):
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL('recipes').query_db( query, data )

    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(fname)s, last_name = %(lname)s, email = %(email)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('recipes').query_db( query, data)

    @classmethod
    def get_user_info(cls, id):
        # query = "SELECT * FROM users LEFT JOIN recipes ON users.id = recipes.users_id WHERE users.id = %(id)s"
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.users_id = users.id;"

        results = connectToMySQL('recipes').query_db(query, id)

        users = []
        for user in results:
            users.append(user)
        return users

    #Used for login to see if the email exists in database
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email_login)s;"
        result = connectToMySQL("recipes").query_db(query,data)
        # Didn't find a matching user
        print(result)
        if not result:
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