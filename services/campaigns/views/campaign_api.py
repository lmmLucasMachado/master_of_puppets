import json
from flask_restplus import Namespace, Resource, fields
# import mongoengine.fields as fields
from flask import request, jsonify
from mongoengine import DoesNotExist, ValidationError

from controller.campaign_controller import CampaignController

from models.campaign import Campaign
from base.controller import BaseController
api = Namespace('campaign', description='Campaign namespace')


def get_controller():
	controller = BaseController(strategy=CampaignController(), model=Campaign, request=request)
	return controller


# Not sure whether should flask.restplus fields or mongoengine fields
# campaign_model = api.model('Campaign', {
#     'name': fields.StringField(required=True, description="Campaign's name"),
#     'gameMaster': fields.ObjectIdField(required=True),
#     'players': fields.ListField(fields.ObjectIdField()),
#     'characters': fields.ListField(fields.ObjectIdField()),
#     'rules': fields.ListField(fields.ObjectIdField()),
#     'session': fields.ObjectIdField(required=True)
# })

campaign_model = api.model('Campaign', {
    'name': fields.String(required=True, description="Campaign's name"),
    'gameMaster': fields.String(required=True),
    'players': fields.List(fields.String),
    'characters': fields.List(fields.String),
    'rules': fields.List(fields.String),
    'session': fields.String()
})

@api.route('/')
class CampaignList(Resource):
    @api.doc("Campaign List")
    def get(self):
        controller = get_controller()
        query = controller.list_elements()

        return jsonify(query)

    @api.doc("Campaign Creation")
    @api.expect(campaign_model)
    def post(self):
        controller = get_controller()
        args = controller.new()

        return args

@api.route('/<string:id>')
@api.response(200, 'Success')
@api.response(400, 'Item not found')
@api.param('id', 'Item identifier')

class CampaignDetail(Resource):

    param = "An integer that represents the campaign's id"

    @api.doc("Get information on a specific campaign", params={'id': param})
    @api.response(400, 'Campaign not found')
    def get(self, id):
        controller = get_controller()

        try:
            campaign = controller.get_element_detail(id)
        except (DoesNotExist, ValidationError):
            api.abort(400, 'Campaign with id {} does not exist')

        return json.loads(campaign)
    
    @api.doc("Update an campaign", params={'id': param})
    @api.expect(campaign_model)
    def put(self, id):
        controller = get_controller()

        try:
            new_campaign = controller.edit(id)
        except(DoesNotExist, ValidationError):
            api.abort(400, "Campaign with id {} does not exist")
        
        return new_campaign

    @api.doc("Delete a campaign", params={'id': param})
    def delete(self, id):
        controller = get_controller()
        deleted = controller.delete(identifier)

        return deleted