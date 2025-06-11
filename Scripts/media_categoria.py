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

# Função que soma os valores da coluna "Preço" agrupando por categoria
def soma_por_categoria(arquivo, coluna):
    return arquivo.groupby(coluna)["Preço"].sum().sort_values(ascending=False)

# ==============================================
# ANÁLISE DE FATURAMENTO POR CATEGORIA - POR LOJA
# ==============================================

# Lista com o faturamento por categoria para cada loja
vendas_categoria = [soma_por_categoria(loja, 'Categoria do Produto') for loja in lojas]

# Exibe o faturamento por categoria de cada loja
for i, categoria in enumerate(vendas_categoria, start=1):
    print(f'\nFaturamento por categoria - Loja {i}:\n')
    for nome_categoria, total in categoria.items():
        print(f' - {nome_categoria}: R$ {total:.2f}')
    print()

# Concatena os dados por categoria
df_categorias = pd.concat(vendas_categoria, axis=1)
df_categorias.columns = [f'Loja {i+1}' for i in range(len(lojas))]
df_categorias = df_categorias.fillna(0)

# Define cores diferentes por loja
cores = ['#4CAF50', '#2196F3', '#FFC107', '#9C27B0']  # Verde, Azul, Amarelo, Roxo

# Cria o gráfico de barras
fig, ax = plt.subplots(figsize=(10, 6))
df_categorias.plot(kind='bar', ax=ax, color=cores)

# Título e rótulos
ax.set_title('Faturamento por Categoria - Comparativo entre Lojas', fontsize=14)
ax.set_xlabel('Categoria do Produto', fontsize=11)
ax.set_ylabel('Faturamento (R$)', fontsize=11)
ax.legend(title='Lojas')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()
