### 1. Create and Activate a Virtual Environment (Optional but Recommended)
    *create**
    python3 -m venv venv

    **activate**
    windows : venv\Scripts\activate
    macos/linus: source venv/bin/activate

### Install Dependencies
  `pip install -r requirements.txt`

### Usage
    Run the FastAPI Server on your terminal:

    `uvicorn product_app.main:app --reload`

        The server will be available at http://127.0.0.1:8000, and you can change the port if needed.

    ### Access FastAPI Interactive Documentation:
    Open your browser and go to http://127.0.0.1:8000/docs to access the FastAPI interactive documentation.
    Here, you can test the two  endpoints:

    Endpoint 1: /upload_products/
        Method: POST
        Description: Takes the directory to your CSV file, writes or updates the database, and returns a success message. If a product is not already existing, it will be added; if it exists, it will be updated.

    Endpoint 2: /get_products/
        Method: GET
        Description: Collects all the products in the store and returns them as a list of objects.

### Testing
To run tests, use the following command:

`pytest tests/`
 or 
`pytest tests/test_main.py`
