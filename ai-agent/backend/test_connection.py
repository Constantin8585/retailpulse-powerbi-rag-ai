import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Charger les variables du .env
load_dotenv()

print("Endpoint:", os.getenv("AZURE_OPENAI_ENDPOINT"))
print("Chat deployment:", os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"))
print("API version:", os.getenv("AZURE_OPENAI_API_VERSION"))

# Créer le client Azure OpenAI
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)

# --- Test 1 : le modèle de chat ---
print("Test du modèle de chat...")
response = client.chat.completions.create(
    model=os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT"),
    messages=[
        {"role": "user", "content": "Réponds juste 'Connexion réussie' en une ligne."}
    ]
)
print("→", response.choices[0].message.content)

# --- Test 2 : le modèle d'embedding ---
print("\nTest du modèle d'embedding...")
emb = client.embeddings.create(
    model=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
    input="Ceci est un test."
)
print(f"→ Embedding généré : {len(emb.data[0].embedding)} dimensions")

print("\n Tout fonctionne !")