from structureDspy import (
    ModuloClassificador
)

# criar funcoes para chamar o dspy!
classificador = ModuloClassificador().activate_assertions()

def getResult(questao : str):
    return classificador(texto_questao=questao)

def formatedResult(questao : str):
    """returns : rationale, distribuição principal, dica"""
    pred = getResult(questao)

    return pred.rationale, pred.distribuicao_principal, pred.dica