from flask import Flask, render_template_string
import urllib.parse
import csv
import requests

app = Flask(__name__)

# Configurações do seu negócio
NUMERO_WHATSAPP = "5515991323719"  
NOME_LOJA = "Multi Eletronic"

# ID da sua planilha do Google
PLANILHA_ID = "1-c0DcrOkeJfV3v9hTf5Nv6QUk9fnWuc9esmeguvkenqs"
LINK_EXPORTACAO_CSV = f"https://google.com{PLANILHA_ID}/export?format=csv"

def buscar_produtos_da_planilha():
    produtos = []
    try:
        resposta = requests.get(LINK_EXPORTACAO_CSV)
        resposta.encoding = 'utf-8'
        linhas = csv.DictReader(resposta.text.splitlines())
        for linha in linhas:
            produtos.append({
                "id": linha.get("id"),
                "nome": linha.get("nome", "Produto"),
                "preco": linha.get("preco", "R$ 0,00"),
                "imagem": linha.get("imagem", ""),
                "descricao": linha.get("descricao", "Sem descrição disponível.")
            })
    except Exception as e:
        print(f"Erro ao ler planilha: {e}")
        # Dados de segurança caso a planilha falhe temporariamente
        produtos = [
            {
                "id": "1", "nome": "🔊 Caixa de Som Bluetooth", "preco": "R$ 79,90", 
                "imagem": "https://postimg.cc",
                "descricao": "Som potente com graves reforçados, alta fidelidade e bateria de longa duração."
            },
            {
                "id": "2", "nome": "⌨️ Teclado Gamer Retroiluminado", "preco": "R$ 119,90", 
                "imagem": "https://postimg.cc",
                "descricao": "Teclas macias com resposta rápida e iluminação LED RGB perfeita para jogar à noite."
            }
        ]
    return produtos

