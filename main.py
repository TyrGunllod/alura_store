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

# Função que soma os valores de uma coluna numérica
def soma_por_coluna(arquivo, coluna):
    # Calcula a soma total da coluna especificada
    soma = arquivo[coluna].sum()
    return soma

# Função que calcula a média dos valores de uma coluna numérica
def media_por_coluna(arquivo, coluna):
    # Calcula a média da coluna e arredonda para 2 casas decimais
    media_valor = round(arquivo[coluna].mean(), 2)
    return media_valor

# Função que soma os valores da coluna "Preço" agrupando por uma categoria
def soma_por_categoria(arquivo, coluna):
    # Agrupa os dados pela categoria e soma os preços de cada grupo
    soma = arquivo.groupby(coluna)["Preço"].sum().sort_values(ascending=False)
    return soma

# Função que conta a quantidade de produtos por tipo ou categoria
def soma_produtos_tipo(arquivo, coluna):
    # Agrupa os dados pela coluna e conta quantas vezes cada valor aparece
    qt_produtos_tipo = arquivo.groupby(coluna).size().sort_values(ascending=False)
    return qt_produtos_tipo


# ==============================================
# ANÁLISE DE FATURAMENTO DAS LOJAS
# ==============================================

# Lista que armazenará o faturamento individual de cada loja
faturamento_loja = []

# Loop para calcular o faturamento (soma da coluna 'Preço') de cada loja
for i in range(len(lojas)):
    faturamento_loja.append(soma_por_coluna(lojas[i], 'Preço'))

# Exibe o faturamento de cada loja individualmente
for i, valor in enumerate(faturamento_loja, start=1):
    print(f'Faturamento da loja {i}: R$ {valor:.2f}')

# Calcula o faturamento total
faturamento_total = sum(faturamento_loja)
print(f'\nFaturamento total das lojas: R$ {faturamento_total:.2f}')

# Geração do gráfico de faturamento por loja

# Lista com nomes das lojas para o eixo X
nomes_lojas = [f'Loja {i}' for i in range(1, len(lojas) + 1)]

# Cria a figura e os eixos do gráfico
fig, ax = plt.subplots(figsize=(8, 6))

# Cria as barras verticais
barras = ax.bar(nomes_lojas, faturamento_loja, color='skyblue')

# Adiciona os valores de faturamento sobre cada barra
for bar, valor in zip(barras, faturamento_loja):
    altura = bar.get_height()
    ax.text(bar.get_x() + bar.get_width() / 2, altura + 500,  # posição do texto
            f'R$ {valor:,.2f}', ha='center', va='bottom', fontsize=9)

# Define título e rótulos
ax.set_title(f'Faturamento por Loja\nFaturamento Total: R$ {faturamento_total:,.2f}', fontsize=14)
ax.set_ylabel('Faturamento (R$)', fontsize=11)
ax.set_xlabel('Lojas', fontsize=11)

# Melhora o layout
plt.tight_layout()

# Exibe o gráfico
plt.show()


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


# ==============================================
# ANÁLISE DE PRODUTOS VENDIDOS POR LOJA
# ==============================================

# Lista que armazenará as quantidades de produtos vendidos por loja
produtos_vendidos = []

# 6. Preenche a lista com as contagens por tipo de produto
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

# 7. Lista para armazenar os objetos de figura gerados pelos gráficos
figs = []

# 8. Loop para gerar os gráficos de cada loja
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

# 9. Exibe todos os gráficos após o processamento
plt.show()


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