from typing import List, Optional
from sqlalchemy.orm import Session

from product_app.models import Product, model_to_dict

def double_query_handler(db: Session, new_products: List[Product], product_to_update: List[Product]) -> None:
    [update_product(db, product.part_number, product) for product in product_to_update if product_to_update]

    [create_product(db, product) for product in new_products if new_products]

def create_product(db: Session, product: Product) -> Product:
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def get_all_products(db: Session) -> List[Product]:
    return db.query(Product).all()

def get_product(db: Session, part_number: str) -> Optional[Product]:
    return db.query(Product).filter(Product.part_number == part_number).first()

def update_product(db: Session, part_number: str, new_data: Product) -> Product:
    new_data_dict = model_to_dict(new_data)
    product = db.query(Product).filter(Product.part_number == part_number).first()
    for key, value in new_data_dict.items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return product

def delete_product(db: Session, part_number: str) -> Product:
    product = db.query(Product).filter(Product.part_number == part_number).first()
    db.delete(product)
    db.commit()
    return product

