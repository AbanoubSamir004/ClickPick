<<<<<<< HEAD
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from selenium.webdriver.chrome.options import Options

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0', 'Accept-Language': 'en-US, en;q=0.5' }

""""
function to scrap each sub category only by passing:
    1- 'category name'
    2- To reach each product block, use a 'category base class name' ('it differs only between each category, not each sub-category').    3-
    3- 'sub category name'
    4- the first page url for each sub category page 

"""
def Amazon_Scrap():
    import json
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

    def scrape_reviews(ids,urls, email, password):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        product_Reviews = []
        # with open('Amazon_Products_reviews.json', 'w', encoding='utf-8') as f:
        #     f.write("[")
        # sign in to Amazon account
        def sign_in():
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

        for asin, url  in zip(ids,urls):
            url = url.split("/dp/")[0]
            url=f"{url}/product-reviews/{asin}/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=1&language=en_AE"
            print("############################################################################# Product Done: ",asin,"#############################################################################")
            # product_Reviews[asin] = []

            # navigate to product reviews page
            driver.get(url)

            try:
                time.sleep(2)
                signin_button=driver.find_element(by=By.CLASS_NAME,value="nav-signin-tt")
                signin_button.click()
                sign_in()
                time.sleep(2)
            except NoSuchElementException:
                pass

            reviews = driver.find_elements(by=By.XPATH, value="//div[@data-hook='review']")
            # check if signed in
            # scrape reviews on current page
            for review in reviews:

                body = review.find_element(by=By.XPATH, value=".//span[@data-hook='review-body']").text

                try:
                    rating = review.find_element(by=By.CSS_SELECTOR, value="i[data-hook='review-star-rating']")
                    rating_value = rating.get_attribute('innerHTML')
                    rating_value = rating_value.split(">")[1].split()[0]
                except:
                    try:
                        rating = review.find_element(by=By.CSS_SELECTOR, value="i[data-hook='cmps-review-star-rating']")
                        rating_value = rating.get_attribute('innerHTML')
                        rating_value = rating_value.split(">")[1].split()[0]
                    except :
                        rating_value = " "

                review_dict = {
                    "ProductID":asin,
                    'review':  body,
                    'rating': rating_value
                }
                product_Reviews.append(review_dict)
                with open('Amazon_Products_reviews.json', 'a', encoding='utf-8') as f:
                    json.dump(review_dict, f,ensure_ascii=False)  
                    f.write(",")
                    f.write("\n")
            # check if there is a next page link
            while True:
                try:
                    try:
                        next_page = driver.find_element(by=By.XPATH, value="//li[@class='a-last']//a")
                    except NoSuchElementException:
                        break

                    # navigate to next page
                    driver.execute_script("arguments[0].click();", next_page)
                    time.sleep(2)

                    # scrape reviews on current page
                    reviews = driver.find_elements(by=By.XPATH, value="//div[@data-hook='review']")
                    try:
                        if driver.find_element(by=By.XPATH, value="//h3[@data-hook='dp-global-reviews-header']"):
                            link_elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-hook="cr-translate-this-review-link"]')
                            # Iterate over the link elements and click each one
                            for link_element in link_elements:
                                time.sleep(1)
                                link_element.click()

                    except NoSuchElementException:
                        pass 
                    for review in reviews:
                        body = review.find_element(by=By.XPATH, value=".//span[@data-hook='review-body']").text

                        try:
                            rating = review.find_element(by=By.CSS_SELECTOR, value="i[data-hook='review-star-rating']")
                            rating_value = rating.get_attribute('innerHTML')
                            rating_value = rating_value.split(">")[1].split()[0]
                        except:
                            try:
                                rating = review.find_element(by=By.CSS_SELECTOR, value="i[data-hook='cmps-review-star-rating']")
                                rating_value = rating.get_attribute('innerHTML')
                                rating_value = rating_value.split(">")[1].split()[0]
                            except:
                                rating_value = " "

                        review_dict = {
                            "ProductID":asin,
                            'review': body,
                            'rating': rating_value
                        }
                        product_Reviews.append(review_dict)
                        with open('Amazon_Products_reviews.json', 'a', encoding='utf-8') as f:
                            json.dump(review_dict, f,ensure_ascii=False)  
                            f.write(",")
                            f.write("\n")
    
                except StaleElementReferenceException:
                    time.sleep(4)
                    driver.refresh()
                    continue
        with open('Amazon_Products_reviews.json', 'a', encoding='utf-8') as f:
            f.write("]")
        driver.quit()
        # except KeyboardInterrupt:
        #     exit()
        return product_Reviews

    def AmazonSellerReviews(names,urls):
        def sign_in2(email="pickclick004@gmail.com", password="Clickpick1234#"):
            # enter email and click continue button
            email_field = driver.find_element(by=By.XPATH, value="//input[@id='ap_email']")
            email_field.send_keys(email)
            continue_button = driver.find_element(by=By.XPATH, value="//span[@id='continue']")
            continue_button.click()
            time.sleep(1)

            # enter password and click sign in button
            password_field = driver.find_element(by=By.ID, value="ap_password")
            password_field.send_keys(password)
            sign_in_button = driver.find_element(by=By.ID, value="signInSubmit")
            sign_in_button.click()
            time.sleep(1)

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        reviews_dic=[]
        # navigate to the seller's review page
        for name,url in zip(names,urls):
            try:
                print("################################## Seller ID: ",name,"#################################")
                driver.get(url)
                try:
                    # time.sleep(100)
                    # time.sleep(100)

                    signin_button=driver.find_element(by=By.XPATH,value="//div[@id='nav-signin-tooltip']//a[@class='nav-action-signin-button']")
                    signin_button.click()
                    sign_in2()
                    time.sleep(20)
                except NoSuchElementException:
                    pass
                try:
                    # wait for the reviews to load
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "feedback-table")))
                except:
                    continue
                # scrape the reviews
                while True:
                    time.sleep(3)
                    # get all the review blocks
                    review_blocks = driver.find_elements(by=By.CSS_SELECTOR, value="#feedback-table .feedback-row")
                    
                    # loop through each review block and extract the rating and review text
                    for review_block in review_blocks:
                        # Extract the content of the tag using BeautifulSoup
                        soup = BeautifulSoup(review_block.get_attribute("outerHTML"), "html.parser")
                        tag_content = soup.select_one(".a-icon-alt").text

                        # Extract the seller rating using regular expressions
                        seller_rating = re.search(r"\d+(\.\d+)?", tag_content).group(0)
                        # rating = review_block.find_element(by=By.XPATH,value='.//div[@class="a-fixed-left-grid-inner"]')
                        # rating = rating.find_element(by=By.XPATH,value='.//span[@class="a-icon-alt"]')
                        review_text = review_block.find_element(by=By.XPATH,value='.//div[@class="a-row a-spacing-small feedback-text"]').text
                        sellerData={
                            "SellerName":name,
                            "review":review_text,
                            "rating":int(seller_rating)
                        }
                        with open('Amazon_Seller_Reviews.json', 'a',encoding='utf-8') as f:
                            json.dump(sellerData, f,ensure_ascii=False)
                            f.write(',')
                            f.write('\n')

                        reviews_dic.append(sellerData)
                    try:
                        if driver.find_element(by=By.XPATH,value='.//span[@data-action="spp-feedback-link-next-page"]/a'):
                            # check if there is a next page button
                            next_button = driver.find_element(by=By.XPATH,value='.//span[@data-action="spp-feedback-link-next-page"]/a')
                            if next_button.text == 'Next':
                                next_button.click()
                                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "feedback-table")))

                            else:
                                break
                    except:
                        print("NO Next Button NavBar")
                        break
                time.sleep(3)
            except:
                print("Error occurring.... ")
                index = names[names == name].index[0]
                new_names=names[index-1:]
                new_urls=urls[index-1:]
                AmazonSellerReviews(new_names,new_urls) 
        # close the webdriver
        driver.quit()
        return reviews_dic

    ############################################################################# Scrap all Products info and details##############################################

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

    # ############################################################################# Scrap all Products Reviews ##############################################
    # with open('Amazon_Products_Dataset_Final.json',encoding='utf-8') as f:
    #     data1 = json.load(f)

    # product_ids = [item['ProductID'] for item in data1]
    # product_links = [item['ProductLink'] for item in data1]

    # prod_rev=scrape_reviews(product_ids[1079:],product_links[1079:],"pickclick004@gmail.com","Clickpick1234#")

    # with open('Amazon_Products_reviews2.json', 'w', encoding='utf-8') as f:
    #     json.dump(prod_rev, f,ensure_ascii=False)  
    # with open('Amazon_Products_reviews.json',encoding='utf-8') as f:
    #     data1 = json.load(f)
    # for row in data1:
    # # Access the value of the "rating" key
    #     rating_value = row['rating']
        
    #     # Convert the string value to an integer
    #     rating_int = int(float(rating_value))
        
    #     # Update the value of the "rating" key with the new integer value
    #     row['rating'] = rating_int
    
    # with open('Amazon_Products_reviews.json', 'w', encoding='utf-8') as f:
    #     json.dump(data1, f,ensure_ascii=False)  
    # ############################################################################ Scrap all Seller Reviews ########################################################


    # import json
    # with open('unique_seller_ids_urls.json', 'r',encoding='utf-8') as f:
    #    unique_seller=json.load(f)
    # with open('Amazon_Seller_Reviews.json', 'r',encoding='utf-8') as f:
    #     sellers=json.load(f)

    # seller_names1 = {row['SellerName'] for row in unique_seller}
    # seller_names2 = {row['SellerName'] for row in sellers}
    # missing_seller_names = seller_names1 - seller_names2
    # missing_sellers = []

    # for row in unique_seller:
    #     if row['SellerName'] in missing_seller_names:
    #         missing_sellers.append(row)

  
    # names_list=[]
    # url_list=[]

    # for seller in missing_sellers:
    #     names_list.append(seller['SellerName'])
    #     url_list .append(seller['SellerUrl'])
            
    # df=pd.DataFrame()
    # df['SellerName']=names_list
    # df['SellerUrl']=url_list
    # df.reset_index(drop=True,inplace=True)
    # df=df[df.SellerName!=""]
    # df=df[df.SellerUrl!=""]

    # # json_data = df.to_dict(orient='records')
    # # # Save the JSON object to a file
    # # with open('unique_seller_ids_urls.json', 'w',encoding='utf-8') as f:
    # #     json.dump(json_data, f,ensure_ascii=False)

    # # with open('Amazon_Seller_Reviews.json', 'a',encoding='utf-8') as f:
    # #     f.write('[')
    # seller_rev=AmazonSellerReviews(df['SellerName'],df['SellerUrl'])
    # with open('Amazon_Seller_Reviews.json', 'a',encoding='utf-8') as f:
    #     f.write(']')


    # with open('Amazon_Seller_Reviews_Final.json', 'w',encoding='utf-8') as f:
    #             json.dump(seller_rev, f,ensure_ascii=False)

    # ############################################################ Data Mergeing Final ########################################################
    # import json

    # Step 1: Read the main JSON file
    with open('Amazon_Products_Dataset_Final.json',encoding='utf-8') as file:
        main_data = json.load(file)

    # Step 2: Read the reviews JSON file
    with open('Amazon_Products_Reviews_Final.json',encoding='utf-8') as file:
        reviews_data = json.load(file)

    # Step 3: Group the reviews based on product ID
    grouped_reviews = {}
    for review in reviews_data:
        product_id = review['ProductID']
        review_data = {
            'review': review['review'],
            'rating': review['rating']
        }
        if product_id in grouped_reviews:
            grouped_reviews[product_id].append(review_data)
        else:
            grouped_reviews[product_id] = [review_data]

    # # Step 5: Add the grouped reviews to the main data
    # for product in main_data:
    #     product_id = product['ProductID']
    #     if product_id in grouped_reviews:
    #         product['ProductReviews'] = grouped_reviews[product_id]
    #     else:
    #         product['ProductReviews'] = []

    # # Step 6: Write the updated data to a new JSON file
    # with open('Amazon_Products_Dataset_Final_with_Reveiws.json', 'w',encoding='utf-8') as file:
    #     json.dump(main_data, file, indent=4,ensure_ascii=False)


    # # Step 1: Read the main JSON file
    # with open('Amazon_Products_Dataset_Final_with_Reveiws.json',encoding='utf-8') as file:
    #     main_data = json.load(file)

    # # Step 2: Read the reviews JSON file
    # with open('Amazon_Seller_Reviews_Final.json',encoding='utf-8') as file:
    #     reviews_data = json.load(file)

    # # Step 3: Group the reviews based on product ID
    # grouped_reviews = {}
    # for review in reviews_data:
    #     product_id = review['SellerID']
    #     review_data = {
    #         'review': review['review'],
    #         'rating': review['rating']
    #     }
    #     if product_id in grouped_reviews:
    #         grouped_reviews[product_id].append(review_data)
    #     else:
    #         grouped_reviews[product_id] = [review_data]

    # # Step 5: Add the grouped reviews to the main data
    # for product in main_data:
    #     product_id = product['SellerID']
    #     if product_id in grouped_reviews:
    #         product['SellerReviews'] = grouped_reviews[product_id]
    #     else:
    #         product['SellerReviews'] = []

    # # Step 6: Write the updated data to a new JSON file
    # with open('Amazon_Dataset_Final.json', 'w',encoding='utf-8') as file:
    #     json.dump(main_data, file, indent=4,ensure_ascii=False)


    return True



