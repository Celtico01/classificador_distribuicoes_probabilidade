from dspy import (
    ChainOfThought,
    Signature
)
from dotenv import load_dotenv
import os


load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_KEY', 'sem chave')
if os.environ['OPENAI_API_KEY'] == 'sem chave':
    exit('Sem chave da OPENAI, coloque uma chave no seu .env e tente novamente!')

# estrutur dspy
