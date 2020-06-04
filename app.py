from flask import Flask, request, jsonify
import json

app = Flask(__name__)

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


@app.route('/tarefa/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def task(id):
    try:
        response = TAREFAS[id]
    except IndexError:
        return jsonify({'msg': 'Essa task %s não existe' % id})
    except Exception:
        return jsonify({'msg': 'Erro genérico'})

    if request.method == "GET":
        return jsonify(response)

    elif request.method == "PUT":
        dados = json.loads(request.data)
        response['status'] = dados['status']
        return jsonify({'msg': 'Alterado com sucesso'})

    elif request.method == 'DELETE':
        TAREFAS.pop(id)
        return jsonify({'msg': 'Excluído com sucesso'})


@app.route('/tarefa/', methods=['GET', 'POST'])
def list_tasks():
    if request.method == 'GET':
        return jsonify(TAREFAS)
    else:
        dados = json.loads(request.data)
        dados['id'] = len(TAREFAS)
        TAREFAS.append(dados)
        return jsonify({'msg': 'Incluído com sucesso'})


if __name__ == '__main__':
    app.run()
