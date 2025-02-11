from flask import render_template, jsonify, request
from app import app
from src.structureDspy import ModuloClassificador, formatedResult

dspy_instance = ModuloClassificador().activate_assertions()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/v1/classificador/classificar/', methods=['POST'])
def classificar():
    data = request.get_json()
    texto_questao = data.get("texto")
    pred = dspy_instance(texto_questao=texto_questao)
    rationale, resultado, dica = formatedResult(pred)

    return jsonify({
        "resultado": resultado,
        "rationale": rationale,
        "dica": dica
    })
