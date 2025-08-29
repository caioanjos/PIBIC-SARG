import streamlit as st
import pandas as pd

st.title("Análise Descritiva")

opcao = st.selectbox(
    "Escolha o arquivo de dados:",
    ["INFLUD21-01-05-2023.csv", "INFLUD22-01-05-2023.csv", 
     "INFLUD23-15-04-2024.csv", "2024.csv"]
)

df = pd.read_csv(f"dados/{opcao}")

st.subheader("Pré-visualização dos dados")
st.dataframe(df.head())

st.subheader("Estatísticas descritivas")
st.write(df.describe())
