
from sqlalchemy.orm import Session
import models, schemas





def get_countries(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Country).offset(skip).limit(limit).all()

def create_country(db: Session, country: schemas.CountryCreate):

    db_obj = models.Country(**country.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def get_brand(db: Session, brand_id: int):
    return db.query(models.Brand).filter(models.Brand.id == brand_id).first()

def get_brands(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Brand).offset(skip).limit(limit).all()

def create_brand(db: Session, brand: schemas.BrandCreate):
    db_brand = models.Brand(**brand.model_dump())
    db.add(db_brand)
    db.commit()
    db.refresh(db_brand)
    return db_brand





def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
     return db.query(models.User).filter(models.User.username == username).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):



    user_data = user.model_dump(exclude={'password'})
    # Add the hashed password if you implement hashing
    # user_data['hashed_password'] = get_password_hash(user.password)
    db_user = models.User(**user_data) # Adjust if using hashed password
    # Add placeholder for password if your model requires it but you aren't hashing yet
    if 'password' in user.model_dump():
         db_user.hashed_password = "placeholder_hash_" + user.password
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_product(db: Session, product_id: int):


    return db.query(models.Product).filter(models.Product.product_id == product_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

def create_product(db: Session, product: schemas.ProductCreate):

    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def delete_product(db: Session, product_id: int):

    db.query(models.CartContent).filter(models.CartContent.product_id == product_id).delete(synchronize_session=False)



    db_product = get_product(db, product_id=product_id)
    if db_product:
        db.delete(db_product)
        db.commit()
    else:

        db.rollback()
    return None


def get_cart(db: Session, cart_id: int):
    return db.query(models.Cart).filter(models.Cart.id == cart_id).first()

def get_carts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cart).offset(skip).limit(limit).all()

def create_cart(db: Session, cart: schemas.CartCreate):
    db_cart = models.Cart(**cart.model_dump())
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart


def get_cart_content(db: Session, cart_content_id: int):
     return db.query(models.CartContent).filter(models.CartContent.id == cart_content_id).first()

def get_cart_contents(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.CartContent).offset(skip).limit(limit).all()

def get_cart_contents_by_cart_id(db: Session, cart_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.CartContent).filter(models.CartContent.cart_id == cart_id).offset(skip).limit(limit).all()

def create_cart_content(db: Session, cart_content: schemas.CartContentCreate):

    # existing_item = db.query(models.CartContent).filter(
    #     models.CartContent.cart_id == cart_content.cart_id,
    #     models.CartContent.product_id == cart_content.product_id
    # ).first()
    # if existing_item:
    #     existing_item.quantity += cart_content.quantity
    #     db.commit()
    #     db.refresh(existing_item)
    #     return existing_item

    db_cart_content = models.CartContent(**cart_content.model_dump())
    db.add(db_cart_content)
    db.commit()
    db.refresh(db_cart_content)
    return db_cart_content

def get_users_count(db: Session) -> int:
    return db.query(models.User).count()

def get_products_count(db: Session) -> int:
    return db.query(models.Product).count()

def get_brands_count(db: Session) -> int:
    return db.query(models.Brand).count()

def get_countries_count(db: Session) -> int:
    return db.query(models.Country).count()

def get_carts_count(db: Session) -> int:
    return db.query(models.Cart).count()

# Add update and delete functions as needed
