# ==============================================
# ANÁLISE DE FATURAMENTO DAS LOJAS
# ==============================================

# 1. Importa as bibliotecas necessárias
import pandas as pd
import matplotlib.pyplot as plt

# 2. Define as URLs dos arquivos CSV de cada loja
url = "https://raw.githubusercontent.com/TyrGunllod/alura_store/refs/heads/main/dados_lojas/loja_1.csv"
url2 = "https://raw.githubusercontent.com/TyrGunllod/alura_store/refs/heads/main/dados_lojas/loja_2.csv"
url3 = "https://raw.githubusercontent.com/TyrGunllod/alura_store/refs/heads/main/dados_lojas/loja_3.csv"
url4 = "https://raw.githubusercontent.com/TyrGunllod/alura_store/refs/heads/main/dados_lojas/loja_4.csv"

# 3. Carrega os arquivos CSV em uma lista de DataFrames
lojas = []
lojas.append(pd.read_csv(url))
lojas.append(pd.read_csv(url2))
lojas.append(pd.read_csv(url3))
lojas.append(pd.read_csv(url4))

# 4. Função que retorna a soma da coluna especificada
def soma_por_coluna(arquivo, coluna):
    soma = arquivo[coluna].sum()
    return soma

# 5. Lista que armazenará o faturamento individual de cada loja
faturamento_loja = []

# 6. Loop para calcular o faturamento (soma da coluna 'Preço') de cada loja
for i in range(len(lojas)):
    faturamento_loja.append(soma_por_coluna(lojas[i], 'Preço'))

# 7. Exibe o faturamento de cada loja individualmente
for i, valor in enumerate(faturamento_loja, start=1):
    print(f'Faturamento da loja {i}: R$ {valor:.2f}')

# 8. Calcula o faturamento total
faturamento_total = sum(faturamento_loja)
print(f'\nFaturamento total das lojas: R$ {faturamento_total:.2f}')

# 9. Geração do gráfico de faturamento por loja

# Lista com nomes das lojas para o eixo X
nomes_lojas = [f'Loja {i}' for i in range(1, len(lojas) + 1)]

# Cria a figura e os eixos do gráfico
fig, ax = plt.subplots(figsize=(8, 6))

# Cria as barras verticais
barras = ax.bar(nomes_lojas, faturamento_loja, color='skyblue')

# 10. Adiciona os valores de faturamento sobre cada barra
for bar, valor in zip(barras, faturamento_loja):
    altura = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, altura + 500,  # posição do texto
            f'R$ {valor:,.2f}', ha='center', va='bottom', fontsize=9)

# 11. Define título e rótulos
ax.set_title(f'Faturamento por Loja\nFaturamento Total: R$ {faturamento_total:,.2f}', fontsize=14)
ax.set_ylabel('Faturamento (R$)', fontsize=11)
ax.set_xlabel('Lojas', fontsize=11)

# 12. Melhora o layout
plt.tight_layout()

# 13. Exibe o gráfico
plt.show()
