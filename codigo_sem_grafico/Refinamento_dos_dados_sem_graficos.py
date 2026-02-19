#Código do tratamento dos dados sem os gráficos

import pandas as pd
import sqlite3
import os

#--- 1) Conectar ao banco ---

DB_PATH = "olist.sqlite"

if not os.path.exists(DB_PATH):
    raise FileNotFoundError("Arquivo olist.sqlite não encontrado!")

conn = sqlite3.connect(DB_PATH)

# Tabelas
orders = pd.read_sql("SELECT * FROM orders", conn)
order_items = pd.read_sql("SELECT * FROM order_items", conn)
products = pd.read_sql("SELECT * FROM products", conn)
customers = pd.read_sql("SELECT * FROM customers", conn)
sellers = pd.read_sql("SELECT * FROM sellers", conn)
payments = pd.read_sql("SELECT * FROM order_payments", conn)
reviews = pd.read_sql("SELECT * FROM order_reviews", conn)


#--- 2) Limpeza ---

orders = orders.drop_duplicates()
order_items = order_items.drop_duplicates()
products = products.drop_duplicates()
customers = customers.drop_duplicates()
sellers = sellers.drop_duplicates()
payments = payments.drop_duplicates()
reviews = reviews.drop_duplicates()

orders["order_delivered_customer_date"] = pd.to_datetime(
    orders["order_delivered_customer_date"],
    errors="coerce"
)

orders["order_delivered_customer_date"] = orders[
    "order_delivered_customer_date"
].fillna(pd.NaT)


#--- 3) Normalização ---

if "product_category_name" in products.columns:
    products["product_category_name"] = (
        products["product_category_name"]
        .str.lower()
        .str.strip()
    )

date_cols = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

for col in date_cols:
    if col in orders.columns:
        orders[col] = pd.to_datetime(orders[col], errors="coerce")


#--- 4) Criar Métricas ---

orders["tempo_entrega_dias"] = (
    orders["order_delivered_customer_date"] - orders["order_purchase_timestamp"]
).dt.days

order_count = (
    order_items.groupby("order_id")
    .size()
    .reset_index(name="compras_por_pedido")
)

orders = orders.merge(order_count, on="order_id", how="left")

orders["order_id"] = orders["order_id"].str.strip()
customers["customer_id"] = customers["customer_id"].str.strip()


#--- 5) Merge geral ---

orders_customers = orders.merge(customers, on="customer_id", how="left")

orders_full = (
    orders_customers
        .merge(order_items, on="order_id", how="left")
        .merge(products, on="product_id", how="left")
        .merge(payments, on="order_id", how="left")
        .merge(reviews, on="order_id", how="left")
)

# Remover colunas inúteis
drop_cols = ["order_status"]
for c in drop_cols:
    if c in orders_full.columns:
        orders_full = orders_full.drop(columns=[c])


#--- 6) Criar CSV intermediário ---

os.makedirs("output", exist_ok=True)
orders_full.to_csv("output/olist_analise_tratada.csv", index=False, encoding="utf-8")


#--- 7) Criar CSV final (igual ao Jupyter) ---

df = pd.read_csv("output/olist_analise_tratada.csv")
df = df.dropna()

# Renomear colunas
Colunas = {
    "order_purchase_timestamp": "data_compra",
    "tempo_entrega_dias": "dias_entrega",
    "price": "preco_produto",
    "payment_type": "tipo_pagamento",
    "payment_value": "valor_pagamento",
    "review_score": "nota_avaliacao",
    "product_category_name": "categoria_produto",
    "customer_state": "estado_cliente"
}
df.rename(columns=Colunas, inplace=True)

# Selecionar apenas colunas necessárias
colunas_uteis = [
    "order_id",
    "categoria_produto",
    "tipo_pagamento",
    "valor_pagamento",
    "preco_produto",
    "nota_avaliacao",
    "data_compra",
    "estado_cliente"
]

df = df[colunas_uteis].copy()

# Traduzir os campos
Traduzir_pagamento = {
    'credit_card': 'Cartão de crédito',
    'boleto': 'Boleto',
    'voucher': 'Cupom',
    'debit_card': 'Cartão de Debito'
}
df['tipo_pagamento'] = df['tipo_pagamento'].replace(Traduzir_pagamento)

#Criação do campo 'mes' no arquivo
df['data_compra'] = pd.to_datetime(df['data_compra'], errors='coerce')
df['mes'] = df['data_compra'].dt.to_period('M')

# Salvar CSV final
df.to_csv("output/olist_tratada.csv", index=False, encoding="utf-8")

print("Arquivo final gerado: output/olist_tratada.csv 🎉")

#Agora é so executar o arquivo Dashboard para poder ver os graficos
