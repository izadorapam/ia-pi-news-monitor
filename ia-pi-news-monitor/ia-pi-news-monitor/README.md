# IA no Piauí • Monitor de Notícias

Painel simplificado para monitorar menções sobre **"Inteligência Artificial no Piauí"** em fontes públicas (Google Notícias RSS), com **análise de sentimento por regras** e **identificação de temas recorrentes**.

## ✨ Funcionalidades
- Coleta RSS do Google Notícias para consultas como `Inteligência Artificial Piauí` e `SIA Piauí`.
- Limpeza de texto, **sentimento por regras (positivo/neutro/negativo)** e extração de **temas** via palavras‑chave.
- Dashboard em **Streamlit** com **gráfico de pizza**, **nuvem de palavras** e **tabela interativa**.
- Botões para **download** dos dados em CSV/JSON.
- Rodapé com **aviso de limitações** e nota de **transparência** sobre o uso de IA.

## 🧰 Tecnologias
`Python`, `requests`, `xml.etree.ElementTree`, `pandas`, `streamlit`, `matplotlib`, `wordcloud`.

## 🚀 Como executar

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
```

Os arquivos gerados ficarão em `data/news.csv` e `data/news.json`.

## 🧪 Teste rápido sem internet
Se você não conseguir coletar agora, o app abre mesmo sem `data/news.csv`. Clique em **"Atualizar dados"** para tentar coletar quando estiver online.


## ⚖️ Ética e Transparência
No rodapé do dashboard há um aviso:  
> "Esta análise de sentimento é baseada em regras simples e pode não capturar sarcasmo ou contextos complexos."

Também indico que a configuração inicial do dashboard e algumas estruturas de código mais complexas receberam **auxílio de um modelo de IA (ChatGPT)**. Todo o restante, incluindo lógica de filtros, análise de sentimento e decisões de design, foi **desenvolvido manualmente pela autora**.


## 📝 Licença
MIT — adapte conforme necessidade.
