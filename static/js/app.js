async function classificarTexto() {
    const texto = document.getElementById('inputTexto').value;
    try {
        const response = await fetch('/api/v1/classificador/classificar/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ texto })
        });
        if (!response.ok) {
            throw new Error('Erro ao buscar classificação');
        }
        const data = await response.json();
        document.getElementById('resultado').textContent = `Resultado: ${data.resultado}`;
        document.getElementById('dica').textContent = `Dica: ${data.dica}`;
    } catch (error) {
        document.getElementById('resultado').textContent = 'Erro: ' + error.message;
    }
}