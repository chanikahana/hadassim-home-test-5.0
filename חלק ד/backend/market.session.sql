-- יצירת טבלת ספקים
CREATE TABLE suppliers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100),
    phone_number VARCHAR(15),
    representative_name VARCHAR(100)
);

-- יצירת טבלת מוצרים
CREATE TABLE goods (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100),
    price_per_item DECIMAL(10, 2),
    min_quantity INT,
    supplier_id INT,
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);

-- יצירת טבלת הזמנות
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    supplier_id INT,
    status VARCHAR(20) DEFAULT 'Pending',
    FOREIGN KEY (supplier_id) REFERENCES suppliers(id)
);
