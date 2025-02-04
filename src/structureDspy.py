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

load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_KEY', 'sem chave')
if os.environ['OPENAI_API_KEY'] == 'sem chave':
    exit('Sem chave da OPENAI, coloque uma chave no seu .env e tente novamente!')

# estrutur dspy
gpt4 = OpenAI(os.getenv('GPT_MODEL'), model_type='chat', max_tokens=4000)
#colbertv2_wiki17_abstracts = ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')
# config dspy
settings.configure(lm=gpt4,trace=[], cache=False, temperature=0.0)

class ClassificarNPSignature(Signature):
    """
    A saida deve ser apenas o resultado!
    Você é um professor de matemática e vai receber o {texto_questao} de uma questão 
    e você precisa identificar qual o tipo principal da distribuição de probabilidade
    ['Distribuição Discreta', 'Distribuição Contínua'] e 
    depois identificar o tipo secundário ou seja o tipo que vai ser usado para resolver a questão!
    como identificar a distribuição de probabilidade de uma questão.
    Identificar a distribuição de probabilidade de um problema envolve analisar os dados ou as características da variável aleatória envolvida. Aqui estão algumas abordagens para determinar a distribuição correta:

    1. Entender a Natureza da Variável Aleatória
    Variável Discreta: Assume valores contáveis (exemplo: número de chamadas recebidas por um call center).
    Variável Contínua: Assume valores dentro de um intervalo contínuo (exemplo: altura de pessoas).
    2. Analisar o Comportamento dos Dados
    Distribuição Uniforme: Todos os resultados têm a mesma probabilidade.
    Distribuição Normal: Dados seguem um formato de sino (bell curve).
    Distribuição Exponencial: Modela o tempo entre eventos em processos de Poisson.
    Distribuição de Poisson: Modela o número de eventos em um intervalo fixo de tempo.
    Distribuição Binomial: Modela o número de sucessos em tentativas independentes.
    3. Métodos Estatísticos para Identificação
    Histograma: Visualizar a forma dos dados e compará-los com distribuições conhecidas.
    Testes de Ajuste (Goodness-of-Fit Tests):
    Teste de Kolmogorov-Smirnov (para distribuições contínuas).
    Teste de Qui-quadrado (para distribuições discretas).
    Teste de Shapiro-Wilk (para normalidade).
    Estimação de Parâmetros:
    Média e variância podem indicar distribuição (por exemplo, Poisson tem média = variância).
    Método dos Momentos ou Máxima Verossimilhança:
    Ajustam distribuições conhecidas aos dados.
    {{ Escolha apenas um tipo e mais nada!}}
    [Distribuição de Bernoulli, Distribuição Geométrica,
    Distribuição de Pascal, '']
    Depois ajude o estudante dando uma dica de como resolver a questão!
    
    Importante: {A saida deve ser apenas um dos tipo de distribuições!}
    """

    
    

    texto_questao : str = InputField(prefix='Texto da Questão:')
    #texto_auxiliar : str = InputField(prefix='Diferença entre os tipos de distribuições de probabilidade:')

    #distribuicao_principal : Literal['Distribuição Discreta', 'Distribuição Contínua'] = OutputField(prefix='Distribuição Principal:')
    distribuicao_principal : Literal['Distribuição binomial', 'Distribuição geométrica', 'Distribuição de Bernoulli', 'Distribuição de Boltzmann',
                                 'Distribuição normal', 'Distribuição exponencial', 'Distribuição uniforme', 'Distribuição gama']  = OutputField(prefix='Destribuição Final:')

    dica : str = OutputField(prefix='Dica:')
import dspy

class ModuloClassificador(dspy.Module):
    def __init__(self):
        super().__init__()
        self.cot_module = dspy.ChainOfThought(ClassificarNPSignature, OutputField(prefix="Raciocínio: Vamos pensar passo a passo em ordem para resolver a questão"))
    
    def forward(self, texto_questao):
        pred = self.cot_module(texto_questao=texto_questao)
        print(pred)

        dspy.Suggest(
            pred.distribuicao_principal in ['Distribuição de Pascal', 'Distribuição geométrica'],
            "{'distribuicao_principal'} deve ser um dos valores a seguir:['Distribuição de Pascal', 'Distribuição geométrica', 'Distribuição de Bernoulli'] e não pode ser maior que 31 caracteres!",
            target_module=self.cot_module
        )

        return pred

#pred = test(texto_questao=q5)
#print(pred)