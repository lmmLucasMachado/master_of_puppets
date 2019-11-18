import json
from flask_restplus import Namespace, Resource, fields
from flask import request, jsonify
from mongoengine import DoesNotExist, ValidationError

from controller.event_controller import EventController

api = Namespace('events', description='Event namespace')

event_model = api.model('Event', {
    'event_type': fields.String(required=True, description='Event type (e.g.: update)'),
    'description': fields.String(required=True, description='Event description'),
    'event_date': fields.String(required=True, description='Event datetime'),
    'data' : fields.String(required=False, description='JSON that might be related')
})


@api.route('/')
class EventList(Resource):
    @api.doc("Event List")
    def get(self):
        controller = EventController(request)
        query = controller.list()

        return jsonify(query)

    @api.doc("Event creation")
    @api.expect(event_model)
    def post(self):
        controller = EventController(request)
        args = controller.new()

        return args


@api.route('/<string:id>')
@api.response(200, 'Success')
@api.response(400, 'Event not found')
@api.param('id', 'Event identifier')
class EventDetail(Resource):
    param = "An string that represents the event's id"

    @api.doc("Get information of a specific event", params={'id': param})
    @api.response(400, 'event not found')
    def get(self, id):
        controller = EventController(request)

        try:
            event = controller.get_element_detail(id)
        except (DoesNotExist, ValidationError):
            api.abort(400, "Event with id {} does not exist".format(id))

        return json.loads(event)

    @api.doc("Update a event", params={'id': param})
    @api.expect(event_model)
    def put(self, id):
        controller = EventController(request)

        try:
            new_event = controller.edit(id)
        except (DoesNotExist, ValidationError): 
            api.abort(400, "Event with id {} does not exist".format(id))

        return new_event

    @api.doc("Delete a event", params={'id': param})
    def delete(self, id):
        controller = EventController(request)
        deleted = controller.delete(id)

        return deleted
        