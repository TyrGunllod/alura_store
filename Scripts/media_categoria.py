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

# Função que soma os valores da coluna "Preço" agrupando por uma categoria
def soma_por_categoria(arquivo, coluna):
    # Agrupa os dados pela categoria e soma os preços de cada grupo
    soma = arquivo.groupby(coluna)["Preço"].sum().sort_values(ascending=False)
    return soma

# ==============================================
# ANÁLISE DE FATURAMENTO POR CATEGORIA - POR LOJA
# ==============================================

# Lista que armazenará os DataFrames com faturamento por categoria de cada loja
vendas_categoria = []

# Loop para calcular o faturamento por categoria de produto em cada loja
for i in range(len(lojas)):
    # Utiliza a função 'soma_por_categoria' para somar os preços por categoria
    vendas_categoria.append(soma_por_categoria(lojas[i], 'Categoria do Produto'))

# Loop para exibir os resultados de faturamento por categoria para cada loja
for i, categoria in enumerate(vendas_categoria, start=1):
    print(f'\nFaturamento por categoria - Loja {i}:\n')

    # Itera sobre os pares (nome da categoria, valor total)
    for nome_categoria, total in categoria.items():
        print(f' - {nome_categoria}: R$ {total:.2f}')

    # Linha em branco entre os resultados de cada loja
    print()

# Concatena todos os DataFrames por categoria, renomeando colunas
df_categorias = pd.concat(vendas_categoria, axis=1)
df_categorias.columns = [f'Loja {i+1}' for i in range(len(lojas))]
df_categorias = df_categorias.fillna(0)

# Cria o gráfico comparativo
fig, ax = plt.subplots(figsize=(10, 6))
df_categorias.plot(kind='bar', ax=ax)

# Título e rótulos
ax.set_title('Faturamento por Categoria - Comparativo entre Lojas', fontsize=14)
ax.set_xlabel('Categoria do Produto', fontsize=11)
ax.set_ylabel('Faturamento (R$)', fontsize=11)
ax.legend(title='Lojas')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()