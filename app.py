
from flask import Flask
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flask import Flask, jsonify, render_template, send_from_directory
from marshmallow import Schema, fields

app = Flask(__name__, template_folder='swagger/templates')


@app.route('/')
def hello_world():
    return "Hello, world!"


spec = APISpec(
    title='flask-api-swagger-doc',
    version='1.0.0',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(), MarshmallowPlugin()]
)

@app.route('/api/swagger.json')
def create_swagger_spec():
    return jsonify(spec.to_dict())

class TodoresponseSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    status = fields.Boolean()


class TodoListresponseSchema(Schema):
    todo_list = fields.List(fields.Nested(TodoresponseSchema))


@app.route('/todo')
def todo():
    """Get list of Todo
        ---
        get:
            description: Getlist of Todos
            responses:
                200:
                    description: Return a Todo list
                    content:
                        application/json:
                            schema: TodoListresponseSchema

    """
    dummy_data = [{
        'id': 1,
        'title': 'Finish this task',
        'status': False
    },{
        'id': 2,
        'title': 'Finish that task',
        'status': True
    }]

    return TodoListresponseSchema().dump({'todo_list': dummy_data})

with app.test_request_context():
    spec.path(view=todo)


@app.route('/docs')
@app.route('/docs/<path:path>')
def swagger_docs(path=None):
    if not path or path == 'index.html':
        return render_template('index.html', base_url='/docs')
    else:
        return send_from_directory('./swagger/static', path)



if __name__ == "__main__":
    app.run(debug=True)