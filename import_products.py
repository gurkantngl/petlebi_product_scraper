import json
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="gtongel553",
    database="petlebi_products"
)

mycursor = mydb.cursor()

# Tablo oluştur
mycursor.execute("CREATE TABLE IF NOT EXISTS petlebi_create (product_name VARCHAR(255), product_id INT, product_price VARCHAR(255), product_category VARCHAR(255), product_brand VARCHAR(255), product_barcode VARCHAR(255), product_description TEXT, product_images TEXT, product_stock INT, product_sku TEXT)")

# JSON dosyasını oku
with open('petlebi_products.json', 'r') as file:
    data = json.load(file)

# JSON verilerini MySQL tablosuna ekle
for product in data:
    product_name = product.get('product_name')
    product_id = product.get('product_id')
    product_price = product.get('product_price')
    product_category = product.get('product_category')
    product_brand = product.get('product_brand')
    product_barcode = product.get('product_barcode')
    product_description = product.get('product_description')
    product_images = ','.join(product.get('product_images', []))
    product_stock = product.get('product_stock')
    product_sku = None
    
    print(type(product_images))

    sql = "INSERT INTO petlebi_create (product_name, product_id, product_price, product_category, product_brand, product_barcode, product_description, product_images, product_stock, product_sku) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (product_name, product_id, product_price, product_category, product_brand, product_barcode, product_description, product_images, product_stock, product_sku)
    mycursor.execute(sql, val)

mydb.commit()
print(mycursor.rowcount, "records inserted.")