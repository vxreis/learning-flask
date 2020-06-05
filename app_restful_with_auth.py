from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)
auth = HTTPBasicAuth()

users = {
    'vanessa': '123'
}


@auth.verify_password
def verify_login(user, password):
    if not (user, password):
        return False
    return users.get(user) == password


class Exemplo(Resource):

    @auth.login_required
    def get(self):
        return {'msg': 'Você está autorizado'}


api.add_resource(Exemplo, '/')


if __name__ == '__main__':
    app.run()
