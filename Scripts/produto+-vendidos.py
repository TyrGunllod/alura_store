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

# Função que soma a quantidade de produtos por tipo
def soma_produtos_tipo(arquivo, coluna):
    # Agrupa os dados pela coluna e conta a quantidade de ocorrências
    qt_produtos_tipo = arquivo.groupby(coluna).size().sort_values(ascending=False)
    return qt_produtos_tipo


# ==============================================
# ANÁLISE DE PRODUTOS VENDIDOS POR LOJA
# ==============================================

# Lista que armazenará as quantidades de produtos vendidos por loja
produtos_vendidos = []

# Preenche a lista com as contagens por tipo de produto
for i in range(len(lojas)):
    produtos_vendidos.append(soma_produtos_tipo(lojas[i], 'Produto'))

for i, df_produtos in enumerate(produtos_vendidos, start=1):
    qtd_mais_vendido = df_produtos.max()
    qtd_menos_vendido = df_produtos.min()

    mais_vendidos = df_produtos[df_produtos == qtd_mais_vendido]
    menos_vendidos = df_produtos[df_produtos == qtd_menos_vendido]

    print(f'Loja {i}:')

    print(f'  Mais vendidos ({qtd_mais_vendido} unidades):')
    for produto, qtd in mais_vendidos.items():
        print(f'   - {produto}')

    print(f'  Menos vendidos ({qtd_menos_vendido} unidades):')
    for produto, qtd in menos_vendidos.items():
        print(f'   - {produto}')

    print()  # Linha em branco entre as lojas

# Lista para armazenar os objetos de figura gerados pelos gráficos
figs = []

# Loop para gerar os gráficos de cada loja
for i, df_produtos in enumerate(produtos_vendidos, start=1):
    # Ordena os produtos do mais vendido ao menos vendido
    df_ordenado = df_produtos.sort_values(ascending=False)

    # Obtém os valores máximo e mínimo para definir as cores
    qtd_max = df_ordenado.max()
    qtd_min = df_ordenado.min()

    # Define as cores para as barras:
    # Verde para o mais vendido, vermelho para o menos vendido, cinza para os demais
    cores = [
        'green' if qtd == qtd_max else
        'red' if qtd == qtd_min else
        'gray'
        for qtd in df_ordenado
    ]

    # Cria a figura do gráfico com altura proporcional à quantidade de produtos
    fig, ax = plt.subplots(figsize=(10, 0.7 * len(df_ordenado) + 2), constrained_layout=True)

    # Cria gráfico de barras horizontais
    bars = ax.barh(df_ordenado.index, df_ordenado.values, color=cores)

    # Define o título e os rótulos dos eixos
    ax.set_title(f'Quantidade Vendida por Produto - Loja {i}', fontsize=12)
    ax.set_xlabel('Quantidade Vendida', fontsize=10)
    ax.set_ylabel('Produto', fontsize=10)

    # Ajusta o tamanho da fonte dos rótulos dos eixos
    ax.tick_params(axis='y', labelsize=7)
    ax.tick_params(axis='x', labelsize=9)

    # Inverte o eixo Y para que o mais vendido fique no topo
    ax.invert_yaxis()

    # Define a posição horizontal para o texto dentro da barra
    x_text = qtd_min * 0.6
    if x_text < 1:
        x_text = 1

    # Adiciona as quantidades dentro das barras
    for bar, qtd in zip(bars, df_ordenado.values):
        y = bar.get_y() + bar.get_height() / 2  # centro vertical da barra
        ax.text(x_text, y, f'{qtd}', va='center', ha='left', fontsize=8, color='white')

    # Armazena a figura na lista
    figs.append(fig)

# Exibe todos os gráficos após o processamento
plt.show()
