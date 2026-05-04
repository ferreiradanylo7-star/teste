import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Dashboard Saúde Digital", layout="wide")

# CARGA DO DADO TRATADO
df = pd.read_csv('data/sleep_clean.csv')

# SIDEBAR (Barra Lateral para Filtros) ---
st.sidebar.header("Filtros de Análise")
lista_ocupacoes = ["Todas"] + sorted(df['occupation'].unique().tolist())
ocupacao_selecionada = st.sidebar.selectbox("Selecione a Ocupação:", lista_ocupacoes)

# Filtragem dos dados baseada na escolha do usuário
if ocupacao_selecionada != "Todas":
    df_filtrado = df[df['occupation'] == ocupacao_selecionada]
else:
    df_filtrado = df

st.title(f" Análise de Bem-estar: {ocupacao_selecionada}")

#VISUALIZAÇÕES CIRCULARES
st.divider()
c1, c2 = st.columns(2)

with c1:
    st.subheader("Proporção de Níveis de Estresse")
    # Gráfico de Pizza Tradicional
    dados_estresse = df_filtrado['categoria_estresse'].value_counts()
    
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        dados_estresse, 
        labels=dados_estresse.index, 
        autopct='%1.1f%%', 
        startangle=90, 
        colors=['#ff9999','#66b3ff','#99ff99'],
        explode=(0.05, 0, 0) # Destaca a primeira fatia
    )
    ax.axis('equal')
    st.pyplot(fig)

with c2:
    st.subheader("Qualidade do Sono")
    # Criando as faixas de qualidade
    df_filtrado['status_sono'] = pd.cut(
        df_filtrado['sleep_quality_score'], 
        bins=[0, 5, 8, 10], 
        labels=['Baixa', 'Regular', 'Alta'], 
        include_lowest=True
    )
    dados_sono = df_filtrado['status_sono'].value_counts()

    fig, ax = plt.subplots(figsize=(7, 7))
    # Grafico de rosca
    ax.pie(
        dados_sono, 
        labels=dados_sono.index, 
        autopct='%1.1f%%', 
        startangle=140, 
        colors=['#ffcc99','#ff6666','#c2c2f0'],
        pctdistance=0.85
    )
    
    centro_circulo = plt.Circle((0,0), 0.70, fc='white')
    fig.gca().add_artist(centro_circulo)
    
    ax.axis('equal')
    st.pyplot(fig)

st.divider()
c3, c4 = st.columns(2)

with c3:
    st.subheader(" Uso de Celular > 6h por Dia")
    # Criando categoria binária para o gráfico
    df_filtrado['uso_celular'] = df_filtrado['daily_screen_time_hours'].apply(
        lambda x: 'Excessivo (>6h)' if x > 6 else 'Moderado (<=6h)'
    )
    dados_celular = df_filtrado['uso_celular'].value_counts()

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        dados_celular, 
        labels=dados_celular.index, 
        autopct='%1.1f%%', 
        colors=['#ff9999','#99ff99'],
        shadow=True
    )
    ax.axis('equal')
    st.pyplot(fig)

with c4:
    st.subheader("Consumo de Cafeína")
    df_filtrado['cat_cafeina'] = df_filtrado['caffeine_intake_cups'].apply(
        lambda x: 'Muita (4+)' if x >= 4 else ('Moderada (1-3)' if x > 0 else 'Nenhuma')
    )
    dados_cafe = df_filtrado['cat_cafeina'].value_counts()

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        dados_cafe, 
        labels=dados_cafe.index, 
        autopct='%1.1f%%', 
        colors=['#c2c2f0','#ffb3e6','#ffcc99'],
        wedgeprops=dict(width=0.3)
    )
    ax.axis('equal')
    st.pyplot(fig)
