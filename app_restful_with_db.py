from flask import Flask, request
from flask_restful import Api, Resource

from models import People, Tasks

app = Flask(__name__)
api = Api(app)


class ManipulatePeople(Resource):

    @staticmethod
    def get_person(nome):
        try:
            person = People.query.filter_by(nome=nome).first()
            if person:
                return True, person
            else:
                return False, {'msg': 'Essa pessoa (%s) não existe' % nome}
        except Exception:
            return False, {'msg': 'Erro genérico'}

    def get(self, nome):
        exist, person = ManipulatePeople.get_person(nome)
        if exist:
            response = {
                'id': person.id,
                'nome': person.nome,
            }
            return response
        else:
            return person

    def put(self, nome):
        exist, person = ManipulatePeople.get_person(nome)
        if exist:
            dados = request.json
            if 'nome' in dados:
                person.nome = dados['nome']
                person.save()
                return {'msg': 'Alterado com sucesso'}
            return {'msg': 'Formato inválido'}
        else:
            return person

    def delete(self, nome):
        exist, person = ManipulatePeople.get_person(nome)
        if exist:
            person.delete()
            return {'msg': 'Excluído com sucesso'}
        else:
            return person


class ListPeople(Resource):

    def get(self):
        people = People.query.all()
        return [{'id': p.id, 'nome': p.nome} for p in people]

    def post(self):
        dados = request.json
        if 'nome' in dados:
            person = People(nome=dados['nome'])
            person.save()
            return {'msg': 'Cadastrado com sucesso'}
        else:
            return {'msg': 'Dado inválido'}


class ListTask(Resource):

    def get(self):
        tasks = Tasks.query.all()
        return [{'id': t.id, 'desc': t.desc, 'status': t.status, 'pessoa': t.pessoa.nome} for t in tasks]

    def post(self):
        dados = request.json
        try:
            exist_person, person = ManipulatePeople.get_person(dados['pessoa'])
        except KeyError:
            return {'msg': 'Chave inválida'}

        if exist_person:
            if 'desc' in dados:
                task = Tasks(desc=dados['desc'], status='pendente', pessoa=person)
                task.save()
                return {'msg': 'Cadastrado com sucesso'}
            else:
                return {'msg': 'Dado inválido'}
        else:
            return person


class ListTaskByPerson(Resource):

    def get(self, nome):
        exist_person, person = ManipulatePeople.get_person(nome)
        if exist_person:
            tasks = Tasks.query.filter_by(pessoa=person).all()
            return [{'id': t.id, 'desc': t.desc, 'status': t.status, 'pessoa': t.pessoa.nome} for t in tasks]
        else:
            return person


class ManipulateTask(Resource):

    @staticmethod
    def get_task(id):
        try:
            person = Tasks.query.filter_by(id=id).first()
            if person:
                return True, person
            else:
                return False, {'msg': 'Essa tarefa (%s) não existe' % id}
        except Exception:
            return False, {'msg': 'Erro genérico'}

    def get(self, id):
        exist, task = ManipulateTask.get_task(id)
        if exist:
            response = {
                'id': task.id,
                'pessoa': task.pessoa.nome,
                'desc': task.desc,
                'status': task.status
            }
            return response
        return task

    def put(self, id):
        exist, task = ManipulateTask.get_task(id)
        if exist:
            dados = request.json
            if 'status' in dados:
                task.status = dados['status']
                task.save()
                return {'msg': 'Alterado com sucesso'}
        else:
            return task

    def delete(self, id):
        exist, task = ManipulateTask.get_task(id)
        if exist:
            task.delete()
            return {'msg': 'Excluído com sucesso'}
        else:
            return task


api.add_resource(ManipulatePeople, '/pessoa/<string:nome>/')
api.add_resource(ListPeople, '/pessoa/')
api.add_resource(ManipulateTask, '/tarefa/<int:id>/')
api.add_resource(ListTask, '/tarefa/')
api.add_resource(ListTaskByPerson, '/tarefa/<string:nome>/')


if __name__ == '__main__':
    app.run()