# Design Front-end Estruturado com Carrinho, Abas e Visual Verde/Azul Claro
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ nome_loja }}</title>
    <style>
        :root {
            --primary: #25D366; /* Verde */
            --secondary: #00b4d8; /* Azul Claro */
            --dark: #111a24; /* Fundo Escuro Moderno */
            --light: #f8f9fa;
        }
        body { font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 0; background: var(--light); color: #333; }
        
        /* Faixa de Benefícios no Topo */
        .top-bar { background: var(--secondary); color: white; padding: 8px; font-size: 13px; font-weight: bold; text-transform: uppercase; letter-spacing: 1px; text-align: center; }
        
        /* Cabeçalho */
        header { background: var(--dark); color: white; padding: 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 4px solid var(--primary); padding-left: 10%; padding-right: 10%; }
        .logo { font-size: 26px; font-weight: bold; color: white; }
        .logo span { color: var(--primary); }
        .cart-icon { position: relative; font-size: 24px; cursor: pointer; background: none; border: none; color: white; }
        .cart-count { position: absolute; top: -8px; right: -10px; background: var(--secondary); color: white; border-radius: 50%; width: 20px; height: 20px; font-size: 12px; display: flex; align-items: center; justify-content: center; font-weight: bold; }
        
        h1 { color: var(--dark); margin-top: 40px; font-size: 28px; text-align: center; }
        
        /* Container de Produtos */
        .container { display: flex; justify-content: center; flex-wrap: wrap; padding: 20px; gap: 30px; }
        .card { background: white; border-radius: 16px; box-shadow: 0 10px 20px rgba(0,0,0,0.08); width: 320px; padding: 20px; text-align: left; transition: 0.3s; display: flex; flex-direction: column; }
        .card:hover { transform: translateY(-8px); box-shadow: 0 15px 30px rgba(0,0,0,0.12); }
        .card img { width: 100%; border-radius: 10px; height: 220px; object-fit: cover; background: #fafafa; }
        .card h3 { margin: 15px 0 10px 0; color: var(--dark); font-size: 20px; }
        .price { color: var(--primary); font-size: 26px; font-weight: bold; margin: 10px 0; }
        
        /* Abas de Informações (Tabs) */
        .tabs { display: flex; border-bottom: 2px solid #eee; margin-bottom: 15px; margin-top: 10px; }
        .tab-btn { background: none; border: none; padding: 8px 12px; cursor: pointer; font-size: 13px; font-weight: bold; color: #777; transition: 0.2s; }
        .tab-btn.active { color: var(--secondary); border-bottom: 2px solid var(--secondary); }
        .tab-content { font-size: 14px; color: #555; line-height: 1.5; min-height: 60px; display: none; }
        .tab-content.active { display: block; }
        
        /* Botões */
        .btn-add { display: block; background: var(--primary); color: white; text-align: center; padding: 14px; border: none; border-radius: 8px; font-weight: bold; font-size: 16px; cursor: pointer; width: 100%; transition: 0.2s; }
        .btn-add:hover { background: #1eb959; transform: scale(1.02); }
        
        /* Janela Modal do Carrinho Lateral */
        .cart-modal { position: fixed; top: 0; right: -400px; width: 350px; height: 100%; background: white; box-shadow: -5px 0 15px rgba(0,0,0,0.1); transition: 0.3s; z-index: 1000; padding: 25px; display: flex; flex-direction: column; text-align: left; }
        .cart-modal.open { right: 0; }
        .cart-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 2px solid #eee; padding-bottom: 15px; }
        .close-cart { background: none; border: none; font-size: 24px; cursor: pointer; color: #777; }
        .cart-items { flex: 1; overflow-y: auto; margin-top: 20px; }
        .cart-item { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; border-bottom: 1px solid #f1f1f1; padding-bottom: 10px; }
        .cart-item-info h4 { margin: 0; font-size: 15px; }
        .cart-item-info p { margin: 5px 0 0 0; color: var(--primary); font-weight: bold; }
        .btn-remove { background: none; border: none; color: #ff4d4d; cursor: pointer; font-size: 13px; }
        .cart-total { font-size: 20px; font-weight: bold; border-top: 2px solid #eee; padding-top: 15px; display: flex; justify-content: space-between; margin-bottom: 20px; }
        .btn-checkout { background: var(--secondary); color: white; text-align: center; padding: 14px; border: none; border-radius: 8px; font-weight: bold; font-size: 16px; width: 100%; cursor: pointer; display: block; text-decoration: none; }
        .btn-checkout:hover { background: #0096c7; }
    </style>
</head>
<body>

    <!-- Faixa de Frete Grátis -->
    <div class="top-bar">🚚 Frete Grátis para todo o Brasil em compras acima de R$ 99!</div>

    <!-- Cabeçalho com Sacola de Compras -->
    <header>
        <div class="logo">Multi <span>Eletronic</span></div>
        <button class="cart-icon" onclick="toggleCart()">
            🛍️ <div class="cart-count" id="cart-count">0</div>
        </button>
    </header>

    <h1>Nossos Produtos Eletrônicos</h1>

    <!-- Grade de Produtos -->
    <div class="container">
        {% for p in produtos %}
        <div class="card">
            {% if p.imagem %}
            <img src="{{ p.imagem }}" alt="{{ p.nome }}">
            {% endif %}
            <h3>{{ p.nome }}</h3>
            
            <!-- Abas (Tabs) de Informações -->
            <div class="tabs">
                <button class="tab-btn active" onclick="switchTab(event, 'desc-{{ p.id }}')">Descrição</button>
                <button class="tab-btn" onclick="switchTab(event, 'envio-{{ p.id }}')">Envio e Garantia</button>
            </div>
            
            <!-- Conteúdo das Abas -->
            <div id="desc-{{ p.id }}" class="tab-content active">{{ p.descricao }}</div>
            <div id="envio-{{ p.id }}" class="tab-content">📦 Envio direto do fornecedor com código de rastreamento pelos Correios. Garantia de 30 dias contra defeitos de fábrica.</div>
            
            <div class="price">{{ p.preco }}</div>
            <button class="btn-add" onclick="addToCart('{{ p.id }}', '{{ p.nome }}', '{{ p.preco }}')">Adicionar ao Carrinho</button>
        </div>
        {% endfor %}
    </div>

    <!-- Janela Lateral da Sacola de Compras -->
    <div class="cart-modal" id="cart-modal">
        <div class="cart-header">
            <h3>Minha Sacola</h3>
            <button class="close-cart" onclick="toggleCart()">✕</button>
        </div>
        <div class="cart-items" id="cart-items">
            <!-- Os itens adicionados entram aqui via JavaScript -->
        </div>
        <div class="cart-total">
            <span>Total:</span>
            <span id="cart-total-val">R$ 0,00</span>
        </div>
        <button class="btn-checkout" onclick="checkoutWhatsApp()">Finalizar Compra</button>
    </div>

    <!-- Motor JavaScript do Carrinho -->
    <script>
        let carrinho = [];

        function switchTab(event, tabId) {
            let card = event.target.closest('.card');
            card.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
            card.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
            
            event.target.classList.add('active');
            card.querySelector('#' + tabId).classList.add('active');
        }

        function toggleCart() {
            document.getElementById('cart-modal').classList.toggle('open');
        }

        function addToCart(id, nome, preco) {
            carrinho.push({ id, nome, preco });
            atualizarInterfaceCarrinho();
            document.getElementById('cart-modal').classList.add('open');
        }

        function removeFromCart(index) {
            carrinho.splice(index, 1);
            atualizarInterfaceCarrinho();
        }

