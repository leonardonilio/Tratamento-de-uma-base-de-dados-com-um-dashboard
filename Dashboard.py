import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(
    page_title="Dashboard de um banco de dados de um E-Commerce",
    page_icon="📊",
    layout="wide",
)

df = pd.read_csv("olist_tratada.csv", encoding="utf-8")

st.sidebar.header("🔎 Filtros")
    
categorias_vendidas = sorted(df['categoria_produto'].unique())
categorias_selecionadas = st.sidebar.multiselect("Categorias", categorias_vendidas, default=categorias_vendidas)

pagamentos_disponiveis = sorted(df['tipo_pagamento'].unique())
pagamentos_selecionados = st.sidebar.multiselect("Tipos de pagamentos", pagamentos_disponiveis, default=pagamentos_disponiveis)

meses_vendas = sorted(df['mes'].unique())
mes_selecionados = st.sidebar.multiselect("Vendas por mês", meses_vendas, default=meses_vendas)


nota_disponiveis = sorted(df['nota_avaliacao'].unique())
nota_selecionada = st.sidebar.multiselect("Categorias com melhores avaliações", nota_disponiveis, default= nota_disponiveis)

estado_disponivel = sorted(df['estado_cliente'].unique())
estado_selecionado = st.sidebar.multiselect("Estados dos consumidores",estado_disponivel, default=estado_disponivel)

df_filtrado = df[
    (df['categoria_produto'].isin(categorias_selecionadas)) &
    (df['tipo_pagamento'].isin(pagamentos_selecionados)) &
    (df['mes'].isin(mes_selecionados)) &
    (df['nota_avaliacao'].isin(nota_selecionada)) &
    (df['estado_cliente'].isin(estado_selecionado))
]
# --- Conteúdo Principal ---
st.title("🎲 Dashboard do E-commerce")
st.markdown("Explore os dados dos produtos. Utilize os filtros à esquerda para refinar sua análise.")

# --- Métricas Principais (KPIs) ---
st.subheader("Métricas gerais (Salário anual em USD)")

if not df.empty:
    avaliacao_media = df['nota_avaliacao'].mean()
    estado_mais_frequente = df["estado_cliente"].mode()[0]
    total_registros = df.shape[0]
    categoria_mais_frequente = df["categoria_produto"].mode()[0]
else:
        avaliacao_media, estado_mais_frequente, total_registros, categoria_mais_frequente, = 0, "", 0, ""

col1, col2, col3, col4 = st.columns([1, 1, 1, 2])

col1.metric("Avaliação do E-commerce", f"{avaliacao_media:,.0f}⭐")
col2.metric("Estado líder em consumo", estado_mais_frequente)
col3.metric("Total de Vendas", f"{total_registros:,}")
col4.metric("Categorias mais vendida", categoria_mais_frequente)

st.markdown("---")

st.subheader("Gráficos")
col_graf1, col_graf2 = st.columns(2)
with col_graf1:
      if not df_filtrado.empty:
            top_categorias = (
            df_filtrado['categoria_produto']
            .value_counts()
            .head(10)
            .sort_values(ascending=True)
            .reset_index()
            )
            top_categorias.columns = ["categoria_produto", "quantidade"]

            fig_top_cat = px.bar(
            top_categorias,
            x="quantidade",
            y="categoria_produto",
            orientation="h",
            title="Top 10 categorias mais vendidas",
            labels={"quantidade": "Quantidade de vendas", "categoria_produto": "Categoria"},
            )
            st.plotly_chart(fig_top_cat, use_container_width=True)
      else:
            st.warning("Nenhum dado para exibir no gráfico")

with col_graf2:
      if not df_filtrado.empty:
            pagamentos = (
            df_filtrado["tipo_pagamento"]
            .value_counts()
            .reset_index()
            )
            pagamentos.columns = ["tipo_pagamento", "quantidade"]

            fig_pag = px.bar(
            pagamentos,
            x="tipo_pagamento",
            y="quantidade",
            title="Quantidade de pedidos por tipo de pagamento",
            labels={"quantidade": "Quantidade", "tipo_pagamento": "Tipo de Pagamento"},
            )
            st.plotly_chart(fig_pag, use_container_width=True)
      else:
            st.warning("Nenhum dado para exibir no gráfico")

col_graf3, col_graf4 = st.columns(2)

with col_graf3:
    if not df_filtrado.empty:
        pedidos_mes = (
        df_filtrado.groupby("mes")["order_id"]
        .nunique()
        .reset_index()
        )

        fig_ped_mes = px.line(
        pedidos_mes,
        x="mes",
        y="order_id",
        markers=True,
        title="Número de pedidos por mês",
        labels={"mes": "Mês", "order_id": "Quantidade de pedidos"},
        )

        st.plotly_chart(fig_ped_mes, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico")

with col_graf4:
    if not df_filtrado.empty:
        preco_categoria = (
        df_filtrado.groupby("categoria_produto")["preco_produto"]
        .mean()
        .sort_values(ascending=False)   # menor → maior
        .head(10)
        .sort_values(ascending=True) 
        .reset_index()
        )

        fig_preco = px.bar(
        preco_categoria,
        x="preco_produto",
        y="categoria_produto",
        orientation="h",
        title="Top 10 categorias com Maior preço médio",
        labels={"preco_produto": "Preço médio (R$)", "categoria_produto": "Categoria"},
        )

         # 👇 FORÇA O PLOTLY A USAR A ORDEM DO DATAFRAME
        fig_preco.update_layout(
        yaxis=dict(
            categoryorder="array",
            categoryarray=preco_categoria["categoria_produto"]
        )
        )

        st.plotly_chart(fig_preco, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico")

col_graf5, col_graf6 = st.columns(2)
with col_graf5:
    if not df_filtrado.empty:
        avaliacoes = (
        df_filtrado.groupby("categoria_produto")["nota_avaliacao"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .sort_values(ascending=True)
        .reset_index()
        )

        fig_avaliacoes = px.bar(
        avaliacoes,
        x="nota_avaliacao",
        y="categoria_produto",
        orientation="h",
        title="Categorias com melhores avaliações",
        labels={"nota_avaliacao": "Nota média", "categoria_produto": "Categoria"},
        )
        st.plotly_chart(fig_avaliacoes, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico")

        
with col_graf6:
    if not df_filtrado.empty:
        compras_estado = (
        df_filtrado.groupby("estado_cliente")["order_id"]
        .nunique()
        .reset_index()
        .rename(columns={"order_id": "total_compras"})
        )

        geojson_url = "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/brazil-states.geojson"

        fig_mapa = px.choropleth(
        compras_estado,
        geojson=geojson_url,
        locations="estado_cliente",
        featureidkey="properties.sigla",
        color="total_compras",
        color_continuous_scale="Viridis",
        title="Total de compras por estado",
        labels={"total_compras": "Compras"},
        )
        fig_mapa.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig_mapa, use_container_width=True)
    else:
        st.warning("Nenhum dado para exibir no gráfico")


# --- Tabela de Dados Detalhados ---

st.subheader("Dados Detalhados")
