\set ON_ERROR_STOP on

\echo 'Loading countries...'
\copy countries(country, country_id) FROM '/docker-entrypoint-initdb.d/countries.csv' WITH (FORMAT csv, HEADER true, DELIMITER ';')

\echo 'Loading brands...'
\copy brands(brand, country_id) FROM '/docker-entrypoint-initdb.d/brands.csv' WITH (FORMAT csv, HEADER true, DELIMITER ';')

\echo 'Loading products...'
\copy products(produrl, perfume, gender, rating_value, rating_count, create_year, top_note, middle_note, base_note, price, brand_id, quantity) FROM '/docker-entrypoint-initdb.d/products.csv' WITH (FORMAT csv, HEADER true, DELIMITER ';')

\echo 'Loading users...'
\copy users(username, full_name, sex, mail, birthdate, country, city, street_address, password_hash) FROM '/docker-entrypoint-initdb.d/users.csv' WITH (FORMAT csv, HEADER true, DELIMITER ';')

\echo 'Loading carts...'
\copy carts(user_id, shipped) FROM '/docker-entrypoint-initdb.d/carts.csv' WITH (FORMAT csv, HEADER true, DELIMITER ';')

\echo 'Loading cart_content...'
\copy cart_content(cart_id, product_id, quantity) FROM '/docker-entrypoint-initdb.d/cart_content.csv' WITH (FORMAT csv, HEADER true, DELIMITER ';')
