from pydantic import BaseModel, ValidationError
from product_app.models import model_to_dict
from typing import List, Dict, Any


class ProductSchema(BaseModel):
    part_number: str
    branch_id: str
    part_price: float
    short_desc: str

    @classmethod
    def validate_objects(cls, objects: List[Dict[str, Any]]) -> List['ProductSchema']:
        objects = [model_to_dict(obj) for obj in objects]
        validated_objects = []
        errors = []

        for obj in objects:
            try:
                product = cls(**obj)
                validated_objects.append(product)
            except ValidationError as e:
                errors.append(f"Object {obj} is invalid. Errors: {e.errors()}")

        if errors:
            raise ValidationError(errors)

        return validated_objects
    

class ProductResponse(BaseModel):
    part_number: str
    branch_id: str
    part_price: float
    short_desc: str

class ListProductsResponse(BaseModel):
    products: List[ProductResponse]
