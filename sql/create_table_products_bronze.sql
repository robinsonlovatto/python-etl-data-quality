CREATE TABLE products_bronze (
    id_product SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    quantity INT NOT NULL,
    price FLOAT NOT NULL,
    category VARCHAR(255) NOT NULL
);