from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from product_app.schema import ListProductsResponse, ProductResponse, ProductSchema
from product_app.services import  upsert_process, process_csv
from product_app.crud import get_all_products
from product_app.models import Product, Base, model_to_dict
from product_app.database import engine, get_db
import uvicorn

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/upload_products/")
async def upload_csv(file: str = Form(...), db: Session = Depends(get_db)) -> JSONResponse:
    try:
        if not file.endswith(".csv"):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed for upload.")
        
        products = process_csv(file)
        validated_products = ProductSchema.validate_objects(products)
        upsert_process(validated_products, db, products)

        return JSONResponse(content={"message": "Product Creation/Upload Successful"}, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

    
@app.get("/get_products/", response_model=ListProductsResponse)
async def list_products(db: Session = Depends(get_db)) -> ListProductsResponse:
    try:
        products = [model_to_dict(product) for product in get_all_products(db)]
        return ListProductsResponse(products=[ProductResponse(**product) for product in products])

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading products from the database: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
