# 1. Importa as bibliotecas necessárias
# Importa as bibliotecas necessárias
import pandas as pd
import matplotlib.pyplot as plt

# Lista com todas as URLs
urls = [
    "https://raw.githubusercontent.com/TyrGunllod/alura_store/refs/heads/main/dados_lojas/loja_1.csv",
    "https://raw.githubusercontent.com/TyrGunllod/alura_store/refs/heads/main/dados_lojas/loja_2.csv",
    "https://raw.githubusercontent.com/TyrGunllod/alura_store/refs/heads/main/dados_lojas/loja_3.csv",
    "https://raw.githubusercontent.com/TyrGunllod/alura_store/refs/heads/main/dados_lojas/loja_4.csv"
]

# Carrega todos os DataFrames usando list comprehension
lojas = [pd.read_csv(url) for url in urls]

def media_por_coluna(arquivo, coluna):
    media_valor = round(arquivo[coluna].mean(), 2)
    return media_valor

# ==============================================
# MÉDIA DE AVALIAÇÃO DAS LOJAS
# ==============================================

# Lista que armazenará a média de avaliação de cada loja
media_avaliacoes = []

# Loop para calcular a média das avaliações em cada loja
for i in range(len(lojas)):
    # Usa a função media_por_coluna para obter a média da coluna 'Avaliação da compra'
    media_avaliacoes.append(media_por_coluna(lojas[i], 'Avaliação da compra'))

# Loop para exibir a média de avaliação de cada loja formatada com 2 casas decimais
for i, media in enumerate(media_avaliacoes, start=1):
    print(f'Média das avaliações da loja {i}: {media:.2f}/5.0')

# Linha em branco para separar visualmente a saída
print()

# Lista com os nomes das lojas
nomes_lojas = [f'Loja {i}' for i in range(1, len(lojas) + 1)]

# Calcula a média geral
media_geral = sum(media_avaliacoes) / len(media_avaliacoes)

# Identifica maior e menor média
media_max = max(media_avaliacoes)
media_min = min(media_avaliacoes)

# Define cores com base na média
cores = [
    'green' if media == media_max else
    'red' if media == media_min else
    'gray'
    for media in media_avaliacoes
]

# Cria figura e eixos
fig, ax = plt.subplots(figsize=(9, 5))

# Gráfico de barras
barras = ax.bar(nomes_lojas, media_avaliacoes, color=cores)

# Adiciona os valores nas barras
for bar, media in zip(barras, media_avaliacoes):
    altura = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, altura + 0.05,
            f'{media:.2f}', ha='center', va='bottom', fontsize=9)

# Define limites do eixo X para abrir espaço à direita
ax.set_xlim(-0.5, len(lojas) - 0.5 + 1)  # adiciona +1 espaço à direita

# Linha da avaliação máxima
ax.axhline(y=5, color='black', linestyle='--', linewidth=1)
# Texto à direita da linha (fora do gráfico)
ax.text(len(lojas) - 0.1 + 0.7, 5, 'Avaliação Máxima (5.0)', color='black', fontsize=9, va='center')

# Linha da média geral
ax.axhline(y=media_geral, color='blue', linestyle='-', linewidth=1)
# Texto à direita da linha (fora do gráfico)
ax.text(len(lojas) - 0.1 + 0.7, media_geral, f'Média Geral ({media_geral:.2f})',
        color='blue', fontsize=9, va='center')

# Títulos e rótulos
ax.set_title('Média de Avaliação por Loja', fontsize=14)
ax.set_ylabel('Média de Avaliação', fontsize=11)
ax.set_xlabel('Lojas', fontsize=11)

# Limite do eixo Y
ax.set_ylim(0, 5.5)

# Melhorar o layout
plt.tight_layout()

# Exibe o gráfico
plt.show()