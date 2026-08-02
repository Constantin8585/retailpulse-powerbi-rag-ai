#!/usr/bin/env bash
# ============================================================
# RetailPulse / NordRetail - Suite Fabric + IA
# Script adapté à la structure existante :
#   - conserve src/ (projet Power BI) tel quel
#   - réutilise le dossier Data/ existant (CSV sources)
#   - ajoute fabric/ et ai-agent/ à côté
# À lancer depuis la racine du dépôt NORDRETAIL.
# ============================================================

set -e

echo "Vérification : on est bien à la racine du dépôt Git..."
if [ ! -d ".git" ]; then
  echo "ERREUR : pas de dossier .git ici. Place-toi à la racine de NORDRETAIL."
  exit 1
fi

echo "Création des nouveaux dossiers de la suite Fabric + IA..."

# --- Données générées pour la suite (dans le Data existant) ---
# On réutilise le dossier Data/ existant plutôt que d'en créer un nouveau.
mkdir -p Data/documents/sample

# --- Fabric (couche data) ---
mkdir -p fabric/notebooks
mkdir -p fabric/sql

# --- AI Agent (couche IA) ---
mkdir -p ai-agent/backend/agents
mkdir -p ai-agent/backend/tools
mkdir -p ai-agent/backend/prompts
mkdir -p ai-agent/backend/evaluation
mkdir -p ai-agent/frontend

# --- Tests (le dossier tests/ existe déjà, on ajoute des sous-dossiers) ---
mkdir -p tests/data-quality
mkdir -p tests/ai-evaluation

# ============================================================
# .gitkeep pour conserver les dossiers vides dans Git
# ============================================================
find fabric ai-agent tests/data-quality tests/ai-evaluation Data/documents \
  -type d -empty -exec touch {}/.gitkeep \;

# ============================================================
# Squelettes de docs (créés seulement s'ils n'existent pas)
# ============================================================
[ ! -f docs/architecture-fabric-ai.md ] && cat > docs/architecture-fabric-ai.md << 'EOF'
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
EOF

[ ! -f docs/ai-governance.md ] && cat > docs/ai-governance.md << 'EOF'
# Gouvernance IA

## Principes
- Sources obligatoires pour toute réponse chiffrée
- Distinction faits confirmés / hypothèses
- Contrôle anti-hallucination
- Alignement avec le RLS Power BI
- Traçabilité (logs des questions, outils, sources)
EOF

[ ! -f docs/demo-script.md ] && cat > docs/demo-script.md << 'EOF'
# Script de démonstration — Suite Fabric + IA

## Plan de démo (15 min)
1. Rappel projet Power BI initial
2. Architecture Fabric (OneLake, Lakehouse, gold tables)
3. Rapport Power BI reconnecté / page Analyse IA
4. Question à l'agent : "Analyse juin 2026"
5. Sources : vue SQL + documents RAG
6. Multi-agent (Data, BI, Document, Reporting, Quality)
7. Évaluation : score, hallucinations
8. Conclusion : GitHub, CI/CD, évolutions
EOF

echo ""
echo "Terminé ! Nouveaux dossiers créés à côté de src/ et Data/."
echo ""
echo "Structure actuelle (hors .git) :"
find . -maxdepth 2 -type d -not -path '*/\.git*' | sort | sed 's|\./||; s|[^/]*/|  |g'
