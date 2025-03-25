from datetime import datetime, timezone
import utils.constants as constants
from db.mongo.models.base_model import BaseModel as BaseMongoModel
from mongoengine import BooleanField, StringField, DictField, DateTimeField

class Recommendation(BaseMongoModel):
    model = StringField(required = True)
    provider = StringField(required = True)
    response = DictField(required = True)
    archived = BooleanField(default = True)
    created_at = DateTimeField(default = lambda: datetime.now(timezone.utc))
    updated_at = DateTimeField(default = lambda: datetime.now(timezone.utc))

    meta = {
        'collection': constants.RECOMMENDATION_COLLECTION_NAME,
        'strict': True # does not allow storing fields not defined in this schema
    }
