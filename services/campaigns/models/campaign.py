import mongoengine
import mongoengine.fields as fields
import datetime
# from bson import ObjectID


class Campaign(mongoengine.Document):
    mongoengine.connect(db='mop', host='mongodb://mongo_main:27017/mop',
                    alias='campaigns_connection')

    meta = {'collection': 'mop_campaigns',
            'allow_inheritance': True, 'db_alias': 'campaigns_connection'}

    name = fields.StringField(required=True)
    gameMaster = fields.StringField(required=True)
    players = fields.ListField(fields.StringField(), required=False)
    characters = fields.ListField(fields.ObjectIdField(), required=False)
    rules = fields.ListField(fields.ObjectIdField())
    initial_date = fields.DateTimeField(default=datetime.datetime.utcnow)
