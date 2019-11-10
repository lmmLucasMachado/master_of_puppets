
from base.controller import Strategy

from flask_restplus import reqparse

class RuleController(Strategy):


    def set_edit_parser(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('character_classes', action='append')
        self.parser.add_argument('description')
        self.parser.add_argument('items', action='append')
        self.parser.add_argument('name', required=True)
        self.parser.add_argument('races', action='append')
        self.parser.add_argument('skills', action='append')

        return self.parser



