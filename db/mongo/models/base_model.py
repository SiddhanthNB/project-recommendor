import config.mongo #need this to make mongo db connection
from bson import ObjectId
from config.logger import logger
from datetime import datetime, timezone
from mongoengine.queryset.queryset import QuerySet
from mongoengine import Document, ValidationError, OperationError

class BaseModel(Document):
	meta = { 'abstract': True }

	@classmethod
	def create_document(cls, fields = {}):
		"""Create a new document."""
		try:
			if not bool(fields): raise OperationError("param 'fields' cannot be empty")

			instance = cls(**fields)
			instance.save()
			return instance
		except ValidationError as e:
			logger.error(f"Validation error: {e}")
			return False
		except Exception as e:
			logger.error(f"Error: {e}", exc_info = True)
			return False

	@classmethod
	def fetch_document_by_id(cls, id):
		"""Find a document by a its id."""
		try:
			if not bool(id): raise OperationError("param 'id' cannot be empty")

			return cls.objects(__raw__ = { '_id': ObjectId(id) }).first()
		except Exception as e:
			logger.error(f"Error: {e}", exc_info = True)
			return False

	@classmethod
	def fetch_documents(cls, filter = {}):
		"""Find all documents by a filter."""
		try:
			return cls.objects(__raw__ = filter)
		except Exception as e:
			logger.error(f"Error: {e}", exc_info = True)
			return False

	@classmethod
	def count(cls, filter = {}):
		"""Count documents by a filter."""
		try:
			return cls.objects(__raw__ = filter).count()
		except Exception as e:
			logger.error(f"Error: {e}", exc_info = True)
			return False

	@classmethod
	def first(cls, count = 1):
		"""Fetches first documents by the given count."""
		try:
			result = cls.objects.order_by('id').limit(count)
			return result.first() if count == 1 else result
		except Exception as e:
			logger.error(f"Error: {e}", exc_info = True)
			return False

	@classmethod
	def last(cls, count = 1):
		"""Fetches last documents by the given count."""
		try:
			result = cls.objects.order_by('-id').limit(count)
			return result.first() if count == 1 else result
		except Exception as e:
			logger.error(f"Error: {e}", exc_info = True)
			return False

	@classmethod
	def update_documents(cls, filter = {}, fields = {}):
		"""Update documents matching the filter with new values."""
		try:
			fields['updated_at'] = datetime.now(timezone.utc)
			result = cls.objects(__raw__ = filter).update(__raw__ = { '$set': fields })
			return result
		except ValidationError as e:
			logger.error(f"Validation error: {e}")
			return False
		except Exception as e:
			logger.error(f"Error: {e}", exc_info = True)
			return False

	def update_fields(self, fields = {}):
		"""Update specific fields of the current instance."""
		try:
			if not bool(fields): raise OperationError("param 'fields' cannot be empty")

			fields['updated_at'] = datetime.now(timezone.utc)
			result = self.update(__raw__ = { '$set': fields })
			return result
		except ValidationError as e:
			logger.error(f"Validation error: {e}")
			return False
		except Exception as e:
			logger.error(f"Error: {e}", exc_info = True)
			return False

	@classmethod
	def delete_documents(cls, filter = {}):
		"""Delete documents matching the filter."""
		try:
			return cls.objects(__raw__ = filter).delete()
		except ValidationError as e:
			logger.error(f"Validation error: {e}")
			return False
		except Exception as e:
			logger.error(f"Error: {e}", exc_info = True)
			return False

	def to_dict(self):
		"""Convert the instance to a dictionary representation."""
		try:
			_self = self.to_mongo().to_dict()
			_self['_id']        = str(_self['_id'])
			_self['created_at'] = _self['created_at'].isoformat()
			_self['updated_at'] = _self['updated_at'].isoformat()
			return _self
		except Exception as e:
			logger.error(f"Error: {e}", exc_info = True)
			return False

	@classmethod
	def get_database(cls):
		"""Get pymongo instance of the database."""
		return Document._get_db()
