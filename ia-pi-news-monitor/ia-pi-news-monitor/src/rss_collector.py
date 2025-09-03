# -*- coding: utf-8 -*-
"""
Coleta notícias do Google Notícias via RSS.
Busca consultas como "Inteligência Artificial Piauí" e "SIA Piauí".
Saída: lista de dicionários com título, link, descrição, data e fonte.
"""
from urllib.parse import quote
from xml.etree import ElementTree as ET
from datetime import datetime
import requests

GOOGLE_NEWS_RSS = "https://news.google.com/rss/search?q={query}&hl=pt-BR&gl=BR&ceid=BR:pt"

def fetch_rss(query: str, timeout: int = 20) -> str:
    url = GOOGLE_NEWS_RSS.format(query=quote(query))
    resp = requests.get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.text

def parse_items(xml_text: str):
    root = ET.fromstring(xml_text)
    # Em feeds RSS do Google Notícias, os itens ficam em channel/item
    channel = root.find("channel")
    if channel is None:
        return []
    items = []
    for it in channel.findall("item"):
        title = it.findtext("title") or ""
        link = it.findtext("link") or ""
        description = it.findtext("description") or ""
        pub_date = it.findtext("pubDate") or ""
        source_el = it.find("{http://www.w3.org/2005/Atom}source") or it.find("source")
        source = source_el.text if source_el is not None else ""
        items.append({
            "title": title.strip(),
            "link": link.strip(),
            "description": description.strip(),
            "pub_date": pub_date.strip(),
            "source": source.strip()
        })
    return items

def collect_news(queries, max_items=15):
    """Coleta e combina itens de múltiplas consultas, limitando a 10-15 notícias."""
    all_items = []
    seen_links = set()
    for q in queries:
        try:
            xml = fetch_rss(q)
            items = parse_items(xml)
        except Exception as e:
            # Em caso de erro no feed, apenas segue para a próxima consulta
            items = []
        for it in items:
            link = it.get("link", "")
            if link and link not in seen_links:
                seen_links.add(link)
                all_items.append(it)
    # Ordenar por data (quando possível)
    def parse_dt(s):
        try:
            return datetime.strptime(s, "%a, %d %b %Y %H:%M:%S %Z")
        except Exception:
            return datetime.min
    all_items.sort(key=lambda x: parse_dt(x.get("pub_date","")), reverse=True)
    return all_items[:max_items]
