# ==============================================
# IMPORTAÇÃO DAS BIBLIOTECAS NECESSÁRIAS
# ==============================================
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import seaborn as sns
import pydeck as pdk
import webbrowser

# ==============================================
# CARREGAMENTO DOS DADOS DAS LOJAS
# ==============================================

# URLs dos arquivos CSV das lojas hospedados no GitHub
urls = [
    "https://raw.githubusercontent.com/TyrGunllod/alura_store/refs/heads/main/dados_lojas/loja_1.csv",
    "https://raw.githubusercontent.com/TyrGunllod/alura_store/refs/heads/main/dados_lojas/loja_2.csv",
    "https://raw.githubusercontent.com/TyrGunllod/alura_store/refs/heads/main/dados_lojas/loja_3.csv",
    "https://raw.githubusercontent.com/TyrGunllod/alura_store/refs/heads/main/dados_lojas/loja_4.csv"
]

# Lê todos os arquivos CSV e armazena em uma lista
lojas = [pd.read_csv(url) for url in urls]

# Define uma cor única para cada loja
cores = ['#4CAF50', '#2196F3', '#FFC107', '#9C27B0']  # Verde, Azul, Amarelo, Roxo

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

# Função para converter uma cor hexadecimal (#RRGGBB) para formato RGB [R, G, B]
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]


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
cores_media = [
    'green' if media == media_max else
    'red' if media == media_min else
    'gray'
    for media in media_avaliacoes
]

# Cria figura e eixos
fig, ax = plt.subplots(figsize=(9, 5))

# Gráfico de barras
barras = ax.bar(nomes_lojas, media_avaliacoes, color=cores_media)

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
    cores_min_max = [
        'green' if qtd == qtd_max else
        'red' if qtd == qtd_min else
        'gray'
        for qtd in df_ordenado
    ]

    # Cria a figura do gráfico com altura proporcional à quantidade de produtos
    fig, ax = plt.subplots(figsize=(10, 0.7 * len(df_ordenado) + 2), constrained_layout=True)

    # Cria gráfico de barras horizontais
    bars = ax.barh(df_ordenado.index, df_ordenado.values, color=cores_min_max)

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
    
# -------- Cálculos derivados e gráficos --------
# Cria DataFrame para comparação
df_comparativo = pd.DataFrame(dados_comparativos)

# Variação percentual em relação à média geral
media_geral = sum(frete_medio) / len(frete_medio)
variacoes = [(valor - media_geral) / media_geral * 100 for valor in frete_medio]

# Gráfico combinado
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# -------- Gráfico 1: Produtos por faixa --------
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


# ==============================================
# PRÉ-PROCESSAMENTO E AGRUPAMENTO DE DADOS
# ==============================================

# Junta todos os DataFrames em um único DataFrame com uma coluna "Loja"
df_lojas = []
for i, loja in enumerate(lojas, start=1):
    df = loja.copy()
    df["Loja"] = f"Loja {i}"
    df_lojas.append(df)

# Concatena os dados de todas as lojas
df_total = pd.concat(df_lojas, ignore_index=True)

# Agrupa os dados por localização e loja, contando número de vendas por ponto
vendas = df_total.groupby(['lat', 'lon', 'Loja']).size().reset_index(name='vendas')

# ==============================================
# CONFIGURAÇÃO DE CORES E DESLOCAMENTO
# ==============================================

# Cores hexadecimais associadas a cada loja
lojas_unicas = sorted(vendas['Loja'].unique())

# Converte cores hex para RGB e cria um dicionário {loja: cor RGB}
cores_pdk = {loja: hex_to_rgb(cores[i]) for i, loja in enumerate(lojas_unicas)}
vendas['color'] = vendas['Loja'].map(cores_pdk)

# Configurações visuais para o gráfico 2D
largura_barra = 0.2      # Largura de cada barra
altura_max = 2.0         # Altura máxima que uma barra pode atingir no gráfico 2D

# Deslocamento lateral automático para evitar sobreposição de barras
deslocamento = 0.35
max_vendas = vendas['vendas'].max()
deslocamentos = {loja: i * deslocamento for i, loja in enumerate(lojas_unicas)}

# ==============================================
# GRÁFICO 2D: DISTRIBUIÇÃO GEOGRÁFICA E MAPA DE CALOR
# ==============================================

