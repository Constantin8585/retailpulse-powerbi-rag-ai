import os
import json
import sys
from dotenv import load_dotenv
from openai import AzureOpenAI

# Permet d'importer l'outil SQL du dossier parent
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.sql_tool import get_kpi_snapshot

load_dotenv()

client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

SYSTEM_PROMPT = """Tu es un analyste commercial pour NordRetail, une enseigne de distribution.
On te fournit des données chiffrées réelles (chiffre d'affaires vs objectif, par région et catégorie).

Règles strictes :
- Utilise UNIQUEMENT les chiffres fournis. N'invente aucune donnée.
- Identifie les 3 situations les plus critiques (écart négatif le plus fort).
- Pour chaque point, cite le chiffre exact (région, catégorie, écart en %).
- Termine par une synthèse de 2 phrases pour la direction.
- Réponds en français, de façon claire et structurée.
"""

def analyze_month(month: str) -> str:
    # 1. Récupérer les vrais chiffres via l'outil SQL
    data = get_kpi_snapshot(month)

    # 2. Préparer les données pour le modèle
    data_text = json.dumps(data, ensure_ascii=False, indent=2, default=str)

    # 3. Demander l'analyse à gpt-5-mini
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Analyse le mois {month}. Voici les données :\n{data_text}"}
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    print("=== Analyse de mars 2024 ===\n")
    print(analyze_month("2024-03"))