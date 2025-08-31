import streamlit as st
import pandas as pd
import plotly.express as px

# Esta função carrega seus dados grandes de forma eficiente.
# O decorador '@st.cache_data' garante que os dados sejam carregados
# apenas uma vez, mesmo que o usuário interaja com a página. Isso
# é crucial para otimizar a performance com tabelas grandes.
@st.cache_data
def load_data():
    """
    Carrega os dados do arquivo CSV.
    Por favor, coloque o arquivo 'INFLUD21-01-05-2023.csv' na mesma pasta deste arquivo.
    """
    # A linha abaixo foi ajustada para usar o nome do seu arquivo.
    df = pd.read_csv('INFLUD21-01-05-2023.csv', sep=';', encoding='ISO-8859-1')
    return df

# --- Estrutura da Aplicação Streamlit ---

# Título da página
st.title('Evolução de Casos de SRAG e Óbitos')

# Subtítulo com uma breve descrição
st.write('Análise interativa dos dados de SRAG, baseada no seu notebook Jupyter.')

# Carrega os dados usando a função otimizada
try:
    data_df = load_data()
    st.write('Dados carregados com sucesso! Aqui estão as 5 primeiras linhas:')
    st.dataframe(data_df.head())

    # --- Processamento dos Dados (extraído do seu notebook) ---
    st.subheader('Processamento de Dados')

    # Limpando e preparando os dados para os gráficos
    data_df['DT_COLETA'] = pd.to_datetime(data_df['DT_COLETA'])

    # Contando casos e óbitos mensais
    casos_mensais = data_df.resample('M', on='DT_COLETA').size()
    obitos_mensais = data_df[data_df['EVOLUCAO'] == 'Óbito'].resample('M', on='DT_COLETA').size()

    # Convertendo as Series para DataFrame para usar no Plotly
    casos_df = casos_mensais.reset_index()
    casos_df.columns = ['Data', 'Casos']
    obitos_df = obitos_mensais.reset_index()
    obitos_df.columns = ['Data', 'Óbitos']

    # --- Gráficos Interativos (usando Plotly) ---

    st.subheader('Evolução Mensal dos Casos de SRAG')
    fig_casos = px.line(
        casos_df,
        x='Data',
        y='Casos',
        title='Evolução Mensal dos Casos de SRAG (2021-2024)',
        labels={'Data': 'Mês/Ano', 'Casos': 'Número de Casos'},
    )
    st.plotly_chart(fig_casos, use_container_width=True)

    st.subheader('Evolução Mensal dos Óbitos por SRAG')
    fig_obitos = px.line(
        obitos_df,
        x='Data',
        y='Óbitos',
        title='Evolução Mensal dos Óbitos por SRAG (2021-2024)',
        labels={'Data': 'Mês/Ano', 'Óbitos': 'Número de Óbitos'},
        color_discrete_sequence=['red']
    )
    st.plotly_chart(fig_obitos, use_container_width=True)

except FileNotFoundError:
    st.error('Arquivo de dados não encontrado. Por favor, coloque '
             'o arquivo "INFLUD21-01-05-2023.csv" na mesma pasta '
             'do arquivo app.py.')
except Exception as e:
    st.error(f'Ocorreu um erro ao carregar ou processar os dados: {e}')
