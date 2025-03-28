from config.logger import logger
from services.google_service import GoogleService
from services.openrouter_service import OpenRouterService
from services.openai_service import OpenAIService
# from services.huggingface_service import HuggingFaceService
from services.groq_service import GroqService
from db.mongo.models.recommendation import Recommendation

_providers_hash = {
    'grok': GroqService,
    'google': GoogleService,
    'openrouter': OpenRouterService,
    'openai': OpenAIService
}

def _persist_recommendations(response, model_name, provider_name):
    new_record_ids = []

    for res in response:
        payload = {
            'model': model_name,
            'provider': provider_name,
            'archived': False,
            'response': res
        }
        record = Recommendation.create_document(payload)
        new_record_ids.append(record.id)

    # archive all non archived recommendations except the newly added ones
    if len(new_record_ids) > 0:
        Recommendation.update_documents({'archived': False, '_id': { '$nin': new_record_ids }}, { 'archived': True })

    return True

def generate_and_save_recommendations():
    for provider_name, provider_service in _providers_hash.items():
        response = None
        try:
            service = provider_service()
            response = service.get_response()
            if isinstance(response, list) and len(response) > 0:
                return _persist_recommendations(response, service.model_name, provider_name)
            else:
                raise Exception("Did not receive expected response from the api call")
        except Exception as e:
            logger.warning(f"Response generation failed for {provider_name} with ERROR: {e}")
            continue

    raise Exception("Failed to generate response: No response from any provider!")

def fetch_active_recommendations_from_db():
    records = Recommendation.fetch_documents({'archived': False})
    return [ record.to_dict() for record in records ]
