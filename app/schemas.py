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

    country_id: int

    class Config:
        from_attributes = True


class BrandBase(BaseModel):

    brand: Optional[str] = Field(None, max_length=255)
    country_id: int

class BrandCreate(BrandBase):
    pass

class Brand(BrandBase):

    brand_id: int


    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str = Field(..., max_length=100)
    full_name: Optional[str] = Field(None, max_length=255)
    sex: Optional[str] = Field(None, max_length=10)

    mail: Optional[str] = Field(None, max_length=255)
    birthdate: Optional[date] = None

    country: Optional[str] = Field(None, max_length=255)
    city: Optional[str] = Field(None, max_length=255)
    street_address: Optional[str] = Field(None, max_length=255)

class UserCreate(UserBase):

    password: str

class User(UserBase):

    user_id: int


    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    produrl: str = Field(..., max_length=2048)

    perfume: Optional[str] = Field(None, max_length=255)
    gender: Optional[str] = Field(None, max_length=50)
    rating_value: Optional[float] = None
    rating_count: Optional[int] = None
    create_year: Optional[int] = None
    top_note: Optional[str] = Field(None, max_length=4000)
    middle_note: Optional[str] = Field(None, max_length=4000)
    base_note: Optional[str] = Field(None, max_length=4000)
    price: Optional[float] = None
    brand_id: int

    quantity: Optional[int] = None

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):

    product_id: int


    class Config:
        from_attributes = True


class CartContentBase(BaseModel):
    product_id: int
    quantity: Optional[int] = None

class CartContentCreate(CartContentBase):
    cart_id: int

class CartContent(CartContentBase):

    cart_content_id: int
    cart_id: int


    class Config:
        from_attributes = True


class CartBase(BaseModel):
    user_id: int
    shipped: Optional[bool] = None

class CartCreate(CartBase):
    pass

class Cart(CartBase):

    cart_id: int
    items: List[CartContent] = []
    # user: Optional[User] = None # Uncomment for user details

    class Config:
        from_attributes = True

# Optional: Rebuild models if using forward references ('CartContent' in Cart)
# Cart.model_rebuild()
# User.model_rebuild() # If Cart is added to User schema
