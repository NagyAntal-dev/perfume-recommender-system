BEGIN;

-- Drop existing tables if re‑initializing
DROP TABLE IF EXISTS cart_content CASCADE;
DROP TABLE IF EXISTS carts CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS brands CASCADE;
DROP TABLE IF EXISTS countries CASCADE;

-- 1) countries lookup
CREATE TABLE countries (
  country_id   SERIAL PRIMARY KEY,
  country      VARCHAR(255) NOT NULL UNIQUE
);

-- 2) brands lookup
CREATE TABLE brands (
  brand_id     SERIAL PRIMARY KEY,
  brand        VARCHAR(255),
  country_id   INTEGER NOT NULL
                REFERENCES countries(country_id)
);

-- 3) users
CREATE TABLE users (
  user_id      SERIAL PRIMARY KEY,
  username     VARCHAR(100)   NOT NULL UNIQUE,
  full_name         VARCHAR(255),
  sex          VARCHAR(10),
  mail         VARCHAR(255),
  birthdate    DATE,
  country      VARCHAR(255),
  city         VARCHAR(255),
  street_address       VARCHAR(255),
  password_hash     VARCHAR(255)
);

-- 4) products
CREATE TABLE products (
  product_id    SERIAL PRIMARY KEY,
  produrl           VARCHAR(2048) NOT NULL,
  perfume       VARCHAR(255),
  gender        VARCHAR(50),
  rating_value  DECIMAL(5,2),
  rating_count  DECIMAL(10,0),
  create_year          INTEGER,
  top_note           VARCHAR(4000),
  middle_note        VARCHAR(4000),
  base_note          VARCHAR(4000),
  price         DECIMAL(10,2),
  country_id    INTEGER NOT NULL
                REFERENCES countries(country_id),
  brand_id      INTEGER NOT NULL
                REFERENCES brands(brand_id)
);

-- 5) carts
CREATE TABLE carts (
  cart_id      SERIAL PRIMARY KEY,
  user_id      INTEGER NOT NULL
                REFERENCES users(user_id),
  shipped      BOOLEAN
);

-- 6) cart contents
CREATE TABLE cart_content (
  cart_content_id  SERIAL PRIMARY KEY,
  cart_id          INTEGER NOT NULL
                   REFERENCES carts(cart_id),
  product_id       INTEGER NOT NULL
                   REFERENCES products(product_id),
  quantity         INTEGER
);

COMMIT;