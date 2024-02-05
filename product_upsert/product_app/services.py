from typing import List, Optional
from fastapi import HTTPException
from product_app.models import Product
from product_app.crud import double_query_handler, get_all_products, create_product

def process_csv(file_path: str) -> List[Product]:
    with open(file_path, 'r') as file_content:
        decoded_contents = file_content.read()
    lines = decoded_contents.split("\n")[1:]  # Skip header
    products: List[Product] = [
        Product(**dict(zip(["part_number", "branch_id", "part_price", "short_desc"], line.split("|"))))
        for line in lines if line
    ]
    return products

def upsert_process(validated_products: List[Product], db, products: List[Product]):
    if validated_products:
        # Retrieve existing products from the database
        all_products = get_all_products(db)

        # If there are existing products, perform upsert
        try:
            if all_products:
                
                    part_numbers = {product.part_number for product in all_products}
                    to_update: List[Product] = []

                    def extractor(_iter):
                        if _iter.part_number not in part_numbers:
                            return _iter
                        else:
                            to_update.append(_iter)

                    new_products, product_to_update = list(filter(extractor, products)), to_update
                    new_products_: List[Product] = []
                    for product in new_products:
                        product.part_price = float(product.part_price)
                        new_products_.append(product)
                    
                    product_to_update_: List[Product] = []
                    for product in product_to_update:
                        product.part_price = float(product.part_price)
                        product_to_update_.append(product)

                    response = double_query_handler(db, new_products_, product_to_update_)

            else:
                # If no existing products, create new ones
                response = [create_product(db, product) for product in products]
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error during the upsert process: {str(e)}")

