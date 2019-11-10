
from base.controller import Strategy

from flask_restplus import reqparse


class EventController(Strategy):

   def set_edit_parser(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', required=False)

        return self.parser



