# -*- coding: utf-8 -*-
"""
Pipeline: coleta -> processamento -> persistência (CSV/JSON).
"""
import csv, json, os
from datetime import datetime
from typing import List
from .rss_collector import collect_news
from .text_processing import strip_html, classify_sentiment, extract_themes

def run_pipeline(queries: List[str], out_csv: str, out_json: str, max_items: int = 15):
    raw_items = collect_news(queries, max_items=max_items)
    rows = []
    for it in raw_items:
        title = strip_html(it.get("title",""))
        desc = strip_html(it.get("description",""))
        link = it.get("link","")
        pub_date = it.get("pub_date","")
        source = it.get("source","")
        # sentimento e temas com base em título+descrição
        text = f"{title}. {desc}"
        label, score = classify_sentiment(text)
        themes = extract_themes(text)
        rows.append({
            "title": title,
            "description": desc,
            "link": link,
            "pub_date": pub_date,
            "source": source,
            "sentiment": label,
            "sentiment_score": score,
            "themes": ", ".join(themes)
        })
    # Salvar CSV
    os.makedirs(os.path.dirname(out_csv), exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()) if rows else
            ["title","description","link","pub_date","source","sentiment","sentiment_score","themes"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    # Salvar JSON
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    return rows

if __name__ == "__main__":
    # Execução direta: coleta padrão
    queries = ["Inteligência Artificial Piauí", "SIA Piauí"]
    out_csv = os.path.join(os.path.dirname(__file__), "..", "data", "news.csv")
    out_json = os.path.join(os.path.dirname(__file__), "..", "data", "news.json")
    rows = run_pipeline(queries, out_csv, out_json, max_items=15)
    print(f"Coletadas {len(rows)} notícias. Arquivos salvos em data/.")