Amazon_Scrap()          

=======
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0', 'Accept-Language': 'en-US, en;q=0.5' }

""""
function to scrap each sub category only by passing:
    1- 'category name'
    2- To reach each product block, use a 'category base class name' ('it differs only between each category, not each sub-category').    3-
    3- 'sub category name'
    4- the first page url for each sub category page 

"""
def Amazon_Scrap():
    def amazon__detals_scraping(urls,categories,sub_categories,page_numbers=80):
        
        json_products=[]
        try: 
            def get_about_item(item_url):
                page_count2=0 
                price=""
                percentage=""
                while True:
                    #make a request to the sub category page
                    response = requests.get(item_url,headers=headers)
                    soup = BeautifulSoup(response.content, 'lxml')
            
                    #get product category and sub_categoy name
                    if(soup.find("ul",{'class':'a-unordered-list a-horizontal a-size-small'})):   
                        print("product found successfully")

                        #get product category name
                        cat=soup.find("ul",{'class':'a-unordered-list a-horizontal a-size-small'})
                        get_cat=cat.find_all(class_='a-link-normal a-color-tertiary')
                        product_category=get_cat[0].text.strip()

                        #get product sub category name
                        product_sub_category=get_cat[len(get_cat)-1].text.strip()
                        break
                    if(page_count2==5):
                        print("can't load any product pages again.")
                        break
                    else: 
                        page_count2+=1
                        print("product page not found")
                        time.sleep(2)
                        pass
                    
                #get sales price and offere percentage    
                sales_block=soup.find("div",{'id':'corePriceDisplay_desktop_feature_div'})

                try:
                    if sales_block.find("div",{'class':'a-section a-spacing-none aok-align-center'}):
                        sales=sales_block.find("div",{'class':'a-section a-spacing-none aok-align-center'})
                        if sales.find("span",{'class':'a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage'}):
                            percentage=soup.find("span",{'class':'a-size-large a-color-price savingPriceOverride aok-align-center reinventPriceSavingsPercentageMargin savingsPercentage'}).text

                            old_price_block=sales_block.find("div",{'class':'a-section a-spacing-small aok-align-center'})
                            old_price=old_price_block.find("span",{'class':'a-size-small a-color-secondary aok-align-center basisPrice'})
                            price=old_price.find(class_='a-offscreen').text
                    else:
                        print("Sales Block Not Found")
                except AttributeError:  
                    print("Error occurred on Sales Block")

                
                # check it this block is found in the product page
                if soup.find("div",{'class':'a-section a-spacing-medium a-spacing-top-small'}):
                    #get all text list 
                    about_item_ul=soup.find("div",{'class':'a-section a-spacing-medium a-spacing-top-small'}).find('ul')
                    about_item_string=[]
                    
                    try:
                        if about_item_ul.find_all('li'):

                            for li in about_item_ul.find_all('li'):
                                if '\n' not in li.text:
                                    about_item_string.append(li.text)

                            about_item_data=about_item_string

                    except Exception:
                        about_item_data=[]
                        return soup,price,percentage,about_item_data
                # else so add it empty
                else:
                    about_item_data=[]

                return soup,price,percentage,about_item_data

                    
            def get_product_details(soup):

                # check it this block is found in the product page
                if soup.find("table",{'class':'a-normal a-spacing-micro'}):
                    
                    #get the product table details
                    product_details=soup.find("table",{'class':'a-normal a-spacing-micro'})
                    product_details=product_details.find_all(class_='a-size-base')

                    #get each row in table
                    poduct_details_l=[]
                    for items in range(0,len(product_details),2):
                        poduct_details_l.append((product_details[items].text,product_details[items+1].text))

                    poduct_details_list=poduct_details_l         
                # else so add it empty
                else:
                    poduct_details_list=[]
                
                return poduct_details_list
                    
            def get_next_page(url):
                
                #loop to get the next sub_category page
                while True:
                    response = requests.get(url,headers=headers)
                    soup = BeautifulSoup(response.content, 'lxml')
                    #get the next page link
                    pages = soup.find('span', {'class': 's-pagination-strip'})
                    
                    # if request not block us
                    if(pages!=None):
                        
                        #if it is not the last page 
                        if not pages.find('span', {'class': 's-pagination-item s-pagination-next s-pagination-disabled'}):
                            url = "https://www.amazon.eg"+str(pages.find('a', {'class': 's-pagination-item s-pagination-next s-pagination-button s-pagination-separator'}).get('href'))
                            break
                            
                        else:
                            #if false so it is the last page and change flage to false to stop the main loop
                            flag=False
                            break
                return url


            for url,category,sub_category in zip(urls,categories,sub_categories):
            
                flag=True
                current_page=0
                while flag==True:
                    if current_page==page_numbers:
                        break
                    current_page+=1
                    print("subcategory page: ",current_page)
                    
                    page_count1=0
                    while True:
                        #make a request to the sub category page
                        response = requests.get(url,headers=headers)
                        soup = BeautifulSoup(response.content, 'lxml')
                        products=[]
                        #get all products block details
                        if(soup.find_all('div',{'class':"a-section a-spacing-base"})):
                            products=soup.find_all('div',{'class':"a-section a-spacing-base"})
                        else: 
                            if(soup.find_all('div',{'class':"a-section a-spacing-base a-text-center"})):
                                products=soup.find_all('div',{'class':'a-section a-spacing-base a-text-center'})
                                
                        if(page_count1==5):
                            print("can't load any pages again.")
            
                        if len(products)==0:
                            page_count1+=1
                            print("Page Not Found")
                            time.sleep(0.5)
                            pass
                        else:
                            break
                    print("Page Found successfully")
                    for i in range(0,len(products)):
                        product_image=""
                        product_name=""
                        product_link=""
                        product_id=""
                        product_price=""
                        stars=""
                        rating_count=""
                        product_seller=""

                        if products[i].find(class_='a-offscreen') != None:
                            #get product image
                            product_image=products[i].find(class_='s-image').attrs['src']

                            #get product name
                            product_name=products[i].find(class_='a-size-base-plus a-color-base a-text-normal').text

                            #get product link
                            item_url= 'https://www.amazon.eg' +products[i].find(class_='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal').attrs['href']
                            product_link=item_url
                            
                            #get asin number from each product link
                            asin=item_url
                            try:
                                asin=asin.split('/dp/')
                                asin=asin[1].split('/',1)
                                asin=asin[0]
                            except IndexError:
                                asin=asin.split('dp%2F')
                                asin=asin[1].split('%2F',1)
                                asin=asin[0]
                            product_id=asin

                            #get product price
                            x=products[i].find(class_='a-offscreen').text.split()
                            product_price=x[0]+" "+x[1]
                            

                            try:
                                #get ratings and ratings count
                                r=products[i].find(class_='a-row a-size-small')
                                stars=r.find('span', attrs={'class': 'a-size-base'}).text
                                rating_count=r.find('span', attrs={'class': 'a-size-base s-underline-text'}).text
                                
                            except AttributeError:
                                print("dont Found Ratings for this product: ",item_url)

                            soup,oldprice,percentage,about_item_data=get_about_item(item_url)

                            try:
                                brand_name="Null"
                                # find all div elements with class "a-section a-spacing-none" that contain an anchor element with id "bylineInfo"
                                divs = soup.find_all('div', {'class': 'a-section a-spacing-none'})
                                for div in divs:
                                    try:
                                        anchor = div.find('a', {'id': 'bylineInfo'})
                                        if anchor is not None:
                                            brand_name = anchor.text.split(': ')[-1]
                                            break
                                    except:
                                        pass

                                if brand_name=="Null":
                                    print('True')
                                    # if no such div elements are found, find all table elements with class "a-normal a-spacing-micro"
                                    tables = soup.find_all('table', {'class': 'a-normal a-spacing-micro'})
                                    for table in tables:
                                        try:
                                            rows = table.find_all('tr', {'class': 'a-spacing-small po-brand'})
                                            for row in rows:
                                                span = row.find('span', {'class': 'a-size-base po-break-word'})
                                                if span is not None:
                                                    brand_name = span.text
                                                    print(brand_name)
                                                    break
                                        except:
                                            pass
                                if brand_name=="Null":
                                    # if no such table elements are found, find all div elements with class "a-section a-spacing-small a-spacing-top-small"
                                    divs = soup.find_all('div', {'class': 'a-section a-spacing-small a-spacing-top-small'})
                                    for div in divs:
                                        try:
                                            table = div.find('table', {'class': 'a-normal a-spacing-micro'})
                                            row = table.find('tr', {'class': 'a-spacing-small po-brand'})
                                            span = row.find('span', {'class': 'a-size-base po-break-word'})
                                            brand_name = span.text
                                            print(brand_name)
                                            break
                                        except:
                                            pass
                                brand_name = brand_name.replace('Visit the ', '')

                            except:
                                brand_name=" "
                                pass
                            try:
                                #get product seller
                                if soup.find("div",{'class':'tabular-buybox-text','tabular-attribute-name':'يباع من'}):
                                    seller=soup.find("div",{'class':'tabular-buybox-text','tabular-attribute-name':'يباع من'})
                                else:
                                    seller=soup.find("div",{'class':'tabular-buybox-text','tabular-attribute-name':'Sold by'})
                                try:
                                    if seller.find("span",{"class":"a-size-small tabular-buybox-text-message"}).find('a'):
                                        seller_url="https://www.amazon.eg"+seller.find("span",{"class":"a-size-small tabular-buybox-text-message"}).find('a').attrs['href']
                                except AttributeError:
                                    seller_url=" "          
                                    print("Dont Found Seller URl")
                                    
                                product_seller=seller.text.strip()
                            except AttributeError:
                                product_seller=" "
                                print("Dont Found Seller Name")

                            #get product details
                            poduct_details_list=get_product_details(soup)

                            product_dic={
                                "ProductCategory":category,
                                "ProductSubCategory": sub_category,
                                "ProducTitle":product_name ,
                                "ProductLink": product_link,
                                "ProductID": product_id,
                                "ProductImage": product_image,
                                "ProductPrice":product_price ,
                                "ProductRatings": stars,
                                "ProductRatingCount":rating_count,
                                "ProductOldPrice":oldprice ,
                                "ProductOffer":percentage ,
                                "SellerName":product_seller ,
                                "SellerUrl":seller_url,
                                "ProductBrand": brand_name,
                                "Product_description": about_item_data,
                                "Product_specifications":poduct_details_list
                            }
                            # Write the data to the file
                            with open('Amazon_Products_Dataset.json', 'a',encoding='utf-8') as f:
                                json.dump(product_dic, f,ensure_ascii=False)
                                f.write(',')
                                f.write('\n')
                            json_products.append(product_dic)
                    # get the next sub_category page
                    url=get_next_page(url)
                
            return json_products
        
        except:
            print("An error occurred while scraping the website.....")
            exit()
        

    def scrape_reviews(ids,urls, email, password):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        product_Reviews = []
        # with open('Amazon_Products_reviews.json', 'w', encoding='utf-8') as f:
        #     f.write("[")
    # sign in to Amazon account
        def sign_in():
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

        for asin, url  in zip(ids,urls):
            url = url.split("/dp/")[0]
            url=f"{url}/product-reviews/{asin}/ref=cm_cr_arp_d_paging_btm_next_2?ie=UTF8&reviewerType=all_reviews&pageNumber=1&language=en_AE"
            print("############################################################################# Product Done: ",asin,"#############################################################################")
            # product_Reviews[asin] = []

            # navigate to product reviews page
            driver.get(url)

            try:
                time.sleep(2)
                signin_button=driver.find_element(by=By.CLASS_NAME,value="nav-signin-tt")
                signin_button.click()
                sign_in()
                time.sleep(2)
            except NoSuchElementException:
                pass
            reviews = driver.find_elements(by=By.XPATH, value="//div[@data-hook='review']")
            # check if signed in
            # scrape reviews on current page
            for review in reviews:
                try:
                    if review.find_element(by=By.XPATH, value=".//a[@data-hook='review-title']/span"):
                        title = review.find_element(by=By.XPATH, value=".//a[@data-hook='review-title']/span").text
                    else:
                        title = " "

                except NoSuchElementException:
                    title = " "

                body = review.find_element(by=By.XPATH, value=".//span[@data-hook='review-body']").text

                try:
                    if review.find_element(by=By.CSS_SELECTOR, value="i[data-hook='review-star-rating']"):
                        rating = review.find_element(by=By.CSS_SELECTOR, value="i[data-hook='review-star-rating']")
                        rating_value = rating.get_attribute('innerHTML')
                        rating_value = rating_value.split(">")[1].split()[0]
                    else:
                        rating_value = " "

                except NoSuchElementException:
                    rating_value = " "


                review_dict = {
                    "ProductID":asin,
                    'review': title + " , " + body,
                    'rating': rating_value
                }
                product_Reviews.append(review_dict)
                with open('Amazon_Products_reviews.json', 'a', encoding='utf-8') as f:
                    json.dump(review_dict, f,ensure_ascii=False)  
                    f.write(",")
                    f.write("\n")
            # check if there is a next page link
            while True:
                try:
                    try:
                        next_page = driver.find_element(by=By.XPATH, value="//li[@class='a-last']//a")
                    except NoSuchElementException:
                        break

                    # navigate to next page
                    driver.execute_script("arguments[0].click();", next_page)
                    time.sleep(2)

                    # scrape reviews on current page
                    reviews = driver.find_elements(by=By.XPATH, value="//div[@data-hook='review']")
                    try:
                        if driver.find_element(by=By.XPATH, value="//h3[@data-hook='dp-global-reviews-header']"):
                            break
                    except NoSuchElementException:
                        pass 
                    for review in reviews:
                        try:
                            if review.find_element(by=By.XPATH, value=".//a[@data-hook='review-title']/span"):
                                title = review.find_element(by=By.XPATH, value=".//a[@data-hook='review-title']/span").text
                            else:
                                title = " "

                        except NoSuchElementException:
                            title = " "

                        body = review.find_element(by=By.XPATH, value=".//span[@data-hook='review-body']").text

                        try:
                            if review.find_element(by=By.CSS_SELECTOR, value="i[data-hook='review-star-rating']"):
                                rating = review.find_element(by=By.CSS_SELECTOR, value="i[data-hook='review-star-rating']")
                                rating_value = rating.get_attribute('innerHTML')
                                rating_value = rating_value.split(">")[1].split()[0]

                            else:
                                rating_value = " "

                        except NoSuchElementException:
                            rating_value = " "

                        review_dict = {
                            "ProductID":asin,
                            'review': title + " , " + body,
                            'rating': rating_value
                        }
                        product_Reviews.append(review_dict)
                        with open('Amazon_Products_reviews.json', 'a', encoding='utf-8') as f:
                            json.dump(review_dict, f,ensure_ascii=False)  
                            f.write(",")
                            f.write("\n")
    
                except StaleElementReferenceException:
                    time.sleep(4)
                    driver.refresh()
                    continue
        with open('Amazon_Products_reviews.json', 'a', encoding='utf-8') as f:
            f.write("]")
        driver.quit()
        # except KeyboardInterrupt:
        #     exit()
        return product_Reviews
    def AmazonSellerReviews(ids,urls):

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        reviews_dic=[]
        # navigate to the seller's review page
        for id,url in zip(ids,urls):
            print("################################## Seller ID: ",id,"#################################")
            driver.get(url)

            # wait for the reviews to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "feedback-table")))

            # scrape the reviews
            while True:
                time.sleep(3)
                # get all the review blocks
                review_blocks = driver.find_elements(by=By.CSS_SELECTOR, value="#feedback-table .feedback-row")
                
                # loop through each review block and extract the rating and review text
                for review_block in review_blocks:
                    # Extract the content of the tag using BeautifulSoup
                    soup = BeautifulSoup(review_block.get_attribute("outerHTML"), "html.parser")
                    tag_content = soup.select_one(".a-icon-alt").text

                    # Extract the seller rating using regular expressions
                    seller_rating = re.search(r"\d+(\.\d+)?", tag_content).group(0)
                    # rating = review_block.find_element(by=By.XPATH,value='.//div[@class="a-fixed-left-grid-inner"]')
                    # rating = rating.find_element(by=By.XPATH,value='.//span[@class="a-icon-alt"]')
                    review_text = review_block.find_element(by=By.XPATH,value='.//div[@class="a-row a-spacing-small feedback-text"]').text
                    sellerData={
                        "SellerID":id,
                        "review":review_text,
                        "rating":int(seller_rating)
                    }
                    with open('Amazon_Seller_Reviews.json', 'a',encoding='utf-8') as f:
                        json.dump(sellerData, f,ensure_ascii=False)
                        f.write(',')
                        f.write('\n')

                    reviews_dic.append(sellerData)
                try:
                    if driver.find_element(by=By.XPATH,value='.//span[@data-action="spp-feedback-link-next-page"]/a'):
                        # check if there is a next page button
                        next_button = driver.find_element(by=By.XPATH,value='.//span[@data-action="spp-feedback-link-next-page"]/a')
                        if next_button.text == 'Next':
                            next_button.click()
                            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "feedback-table")))

                        else:
                            break
                except:
                    print("NO Next Button NavBar")
                    break
            time.sleep(3)
        # close the webdriver
        driver.quit()
        return reviews_dic

    ############################################################################# Scrap all Products info and details##############################################
    # mobile devices & computers & men & women 
    Links=["https://www.amazon.eg/s?rh=n%3A21832868031&fs=true&language=en&ref=lp_21832868031_sar",
                "https://www.amazon.eg/s?rh=n%3A21832872031&fs=true&language=en&ref=lp_21832872031_sar",
                "https://www.amazon.eg/s?rh=n%3A21845147031&fs=true&language=en&ref=lp_21845147031_sar",
                "https://www.amazon.eg/s?rh=n%3A21845145031&fs=true&language=en&ref=lp_21845145031_sar",
    ]
    categories=["Electronics","Electronics","Fashion","Fashion"]
    sub_categories=['Mobile Phones & Communication','Computers, Components & Accessories',"Men","Woman"]
    amazon_data=amazon__detals_scraping(Links,categories,sub_categories,page_numbers=80)

    with open('Amazon_Products_Dataset_Final.json', 'w',encoding='utf-8') as f:
        json.dump(amazon_data, f,ensure_ascii=False)  

    with open('Amazon_Products_Dataset_Final.json', 'r',encoding='utf-8') as f:
        data = json.load(f)

    for row in data:
        seller_url = row["SellerUrl"]
        if seller_url!= " ":
            # print(seller_url)
            seller_id = seller_url.split("&seller=")[1].split("&")[0]
            row["SellerID"] = seller_id
        else:
            row["SellerUrl"]=""
            row["SellerID"] = ""

    with open('Amazon_Products_Dataset_Final.json', 'w',encoding='utf-8') as f:
        json.dump(data, f,ensure_ascii=False)

    ############################################################################# Scrap all Products Reviews ##############################################
    with open('Amazon_Products_Dataset_Final.json') as file:
        data1 = json.load(file)

    product_ids = [item['ProductID'] for item in data1]
    product_links = [item['ProductLink'] for item in data1]

    prod_rev=scrape_reviews(product_ids,product_links,"scraper004@gmail.com","20190001Scraper#")

    with open('Amazon_Products_reviews2.json', 'w', encoding='utf-8') as f:
        json.dump(prod_rev, f,ensure_ascii=False)  

    ############################################################################ Scrap all Seller Reviews ########################################################


    import json
    with open('Amazon_Products_Dataset_Final.json', 'r',encoding='utf-8') as f:
            data = json.load(f)

    unique_seller_urls = []
    unique_seller_ids = []

    # iterate through each row in the data
    for row in data:
        # extract the seller URL and ID from the row
        seller_url = row['SellerUrl']
        seller_id = row['SellerID']
        
        # check if the seller URL has already been added to the list
        if seller_id not in unique_seller_ids:
            # if the seller URL is not in the list, add it to the list
            unique_seller_urls.append(seller_url)
            
            # add the corresponding seller ID to the IDs list
            unique_seller_ids.append(seller_id)
            
    df=pd.DataFrame()
    df['SellerID']=unique_seller_ids
    df['SellerUrl']=unique_seller_urls
    df.reset_index(drop=True,inplace=True)
    df=df[df.SellerID!=""]
    df=df[df.SellerUrl!=""]

    # json_data = df.to_dict(orient='records')
    # # Save the JSON object to a file
    # with open('unique_seller_ids_urls.json', 'w',encoding='utf-8') as f:
    #     json.dump(json_data, f,ensure_ascii=False)

    with open('Amazon_Seller_Reviews.json', 'a',encoding='utf-8') as f:
        f.write('[')
    seller_rev=AmazonSellerReviews(df['SellerID'][10:],df['SellerUrl'][10:])
    with open('Amazon_Seller_Reviews.json', 'a',encoding='utf-8') as f:
        f.write(']')


    with open('Amazon_Seller_Reviews_Final.json', 'w',encoding='utf-8') as f:
                json.dump(seller_rev, f,ensure_ascii=False)
    
    return True

Amazon_Scrap()          
>>>>>>> 258993e1470e0b47fb4ac91d228c68a0c2c3ef21
