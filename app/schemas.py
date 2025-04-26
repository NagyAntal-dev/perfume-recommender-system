# app/schemas.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date # Import date for birthdate

# --- Country Schemas ---
class CountryBase(BaseModel):
    # SQL column: country
    country: str = Field(..., max_length=255) # Changed 'name' to 'country'

class CountryCreate(CountryBase):
    pass

class Country(CountryBase):
    # SQL column: country_id
    country_id: int # Changed 'id' to 'country_id'

    class Config:
        from_attributes = True

# --- Brand Schemas ---
class BrandBase(BaseModel):
    # SQL column: brand
    brand: Optional[str] = Field(None, max_length=255) # Changed 'name' to 'brand'
    country_id: int

class BrandCreate(BrandBase):
    pass

class Brand(BrandBase):
    # SQL column: brand_id
    brand_id: int # Changed 'id' to 'brand_id'
    # country: Optional[Country] = None # Uncomment for nested details

    class Config:
        from_attributes = True

# --- User Schemas ---
class UserBase(BaseModel):
    username: str = Field(..., max_length=100)
    full_name: Optional[str] = Field(None, max_length=255)
    sex: Optional[str] = Field(None, max_length=10)
    # SQL column: mail
    mail: Optional[str] = Field(None, max_length=255) # Changed 'email' to 'mail'
    birthdate: Optional[date] = None
    # SQL column: country (user's country, not FK)
    country: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=255)
    street_address: Optional[str] = Field(None, max_length=255)

class UserCreate(UserBase):
    # Input field, corresponds to 'password_hash' column after hashing
    password: str

class User(UserBase):
    # SQL column: user_id
    user_id: int # Changed 'id' to 'user_id'
    # carts: List['Cart'] = [] # Relationship backref

    class Config:
        from_attributes = True

# --- Product Schemas ---
class ProductBase(BaseModel):
    produrl: str = Field(..., max_length=2048)
    # SQL column: perfume
    perfume: Optional[str] = Field(None, max_length=255) # Changed 'name' to 'perfume'
    gender: Optional[str] = Field(None, max_length=50)
    rating_value: Optional[float] = None # DECIMAL(5,2)
    rating_count: Optional[int] = None # DECIMAL(10,0)
    create_year: Optional[int] = None
    top_note: Optional[str] = Field(None, max_length=4000)
    middle_note: Optional[str] = Field(None, max_length=4000)
    base_note: Optional[str] = Field(None, max_length=4000)
    price: Optional[float] = None # DECIMAL(10,2)
    brand_id: int
    # SQL column: quantity
    quantity: Optional[int] = None # Changed 'stock' to 'quantity'

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    # SQL column: product_id
    product_id: int # Changed 'id' to 'product_id'
    # brand: Optional[Brand] = None # Uncomment for nested details

    class Config:
        from_attributes = True

# --- CartContent Schemas ---
class CartContentBase(BaseModel):
    product_id: int
    quantity: Optional[int] = None

class CartContentCreate(CartContentBase):
    cart_id: int # Required when creating directly

class CartContent(CartContentBase):
    # SQL column: cart_content_id
    cart_content_id: int # Changed 'id' to 'cart_content_id'
    cart_id: int
    # product: Optional[Product] = None # Uncomment for product details

    class Config:
        from_attributes = True

# --- Cart Schemas ---
class CartBase(BaseModel):
    user_id: int
    shipped: Optional[bool] = None

class CartCreate(CartBase):
    pass

class Cart(CartBase):
    # SQL column: cart_id
    cart_id: int # Changed 'id' to 'cart_id'
    items: List[CartContent] = [] # Include cart items
    # user: Optional[User] = None # Uncomment for user details

    class Config:
        from_attributes = True

# Optional: Rebuild models if using forward references ('CartContent' in Cart)
# Cart.model_rebuild()
# User.model_rebuild() # If Cart is added to User schema
