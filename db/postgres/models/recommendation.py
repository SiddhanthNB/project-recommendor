from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, UUID, String, Boolean, DateTime
from db.postgres.models.base_model import BaseModel as BasePostgresModel

class Recommendation(BasePostgresModel):
    __tablename__ = "generated_recommendations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), server_default=func.uuid_generate_v4(), nullable=False)
    provider = Column(String, nullable=False)
    model = Column(String, nullable=False)
    response = Column(String, nullable=False)
    archived = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
