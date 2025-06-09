# Importa as bibliotecas necessárias
import pandas as pd
import matplotlib.pyplot as plt

# Define as URLs dos arquivos CSV de cada loja
url = "https://raw.githubusercontent.com/TyrGunllod/alura_store/refs/heads/main/dados_lojas/loja_1.csv"
url2 = "https://raw.githubusercontent.com/TyrGunllod/alura_store/refs/heads/main/dados_lojas/loja_2.csv"
url3 = "https://raw.githubusercontent.com/TyrGunllod/alura_store/refs/heads/main/dados_lojas/loja_3.csv"
url4 = "https://raw.githubusercontent.com/TyrGunllod/alura_store/refs/heads/main/dados_lojas/loja_4.csv"

# Carrega os arquivos CSV em uma lista de DataFrames
lojas = []
lojas.append(pd.read_csv(url))
lojas.append(pd.read_csv(url2))
lojas.append(pd.read_csv(url3))
lojas.append(pd.read_csv(url4))

# Função que calcula a média dos valores de uma coluna numérica
def media_por_coluna(arquivo, coluna):
    # Calcula a média da coluna e arredonda para 2 casas decimais
    media_valor = round(arquivo[coluna].mean(), 2)
    return media_valor


# ==============================================
# ANÁLISE DO FRETE MÉDIO POR LOJA
# ==============================================

# 1. Lista para armazenar o valor médio do frete de cada loja
frete_medio = []

# 2. Loop para calcular a média da coluna "Frete" em cada loja
for i in range(len(lojas)):
    # Usa a função definida anteriormente para calcular a média do frete
    frete_medio.append(media_por_coluna(lojas[i], 'Frete'))

# 3. Exibe o valor médio do frete para cada loja
for i, media in enumerate(frete_medio, start=1):
    print(f'Custo do frete médio da loja {i}: R${media:.2f}')

# Média geral entre todas as lojas
media_geral = round(sum(frete_medio) / len(frete_medio), 2)

# Nomes das lojas
nomes_lojas = [f'Loja {i}' for i in range(1, len(frete_medio) + 1)]

# Cores personalizadas para cada barra
cores = ['#3498db', '#e67e22', '#9b59b6', '#2ecc71']

# Criação do gráfico
fig, ax = plt.subplots(figsize=(8, 6))

barras = ax.bar(nomes_lojas, frete_medio, color=cores)

# Adiciona rótulos com os valores sobre cada barra
for bar, valor in zip(barras, frete_medio):
    altura = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, altura + 0.05, f'R$ {valor:.2f}',
            ha='center', va='bottom', fontsize=9)

# Linha da média geral
ax.axhline(media_geral, color='gray', linestyle='--', linewidth=1)
ax.text(len(lojas) - 0.35, media_geral, f'Média geral (R$ {media_geral:.2f})', va='center', ha='left', fontsize=9, color='gray', bbox=dict(facecolor='white', edgecolor='none'))
#ax.text(len(lojas) - 0.1 + 0.7, media_geral, f'Média Geral ({media_geral:.2f})', color='blue', fontsize=9, va='center')
# Títulos e rótulos
ax.set_title('Frete Médio por Loja', fontsize=14)
ax.set_ylabel('Valor Médio do Frete (R$)', fontsize=11)
ax.set_xlabel('Lojas', fontsize=11)

# Ajusta o layout para melhor visualização
plt.tight_layout()

# Exibe o gráfico
plt.show()