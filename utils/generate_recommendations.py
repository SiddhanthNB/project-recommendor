from services.google_service import GoogleService
from services.openrouter_service import OpenRouterService
from services.openai_service import OpenAIService
# from services.huggingface_service import HuggingFaceService
from services.groq_service import GroqService
from db.mongo.models.recommendation import Recommendation

providers_hash = {
    'grok': GroqService,
    'google': GoogleService,
    'openrouter': OpenRouterService,
    'openai': OpenAIService
}

# generate new recommendations
for provider_name, provider_service in providers_hash.items():
    response = None
    try:
        service = provider_service()
        response = service.get_response()
        if response is not None and isinstance(response, list):
            break
    except Exception as e:
        continue

# fetch active recommendations from the database
active_recommendations = Recommendation.fetch_documents({'archived': False})

for res in response:
    payload = {
        'model': service.model_name,
        'provider': provider_name,
        'archived': False,
        'response': res
    }
    Recommendation.create_document(payload)

# archive all previously active recommendations
active_recommendations.update(archived=True)
