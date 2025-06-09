# Importa as bibliotecas necessárias
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap

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

# Junta todos os dados das lojas em um único DataFrame e adiciona uma coluna com o nome da loja
df_lojas = []
for i, loja in enumerate(lojas, start=1):
    df = loja.copy()
    df["Loja"] = f"Loja {i}"
    df_lojas.append(df)

df_total = pd.concat(df_lojas, ignore_index=True)

# Verifica se as colunas de latitude e longitude existem
if 'lat' in df_total.columns and 'lon' in df_total.columns:
    # Gráfico de dispersão por loja
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df_total, x='lon', y='lat', hue='Loja', alpha=0.6, palette='Set2')
    plt.title('Distribuição Geográfica das Vendas por Loja')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # Mapa de calor geral (todas as lojas combinadas)
    plt.figure(figsize=(10, 6))
    sns.kdeplot(
        data=df_total, x='lon', y='lat',
        fill=True, cmap='Reds', thresh=0.05
    )
    plt.title('Mapa de Calor da Concentração de Vendas (Todas as Lojas)')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
else:
    print("As colunas 'lat' e 'lon' não foram encontradas no DataFrame.")

# Mapa base centralizado
mapa = folium.Map(location=[df_total['lat'].mean(), df_total['lon'].mean()], zoom_start=6)

# Adiciona o HeatMap
heat_data = df_total[['lat', 'lon']].dropna().values.tolist()
HeatMap(heat_data, radius=8).add_to(mapa)

# Exibe o mapa (em ambiente Jupyter/Notebook)
mapa