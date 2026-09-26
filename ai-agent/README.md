# Suite Fabric + IA — NordRetail

Extension du projet Power BI NordRetail avec une couche data Microsoft Fabric et une couche IA agentique (Azure OpenAI, Azure AI Search). Développée sur la branche `feature/fabric-ai-agent-extension` — voir [`docs/architecture-fabric-ai.md`](../docs/architecture-fabric-ai.md), [`docs/ai-governance.md`](../docs/ai-governance.md) et [`docs/demo-script.md`](../docs/demo-script.md) pour le contexte, les principes de gouvernance IA et le scénario de démo.

## État actuel de l'implémentation

Ce qui existe aujourd'hui dans `ai-agent/backend/` :

- `tools/sql_tool.py` — connexion au Fabric SQL endpoint (auth Azure AD via `DefaultAzureCredential`) et requête `get_kpi_snapshot(month)` sur la vue `dbo.vw_ai_kpi_snapshot`.
- `agents/analysis_agent.py` — un agent unique qui interroge `sql_tool`, puis demande à Azure OpenAI (`gpt-5-mini` ou équivalent) une analyse en français des 3 écarts de CA les plus critiques du mois.
- `create_index.py` — création/mise à jour d'un index Azure AI Search (recherche vectorielle, dimension 1536) pour la partie RAG documentaire.
- `test_connection.py` — script de vérification de la connexion Azure OpenAI (chat + embeddings).

Ce qui est décrit dans `docs/` mais **pas encore implémenté** :

- L'orchestration multi-agent (Data, BI, Document, Reporting, Quality) mentionnée dans `demo-script.md` — seul l'agent d'analyse existe pour l'instant.
- Le pipeline RAG complet (ingestion de documents dans l'index Azure AI Search) — `create_index.py` crée l'index mais aucun script d'ingestion n'est présent.
- Le frontend (`ai-agent/frontend/` est vide, placeholder uniquement).
- Les notebooks et scripts SQL Fabric (`fabric/notebooks/` et `fabric/sql/` sont vides, placeholders uniquement).

## Prérequis

- Python 3.13
- Un environnement Fabric (Lakehouse/Warehouse) exposant la vue `dbo.vw_ai_kpi_snapshot`
- Une ressource Azure OpenAI avec un déploiement chat et un déploiement embedding
- Une ressource Azure AI Search (pour la partie RAG)
- Droits Azure AD sur le SQL endpoint Fabric (authentification interactive via `DefaultAzureCredential`)

## Installation

```bash
cd ai-agent/backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env       # puis renseigner les valeurs
```

> **Note requirements.txt** : les entrées `httpcore2` et `httpx2` ressemblent à une erreur de génération (`pip freeze`) — à vérifier, les paquets attendus sont probablement `httpcore` et `httpx`.

## Utilisation

```bash
python test_connection.py            # vérifie la connexion Azure OpenAI
python tools/sql_tool.py              # teste la requête KPI Fabric
python agents/analysis_agent.py       # lance une analyse de mois (exemple : 2024-03)
python create_index.py                # crée/màj l'index Azure AI Search
```

## Sécurité et gouvernance

- Aucune donnée personnelle (PII) n'est manipulée par l'agent : seules les vues KPI agrégées sont exposées.
- Voir [`docs/ai-governance.md`](../docs/ai-governance.md) pour les principes anti-hallucination et de traçabilité.
- Le fichier `.env` ne doit jamais être committé (exclu via `.gitignore`) ; utiliser `.env.example` comme modèle.
