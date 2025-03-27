import config.mongo
from invoke.collection import Collection
from utils.tasks.one_time_tasks import create_recommendations_collection_on_mongodb, populate_recommendations_collection

ns = Collection()
ns.add_task(create_recommendations_collection_on_mongodb)
ns.add_task(populate_recommendations_collection)
