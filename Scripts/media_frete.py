# Importa as bibliotecas necessárias
# Importa as bibliotecas necessárias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns
#import folium
#from folium.plugins import HeatMap

# Lista com todas as URLs
urls = [
    "https://raw.githubusercontent.com/TyrGunllod/alura_store/refs/heads/main/dados_lojas/loja_1.csv",
    "https://raw.githubusercontent.com/TyrGunllod/alura_store/refs/heads/main/dados_lojas/loja_2.csv",
    "https://raw.githubusercontent.com/TyrGunllod/alura_store/refs/heads/main/dados_lojas/loja_3.csv",
    "https://raw.githubusercontent.com/TyrGunllod/alura_store/refs/heads/main/dados_lojas/loja_4.csv"
]

# Carrega todos os DataFrames usando list comprehension
lojas = [pd.read_csv(url) for url in urls]

# Função que calcula a média dos valores de uma coluna numérica
def media_por_coluna(arquivo, coluna):
    # Calcula a média da coluna e arredonda para 2 casas decimais
    media_valor = round(arquivo[coluna].mean(), 2)
    return media_valor

# ==============================================
# ANÁLISE DO FRETE MÉDIO E PRODUTOS POR FAIXA DE FRETE
# ==============================================

# Parâmetros de faixa de frete
bins = [0, 10, 20, 30, 40, 50, float('inf')]
labels = ['0-10', '10-20', '20-30', '30-40', '40-50', '50+']

frete_medio = []
dados_comparativos = {}

# Processa todas as lojas
for i, loja in enumerate(lojas, start=1):
    # Filtra fretes maiores que zero
    dados_filtrados = loja[loja['Frete'] > 0].copy()

    # Calcula frete médio
    media_frete = media_por_coluna(dados_filtrados, 'Frete')
    frete_medio.append(media_frete)

    # Cria faixa de frete
    dados_filtrados['Faixa de Frete'] = pd.cut(dados_filtrados['Frete'], bins=bins, labels=labels, right=False)

    # Conta produtos por faixa
    produtos_por_faixa = dados_filtrados['Faixa de Frete'].value_counts().reindex(labels)

    # Armazena para gráfico comparativo
    dados_comparativos[f'Loja {i}'] = produtos_por_faixa

    # Mostra resumo no terminal
    print(f"\n📊 Loja {i} - Frete Médio: R${media_frete:.2f}")
    print(produtos_por_faixa)
    
# ==============================================
# CÁLCULOS DERIVADOS E GRÁFICOS
# ==============================================

# Cria DataFrame para comparação
df_comparativo = pd.DataFrame(dados_comparativos)

# Variação percentual em relação à média geral
media_geral = sum(frete_medio) / len(frete_medio)
variacoes = [(valor - media_geral) / media_geral * 100 for valor in frete_medio]

# Gráfico combinado
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# -------- Gráfico 1: Produtos por faixa --------
cores = ['#4CAF50', '#2196F3', '#FFC107', '#9C27B0'] # Verde, Azul, Amarelo, Roxo
largura_barra = 0.15
x = np.arange(len(labels))
offsets = np.linspace(-1.5 * largura_barra, 1.5 * largura_barra, len(lojas))

for i, (coluna, cor) in enumerate(zip(df_comparativo.columns, cores)):
    barras = ax1.bar(x + offsets[i], df_comparativo[coluna], width=largura_barra,
                     label=coluna, color=cor, edgecolor='black')

    # Adiciona rótulos
    for barra in barras:
        altura = barra.get_height()
        ax1.annotate(f'{int(altura)}',
                     xy=(barra.get_x() + barra.get_width() / 2, altura),
                     xytext=(0, 3),
                     textcoords='offset points',
                     ha='center', va='bottom', fontsize=9)

ax1.set_title('Produtos Vendidos por Faixa de Frete (por Loja)')
ax1.set_ylabel('Quantidade de Produtos')
ax1.set_xticks(x)
ax1.set_xticklabels(labels)
ax1.grid(axis='y', linestyle='--', alpha=0.7)
ax1.legend()

# -------- Gráfico 2: Frete médio e variação --------
x_lojas = np.arange(len(lojas))
ax2.plot(x_lojas, frete_medio, color='red', marker='o', linestyle='-', linewidth=2, label='Frete Médio')

for i, valor in enumerate(frete_medio):
    variacao = variacoes[i]
    texto = f'R${valor:.2f}\n({variacao:+.1f}%)' if abs(variacao) >= 0.05 else f'R${valor:.2f}\n(= média)'
    
    ax2.annotate(texto,
                 xy=(x_lojas[i], valor),
                 xytext=(0, 10),
                 textcoords='offset points',
                 ha='center', va='bottom',
                 fontsize=10, color='red')

ax2.set_title('Frete Médio por Loja (Variação em Relação à Média Geral)')
ax2.set_xlabel('Lojas')
ax2.set_ylabel('Frete Médio (R$)')
ax2.set_xticks(x_lojas)
ax2.set_xticklabels([f'Loja {i+1}' for i in range(len(lojas))])
ax2.set_ylim(30, 40)
ax2.grid(axis='y', linestyle='--', alpha=0.7)
ax2.axhline(media_geral, color='gray', linestyle='--', linewidth=1, label='Média Geral')
ax2.legend()

plt.tight_layout()
plt.show()