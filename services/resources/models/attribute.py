import mongoengine
import mongoengine.fields as fields

from models.base_document import BaseDocument


class Attribute(BaseDocument):
    meta = {'collection': 'mop_attributes'}
    
    strength = fields.IntField(min_value=0)
    dexterity = fields.IntField(min_value=0)
    constitution = fields.IntField(min_value=0)
    intelligence = fields.IntField(min_value=0)
    wisdom = fields.IntField(min_value=0)
    charisma = fields.IntField(min_value=0)
