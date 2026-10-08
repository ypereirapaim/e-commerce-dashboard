# 📊 E-commerce Analytics Dashboard

Dashboard interativo criado para complementar o projeto **Projeto-SQL-E-commerce** do GitHub.

Repositório de origem:

https://github.com/ypereirapaim/Projeto-SQL-E-commerce

O objetivo é transformar os dados do projeto SQL em uma camada visual de análise, aproximando o trabalho de um cenário real de **Data Analytics / BI**.

## 🎯 O que o dashboard mostra

- 💰 Faturamento total
- 🛒 Quantidade de pedidos
- 👥 Clientes
- 📈 Ticket médio
- Evolução do faturamento
- Faturamento por categoria
- Faturamento por estado
- Top 10 produtos
- Ranking de clientes
- Tabela de dados filtrados
- Exportação dos dados filtrados para CSV

## 🧰 Tecnologias

- Python
- Streamlit
- Pandas
- Plotly

## 🏗️ Arquitetura

```text
Projeto SQL E-commerce
        │
        │ Query / Export
        ▼
   Dataset analítico
        │
        ▼
      Pandas
        │
        ▼
    Streamlit
        │
        ├── KPIs
        ├── Gráficos
        ├── Rankings
        └── Filtros
```

## 📁 Estrutura

```text
ecommerce-dashboard-portfolio/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── data/
    └── ecommerce_dashboard.csv
```

## 🚀 Como executar

### 1. Criar ambiente virtual

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Iniciar dashboard

```bash
streamlit run app.py
```

O navegador abrirá automaticamente. Caso não abra, acesse:

```text
http://localhost:8501
```

## 🔄 Como conectar aos dados reais do projeto SQL

O arquivo:

```text
data/ecommerce_dashboard.csv
```

contém dados de exemplo com a mesma ideia de modelo do projeto SQL.

Para usar os seus dados reais, gere uma consulta que una:

```text
clientes
    +
pedidos
    +
itens_pedido
    +
produtos
```

O resultado precisa possuir estas colunas:

```text
pedido_id
data_pedido
cliente_id
cliente
estado
produto_id
produto
categoria
preco_unitario
quantidade
faturamento
```

Depois substitua:

```text
data/ecommerce_dashboard.csv
```

pelo CSV exportado da sua consulta.

### Exemplo de consulta analítica

Adapte os nomes das colunas conforme o seu schema:

```sql
SELECT
    p.id AS pedido_id,
    p.data_pedido,
    c.id AS cliente_id,
    c.nome AS cliente,
    c.estado,
    pr.id AS produto_id,
    pr.nome AS produto,
    pr.categoria,
    ip.preco_unitario,
    ip.quantidade,
    ip.preco_unitario * ip.quantidade AS faturamento
FROM pedidos p
JOIN clientes c
    ON c.id = p.cliente_id
JOIN itens_pedido ip
    ON ip.pedido_id = p.id
JOIN produtos pr
    ON pr.id = ip.produto_id;
```

> A consulta acima é um modelo. Confira os nomes exatos das colunas no seu `schema.sql` antes de executar.

## 📊 Indicadores

### Faturamento

Soma do valor dos itens vendidos no período filtrado.

### Pedidos

Quantidade de pedidos únicos.

### Clientes

Quantidade de clientes únicos que realizaram pedidos.

### Ticket médio

```text
faturamento total / quantidade de pedidos
```

## 💼 Valor para o portfólio

Este projeto complementa o seu projeto SQL porque demonstra uma cadeia mais completa:

```text
SQL
 ↓
Modelagem
 ↓
Query analítica
 ↓
Dataset
 ↓
Python/Pandas
 ↓
Dashboard
 ↓
Business Insights
```

Assim, em vez de mostrar somente consultas SQL, você consegue apresentar também o **resultado visual da análise**.

## 🚀 Próximas evoluções

Para transformar o projeto em uma solução ainda mais profissional:

- conectar diretamente ao PostgreSQL;
- criar camada de tratamento com Pandas;
- adicionar Docker;
- publicar no Streamlit Community Cloud;
- criar pipeline ETL;
- adicionar atualização automática;
- integrar o dashboard ao projeto Lakehouse;
- adicionar métricas de margem e lucro;
- incluir análise temporal e sazonalidade.

## 📄 Licença

MIT
