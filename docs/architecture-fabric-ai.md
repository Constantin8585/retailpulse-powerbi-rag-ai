# Architecture — Suite Fabric + IA

## Contexte
Extension du projet Power BI NordRetail avec une couche data (Microsoft Fabric)
et une couche IA agentique (Azure OpenAI, Azure AI Search).

## Couches
- Data : OneLake, Lakehouse (bronze/silver/gold), Warehouse SQL
- BI : semantic model Power BI (référence certifiée)
- IA : agents spécialisés, RAG documentaire, orchestrateur

## Principe fondamental
La BI reste la source de vérité des indicateurs. L'IA explique et synthétise,
elle n'invente pas les chiffres.
