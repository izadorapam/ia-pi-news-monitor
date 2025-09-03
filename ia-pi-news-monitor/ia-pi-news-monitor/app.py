# -*- coding: utf-8 -*-
import os
import pandas as pd
import streamlit as st
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Importa funções do src
from src.pipeline import run_pipeline
from src.text_processing import word_frequencies

# --- Configurações da página ---
st.set_page_config(page_title="IA no Piauí • Monitor de Notícias", layout="wide", page_icon="🛰️")

# --- CSS personalizado ---
st.markdown("""
    <style>
    /* Fundo escuro e gradiente */
    body, .stApp {
        background: linear-gradient(135deg, #1e1e2f, #2c2c44, #3a3a5c);
        color: #e0e0ff;
    }
    /* Título principal */
    .stTitle {
        font-size: 42px !important;
        font-weight: bold;
        color: #ffddff;
        text-align: center;
    }
    /* Cards de métricas */
    .stMetric {
        background-color: #2a2a40;
        border-radius: 12px;
        padding: 10px;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.5);
        color: #ffffff;
    }
    /* Sidebar */
    .sidebar .sidebar-content {
        background-color: #2a2a40;
        color: #ffffff;
        border-radius: 12px;
        padding: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- Título e descrição ---
st.title("🛰️ IA no Piauí • Monitor de Notícias")
st.caption("Monitor de menções sobre **Inteligência Artificial** no Piauí em fontes públicas (Google Notícias RSS).")

# --- Sidebar: parâmetros ---
st.sidebar.header("Parâmetros de coleta")
default_queries = ["Inteligência Artificial Piauí", "SIA Piauí"]
queries = st.sidebar.text_area("Consultas (uma por linha)", value="\n".join(default_queries)).splitlines()
max_items = st.sidebar.slider("Máximo de notícias", 10, 30, 15, 1)

if st.sidebar.button("🔄 Atualizar dados (coletar agora)"):
    with st.spinner("Coletando e processando notícias..."):
        rows = run_pipeline(queries, "data/news.csv", "data/news.json", max_items=max_items)
        st.success(f"Coletadas {len(rows)} notícias.")

# --- Carrega dados ---
df = None
if os.path.exists("data/news.csv"):
    df = pd.read_csv("data/news.csv")
else:
    st.info("Nenhum arquivo encontrado em **data/news.csv**. Clique em 'Atualizar dados' para coletar.")
    df = pd.DataFrame(columns=["title","description","link","pub_date","source","sentiment","sentiment_score","themes"])

# --- Filtros ---
with st.expander("🔍 Filtros"):
    query = st.text_input("Buscar por palavra-chave (em título/descrição/temas):", "")
    sentiments = st.multiselect("Filtrar por sentimento", ["positivo","negativo","neutro"], default=[])
    
    # Filtro por data
    date_min, date_max = None, None
    if not df.empty and "pub_date" in df.columns and df["pub_date"].notna().any():
        try:
            dates = pd.to_datetime(df["pub_date"], errors="coerce")
            min_d = dates.min()
            max_d = dates.max()
            if pd.notna(min_d) and pd.notna(max_d):
                date_min, date_max = st.slider("Intervalo de datas (pubDate)", min_value=min_d.to_pydatetime(), max_value=max_d.to_pydatetime(), value=(min_d.to_pydatetime(), max_d.to_pydatetime()))
                mask_dates = (dates >= date_min) & (dates <= date_max)
                df = df[mask_dates]
        except Exception:
            pass

    if query:
        q = query.lower()
        df = df[df.apply(lambda r: q in str(r["title"]).lower() or q in str(r["description"]).lower() or q in str(r.get("themes","")).lower(), axis=1)]
    if sentiments:
        df = df[df["sentiment"].isin(sentiments)]

# --- KPIs ---
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total de notícias", len(df))
c2.metric("Positivas", int((df["sentiment"] == "positivo").sum()) if "sentiment" in df else 0)
c3.metric("Neutras", int((df["sentiment"] == "neutro").sum()) if "sentiment" in df else 0)
c4.metric("Negativas", int((df["sentiment"] == "negativo").sum()) if "sentiment" in df else 0)

# --- Gráfico de pizza com Plotly ---
st.subheader("Distribuição de Sentimentos")
if not df.empty and "sentiment" in df.columns:
    counts = df["sentiment"].value_counts().reindex(["positivo","neutro","negativo"]).fillna(0)
    fig = px.pie(
        names=counts.index,
        values=counts.values,
        color=counts.index,
        color_discrete_map={"positivo":"#8A2BE2", "neutro":"#9370DB", "negativo":"#4B0082"},
        title="Sentimentos das notícias"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("Sem dados para plotar.")

# --- Nuvem de palavras ---
st.subheader("Nuvem de Palavras")
if not df.empty:
    texts = (df["title"].fillna("") + ". " + df["description"].fillna("")).tolist()
    freqs = word_frequencies(texts, top_k=200)
    if freqs:
        wc = WordCloud(
            width=1200,
            height=500,
            background_color="#1e1e2f",
            colormap="plasma",
            contour_width=3,
            contour_color='#8A2BE2'
        ).generate_from_frequencies(freqs)
        fig2, ax2 = plt.subplots(figsize=(10,4))
        ax2.imshow(wc, interpolation="bilinear")
        ax2.axis("off")
        st.pyplot(fig2)
    else:
        st.write("Sem termos suficientes para gerar a nuvem.")
else:
    st.write("Sem dados para nuvem.")

# --- Tabela de notícias ---
st.subheader("Tabela de Notícias")
st.dataframe(df, use_container_width=True)

# --- Download dos dados ---
st.download_button("Baixar CSV", data=df.to_csv(index=False).encode("utf-8"), file_name="news.csv", mime="text/csv")
st.download_button("Baixar JSON", data=df.to_json(orient="records", force_ascii=False, indent=2), file_name="news.json", mime="application/json")

# --- Rodapé ---
st.markdown("---")
st.caption("**Limitações**: Esta análise de sentimento é baseada em regras simples e pode não capturar sarcasmo ou contextos complexos. Resultados podem variar conforme a cobertura do feed RSS.")
st.caption("**Transparência**: A configuração inicial do dashboard e algumas estruturas de código mais complexas receberam auxílio de um modelo de IA (ChatGPT). Todo o restante, incluindo lógica de filtros, análise de sentimento e decisões de design, foi desenvolvido manualmente pela autora.")
