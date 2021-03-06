import json
from flask_restplus import Namespace, Resource, fields
from flask import request, jsonify
from mongoengine import DoesNotExist, ValidationError

from controller.character_controller import CharacterController

from models.character import Character

api = Namespace('characters', description='Character namespace')

def get_controller():
	controller = CharacterController(model=Character, request=request)
	return controller

character_model = api.model('Character', {
    'user': fields.String(required=True, description='Character\'s user'),
    'character_sheet': fields.String(required=True, description='Character\'s sheet'),
    'campaign': fields.String(required=True, description='Campaign\'s to which the character belongs')
})

@api.route('/')
class CharacterList(Resource):

    @api.doc("Character List")
    def get(self):
        controller = get_controller()
        query = controller.list_elements()

        return jsonify(query)

    @api.doc("Character creation")
    @api.expect(character_model)
    def post(self):
        controller = get_controller()
        args = controller.new()

        return args


@api.route('/<string:id>')
@api.response(200, 'Success')
@api.response(400, 'Character not found')
@api.param('id', 'Character identifier')
class CharacterDetail(Resource):

    param = "An string that represents the character's id"

    @api.doc("Get information of a specific charcter", params={'id': param})
    @api.response(400, 'Character not found')
    def get(self, id):
        controller = get_controller()

        try:
            character = controller.get_element_detail(id)
        except (DoesNotExist, ValidationError):
            api.abort(400, "Character with id {} does not exist".format(id))

        return json.loads(character)

    @api.doc("Update a character", params={'id': param})
    @api.expect(character_model)
    def put(self, id):
        controller = get_controller()

        try:
            new_character = controller.edit(id)
        except (DoesNotExist, ValidationError): 
            api.abort(400, "Character with id {} does not exist".format(id))

        return new_character

    @api.doc("Delete a character", params={'id': param})
    def delete(self, id):
        controller = get_controller()
        deleted = controller.delete(id)

        return deleted


@api.route('/<string:id>/backup')
@api.response(200, 'Success')
@api.response(400, 'Character not found')
@api.param('id', 'Character identifier')
class CharacterBackup(Resource):

    param = "An string that represents the character's id"

    @api.doc("Creates a character memento", params={'id': param})
    def post(self, id):
        controller = get_controller()
        try:
            character = controller.backup(id)
        except (DoesNotExist, ValidationError):
            api.abort(400, "Character with id {} does not exist".format(id))
        return character


@api.route('/<string:id>/undo')
@api.response(200, 'Success')
@api.response(400, 'Character not found')
@api.param('id', 'Character identifier')
class CharacterUndo(Resource):

    param = "An string that represents the character's id"

    @api.doc("Restores a character to the last memento", params={'id': param})
    def post(self, id):
        controller = get_controller()
        try:
            character = controller.undo(id)
        except (DoesNotExist, ValidationError):
            api.abort(400, "Character with id {} does not exist".format(id))

        return character
