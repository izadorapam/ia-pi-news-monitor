# IA PI News Monitor

**Monitoramento e análise de notícias do Piauí com visualização interativa em Streamlit.**

---

## 🚀 Sobre o projeto

O **IA PI News Monitor** é um sistema desenvolvido em Python para coletar, processar e visualizar notícias do estado do Piauí. Ele realiza o ETL (Extração, Transformação e Carga) dos dados, gera arquivos CSV/JSON e oferece um dashboard interativo para análise das informações.  

### Funcionalidades

- Coleta automatizada de notícias.
- Processamento e limpeza dos dados.
- Geração de relatórios em CSV ou JSON.
- Dashboard interativo com gráficos e nuvem de palavras.
- Visualização de tendências e análises de conteúdo.

### Tecnologias

- Python
- Pandas
- Plotly
- Matplotlib
- WordCloud
- Streamlit

---

## 🛠 Como executar

```bash
# 1) Clonar o repositório
git clone <seu-repo>.git
cd ia-pi-news-monitor

# 2) Criar venv (opcional, recomendado)
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux / MacOS

# 3) Instalar dependências
pip install -r requirements.txt

# 4) Executar a coleta/ETL
python -m src.pipeline

# 5) Rodar o dashboard
streamlit run app.py
