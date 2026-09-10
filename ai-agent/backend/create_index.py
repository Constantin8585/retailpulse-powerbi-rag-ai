import os
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.search.documents.indexes import SearchIndexClient
from azure.search.documents.indexes.models import (
    SearchIndex, SimpleField, SearchableField, SearchField,
    SearchFieldDataType, VectorSearch, VectorSearchProfile,
    HnswAlgorithmConfiguration
)

load_dotenv()

endpoint = os.getenv("AZURE_SEARCH_ENDPOINT")
key = os.getenv("AZURE_SEARCH_KEY")
index_name = os.getenv("AZURE_SEARCH_INDEX")

client = SearchIndexClient(endpoint, AzureKeyCredential(key))

# Définition des champs de l'index
fields = [
    SimpleField(name="id", type=SearchFieldDataType.String, key=True),
    SearchableField(name="content", type=SearchFieldDataType.String),
    SimpleField(name="document_name", type=SearchFieldDataType.String, filterable=True),
    SimpleField(name="month", type=SearchFieldDataType.String, filterable=True),
    SearchField(
        name="content_vector",
        type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
        searchable=True,
        vector_search_dimensions=1536,
        vector_search_profile_name="my-profile"
    )
]

# Configuration de la recherche vectorielle
vector_search = VectorSearch(
    algorithms=[HnswAlgorithmConfiguration(name="my-hnsw")],
    profiles=[VectorSearchProfile(name="my-profile", algorithm_configuration_name="my-hnsw")]
)

index = SearchIndex(name=index_name, fields=fields, vector_search=vector_search)

# Créer ou mettre à jour l'index
client.create_or_update_index(index)
print(f"Index '{index_name}' créé avec succès !")