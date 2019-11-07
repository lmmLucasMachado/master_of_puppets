
from services.base_controller import BaseController
from flask_restplus import reqparse

class CampaignController(BaseController):
    def set_new_parser(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('characters', action='append')
        self.parser.add_argument('gameMaster', required=True)
        self.parser.add_argument('name', required=True)
        self.parser.add_argument('players', action='append')
        self.parser.add_argument('rules', action='append')
        self.parser.add_argument('session')

        return self.parser


    def set_edit_parser(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('characters', required=False)
        self.parser.add_argument('gameMaster', required=False)
        self.parser.add_argument('name', required=False)
        self.parser.add_argument('players', required=False)
        self.parser.add_argument('rules', required=False)
        self.parser.add_argument('session', required=False)

        return self.parser



    def __init__(self, request):
        self.request = request

    def new(self):

        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('gameMaster', required=True)
        parser.add_argument('players', action='append')
        parser.add_argument('characters', action='append')
        parser.add_argument('rules', action='append')
        parser.add_argument('session')
        parse_result = parser.parse_args(req=self.request)

        Campaign.from_json(dumps(parse_result)).save()
    
    @staticmethod
    def list():
        list_of_campaigns = list(map(lambda campaign: loads(campaign.to_json()), Campaign.objects.all()))
        return list_of_campaigns

    @staticmethod
    def get_element_detail(identifier):
        return Campaign.objects.get(id=identifier).to_json()
    
    def edit(self, identifier):
        campaign = Campaign.objects.get(id=identifier)
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=False)
        parser.add_argument('gameMaster', required=False)
        parser.add_argument('players', required=False)
        parser.add_argument('characters', required=False)
        parser.add_argument('rules', required=False)
        parser.add_argument('session', required=False)
        parse_result = parser.parse_args(req=self.request)

        filtered_result = {k: v for k, v in parse_result.items() if v is not None}
        
        no_docs_updated = campaign.update(**filtered_result)

        if no_docs_updated == 1:
            return loads(campaign.to_json())
    
    @staticmethod
    def delete(identifier):
        target = Campaign.objects.get(id=identififer)
        target_data = loads(target.to_json())
        target.delete()

        return target_data