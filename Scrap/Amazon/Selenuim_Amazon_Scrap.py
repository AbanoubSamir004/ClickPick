from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
import json
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium import webdriver
from selenium.webdriver.common.by import By
driver = webdriver.Chrome()

def sign_in(email="pickclick004@gmail.com",password="Clickpick1234#"):
        # enter email and click continue button
        email_field = driver.find_element(by=By.ID, value="ap_email")
        email_field.send_keys(email)
        continue_button = driver.find_element(by=By.ID, value="continue")
        continue_button.click()
        time.sleep(1)

        # enter password and click sign in button
        password_field = driver.find_element(by=By.ID, value="ap_password")
        password_field.send_keys(password)
        sign_in_button = driver.find_element(by=By.ID, value="signInSubmit")
        sign_in_button.click()
        time.sleep(1)

def amazon__page_scraping(urls,categories,sub_categories):
    for url,category,subcatogry in zip(urls,categories,sub_categories):
        driver.get(url)       
        time.sleep(3)
        for page_num in range(1,80):
            # new_url=url+f'&page={page_num}'
            # print(new_url)
            try:
                signin_button=driver.find_element(by=By.CLASS_NAME,value="nav-signin-tt")
                signin_button.click()
                sign_in()
                time.sleep(20)
            except NoSuchElementException:
                pass

            time.sleep(2)
            # Find the main container element
            page_data = driver.find_element(By.CSS_SELECTOR, 'div.s-main-slot.s-result-list.s-search-results.sg-row')
            try:
                # Find all product boxes
                product_boxes = page_data.find_elements(By.CSS_SELECTOR, 'div.sg-col-4-of-24.sg-col-4-of-12.s-result-item.s-asin.sg-col-4-of-16.sg-col.s-widget-spacing-small.sg-col-4-of-20')

                # Iterate over each product box
                for box in product_boxes:
                    # time.sleep(5)
                    # Extract product information
                    product_name = box.find_element(By.CSS_SELECTOR, 'span.a-size-base-plus.a-color-base.a-text-normal').text
                    product_link = box.find_element(By.CSS_SELECTOR, 'a.a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal').get_attribute('href')
                    product_id = box.get_attribute('data-asin')
                    product_image = box.find_element(By.CSS_SELECTOR, 'img.s-image').get_attribute('src')
                    try:
                        product_price = box.find_element(By.CSS_SELECTOR, 'span.a-price-whole').text

                    except:
                        product_price=""
                    try:
                        stars_element = box.find_element(By.CSS_SELECTOR, 'span.a-icon-alt')
                        stars = stars_element.get_attribute('innerHTML').split()[0]  
                    except:
                        stars=""
                    try:
                        rating_count = box.find_element(By.CSS_SELECTOR, 'span.a-size-base.s-underline-text').text
                    except:
                        rating_count=""

                    try:
                        oldprice = box.find_element(By.CSS_SELECTOR, 'span.a-price.a-text-price').text
                        oldprice=oldprice.replace("EGP","")
                    except:
                        oldprice=""
                    product_dic={
                        "Marketplace":"Amazon",
                        "ProductCategory":category,
                        "ProductSubCategory": subcatogry,
                        "ProductTitle":product_name ,
                        "ProductLink": product_link,
                        "ProductID": product_id,
                        "ProductImage": product_image,
                        "ProductPrice":product_price ,
                        "ProductRatings": stars,
                        "ProductRatingCount":rating_count,
                        "ProductOldPrice":oldprice ,
                    }
                    # Write the data to the file
                    with open('Amazon_Products_Dataset.json', 'a',encoding='utf-8') as f:
                        json.dump(product_dic, f,ensure_ascii=False)
                        f.write(',')
                        f.write('\n')
                    json_products.append(product_dic)
                try:
                    time.sleep(2)
                    next_button = driver.find_element(By.CSS_SELECTOR, 'a.s-pagination-next')

                    # Click on the "Next" button
                    next_button.click()
                except:
                    print("No Next Page",url)
                    break
            except:
                print("NO Pages Again in this subcategory ",url)
                break
    # Close the webdriver
    driver.quit()


