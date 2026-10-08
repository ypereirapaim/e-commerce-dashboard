import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="E-commerce Analytics",
    page_icon="📊",
    layout="wide",
)

DATA_FILE = "data/ecommerce_dashboard.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE, parse_dates=["data_pedido"])
    return df


df = load_data()

st.title("📊 E-commerce Analytics Dashboard")
st.caption("Dashboard de análise construído sobre o projeto SQL E-commerce.")

st.sidebar.header("Filtros")

states = st.sidebar.multiselect(
    "Estado",
    sorted(df["estado"].unique()),
    default=sorted(df["estado"].unique()),
)

categories = st.sidebar.multiselect(
    "Categoria",
    sorted(df["categoria"].unique()),
    default=sorted(df["categoria"].unique()),
)

date_range = st.sidebar.date_input(
    "Período",
    value=(df["data_pedido"].min().date(), df["data_pedido"].max().date()),
)

filtered = df[
    df["estado"].isin(states)
    & df["categoria"].isin(categories)
]

if isinstance(date_range, tuple) and len(date_range) == 2:
    filtered = filtered[
        (filtered["data_pedido"].dt.date >= date_range[0])
        & (filtered["data_pedido"].dt.date <= date_range[1])
    ]

total_revenue = filtered["faturamento"].sum()
orders = filtered["pedido_id"].nunique()
customers = filtered["cliente_id"].nunique()
avg_ticket = total_revenue / orders if orders else 0

col1, col2, col3, col4 = st.columns(4)
col1.metric("Faturamento", f"R$ {total_revenue:,.2f}")
col2.metric("Pedidos", f"{orders:,}")
col3.metric("Clientes", f"{customers:,}")
col4.metric("Ticket médio", f"R$ {avg_ticket:,.2f}")

st.divider()

left, right = st.columns(2)

with left:
    monthly = (
        filtered.assign(mes=filtered["data_pedido"].dt.to_period("M").astype(str))
        .groupby("mes", as_index=False)["faturamento"]
        .sum()
    )

    fig = px.line(
        monthly,
        x="mes",
        y="faturamento",
        markers=True,
        title="Evolução do faturamento",
        labels={"mes": "Mês", "faturamento": "Faturamento (R$)"},
    )
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

with right:
    category = (
        filtered.groupby("categoria", as_index=False)["faturamento"]
        .sum()
        .sort_values("faturamento", ascending=False)
    )

    fig = px.bar(
        category,
        x="categoria",
        y="faturamento",
        title="Faturamento por categoria",
        labels={"categoria": "Categoria", "faturamento": "Faturamento (R$)"},
    )
    st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)

with left:
    state = (
        filtered.groupby("estado", as_index=False)["faturamento"]
        .sum()
        .sort_values("faturamento", ascending=False)
    )

    fig = px.bar(
        state,
        x="estado",
        y="faturamento",
        title="Faturamento por estado",
        labels={"estado": "Estado", "faturamento": "Faturamento (R$)"},
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    products = (
        filtered.groupby("produto", as_index=False)
        .agg(
            faturamento=("faturamento", "sum"),
            quantidade=("quantidade", "sum"),
        )
        .sort_values("faturamento", ascending=False)
        .head(10)
    )

    fig = px.bar(
        products.sort_values("faturamento"),
        x="faturamento",
        y="produto",
        orientation="h",
        title="Top 10 produtos por faturamento",
        labels={"produto": "Produto", "faturamento": "Faturamento (R$)"},
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("🏆 Clientes com maior faturamento")

ranking = (
    filtered.groupby(["cliente", "estado"], as_index=False)
    .agg(
        faturamento=("faturamento", "sum"),
        pedidos=("pedido_id", "nunique"),
    )
    .sort_values("faturamento", ascending=False)
    .head(10)
)

st.dataframe(
    ranking,
    use_container_width=True,
    hide_index=True,
    column_config={
        "faturamento": st.column_config.NumberColumn(
            "Faturamento",
            format="R$ %.2f",
        ),
        "pedidos": st.column_config.NumberColumn("Pedidos"),
    },
)

st.subheader("🔎 Dados utilizados")
st.dataframe(filtered.head(100), use_container_width=True, hide_index=True)

csv_download = filtered.to_csv(index=False).encode("utf-8")
st.download_button(
    "⬇️ Baixar dados filtrados",
    csv_download,
    "ecommerce_filtrado.csv",
    "text/csv",
)
