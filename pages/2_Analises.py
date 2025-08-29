import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

st.title("📊 Análises Avançadas: Séries Temporais, Casos e Óbitos")

# ========================
# 1. Carregar dados
# ========================
@st.cache_data
def carregar_dados():
    tabela_2021 = pd.read_csv("dados/INFLUD21-01-05-2023.csv", sep=",")
    tabela_2022 = pd.read_csv("dados/INFLUD22-01-05-2023.csv", sep=",")
    tabela_2023 = pd.read_csv("dados/INFLUD23-15-04-2024.csv", sep=",")
    tabela_2024 = pd.read_csv("dados/2024.csv", sep=",")
    return tabela_2021, tabela_2022, tabela_2023, tabela_2024

tabela_2021, tabela_2022, tabela_2023, tabela_2024 = carregar_dados()

# Garantir formato datetime
for tabela in [tabela_2021, tabela_2022, tabela_2023, tabela_2024]:
    tabela['DT_SIN_PRI'] = pd.to_datetime(tabela['DT_SIN_PRI'], dayfirst=True, errors='coerce')

todas_tabelas = pd.concat([tabela_2021, tabela_2022, tabela_2023, tabela_2024])

# ========================
# 2. Casos mensais
# ========================
casos = todas_tabelas.dropna(subset=['DT_SIN_PRI'])
casos_mensais = (
    casos
    .set_index('DT_SIN_PRI')
    .resample('M')
    .size()
)

# ========================
# 3. Óbitos mensais
# ========================
if todas_tabelas['EVOLUCAO'].dtype != 'object':
    obitos = todas_tabelas[todas_tabelas['EVOLUCAO'] == 2]
else:
    obitos = todas_tabelas[todas_tabelas['EVOLUCAO'].str.lower().str.strip() == 'óbito']

obitos = obitos.dropna(subset=['DT_SIN_PRI'])
obitos_mensais = (
    obitos
    .set_index('DT_SIN_PRI')
    .resample('M')
    .size()
)

# ajustar índices
casos_mensais = casos_mensais.sort_index()
obitos_mensais = obitos_mensais.reindex(casos_mensais.index, fill_value=0)

# ========================
# 4. Gráficos no Streamlit
# ========================

st.subheader("📈 Evolução Mensal dos Casos de SRAG")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(casos_mensais.index, casos_mensais.values, linestyle='-', marker='o', color='royalblue')
ax.set_xlabel("Mês/Ano")
ax.set_ylabel("Número de Casos")
ax.grid(True)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader("⚰️ Evolução Mensal dos Óbitos por SRAG")
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(obitos_mensais.index, obitos_mensais.values, linestyle='--', marker='s', color='crimson')
ax.set_xlabel("Mês/Ano")
ax.set_ylabel("Número de Óbitos")
ax.grid(True)
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
plt.xticks(rotation=45)
st.pyplot(fig)

st.subheader("📊 Casos e Óbitos (Sobrepostos)")
fig, ax1 = plt.subplots(figsize=(12, 6))

# Casos
color_casos = 'royalblue'
ax1.set_xlabel("Mês/Ano")
ax1.set_ylabel("Casos", color=color_casos)
ax1.plot(casos_mensais.index, casos_mensais.values, marker='o', color=color_casos)
ax1.tick_params(axis='y', labelcolor=color_casos)

ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
plt.xticks(rotation=45)

# Óbitos
ax2 = ax1.twinx()
color_obitos = 'crimson'
ax2.set_ylabel("Óbitos", color=color_obitos)
ax2.plot(obitos_mensais.index, obitos_mensais.values, linestyle='--', marker='s', color=color_obitos)
ax2.tick_params(axis='y', labelcolor=color_obitos)

st.pyplot(fig)
