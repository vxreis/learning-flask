import json

from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

TAREFAS = [
    {
        "id": 0,
        "nome": "Vanessa",
        "tarefa": "Criar método GET",
        "status": "concluído"
    },
    {
        "id": 1,
        "nome": "Vanessa",
        "tarefa": "Criar método PUT",
        "status": "pendente"
    }
]


class Task(Resource):

    @staticmethod
    def get_task(id):
        try:
            return TAREFAS[id]
        except IndexError:
            return {'msg': 'Essa task %s não existe' % id}
        except Exception:
            return {'msg': 'Erro genérico'}

    def get(self, id):
        return Task.get_task(id)

    def put(self, id):
        dados = json.loads(request.data)
        task = Task.get_task(id)
        if 'msg' in task:
            return task
        task['status'] = dados['status']
        return {'msg': 'Alterado com sucesso'}

    def delete(self, id):
        task = Task.get_task(id)
        if 'msg' in task:
            return task
        TAREFAS.pop(id)
        return {'msg': 'Excluído com sucesso'}


class ListTask(Resource):
    def get(self):
        return TAREFAS

    def post(self):
        dados = json.loads(request.data)
        dados['id'] = len(TAREFAS)
        TAREFAS.append(dados)
        return {'msg': 'Incluído com sucesso'}


api.add_resource(Task, '/tarefa/<int:id>/')
api.add_resource(ListTask, '/tarefa/')


if __name__ == '__main__':
    app.run()
