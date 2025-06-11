# ==============================================
# IMPORTAÇÃO DAS BIBLIOTECAS NECESSÁRIAS
# ==============================================
import pandas as pd
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

# Função para converter uma cor hexadecimal (#RRGGBB) para formato RGB [R, G, B]
def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]

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
cores = ['#4CAF50', '#2196F3', '#FFC107', '#9C27B0']
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