# Cria duas visualizações lado a lado
fig, axes = plt.subplots(1, 2, figsize=(18, 8))
ax1, ax2 = axes

# === GRÁFICO 1: Barras Geográficas (2D) ===
legendas_adicionadas = set()

for i, loja in enumerate(lojas_unicas):
    dados_loja = vendas[vendas['Loja'] == loja]
    for _, row in dados_loja.iterrows():
        lat = row['lat']
        lon = row['lon'] + deslocamentos[loja]  # aplica deslocamento horizontal
        altura = (row['vendas'] / max_vendas) * altura_max
        base_lat = lat - altura  # base da barra

        # Adiciona o retângulo (barra) ao gráfico
        rect = Rectangle(
            (lon - largura_barra / 2, base_lat),
            largura_barra, altura,
            color=cores[i], alpha=0.7
        )
        ax1.add_patch(rect)

        # Garante que a legenda para cada loja seja adicionada apenas uma vez
        if loja not in legendas_adicionadas:
            rect.set_label(loja)
            legendas_adicionadas.add(loja)

# Ajusta limites e estilo do gráfico 1
ax1.set_xlim(df_total['lon'].min() - 1, df_total['lon'].max() + 1)
ax1.set_ylim(df_total['lat'].min() - 2, df_total['lat'].max() + 2)
ax1.set_xlabel("Longitude")
ax1.set_ylabel("Latitude")
ax1.set_title("Distribuição Geográfica das Vendas por Loja (com Barras)")
ax1.legend(title="Loja")
ax1.grid(True)

# === GRÁFICO 2: Mapa de Calor ===
sns.kdeplot(
    data=df_total, x='lon', y='lat',
    fill=True, cmap='Reds', thresh=0.05, ax=ax2
)
ax2.set_title('Mapa de Calor da Concentração de Vendas (Todas as Lojas)')
ax2.set_xlabel('Longitude')
ax2.set_ylabel('Latitude')
ax2.grid(True)

# Exibe os gráficos 2D
plt.tight_layout()
plt.show()

# ==============================================
# MAPA 3D INTERATIVO COM PYDECK
# ==============================================

# Define deslocamentos fixos para longitude no mapa 3D
offsets = {
    'Loja 1': -0.45,
    'Loja 2': -0.15,
    'Loja 3': 0.15,
    'Loja 4': 0.45
}

# Cria coluna de longitude ajustada (para evitar sobreposição)
vendas['lon_ajustada'] = vendas.apply(lambda row: row['lon'] + offsets[row['Loja']], axis=1)

# Combina latitude e longitude ajustada em uma única lista para cada linha
vendas['coordinates'] = vendas[['lon_ajustada', 'lat']].values.tolist()

# Define a altura das colunas com base na quantidade de vendas
vendas['elevation'] = vendas['vendas'] * 50

# Cria a camada de colunas 3D
column_layer = pdk.Layer(
    "ColumnLayer",                    # Tipo de camada
    data=vendas,                      # DataFrame com os dados
    get_position="coordinates",       # Posição das colunas
    get_elevation="elevation",        # Altura proporcional às vendas
    elevation_scale=1,                # Escala da elevação
    radius=15000,                     # Tamanho da base da coluna
    get_fill_color="color",           # Cor da coluna por loja
    pickable=True,                    # Permite interação (tooltip)
    auto_highlight=True               # Destaque automático ao passar o mouse
)

# Define o estado inicial da visualização do mapa
view_state = pdk.ViewState(
    longitude=df_total['lon'].mean(),  # Centraliza longitude
    latitude=df_total['lat'].mean(),   # Centraliza latitude
    zoom=4,                            # Nível de zoom
    pitch=45                           # Inclinação da câmera para efeito 3D
)

# Cria o mapa 3D completo
deck = pdk.Deck(
    layers=[column_layer],             # Adiciona a camada de colunas
    initial_view_state=view_state,     # Configura o ponto de vista
    tooltip={"text": "Loja: {Loja}\nVendas: {vendas}"}  # Tooltip interativo
)

# Salva o mapa em HTML e abre automaticamente no navegador
html_path = "mapa_vendas_3d_barras.html"
deck.to_html(html_path)
webbrowser.open(html_path)

# (Opcional) Exibe no notebook caso esteja rodando no Google Colab
deck.show()