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

# Função que conta produtos por categoria
def contar_por_categoria(arquivo, coluna):
    return arquivo[coluna].value_counts()

# ==============================================
# ANÁLISE DE FATURAMENTO POR CATEGORIA - POR LOJA
# ==============================================

# Lista com o faturamento por categoria para cada loja
vendas_categoria = [soma_por_categoria(loja, 'Categoria do Produto') for loja in lojas]

# Lista com a contagem de produtos por categoria para cada loja
quantidade_categoria = [contar_por_categoria(loja, 'Categoria do Produto') for loja in lojas]

# Concatena os dados por categoria
df_categorias = pd.concat(vendas_categoria, axis=1).fillna(0)
df_categorias.columns = [f'Loja {i+1}' for i in range(len(lojas))]

df_quantidade = pd.concat(quantidade_categoria, axis=1).fillna(0).astype(int)
df_quantidade.columns = [f'Loja {i+1}' for i in range(len(lojas))]

# Define cores diferentes por loja
cores = ['#4CAF50', '#2196F3', '#FFC107', '#9C27B0']  # Verde, Azul, Amarelo, Roxo

# Cria o gráfico de barras
fig, ax = plt.subplots(figsize=(12, 6))
bar_container = df_categorias.plot(kind='bar', ax=ax, color=cores)

# Título e rótulos
ax.set_title('Faturamento por Categoria - Comparativo entre Lojas', fontsize=14)
ax.set_xlabel('Categoria do Produto', fontsize=11)
ax.set_ylabel('Faturamento (R$)', fontsize=11)
ax.legend(title='Lojas')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

# Adiciona as quantidades no topo das barras
for bars, loja in zip(bar_container.containers, df_quantidade.columns):
    for bar, (cat, qtd) in zip(bars, df_quantidade[loja].items()):
        altura = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            altura,
            f'{qtd}',
            ha='center', va='bottom', fontsize=6, color='black'
        )

plt.show()
