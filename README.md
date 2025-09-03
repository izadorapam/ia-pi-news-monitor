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
cd "C:\Users\SeuUsuario\local\ia-pi-news-monitor\ia-pi-news-monitor"

# 2) Criar o ambiente virtual (recomendado)
python -m venv .venv

# 3) Ativar o ambiente virtual
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Linux/Mac:
source .venv/bin/activate

# 4) Atualizar o pip (opcional, mas recomendado)
python -m pip install --upgrade pip

# 5) Instalar todas as dependências
pip install -r requirements.txt

# 6) Executar a coleta/ETL pela linha de comando (opcional)
python -m src.pipeline

# 7) Rodar o dashboard Streamlit
streamlit run app.py
