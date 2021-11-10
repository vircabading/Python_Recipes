# import the function that will return an instance of a connection ////////
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import login_model
import re

TARGETDATABASE = 'recipes_db'                                               # Designates the database we are using
TABLENAME = "recipes"                                                             # Designates the table we are using

# //// RECIPES CLASS ////////////////////////////////////////////////////////
class Recipes:
    def __init__( self , data ):                                        # Constructor function
        self.id = data['id']                                            # Recipe ID
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made_on = data['date_made_on']
        self.under_30_minutes = data['under_30_minutes']
        self.user_id = data['user_id']
        data['id'] = data['user_id']                                    # User ID
        self.user = login_model.LoginUsers.get_one(data)                # Get an instamnce of the user that created the recipe
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # //// FLASH ///////////////////////////////////////////////////////////

    @staticmethod
    def is_valid_recipe_data(data:dict):
        print("////////////// IS IN IS VALID RECIPE DATA ////////////////////////////////")
        is_valid = True
        if len(data['name']) < 3:
            flash("Recipe name nust be at least 3 characters long")
            is_valid = False
        if len(data['description']) < 3:
            flash("Description must be at least 3 characters long")
            is_valid = False
        if len(data['instructions']) <3:
            flash("Instructions must be at least 3 characters long")
            is_valid = False
        if len(data['date_made_on']) < 1:
            flash("Must Submit Date Made On")
            is_valid = False
        return is_valid

    # //// CREATE //////////////////////////////////////////////////////////

    # **** Insert One Method ***********************************************
    # @returns ID of created user
    @classmethod
    def create(cls, data ):
        print("**** In Create One recipe")
        query = "INSERT INTO " + TABLENAME +" ( name, description, instructions , date_made_on , under_30_minutes, user_id) VALUES ( %(name)s ,%(description)s, %(instructions)s , %(date_made_on)s, %(under_30_minutes)s, %(user_id)s );"
        print("data and query")
        print(data)
        print(query)
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL(TARGETDATABASE).query_db( query, data )
        
    # //// RETRIEVE /////////////////////////////////////////////////////////

    # **** Get All Class Method *******************************************
    # @Returns: a list of instances of the class
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM " + TABLENAME + ";"
        results = connectToMySQL(TARGETDATABASE).query_db(query)        # Call the connectToMySQL function with the target db
        list_of_instances = []                                          # Initialize an empty list where we can store instances of the class
        for class_instance in results:                                  # Iterate over the db results and create instances of the cls objects
            list_of_instances.append( cls(class_instance) )             # Add each instance of the class to the list of instances
        return list_of_instances
    
    # **** Get One Class Method *******************************************
    # @Returns: an instance of the class
    @classmethod
    def get_one(cls, data:dict):
        query = "SELECT * FROM " + TABLENAME +" WHERE id = %(id)s;"
        results = connectToMySQL(TARGETDATABASE).query_db(query, data)  # Call the connectToMySQL function with the target db
                                                                        # result is a list of a single dictionary
        return cls(results[0])                                          # return an instance of the dictionary

    # //// UPDATE //////////////////////////////////////////////////////////

    # **** Update One Class Method *****************************************
    # @Returns: Nothing
    @classmethod
    def update_one(cls, data:dict):
        query = "UPDATE " + TABLENAME +" SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_made_on=%(date_made_on)s, under_30_minutes=%(under_30_minutes)s, user_id=%(user_id)s WHERE id=%(id)s"
        return connectToMySQL(TARGETDATABASE).query_db(query, data)

    # //// DELETE //////////////////////////////////////////////////////////

    # **** Delete One Class Method *****************************************
    # @Returns: Nothing
    @classmethod
    def delete(cls, data:dict):
        query = "DELETE FROM " + TABLENAME + " WHERE id=%(id)s"
        return connectToMySQL(TARGETDATABASE).query_db(query, data)