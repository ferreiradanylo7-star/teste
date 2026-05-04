# INSTALAÇÃO E IMPORTAÇÃO
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# EXTRAÇÃO (Extract) do Arquivo do Kaggle

arquivo = 'data/sleep_mobile_stress_dataset_15000.csv'
df = pd.read_csv(arquivo)
print("Dados carregados com sucesso!")

# TRANSFORMAÇÃO (Transform)
# Limpeza e preparação dos dados

# Remover duplicatas
df = df.drop_duplicates()

# Tratar valores faltantes (preenche com 0 ou média)
df.fillna(0, inplace=True)

#  Criar nova coluna: Categoria de Estresse
df['categoria_estresse'] = pd.cut(
    df['stress_level'], 
    bins=[0, 4, 7, 10], 
    labels=['Baixo', 'Médio', 'Alto'], 
    include_lowest=True
)

# Calcular métricas (Média de sono por ocupação)
media_sono = df.groupby('occupation')['sleep_duration_hours'].mean().sort_values()
print("\n Média de sono por profissão calculada!")

# CARGA / VISUALIZAÇÃO (Load/Viz)
# Gerando os gráficos do Dashboard

# Gráfico 1: Relação Sono vs Estresse (Scatter Plot)
plt.figure(figsize=(12, 6))
sns.scatterplot(
    data=df, 
    x='sleep_duration_hours', 
    y='stress_level', 
    hue='categoria_estresse', 
    palette='viridis'
)
plt.title('Dashboard Eco-Ciclo: Impacto do Sono no Estresse')
plt.xlabel('Horas de Sono')
plt.ylabel('Nível de Estresse')
plt.grid(True, alpha=0.3)
plt.show()

# Gráfico 2: Heatmap de Correlação
plt.figure(figsize=(10, 8))
# Selecionamos apenas colunas numéricas para a correlação
sns.heatmap(df.select_dtypes(include=['number']).corr(), annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Mapa de Correlação entre Variáveis')
plt.show()

#CARGA (Salvar arquivo limpo)salva o processo de limpeza (ETL)
df.to_csv('data/sleep_clean.csv', index=False)
print("Arquivo 'data/sleep_clean.csv' salvo e pronto para o dashboard!")
