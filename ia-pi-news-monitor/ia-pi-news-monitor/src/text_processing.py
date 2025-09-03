# -*- coding: utf-8 -*-
"""
Limpeza de texto e classificação de sentimento por regras simples (pt-BR).
Também extrai temas recorrentes via match de palavras-chave.
"""
import re
import html
from collections import Counter
from typing import List, Dict, Tuple

# Lista curta de stopwords pt-BR suficiente para nuvem simples
STOPWORDS = set("""a ao aos à às aquele aquela aquilo aquele(a) aquilo as assim com como da das de do dos e é em entre era eram essa esse isso esta este isto eu ele ela eles elas foi foram há isso já la lá mas mais mesmo muito na nas nem no nos nós o os ou para pela pelas pelo pelos por qual quais que quem sem sob sobre sua suas seu seus também tem têm um uma umas uns você vocês""".split())

POSITIVE = {
    "avanço","benefício","melhoria","positivo","inovador","inovação","crescimento","oportunidade",
    "eficiente","eficiência","sucesso","premiado","parceria","liderança","recorde","melhor","otimista"
}
NEGATIVE = {
    "problema","crise","queda","negativo","risco","falha","polêmica","atraso","corte","fraude",
    "dificuldade","prejuízo","erro","ameaça","desafio","escândalo","denúncia"
}

THEMES = {
    "educação": {"ufpi","ifpi","universidade","escola","pesquisa","campus","extensão","aula"},
    "governo": {"governo","estado","secretaria","prefeitura","poder público","política","decreto"},
    "saúde": {"saúde","hospital","clínica","sus","diagnóstico","doença"},
    "economia": {"economia","negócios","mercado","investimento","emprego","renda","indústria"},
    "segurança": {"segurança","polícia","fraude","cyber","cibernética","ataque","golpe"},
    "agro": {"agro","agricultura","agronegócio","campo"},
    "startups": {"startup","empreendedorismo","aceleração","incubadora"},
    "tecnologia": {"ia","inteligência artificial","machine learning","algoritmo","robô","chatbot","modelo"},
    "cultura": {"cultura","evento","festival","mostra","seminário","workshop","oficina"},
    "setor público": {"piauí","teresina","parnaíba","picos","floriano","piripiri","altos"}
}

def strip_html(text: str) -> str:
    # Desescapa entidades e remove tags simples
    text = html.unescape(text or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize(text: str) -> List[str]:
    text = text.lower()
    # mantem letras e números, separa demais
    tokens = re.findall(r"[a-záâãàéêíóôõúç0-9]+", text, flags=re.IGNORECASE)
    return tokens

def classify_sentiment(text: str) -> Tuple[str, int]:
    tokens = tokenize(text)
    pos = sum(1 for t in tokens if t in POSITIVE)
    neg = sum(1 for t in tokens if t in NEGATIVE)
    score = pos - neg
    label = "neutro"
    if score > 0:
        label = "positivo"
    elif score < 0:
        label = "negativo"
    return label, score

def extract_themes(text: str) -> List[str]:
    text_l = text.lower()
    found = set()
    for theme, keys in THEMES.items():
        for k in keys:
            if k in text_l:
                found.add(theme)
                break
    return sorted(found)

def word_frequencies(texts: List[str], top_k: int = 100) -> Dict[str,int]:
    c = Counter()
    for t in texts:
        tokens = [w for w in tokenize(strip_html(t)) if w not in STOPWORDS and len(w) > 2]
        c.update(tokens)
    return dict(c.most_common(top_k))
