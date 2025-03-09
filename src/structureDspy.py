from dspy import (
    ChainOfThought,
    Signature,
    OpenAI,
    settings,
    InputField,
    OutputField,
    Module,
    Retrieve,
    ColBERTv2,
    Suggest
)
from dotenv import load_dotenv
import os
from typing import Literal
import dspy
dspy.settings.cache_dir = None
load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_KEY', 'sem chave')
if os.environ['OPENAI_API_KEY'] == 'sem chave':
    exit('Sem chave da OPENAI, coloque uma chave no seu .env e tente novamente!')

# estrutur dspy
gpt4 = OpenAI(os.getenv('GPT_MODEL'), model_type='chat', max_tokens=6000)
#colbertv2_wiki17_abstracts = ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')
# config dspy
settings.configure(lm=gpt4,trace=[], cache=False, temperature=0.0)

class ClassificarNPSignature(Signature):
    """
    A saída deve ser apenas o resultado!

    Você é um professor de matemática e receberá o {texto_questao} de uma questão. Primeiramente idenfique se o texto é uma pergunta, se não for apenas diga que não é uma pergunta compativel, caso seja uma pergunta seu objetivo é identificar primeiro o tipo principal da distribuição de probabilidade entre:

    Distribuição Discreta (quando a variável assume valores contáveis, como número de sucessos em experimentos).
    Distribuição Contínua (quando a variável pode assumir qualquer valor em um intervalo, como alturas ou tempos).
    Depois, determine o tipo secundário, ou seja, a distribuição específica que melhor representa o problema. Escolha apenas um dos seguintes tipos de distribuições discretas:

    Distribuição de Bernoulli: Modela experimentos com apenas uma tentativa, onde há dois resultados possíveis (sucesso ou fracasso). Exemplo: lançar uma moeda uma vez.
    Distribuição Binomial: Modela o número de sucessos em várias tentativas independentes, onde cada tentativa segue uma distribuição de Bernoulli. Exemplo: jogar uma moeda 10 vezes e contar quantas vezes sai cara.
    Distribuição Geométrica: Modela o número de tentativas necessárias até o primeiro sucesso ocorrer. Exemplo: quantas vezes preciso lançar um dado até obter um 6?
    Distribuição de Pascal (ou Binomial Negativa): Modela o número de tentativas até que um número fixo de sucessos ocorra. Exemplo: quantas vezes preciso lançar um dado até obter três números 6?
    Distribuição de Poisson: Modela a quantidade de eventos que ocorrem em um intervalo fixo de tempo ou espaço, quando os eventos ocorrem de forma aleatória. Exemplo: número de chamadas recebidas por um call center por hora.
    Distribuição Hipergeométrica: Modela o número de sucessos em uma amostra retirada sem reposição de uma população finita. Exemplo: selecionar cartas de um baralho sem devolvê-las e contar quantas são ases.
    A identificação pode ser feita analisando:

    A natureza da variável aleatória

    Se assume valores contáveis → Discreta
    Se assume valores contínuos → Contínua
    O comportamento do problema

    Se há apenas uma tentativa → Bernoulli
    Se há várias tentativas com número fixo de sucessos → Binomial ou Pascal
    Se estamos contando tentativas até o primeiro sucesso → Geométrica
    Se estamos contando eventos que ocorrem ao longo do tempo ou espaço → Poisson
    Se estamos extraindo amostras sem reposição → Hipergeométrica
    Importante: A saída deve ser apenas o nome da distribuição que melhor se aplica ao problema, sem explicações adicionais.

    Exemplo de saída:

    Distribuição Binomial
    Distribuição de Poisson
    Distribuição Hipergeométrica
    Escolha somente um tipo e nada mais!

    E o rationale!

    """

    texto_questao : str = InputField(prefix='Texto da Questão:')
    #texto_auxiliar : str = InputField(prefix='Diferença entre os tipos de distribuições de probabilidade:')

    #distribuicao_principal : Literal['Distribuição Discreta', 'Distribuição Contínua'] = OutputField(prefix='Distribuição Principal:')
    distribuicao_principal : Literal['Distribuição Binomial', 'Distribuição Geométrica', 'Distribuição de Bernoulli',
                                 'Distribuição de Pascal', 'Distribuição de Poisson', 'Distribuição Hipergeométrica']  = OutputField(prefix='Destribuição Final:')

class ModuloClassificador(dspy.Module):
    def __init__(self):
        super().__init__()
        self.cot_module = dspy.ChainOfThought(ClassificarNPSignature, OutputField(prefix="Raciocínio: Vamos pensar passo a passo em ordem para resolver a questão"))
    
    def forward(self, texto_questao):
        pred = self.cot_module(texto_questao=texto_questao)
        
        print(pred)

        dspy.Suggest(
            pred.distribuicao_principal in ['Não é Distribuição','Distribuição Binomial', 'Distribuição Geométrica', 'Distribuição de Bernoulli',
                                 'Distribuição de Pascal', 'Distribuição de Poisson', 'Distribuição Hipergeométrica'],
            "{'distribuicao_principal'} deve ser um dos valores a seguir:[Distribuição Binomial, Distribuição Geométrica, Distribuição de Bernoulli, Distribuição de Pascal, Distribuição de Poisson, Distribuição Hipergeométrica, Não é Distribuição] e não pode ser maior que 50 caracteres!, nenhum dos campos não pode ser vazio.",
            target_module=self.cot_module
        )

        return pred

def formatedResult(pred):
    """returns : rationale, distribuição principal, dica"""
    return pred.rationale, pred.distribuicao_principal, None

#pred = test(texto_questao=q5)
#print(pred)