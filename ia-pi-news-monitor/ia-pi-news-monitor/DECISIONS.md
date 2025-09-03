# DECISIONS.md

## Por que análise de sentimento baseada em regras?
- **Simplicidade e transparência**: listas de palavras positivas/negativas são fáceis de auditar e ajustar.
- **Custo zero de treinamento**: não há necessidade de anotar dados nem treinar modelos.
- **Baixo risco de dependência**: funciona offline (após coleta) e sem serviços externos.
- **Ajustável ao domínio**: podemos incluir termos específicos do Piauí e do contexto de IA.

> Trade‑off: resultados mais limitados que ML; não captura ironia/sarcasmo ou nuances semânticas.

## Como lidar com erros ou falta de notícias no RSS?
- **Tratamento de exceções** por consulta: a falha de uma query não derruba o pipeline.
- **Deduplicação por link**: evita repetição da mesma notícia em consultas diferentes.
- **Limite de itens** (10–15) com **ordenação por data** quando disponível.
- **Fallback no app**: se não existir `data/news.csv`, o Streamlit exibe uma mensagem clara e permite tentar coletar de novo.

## Critérios extras adotados
- **Temas recorrentes** por palavras‑chave simples (educação, governo, saúde, etc.).
- **Filtro por palavra‑chave** e **intervalo de datas** (quando `pubDate` disponível) no próprio dashboard.

## Transparência sobre uso de IA
- E a configuração inicial do dashboard e algumas estruturas de código mais complexas receberam **auxílio de um modelo de IA (ChatGPT)**.
- Todo o restante, incluindo lógica de filtros, análise de sentimento e decisões de design, foi **desenvolvido manualmente pela autora**.
