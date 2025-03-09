# Classificador de Distribuições de Probabilidade

Este projeto utiliza uma **LLM (Large Language Model)** para classificar questões sobre distribuições de probabilidade e fornecer explicações sobre os resultados obtidos.

## **Requisitos**

- **Python 3.13.0** (versão recomendada)
- **Dependências listadas no `requirements.txt`**

## **Configuração do ambiente**

### **1. Criar e ativar um ambiente virtual**

Antes de instalar as dependências, é recomendável criar um ambiente virtual para isolar o projeto. Para isso, siga os passos abaixo:

#### **No Windows (CMD/Powershell):**
```sh
python -m venv venv
venv\Scripts\activate
```

#### **No macOS/Linux (Terminal):**
```sh
python -m venv venv
source venv/bin/activate
```

### **2. Instalar dependências**

Com o ambiente virtual ativado, instale as bibliotecas necessárias com o seguinte comando:
```sh
pip install -r requirements.txt
```

### **3. Configuração do arquivo `.env`**

O projeto requer algumas variáveis de ambiente para funcionar corretamente. No diretório raiz, renomeie o arquivo `.env-example` para `.env` e edite seu conteúdo:
```sh
OPENAI_KEY="sua-chave-aqui"
GPT_MODEL="modelo-aqui"
```

- **OPENAI_KEY**: Insira sua chave de API da OpenAI.
- **GPT_MODEL**: Defina o modelo de linguagem que será utilizado (ex: `gpt-4`, `gpt-3.5-turbo`).

## **Execução do projeto**

Para iniciar o aplicativo, execute o seguinte comando:
```sh
python app.py
```

Se o servidor for iniciado corretamente, você verá uma mensagem indicando a URL onde o aplicativo está rodando, geralmente:
```sh
Running on http://127.0.0.1:8080/
```

Abra essa URL no seu navegador para acessar a aplicação.

---

