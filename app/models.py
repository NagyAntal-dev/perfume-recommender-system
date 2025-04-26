
from sqlalchemy import (
    Column, Integer, String, Boolean, DECIMAL, Date, ForeignKey
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Country(Base):
    __tablename__ = "countries"
    country_id = Column(Integer, primary_key=True, index=True)
    country    = Column(String, unique=True, nullable=False)
    brands     = relationship("Brand", back_populates="country")

class Brand(Base):
    __tablename__ = "brands"
    brand_id   = Column(Integer, primary_key=True, index=True)
    brand      = Column(String)
    country_id = Column(Integer, ForeignKey("countries.country_id"), nullable=False)
    country    = relationship("Country", back_populates="brands")

class User(Base):
    __tablename__ = "users"
    user_id        = Column(Integer, primary_key=True, index=True)
    username       = Column(String(100), unique=True, nullable=False)
    full_name      = Column(String)
    sex            = Column(String(10))
    mail           = Column(String)
    birthdate      = Column(Date)
    country        = Column(String)
    city           = Column(String)
    street_address = Column(String)
    password_hash  = Column(String)

class Product(Base):
    __tablename__ = "products"
    product_id    = Column(Integer, primary_key=True, index=True)
    produrl       = Column(String(2048), nullable=False)
    perfume       = Column(String)
    gender        = Column(String(50))
    rating_value  = Column(DECIMAL(5,2))
    rating_count  = Column(DECIMAL(10,0))
    create_year   = Column(Integer)
    top_note      = Column(String(4000))
    middle_note   = Column(String(4000))
    base_note     = Column(String(4000))
    price         = Column(DECIMAL(10,2))
    brand_id      = Column(Integer, ForeignKey("brands.brand_id"), nullable=False)
    quantity      = Column(Integer)
    brand         = relationship("Brand")

class Cart(Base):
    __tablename__ = "carts"
    cart_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    shipped = Column(Boolean, default=False)
    user    = relationship("User")
    contents = relationship("CartContent", back_populates="cart")

class CartContent(Base):
    __tablename__ = "cart_content"
    cart_content_id = Column(Integer, primary_key=True, index=True)
    cart_id         = Column(Integer, ForeignKey("carts.cart_id"), nullable=False)
    product_id      = Column(Integer, ForeignKey("products.product_id"), nullable=False)
    quantity        = Column(Integer)
    cart            = relationship("Cart", back_populates="contents")
    product         = relationship("Product")
