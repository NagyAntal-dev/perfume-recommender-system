-- Add constraints to existing tables
ALTER TABLE products
ADD CONSTRAINT check_price CHECK (price >= 0);

ALTER TABLE cart_content
ADD CONSTRAINT check_quantity CHECK (quantity >= 0);

ALTER TABLE products
ADD CONSTRAINT check_rating_value CHECK (rating_value BETWEEN 0 AND 5);

ALTER TABLE products
ADD CONSTRAINT check_gender CHECK (gender IN ('men', 'women', 'unisex'));

-- Create price_history table (Added to fix "relation does not exist" error)
CREATE TABLE price_history (
    id SERIAL PRIMARY KEY,
    product_id INTEGER NOT NULL,
    old_price DECIMAL(10,2) NOT NULL,
    new_price DECIMAL(10,2) NOT NULL,
    change_date TIMESTAMP NOT NULL,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- Create or replace functions
CREATE OR REPLACE FUNCTION update_product_quantity()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE products
    SET quantity = quantity - NEW.quantity
    WHERE product_id = NEW.product_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION check_product_stock()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT quantity FROM products WHERE product_id = NEW.product_id) < NEW.quantity THEN
        RAISE EXCEPTION 'Not enough stock available for product-id %', NEW.product_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION restore_product_quantity()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE products
    SET quantity = quantity + OLD.quantity
    WHERE product_id = OLD.product_id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION log_price_change()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO price_history (product_id, old_price, new_price, change_date)
    VALUES (OLD.product_id, OLD.price, NEW.price, NOW());
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION validate_product_constraint()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.price <= 0 THEN
        RAISE EXCEPTION 'Price must be greater than 0. Product ID: %', NEW.product_id;
    END IF;
    IF NEW.quantity < 0 THEN
        RAISE EXCEPTION 'Quantity cannot be negative. Product ID: %', NEW.product_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers
CREATE TRIGGER after_insert_cart_content
AFTER INSERT ON cart_content
FOR EACH ROW
EXECUTE FUNCTION update_product_quantity();

CREATE TRIGGER before_insert_cart_content
BEFORE INSERT ON cart_content
FOR EACH ROW
EXECUTE FUNCTION check_product_stock();

CREATE TRIGGER after_delete_cart_content
AFTER DELETE ON cart_content
FOR EACH ROW
EXECUTE FUNCTION restore_product_quantity();

CREATE TRIGGER after_update_price
AFTER UPDATE OF price ON products
FOR EACH ROW
EXECUTE FUNCTION log_price_change();

CREATE TRIGGER before_insert_or_update_product
BEFORE INSERT OR UPDATE ON products
FOR EACH ROW
EXECUTE FUNCTION validate_product_constraint();

-- Create audit table
CREATE TABLE audit_log (
    id SERIAL PRIMARY KEY,
    table_name TEXT NOT NULL,
    operation_type TEXT NOT NULL,
    user_name TEXT NOT NULL,
    event_timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    old_values JSONB,
    new_values JSONB
);

-- Create audit trigger function
CREATE OR REPLACE FUNCTION audit_trigger_function()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO audit_log (
        table_name, operation_type, user_name, event_timestamp, old_values, new_values
    )
    VALUES (
        TG_TABLE_NAME,
        TG_OP,
        CURRENT_USER,
        NOW(),
        to_jsonb(OLD),
        to_jsonb(NEW)
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create audit triggers for specific tables
CREATE TRIGGER audit_users
AFTER INSERT OR UPDATE OR DELETE ON users
FOR EACH ROW
EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_carts
AFTER INSERT OR UPDATE OR DELETE ON carts
FOR EACH ROW
EXECUTE FUNCTION audit_trigger_function();

CREATE TRIGGER audit_products
AFTER INSERT OR UPDATE OR DELETE ON products
FOR EACH ROW
EXECUTE FUNCTION audit_trigger_function();
