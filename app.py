import os
import pandas as pd
import plotly.express as px
import streamlit as st

# Configuração da página
st.set_page_config(page_title="Dashboard de Vendas de Carros", layout="wide")

# Carregar os dados
@st.cache_data
def load_data():
    file_path = os.path.join(os.path.dirname(__file__), "vehicles_us.xlsx")
    return pd.read_excel(file_path)

# Carregar dados
car_data = load_data()

# Criar coluna 'brand' a partir do modelo
car_data['brand'] = car_data['model'].apply(lambda x: str(x).split()[0] if pd.notnull(x) else 'Desconhecido')

# Título principal
st.header('Dashboard de Análise de Vendas de Carros 🚗')

# Mostrar informações básicas dos dados
st.subheader('Visão Geral dos Dados')
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total de Carros", len(car_data))
with col2:
    st.metric("Preço Médio", f"${car_data['price'].mean():,.0f}")
with col3:
    st.metric("Ano Médio", f"{car_data['model_year'].mean():.0f}")
with col4:
    st.metric("Quilometragem Média", f"{car_data['odometer'].mean():,.0f} milhas")

# Seção de visualizações
st.header('Visualizações Interativas')

# Criar duas colunas para os controles
col1, col2 = st.columns(2)

with col1:
    # Botão para criar histograma
    hist_button = st.button('Criar Histograma de Preços')
    
    if hist_button:
        st.write('Criando um histograma para os preços dos carros')
        fig_hist = px.histogram(
            car_data, 
            x="price", 
            nbins=50,
            title="Distribuição de Preços dos Carros",
            labels={'price': 'Preço ($)', 'count': 'Quantidade'}
        )
        fig_hist.update_layout(bargap=0.1)
        st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    # Botão para criar gráfico de dispersão
    scatter_button = st.button('Criar Gráfico de Dispersão')
    
    if scatter_button:
        st.write('Criando gráfico de dispersão: Preço vs Quilometragem')
        fig_scatter = px.scatter(
            car_data, 
            x="odometer", 
            y="price",
            title="Preço vs Quilometragem",
            labels={'odometer': 'Quilometragem (milhas)', 'price': 'Preço ($)'},
            opacity=0.6
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

# Seção com checkboxes (desafio extra)
st.header('Análises Adicionais')

# Checkbox para mostrar estatísticas por marca
show_brand_stats = st.checkbox('Mostrar estatísticas por marca')

if show_brand_stats:
    st.subheader('Top 10 Marcas por Quantidade')
    brand_counts = car_data['brand'].value_counts().head(10)
    
    fig_brands = px.bar(
        x=brand_counts.index,
        y=brand_counts.values,
        title="Top 10 Marcas Mais Anunciadas",
        labels={'x': 'Marca', 'y': 'Quantidade de Anúncios'}
    )
    st.plotly_chart(fig_brands, use_container_width=True)

# Checkbox para análise por ano
show_year_analysis = st.checkbox('Mostrar análise por ano do modelo')

if show_year_analysis:
    st.subheader('Preço Médio por Ano do Modelo')
    
    # Filtrar anos válidos (remover valores muito baixos ou muito altos)
    valid_years = car_data[(car_data['model_year'] >= 1990) & (car_data['model_year'] <= 2023)]
    
    yearly_avg = valid_years.groupby('model_year')['price'].mean().reset_index()
    
    fig_year = px.line(
        yearly_avg,
        x='model_year',
        y='price',
        title='Preço Médio por Ano do Modelo',
        labels={'model_year': 'Ano do Modelo', 'price': 'Preço Médio ($)'}
    )
    st.plotly_chart(fig_year, use_container_width=True)

# Filtros interativos
st.header('Filtros de Dados')

# Seletor de marca
available_brands = sorted(car_data['brand'].dropna().unique())
selected_brand = st.selectbox('Selecione uma marca:', ['Todas'] + available_brands)

# Filtro de preço
price_range = st.slider(
    'Faixa de preço:',
    min_value=int(car_data['price'].min()),
    max_value=int(car_data['price'].max()),
    value=(int(car_data['price'].min()), int(car_data['price'].max())),
    format="$%d"
)

# Aplicar filtros
filtered_data = car_data[
    (car_data['price'] >= price_range[0]) & 
    (car_data['price'] <= price_range[1])
]

if selected_brand != 'Todas':
    filtered_data = filtered_data[filtered_data['brand'] == selected_brand]

# Mostrar dados filtrados
st.subheader(f'Dados Filtrados ({len(filtered_data)} carros)')
if st.checkbox('Mostrar tabela de dados filtrados'):
    st.dataframe(filtered_data[['brand', 'model', 'model_year', 'price', 'odometer']].head(100))

# Rodapé
st.markdown('---')
st.markdown('Dashboard criado com Streamlit 🚀 | Dados de anúncios de carros')
