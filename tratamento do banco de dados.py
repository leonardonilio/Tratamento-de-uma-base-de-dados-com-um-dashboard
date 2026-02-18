import pandas as pd
import sqlite3

DB_PATH = "olist.sqlite"

conn = sqlite3.connect(DB_PATH)

orders = pd.read_sql("SELECT * FROM orders", conn)
order_items = pd.read_sql("SELECT * FROM order_items", conn)
products = pd.read_sql("SELECT * FROM products", conn)
customers = pd.read_sql("SELECT * FROM customers", conn)
sellers = pd.read_sql("SELECT * FROM sellers", conn)
payments = pd.read_sql("SELECT * FROM order_payments", conn)
reviews = pd.read_sql("SELECT * FROM order_reviews", conn)

orders = orders.drop_duplicates()
order_items = order_items.drop_duplicates()
products = products.drop_duplicates()
customers = customers.drop_duplicates()
sellers = sellers.drop_duplicates()
payments = payments.drop_duplicates()
reviews = reviews.drop_duplicates()

orders["order_delivered_customer_date"] = pd.to_datetime(
    orders["order_delivered_customer_date"], errors="coerce"
)

orders["order_delivered_customer_date"] = orders[
    "order_delivered_customer_date"
].fillna(pd.NaT)

print("Valores nulos em orders:\n", orders.isna().sum())
print("Valores nulos em payments:\n", payments.isna().sum())

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

print("TIPOS DE orders\n", orders.dtypes)
print("TIPOS DE products\n", products.dtypes)

orders_customers = orders.merge(customers, on="customer_id", how="left")

orders_full = orders_customers.merge(
    order_items, on="order_id", how="left"
).merge(products, on="product_id", how="left")

orders_full = orders_full.merge(payments, on="order_id", how="left")

orders_full = orders_full.merge(reviews, on="order_id", how="left")

drop_cols = [
    "order_status",
]

for c in drop_cols:
    if c in orders_full.columns:
        orders_full = orders_full.drop(columns=[c])



orders_full.to_csv("olist_analise_tratada.csv", index=False, encoding="utf-8")

print("Tratamento concluído 🚀")
