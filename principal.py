from flask import Flask, render_template
import urllib.parse
import csv
import requests

app = Flask(__name__)

NUMERO_WHATSAPP = "5515991323719"  
NOME_LOJA = "Multi Eletronic"
PLANILHA_ID = "1-c0DcrOkEJf3v9hTfSNv6QUk9fnWuc9esmeguvkenqs"
LINK_EXPORTACAO_CSV = f"https://google.com{PLANILHA_ID}/export?format=csv"

def buscar_produtos():
    produtos = []
    try:
        resposta = requests.get(LINK_EXPORTACAO_CSV)
        resposta.encoding = 'utf-8'
        linhas = csv.DictReader(resposta.text.splitlines())
        for linha in list(linhas):
            produtos.append({
                "id": linha.get("id"),
                "nome": linha.get("nome", "Produto"),
                "preco": linha.get("preco", "R$ 0,00"),
                "imagem": linha.get("imagem", ""),
                "descricao": linha.get("descricao", "")
            })
    except Exception as e:
        print(f"Erro: {e}")
    return produtos

@app.route('/')
def home():
    lista = buscar_produtos()
    mensagens = {}
    for p in lista:
        texto = f"Olá! Vi no site da {NOME_LOJA} e quero comprar: {p['nome']} no valor de {p['preco']}."
        mensagens[p['id']] = urllib.parse.quote(texto)
    return render_template('index.html', produtos=lista, nome_loja=NOME_LOJA, numero_whatsapp=NUMERO_WHATSAPP, mensagens=mensagens)

if __name__ == '__main__':
    app.run(debug=True)
