
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue?logo=sqlite&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Cleaning-150458?logo=pandas)
![Plotly](https://img.shields.io/badge/Plotly-Visualizações-3F4F75?logo=plotly)

# 🛒 Análise e Dashboard de Dados — Base E-commerce Olist

Este projeto realiza **tratamento, limpeza, normalização e análise exploratória** de uma grande base de dados de um e-commerce brasileiro (Olist).  
Após o processamento, é gerado um arquivo final **CSV tratado**, que alimenta um **dashboard interativo em Streamlit**.

---

## 📦 Sobre o Dataset

A base utilizada é o **Olist E-commerce Dataset**, disponibilizada publicamente no Kaggle.

🔗 **Link para download do banco completo (.sqlite):**  
https://www.kaggle.com/datasets/terencicp/e-commerce-dataset-by-olist-as-an-sqlite-database

⚠️ **Importante:**  
O arquivo `olist.sqlite` **não está incluído no repositório**, pois ultrapassa o limite de tamanho do GitHub.  
Por isso ele está listado no `.gitignore`.  
Para rodar o projeto, basta fazer o download do arquivo pelo link acima e colocá-lo na raíz do projeto.

---

## 🧠 Objetivo do Projeto

O projeto tem dois propósitos principais:

1. **Tratamento e normalização** dos dados do banco Olist.
2. **Criação de um dashboard visual** para análise de vendas, categorias, pagamentos e comportamento dos clientes.

---

## 🛠️ Tecnologias Utilizadas

### **Backend / Processamento**
- Python
- Pandas
- SQLite3


### **Dashboard**
- Streamlit
- Plotly Express

### **Outras dependências utilizadas**
- sqlalchemy 
- seaborn
- matplotlib

---

## 🗂️ Estrutura do Projeto
📁 Tratamento-de-uma-base-de-dados-com-um-dashboard

│

├── codigo_sem_grafico

│ ├── Refinamento_dos_dados_sem_graficos.py

│

├── output/

│ ├── olist_analise_tratada.csv

│ └── olist_tratada.csv # CSV final utilizado no dashboard

│

├── .gitignore

│

├── olist.sqlite # (não incluído – baixar do Kaggle)

│

├── Dashboard.py

├── Refinamento_dos_dados.ipynb

│

├── README.md

│

└── requirements.txt # (aqui fica as dependências que precisa instalar para funcionar o projeto)

---

## 🔧 Como Rodar o Projeto

### 🔹 1) Instalar as dependências do arquivo 'requirements.txt'

```bash
pip install -r requirements.txt
```

### 🔹 2) Baixar o banco de dados
Baixe o arquivo olist.sqlite no Kaggle e coloque-o na pasta raiz do projeto. Link: https://www.kaggle.com/datasets/terencicp/e-commerce-dataset-by-olist-as-an-sqlite-database

### 🔹 3) Executar o tratamento dos dados

Você pode executar o processo de limpeza de duas formas:

✔️ 1. Via Jupyter Notebook (mais didático)

Arquivo:

'Refinamento_dos_dados.ipynb'

Basta abrir no Jupyter Notebook ou VS Code.

✔️ 2. Via script Python (mais rápido)

Arquivo:

'codigo_sem_grafico/Refinamento_dos_dados_sem_graficos.py'

Execução:
```bash
python codigo_sem_grafico/Refinamento_dos_dados_sem_graficos.py
```

📌 Esse processo irá gerar automaticamente os arquivos:

output/olist_analise_tratada.csv

output/olist_tratada.csv → usado no dashboard

## 📊 Como Executar o Dashboard
Após gerar o arquivo olist_tratada.csv, execute:

```bash
streamlit run Dashboard.py
```
Em seguida, o Streamlit abrirá o dashboard no navegador.

### 📊 Sobre o Dashboard

O dashboard inclui visualizações como:

. Produtos mais vendidos

. Distribuição por categoria

. Tipos de pagamento

. Média de avaliações

. Receita por mês

. Estado dos clientes

E outras análises baseadas no dataset tratado.

---

## 🧹 Sobre o tratamento dos dados

O script realiza:

### ✔ Limpeza:

. Remoção de duplicados

. Padronização de datas

. Normalização de nomes de categorias

. Preenchimento de valores nulos quando possível

### ✔ Enriquecimento:

. Cálculo do tempo de entrega

. Quantidade de itens por pedido

. Tradução dos tipos de pagamento

. Extração do mês da compra

### ✔ Merge Geral:

Integração de 7 tabelas do SQLite em um único dataset final:

. orders

. order_items

. products

. customers

. sellers

. payments

. reviews