def get_product_details(product_dic):
    # Initialize Selenium webdriver
    # driver = webdriver.Chrome()  # You can change the webdriver based on your browser choice

    # Iterate over each product in the dictionary
    for product in product_dic:
        # Open the product page
        print(product["ProductID"])
        # Open the product page
        driver.get(product["ProductLink"])
        try:
            signin_button=driver.find_element(by=By.CLASS_NAME,value="nav-signin-tt")
            signin_button.click()
            sign_in()
            time.sleep(20)
        except NoSuchElementException:
            pass
        time.sleep(2)

        # Get SellerName and SellerURL
        try:
            seller_element = driver.find_element(By.ID, "sellerProfileTriggerId")
            product["SellerName"] = seller_element.text
            try:
                product["SellerUrl"] = seller_element.get_attribute("href")
            except:
                product["SellerUrl"]=""
        except:
            product["SellerName"] = ""
            product["SellerUrl"] = ""
        

        # Get ProductBrand
        try:
            brand_row = driver.find_element(By.CSS_SELECTOR, "tr.po-brand")
            brand_name = brand_row.find_element(By.CSS_SELECTOR, "td:nth-child(2) span.a-size-base")
            product["ProductBrand"] = brand_name.text
        except:
            try:
                brand_element = driver.find_element(By.CSS_SELECTOR, "#bylineInfo[href*='/s/ref=bl_dp_s_web_0']")
                product["ProductBrand"] = brand_element.text
            except:
                product["ProductBrand"]=""
        try:
            # Get ProductDescription
            description_element = driver.find_element(By.ID, "productDescription")
            product["ProductDescription"] = description_element.text.strip()
        except:
            product["ProductDescription"] = ""

        flag=0
            # Get ProductSpecifications
        try:
            specifications_table = driver.find_element(By.ID, "productDetails_techSpec_section_1")
            rows = specifications_table.find_elements(By.TAG_NAME, "tr")
            extracted_rows = []
            for row in rows:
                # Find the key and value elements in the row
                key_element = row.find_element(By.TAG_NAME, "th")
                value_element = row.find_element(By.TAG_NAME, "td")

                # Extract the text of the key and value elements
                key = key_element.text.strip()
                value = value_element.text.strip()

                # Append the key-value pair to the list
                extracted_rows.append(f"{key}: {value}")

            product["ProductSpecifications"] = extracted_rows
        except:
            flag=1

        if flag==1:
            try:
                specifications_table =driver.find_element(By.CSS_SELECTOR, "table.a-normal.a-spacing-micro")
                rows = specifications_table.find_elements(By.TAG_NAME, "tr")
                extracted_rows = []
                for row in rows:
                    key_element = row.find_element(By.CSS_SELECTOR, "td.a-span3 span.a-size-base.a-text-bold")
                    value_element = row.find_element(By.CSS_SELECTOR, "td.a-span9 span.a-size-base.po-break-word")
                    key = key_element.text.strip()
                    value = value_element.text.strip()
                    if key and value:
                        extracted_rows.append(f"{key}: {value}")

                product["ProductSpecifications"] = extracted_rows
            except: 
                product["ProductSpecifications"] = []
                
        # Process only one product, remove the break statement if you want to process all products
        with open('Amazon_ALL_Products_Data_Updated.json', 'a',encoding='utf-8') as f:
                json.dump(product, f,ensure_ascii=False)
                f.write(',')
                f.write('\n')
    # Close the webdriver
    driver.quit()

    return product_dic

# Links=[
#     'https://www.amazon.eg/s?i=electronics&rh=n%3A21832883031&s=price-desc-rank&fs=true',
#     'https://www.amazon.eg/s?rh=n%3A21832915031&fs=true&language=en&ref=lp_21832915031_sar',
#     'https://www.amazon.eg/s?rh=n%3A21832907031&fs=true&language=en&ref=lp_21832907031_sar',
#     'https://www.amazon.eg/s?rh=n%3A21832887031&fs=true&language=en&ref=lp_21832887031_sar',

