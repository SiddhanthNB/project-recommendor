from invoke.tasks import task
import utils.constants as constants
from config.postgres import execute_query
from db.mongo.models.base_model import BaseModel as BaseMongoModel
from db.mongo.schemas.recommendation import schema as recommendation_schema
from db.mongo.models.recommendation import Recommendation

@task()
def create_recommendations_collection_on_mongodb(ctx):
	try:
		print('Task started...')
		db = BaseMongoModel.get_database()
		collection_name = constants.RECOMMENDATION_COLLECTION_NAME
		db.create_collection(collection_name, validator = recommendation_schema, validationLevel = "strict")
		print(f"Collection '{collection_name}' created successfully.")
		print('Task completed')
	except Exception as e:
		if "already exists" in str(e):
			print(f"Collection '{collection_name}' already exists.")
		else:
			print(f"Unexpected error: {e}")

@task()
def populate_recommendations_collection(ctx):
    result = execute_query("SELECT * FROM generated_recommendations;")
    rows = result.get('rows')
    columns = result.get('columns')

    for row in rows:
        record_hash = dict(zip(columns, row))
        payload = {
            'model': record_hash.get('model'),
            'provider': record_hash.get('provider'),
            'response': record_hash.get('response'),
            'archived': record_hash.get('archived'),
            'created_at': record_hash.get('created_at'),
            'updated_at': record_hash.get('created_at')
        }
        Recommendation.create_document(payload)

    print('Recommendations collection populated successfully.')

       

