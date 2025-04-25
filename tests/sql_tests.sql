-- =========================================================================
-- TEST SUITE ▸ Ecommerce triggers, constraints & audit log
--              *SAFE‑MODE* VERSION – leaves your real data untouched
-- ---------------------------------------------------------------------------

-- ▶ 1. START WRAPPER TRANSACTION (safe mode) ---------------------------------
BEGIN;                    -- everything below is temporary

-- ▶ 2. RESET SECTION ---------------------------------------------------------
TRUNCATE cart_content, carts, products, brands, countries, users,
         price_history, audit_log
       RESTART IDENTITY CASCADE;


-- ▶ 3. SEED REFERENCE DATA ---------------------------------------------------

-- Countries
INSERT INTO countries (country) VALUES
  ('France'),      -- id = 1
  ('United States'); -- id = 2

-- Brands
INSERT INTO brands (brand, country_id) VALUES
  ('Chanel',       1),
  ('Calvin Klein', 2);

-- Users
INSERT INTO users (username, full_name, sex, mail, birthdate,
                   country, city, street_address, password_hash)
VALUES ('alice', 'Alice Smith', 'F', 'alice@example.com',
        '1990-01-01', 'USA', 'New York', '123 Main St', 'hash');

-- Carts
INSERT INTO carts (user_id, shipped) VALUES (1, false);

-- Products
INSERT INTO products (produrl, perfume, gender, rating_value, rating_count,
                      create_year, top_note, middle_note, base_note, price,
                      brand_id, quantity)
VALUES
  ('https://example.com/bleu', 'Bleu de Chanel', 'men', 4.5, 2000, 2010,
   'citrus', 'cedar', 'sandalwood', 120.00, 1, 100),
  ('https://example.com/ck1',  'CK One',         'unisex', 4.2, 1500, 1994,
   'bergamot', 'green tea', 'musk', 55.00, 2, 50);


-- ▶ 4. HAPPY PATH ▸ add 2 units of product‑1 to cart ------------------------

INSERT INTO cart_content (cart_id, product_id, quantity)
VALUES                   (1,       1,          2);

SELECT 'Product‑1 stock after insert → ' || quantity AS info
FROM   products WHERE product_id = 1;


-- ▶ 5. FAILURE PATH ▸ attempt to over‑sell stock -----------------------------
DO $$
BEGIN
    BEGIN
        INSERT INTO cart_content (cart_id, product_id, quantity)
        VALUES                   (1,       1,          500);  -- exceeds stock
    EXCEPTION WHEN others THEN
        RAISE NOTICE '✅ Oversell blocked as expected → %', SQLERRM;
    END;
END;
$$;


-- ▶ 6. PRICE CHANGE ▸ verify price_history trigger ---------------------------

UPDATE products SET price = 130.00 WHERE product_id = 1;

SELECT 'Logged price history rows → ' || COUNT(*) AS info
FROM   price_history WHERE product_id = 1;

SELECT *
FROM   price_history
WHERE  product_id = 1
ORDER  BY change_date DESC
LIMIT 3;


-- ▶ 7. DELETE CART LINE ▸ stock restoration ---------------------------------

DELETE FROM cart_content WHERE cart_id = 1 AND product_id = 1;

SELECT 'Product‑1 stock after delete → ' || quantity AS info
FROM   products WHERE product_id = 1;


-- ▶ 8. NEGATIVE PRICE ▸ guard‑rail check ------------------------------------
DO $$
BEGIN
    BEGIN
        UPDATE products SET price = -5 WHERE product_id = 2;
    EXCEPTION WHEN others THEN
        RAISE NOTICE '✅ Negative price blocked as expected → %', SQLERRM;
    END;
END;
$$;


-- ▶ 9. BAD GENDER VALUE ▸ check constraint failure --------------------------
DO $$
BEGIN
    BEGIN
        INSERT INTO products (produrl, perfume, gender, price, brand_id, quantity)
        VALUES ('broken', 'Invalid Gender', 'kids', 10, 1, 1);
    EXCEPTION WHEN others THEN
        RAISE NOTICE '✅ Gender constraint blocked as expected → %', SQLERRM;
    END;
END;
$$;


-- ▶ 10. AUDIT LOG INSPECTION -------------------------------------------------
SELECT table_name, operation_type, user_name, event_timestamp
FROM   audit_log ORDER BY id DESC LIMIT 20;


-- ▶ 11. END WRAPPER TRANSACTION ---------------------------------------------
ROLLBACK;    -- ← default: discard everything
-- COMMIT;  -- ← uncomment if you actually want to keep the changes

-- =========================================================================
-- END OF SAFE‑MODE TEST SUITE
-- =========================================================================
