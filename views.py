from flask import render_template, jsonify, request
from app import app
from src.functions import getResult, formatedResult

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/v1/classificador/classificar/')
def classificar():
    data = request.get_json()
    texto_questao = data.get("texto")

    rationale, resultado, dica = formatedResult(texto_questao)

    return jsonify({
        "resultado": resultado,
        "rationale": rationale,
        "dica": dica
    })

# pascal
'''Qual a probabilidade de que no 25º lançamento de um 
    dado ocorra a face 4 pela 5º vez?'''

# bernoulli
'''Tendo uma questão objetiva de 5 opcões, 
    qual seria a probabilidade de eu acertar e a de eu errar a questão chutando?'''

# geometrica
'''No Callcenter de uma empresa distribuidora de telefonia,
    apenas 35% das chamadas são relacionadas a reclamações sobre erros nas faturas emitidas
    pela empresa. Qual a probabilidade da primeira reclamação sobre erro na fatura emitida da conta,
    ocorrer até a 2º chamada?'''