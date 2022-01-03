import os
import pathlib

import peewee
from flask import Flask, render_template
from flask_restful import Api, Resource, fields, marshal_with

from .models import Task

app = Flask(__name__, template_folder=f'{pathlib.Path(__file__).parent.resolve()}/templates')
api = Api(app)


class TaskItem(Resource):
    tag_fields = {
        'title': fields.String,
        'uuid': fields.String,
    }
    task_fields = {
        'uuid': fields.String,
        'title': fields.String,
        'modified': fields.DateTime(),
        'tags': fields.List(fields.Nested(tag_fields))
    }

    @marshal_with(task_fields)
    def get(self, _id=""):
        if not _id:
            return [*Task.select()]
        try:
            return Task.get_by_id(_id)
        except peewee.DoesNotExist:
            return {}


@app.route('/')
def index():
    print(os.listdir(os.curdir))
    return render_template('index.html')


api.add_resource(TaskItem, '/tasks', '/tasks/<string:_id>')

if __name__ == '__main__':
    app.run(debug=False, port=5)
