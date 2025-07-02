from services.openai_service import OpenAIService
from db.mongo.models.recommendation import Recommendation

service = OpenAIService()
response = service.get_response()

new_record_ids = []
for res in response:
    payload = {
        'model': service.model_name,
        'provider': 'openai',
        'archived': False,
        'response': res
    }
    record = Recommendation.create_document(payload)
    new_record_ids.append(record.id)

# archive all non archived recommendations except the newly added ones
if len(new_record_ids) > 0:
    Recommendation.update_documents({'archived': False, '_id': { '$nin': new_record_ids }}, { 'archived': True })
