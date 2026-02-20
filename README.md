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
└── requirements.txt

---

## 🔧 Como Rodar o Projeto

### 🔹 1) Instalar as dependências do arquivo 'requirements.txt'
```bash
pip install -r requirements.txt
