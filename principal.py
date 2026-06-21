from flask import Flask, render_template_string
import urllib.parse
import csv
import requests

app = Flask(__name__)

# Configurações do seu negócio
NUMERO_WHATSAPP = "5515991323719"  
NOME_LOJA = "Multi Eletronic"

# ID da sua planilha do Google corrigido
PLANILHA_ID = "1-cb0erDkklfH9ihtf5Nv6SjUk9mwkUc9esmeguvkenqs"
LINK_EXPORTACAO_CSV = f"https://google.com{PLANILHA_ID}/export?format=csv"

def buscar_produtos_da_planilha():
    produtos = []
    try:
        # Baixa os dados atualizados da sua planilha em formato de texto (CSV)
        resposta = requests.get(LINK_EXPORTACAO_CSV)
        resposta.encoding = 'utf-8'
        
        # Lê linha por linha da tabela
        linhas = csv.DictReader(resposta.text.splitlines())
        for linha in linhas:
            # Organiza os dados para o site entender, usando os nomes exatos das colunas
            produtos.append({
                "id": linha.get("id"),
                "nome": linha.get("nome"),
                "preco": linha.get("preco"),
                "imagem": linha.get("imagem"),
                "descricao": linha.get("descricao")
            })
    except Exception as e:
        print(f"Erro ao ler planilha: {e}")
        # Caso a planilha falhe, exibe um produto de segurança
        produtos = [{
            "id": "1", "nome": "Erro ao carregar", "preco": "R$ 0,00", "imagem": "", 
            "descricao": "Verifique o compartilhamento da planilha."
        }]
    return produtos

# Modelo visual ajustado para carregar as fotos e dados da planilha
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ nome_loja }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f4f4f4; text-align: center; }
        header { background: #1a1a1a; color: #25D366; padding: 25px; font-size: 28px; font-weight: bold; border-bottom: 4px solid #25D366; }
        h1 { color: #333; margin-top: 30px; }
        .container { display: flex; justify-content: center; flex-wrap: wrap; padding: 20px; gap: 25px; }
        .card { background: white; border-radius: 12px; box-shadow: 0 6px 12px rgba(0,0,0,0.15); width: 300px; padding: 20px; text-align: left; transition: 0.3s; }
        .card:hover { transform: translateY(-5px); }
        .card img { width: 100%; border-radius: 8px; height: 220px; object-fit: cover; background: #fafafa; }
        .card h3 { margin: 15px 0 10px 0; color: #222; font-size: 20px; }
        .card p { color: #666; font-size: 14px; height: 40px; margin-bottom: 15px; line-height: 1.4; }
        .price { color: #25D366; font-size: 24px; font-weight: bold; margin: 15px 0; }
        .btn-buy { display: block; background: #25D366; color: white; text-align: center; padding: 12px; text-decoration: none; border-radius: 6px; font-weight: bold; font-size: 16px; }
        .btn-buy:hover { background: #128C7E; }
    </style>
</head>
<body>
    <header>{{ nome_loja }}</header>
    <h1>Nossos Produtos</h1>
    <div class="container">
        {% for p in produtos %}
        <div class="card">
            {% if p.imagem %}
            <img src="{{ p.imagem }}" alt="{{ p.nome }}">
            {% endif %}
            <h3>{{ p.nome }}</h3>
            <p>{{ p.descricao }}</p>
            <div class="price">{{ p.preco }}</div>
            <a href="https://wa.me{{ numero_whatsapp }}?text={{ mensagens[p.id] }}" target="_blank" class="btn-buy">Comprar pelo WhatsApp</a>
        </div>
        {% endfor %}
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    # Busca a lista atualizada direto da sua planilha
    lista_produtos = buscar_produtos_da_planilha()
    
    mensagens = {}
    for p in lista_produtos:
        texto = f"Olá! Vi no site da {NOME_LOJA} e quero comprar o produto: {p['nome']} no valor de {p['preco']}."
        mensagens[p['id']] = urllib.parse.quote(texto)
        
    return render_template_string(HTML_TEMPLATE, produtos=lista_produtos, nome_loja=NOME_LOJA, numero_whatsapp=NUMERO_WHATSAPP, mensagens=mensagens)

if __name__ == '__main__':
    app.run(debug=True)
