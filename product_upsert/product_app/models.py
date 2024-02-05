from sqlalchemy import Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from typing import Dict, Any

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    part_number = Column(String, primary_key=True, index=True)
    branch_id = Column(String)
    part_price = Column(Float)
    short_desc = Column(String)

def model_to_dict(model_instance: Any) -> Dict[str, Any]:
    return {column.key: getattr(model_instance, column.key) for column in model_instance.__table__.columns}