# ]
# categories=["Electronics","Electronics","Electronics","Electronics"]
# sub_categories=['Mobile Phones','Tablets', 'Laptops','Headphones']
json_products=[]
# amazon_data=amazon__page_scraping(Links,categories,sub_categories)

# with open('Amazon_Products_Dataset.json',encoding='utf-8') as f:
#     data = json.load(f)

# new_data=get_product_details(data)

# with open('Amazon_ALL_Products_Data.json', 'w',encoding='utf-8') as f:
#     json.dump(data, f,ensure_ascii=False)

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
def get_product_Specifications(product_dic):
    # Initialize Selenium webdriver
    # driver = webdriver.Chrome()  # You can change the webdriver based on your browser choice

    # Iterate over each product in the dictionary
    for product in product_dic:
        # Open the product page
        if(product['ProductSpecifications']==[]):

            print(product["ProductID"])
            # Open the product page
            driver.get(product["ProductLink"])
            try:
                signin_button=driver.find_element(by=By.CLASS_NAME,value="nav-signin-tt")
                signin_button.click()
                sign_in()
                time.sleep(20)
            except NoSuchElementException:
                pass
            time.sleep(3)

        
            flag=0
            # Get ProductSpecifications
            try:
                specifications_table = driver.find_element(By.ID, "productDetails_techSpec_section_1")
                rows = specifications_table.find_elements(By.TAG_NAME, "tr")
                extracted_rows = []
                for row in rows:
                    # Find the key and value elements in the row
                    key_element = row.find_element(By.TAG_NAME, "th")
                    value_element = row.find_element(By.TAG_NAME, "td")

                    # Extract the text of the key and value elements
                    key = key_element.text.strip()
                    value = value_element.text.strip()

                    # Append the key-value pair to the list
                    extracted_rows.append(f"{key}: {value}")

                product["ProductSpecifications"] = extracted_rows
            except:
                flag=1

            if flag==1:
                try:
                    specifications_table =driver.find_element(By.CSS_SELECTOR, "table.a-normal.a-spacing-micro")
                    rows = specifications_table.find_elements(By.TAG_NAME, "tr")
                    extracted_rows = []
                    for row in rows:
                        key_element = row.find_element(By.CSS_SELECTOR, "td.a-span3 span.a-size-base.a-text-bold")
                        value_element = row.find_element(By.CSS_SELECTOR, "td.a-span9 span.a-size-base.po-break-word")
                        key = key_element.text.strip()
                        value = value_element.text.strip()
                        if key and value:
                            extracted_rows.append(f"{key}: {value}")

                    product["ProductSpecifications"] = extracted_rows
                except: 
                    product["ProductSpecifications"] = []
                    
            # Process only one product, remove the break statement if you want to process all products
            with open('Amazon_ALL_Products_Data_Updated.json', 'a',encoding='utf-8') as f:
                    json.dump(product, f,ensure_ascii=False)
                    f.write(',')
                    f.write('\n')
        else:
            with open('Amazon_ALL_Products_Data_Updated.json', 'a',encoding='utf-8') as f:
                json.dump(product, f,ensure_ascii=False)
                f.write(',')
                f.write('\n')
    # Close the webdriver
    driver.quit()

    return product_dic

# with open('Amazon_ALL_Products_Dataset.json',encoding='utf-8') as f:
#     data = json.load(f)
# get_product_Specifications(data)
# Read the JSON file
# with open('Amazon_ALL_Products_Dataset.json', 'r',encoding='utf-8') as f:
#     data = json.load(f)

# filtered_data = []

# # Iterate over each row
# for row in data:
#     # Check if the "ProductTitle" starts with "2 Year Extended"
#     if not row.get('ProductTitle', '').startswith('2 Year Extened Warranty'):
#         filtered_data.append(row)

# # Save the filtered data to a new JSON file
# with open('Amazon_ALL_Products_Dataset.json', 'w',encoding='utf-8') as f:
#     json.dump(filtered_data, f, indent=4,ensure_ascii=False)
