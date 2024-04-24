LOAD DATA INFILE '/petlebiproducts.json'
INTO TABLE products
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
(product_name, product_id, product_price, product_category, product_brand, product_barcode, product_description, product_images, product_stock, product_sku);
