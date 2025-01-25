import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def get_product_info(url):
    # Set up the Chrome driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(url)

    # Find the product elements
    product_elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-refreshpage="true"]')

    products = []
    for product in product_elements:
        try:
            brand = product.find_element(By.CSS_SELECTOR, 'h3.product-brand').text
            price = product.find_element(By.CSS_SELECTOR, 'span.product-discountedPrice').text
            # Remove 'Rs. ' and convert price to integer for sorting
            price_value = int(price.replace('Rs. ', '').replace(',', ''))
            products.append({'brand': brand, 'price': price_value})
        except Exception as e:
            print(f"An error occurred: {e}")

    driver.quit()
    return products

def write_to_csv(products, filename):
    if not products:
        print("No products found to write to CSV.")
        return

    # Sort products by price (low to high)
    products = sorted(products, key=lambda x: x['price'])

    keys = products[0].keys()
    with open(filename, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(products)
    print(f"Data written to {filename}")

if __name__ == "__main__":
    url = 'https://www.myntra.com/footwear?f=Gender%3Amen%2Cmen%20women&plaEnabled=false&rf=Discount%20Range%3A40.0_100.0_40.0%20TO%20100.0'
    product_info = get_product_info(url)
    if product_info:
        for product in product_info:
            print(f"Brand: {product['brand']}, Price: Rs. {product['price']}")
    
    # Write the product information to a CSV file
    write_to_csv(product_info, 'products.csv')