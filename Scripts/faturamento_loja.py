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

# Função para somar uma coluna
def soma_por_coluna(arquivo, coluna):
    return arquivo[coluna].sum()

# ==============================================
# ANÁLISE DE FATURAMENTO DAS LOJAS
# ==============================================

# Calcula o faturamento por loja
faturamento_loja = [soma_por_coluna(loja, 'Preço') for loja in lojas]

# Exibe o faturamento por loja
for i, valor in enumerate(faturamento_loja, start=1):
    print(f'Faturamento da loja {i}: R$ {valor:.2f}')

# Faturamento total
faturamento_total = sum(faturamento_loja)
print(f'\nFaturamento total das lojas: R$ {faturamento_total:.2f}')

# Nomes das lojas
nomes_lojas = [f'Loja {i}' for i in range(1, len(lojas) + 1)]

# === Gráfico de faturamento por loja ===

# Define uma cor única para cada loja
cores = ['#4CAF50', '#2196F3', '#FFC107', '#9C27B0']  # Verde, Azul, Amarelo, Roxo

fig, ax = plt.subplots(figsize=(8, 6))

# Cria o gráfico de barras com cores diferentes
barras = ax.bar(nomes_lojas, faturamento_loja, color=cores)

# Adiciona os valores sobre cada barra
for bar, valor in zip(barras, faturamento_loja):
    altura = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, altura + 500,
            f'R$ {valor:,.2f}', ha='center', va='bottom', fontsize=9)

# Título e rótulos
ax.set_title(f'Faturamento por Loja\nFaturamento Total: R$ {faturamento_total:,.2f}', fontsize=14)
ax.set_ylabel('Faturamento (R$)', fontsize=11)
ax.set_xlabel('Lojas', fontsize=11)

# Layout final
plt.tight_layout()
plt.show()
