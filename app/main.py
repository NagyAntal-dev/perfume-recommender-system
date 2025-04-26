# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import crud, models, schemas, database
from pydantic import BaseModel

class StatsCounts(BaseModel):
    users: int
    products: int
    brands: int
    countries: int
    carts: int

app = FastAPI(title="OLTP API")

# --- CORS Configuration ---
# List of origins that are allowed to make requests to this API.
# Use ["*"] to allow all origins (less secure, okay for local dev)
# Or be specific: ["http://localhost:5173", "http://127.0.0.1:5173"] for your Svelte dev server
origins = [
    "http://localhost:5173", # Default Vite/Svelte dev server port
    "http://127.0.0.1:5173",
    # Add any other origins if needed (e.g., your deployed frontend URL)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Allows specific origins
    allow_credentials=True, # Allows cookies (if you use auth)
    allow_methods=["*"],    # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],    # Allows all headers
)
# --- End CORS Configuration ---

# Initialize tables on startup
@app.on_event("startup")
def on_startup():
    database.init_db()

# Dependency
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/stats/counts/", response_model=StatsCounts)
def read_stats_counts(db: Session = Depends(get_db)):
    return StatsCounts(
        users=crud.get_users_count(db),
        products=crud.get_products_count(db),
        brands=crud.get_brands_count(db),
        countries=crud.get_countries_count(db),
        carts=crud.get_carts_count(db)
    )

@app.post("/countries/", response_model=schemas.Country)
def create_country(country: schemas.CountryCreate, db: Session = Depends(get_db)):
    return crud.create_country(db, country)

@app.get("/countries/", response_model=list[schemas.Country])
def read_countries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_countries(db, skip, limit)

# --- Brands ---
@app.post("/brands/", response_model=schemas.Brand)
def create_brand(brand: schemas.BrandCreate, db: Session = Depends(get_db)):
    # You might want to add checks, e.g., if country_id exists
    return crud.create_brand(db, brand)

@app.get("/brands/", response_model=list[schemas.Brand])
def read_brands(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_brands(db, skip, limit)

# --- Users ---
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Add logic to hash password before saving
    # db_user = crud.get_user_by_username(db, username=user.username)
    # if db_user:
    #     raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# --- Products ---
@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    # Add checks, e.g., if brand_id exists
    return crud.create_product(db, product)

@app.get("/products/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 100000, db: Session = Depends(get_db)):
    return crud.get_products(db, skip, limit)

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.delete("/products/{product_id}", status_code=204) # Use 204 No Content for successful DELETE
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    crud.delete_product(db=db, product_id=product_id)
    return None

# --- Carts ---
@app.post("/carts/", response_model=schemas.Cart)
def create_cart(cart: schemas.CartCreate, db: Session = Depends(get_db)):
    # Add checks, e.g., if user_id exists
    return crud.create_cart(db, cart)

@app.get("/carts/", response_model=list[schemas.Cart])
def read_carts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_carts(db, skip, limit)

@app.get("/carts/{cart_id}", response_model=schemas.Cart)
def read_cart(cart_id: int, db: Session = Depends(get_db)):
    db_cart = crud.get_cart(db, cart_id=cart_id)
    if db_cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return db_cart

# --- Cart Contents ---
@app.post("/cart_contents/", response_model=schemas.CartContent)
def create_cart_content(cart_content: schemas.CartContentCreate, db: Session = Depends(get_db)):
    # Add checks, e.g., if cart_id and product_id exist
    # Add logic to handle quantity updates if item already in cart
    return crud.create_cart_content(db, cart_content)

@app.get("/cart_contents/", response_model=list[schemas.CartContent])
def read_cart_contents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # Might be more useful to get contents by cart_id
    return crud.get_cart_contents(db, skip, limit)

@app.get("/carts/{cart_id}/contents/", response_model=list[schemas.CartContent])
def read_contents_for_cart(cart_id: int, db: Session = Depends(get_db)):
    # Assumes a crud function get_cart_contents_by_cart_id exists
    db_cart = crud.get_cart(db, cart_id=cart_id)
    if db_cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    return crud.get_cart_contents_by_cart_id(db, cart_id=cart_id)

# Add more specific endpoints as needed, e.g., PUT for updates, DELETE for removals
