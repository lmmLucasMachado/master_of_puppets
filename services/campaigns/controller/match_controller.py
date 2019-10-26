from flask_restplus import reqparse
from services.strategy import Strategy

class MatchController(Strategy):
    def set_parser(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', required=True)
        self.parser.add_argument('events', action='append')
        self.parser.add_argument('description')
        return self.parser