from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app

# model the class after the friend table from our database
class Recipe:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under30 = data['under30']
        self.made_on = data['made_on']
        self.users_id = data['users_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data ):
        query = "INSERT INTO recipes ( name , description , instructions , under30, made_on, users_id, created_at, updated_at ) VALUES ( %(name)s , %(description)s , %(instructions)s , %(flexRadioDefault)s, %(date)s, %(user_id)s, NOW() , NOW() );"
        return connectToMySQL('recipes').query_db( query, data )

    @classmethod
    def get_one(cls, recipe_id):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"

        results = connectToMySQL('recipes').query_db(query, recipe_id)
        recipes = []
        for recipe in results:    
            recipes.append( cls(recipe) )
        return recipes[0]
    
    @classmethod
    def delete(cls, data ):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL('recipes').query_db( query, data )

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under30 = %(flexRadioDefault)s, made_on = %(date)s,  updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL('recipes').query_db( query, data)

    @staticmethod
    def validate_recipe( recipe ):
        is_valid = True

        if len(recipe['name']) == 0: 
            flash("Recipe name can't be blank")
            is_valid = False
        elif len(recipe['name']) < 3:
            flash("Recipe name is too short!")
            is_valid = False

        if len(recipe['description']) == 0: 
            flash("Description can't be blank")
            is_valid = False
        elif len(recipe['description']) < 3:
            flash("Description is too short!")
            is_valid = False

        if len(recipe['instructions']) == 0: 
            flash("Instructions can't be blank")
            is_valid = False
        elif len(recipe['instructions']) < 3:
            flash("Intructions are too short!")
            is_valid = False

        if not recipe['date']: 
            flash("Please select a date!")
            is_valid = False
    
        return is_valid