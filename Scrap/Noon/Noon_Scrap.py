from bs4 import BeautifulSoup
import pandas as pd
import json
from selenium import webdriver
import time
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException,NoSuchWindowException,StaleElementReferenceException,ElementClickInterceptedException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium import webdriver

headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0', 'Accept-Language': 'en-US, en;q=0.5' }


def Noon_Scrap():

    products_data=[]

    def noon_Marketplace_Data(links):

        # options = webdriver.ChromeOptions()
        # options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome()
        
        for link in links:
            url = link['url']
            category = link['category']
            subcategory = link['subcategory']
            driver.get(url)
            time.sleep(2)
            print("################################################### New Category #######################################################################")


            pages_count=0
            next_page_available = True
            while next_page_available:
                pages_count+=1
                if pages_count==31:
                    break
                time.sleep(4)
                print("#################### page number: ",pages_count,"####################")
                # Get the page source and create the BeautifulSoup object

                # Find all product containers
                products_container = driver.find_element(By.CLASS_NAME, "sc-794c6902-7")

                # Find all the product elements within the container
                product_elements = products_container.find_elements(By.CLASS_NAME, "sc-5e739f1b-0")

                # Iterate over each product element and extract the desired data
                for product_element in product_elements:
                    try:
                        ProductRatings = product_element.find_element(By.CLASS_NAME, "sc-e568c3b8-1").text
                    except:
                        ProductRatings = ""
                    try:   
                        ProductRatingCount = product_element.find_element(By.CLASS_NAME, "sc-61515602-2").text
                    except:
                        ProductRatingCount = ""
                    try:
                        ProductOldPrice = product_element.find_element(By.CSS_SELECTOR, "div.sc-6073040e-2.iTAgLM span.oldPrice").text
                    except:
                        ProductOldPrice = ""
                    product_data = {
                        "ProductCategory": category,
                        "ProductSubCategory": subcategory,
                        "ProductTitle": product_element.find_element(By.CLASS_NAME, "sc-ea72a08b-20").text,
                        "ProductLink": product_element.find_element(By.TAG_NAME, "a").get_attribute("href"),
                        "ProductID": product_element.find_element(By.TAG_NAME, "a").get_attribute("id").replace("productBox-", ""),
                        "ProductPrice": product_element.find_element(By.CLASS_NAME, "amount").text,
                        "ProductRatings": ProductRatings,
                        "ProductRatingCount": ProductRatingCount,
                        "ProductOldPrice": ProductOldPrice,
                    }

                    products_data.append(product_data)

                    # Write the data to the file
                    with open('noon_pages_data_new.json', 'a') as f:
                        json.dump(product_data, f)
                        f.write(',')
                        f.write('\n')

                # Check if there is a "Next" button
                try:
                    next_button = driver.find_element(by=By.CSS_SELECTOR,value= 'li.next > a.arrowLink')
                    driver.execute_script("arguments[0].scrollIntoView();", next_button)  # Scroll to the button
                    time.sleep(1)
                    next_button.click()
                    time.sleep(2)
                except:
                    next_page_available = False

        driver.quit()
        return products_data




    def get_seller_code(links):
        # Set up the Selenium driver
        driver = webdriver.Chrome()
        seller_dict = {}

        # Loop through each URL in the list
        for link in links:
            # Navigate to the URL
            url=link['url']
            print("url: ",url)
            driver.get(url)
            time.sleep(4)
            # Find the seller block
            seller_block=driver.find_element(by=By.CSS_SELECTOR, value='div[data-qa="Seller"]')

            # Click the "See All" button
            see_all_button = seller_block.find_element(by=By.CSS_SELECTOR, value='button[data-qa="btn-see-all"]')
            see_all_button.click()

            # Find the div tag with the label elements
            brand_filter_div = seller_block.find_element(by=By.CSS_SELECTOR, value='div[data-qa="brand-filter-list"]')

            # Extract the last number from each label element
            labels = brand_filter_div.find_elements(by=By.CSS_SELECTOR, value='label[for^="filters-partner-p_"]')
            for label in labels:
                id_str = label.get_attribute('for')
                last_number = id_str.split('-')[-1]
                seller_name = label.find_element(by=By.CSS_SELECTOR,value= 'span.labelText').text
                seller_dict[seller_name] = last_number
            time.sleep(5)
        # Close the driver
        driver.quit()
        with open('Noon_seller_code_dictionary.json', 'w',encoding='utf-8') as f:
            json.dump(seller_dict, f,ensure_ascii=False)

        # Return the dictionary of seller names and codes for all URLs
        return seller_dict



    def Noon_get_img_seller_info(product_link,driver):
        product_img=""
        seller_code=""
        seller_name=""
        soup = BeautifulSoup(driver.page_source, 'lxml')

        
        check = 0

        while check !=10:

            imgs = soup.find_all("div",{"class":"sc-c5b1d4c4-3 bEHGRQ"})

            if len(imgs)!=0 :
                product_img=imgs[0].find('img').attrs['src']
                break
            else:
                check +=1 
                driver.refresh()
                time.sleep(3)

                soup = BeautifulSoup(driver.page_source, 'lxml')

        check = 0

        while check !=10:

            seller_driver = soup.find("div",{"class":"sc-7161241a-2 QxbsR"})
            # print(seller_driver)
            if seller_driver!=None:
                seller_name=seller_driver.find("span",{"class":"allOffers"}).text
                break
            else:
                check +=1 
                driver.refresh()
                time.sleep(3)

                soup = BeautifulSoup(driver.page_source, 'lxml')
        # try:
        #     seller_code=unique_sellers[seller_name]
        # except KeyError:
        #     seller_code=""           
        
        return product_img,seller_code,seller_name
    def scrape_products_info(product_urls,IDs, chunk_size=500,CHECK_INDEX=0):
        index = 0
        max_attempts = 3
        product_img=""
        seller_code=""
        seller_name=""


        driver = webdriver.Chrome()
        try:
            while index < len(product_urls):
                time.sleep(3)
                print("################## Remainig Products:",(len(product_urls)-index),"out of 2781 ##################",'\n')


                index_end = index + chunk_size
                if index_end > len(product_urls):
                    index_end = len(product_urls)

                chunk_urls = product_urls[index:index_end]
                chunk_ids=IDs[index:index_end]
                for product_url, product_id in zip(chunk_urls, chunk_ids):
                    # Open the website
                    driver.get(product_url)

                    #if Product not found!
                    product_not_found=driver.find_elements(By.CLASS_NAME, "sc-ad141e45-0")
                    if(product_not_found):
                        print("Product not found!")
                        time.sleep(2)
                        continue
                    try:
                        brand_div = driver.find_element(by=By.CSS_SELECTOR, value='div[data-qa^="pdp-brand"]')
                        # extract the brand text
                        brand = brand_div.text
                        time.sleep(1)
                    except:
                        brand=" "
                        pass
                    try:
                        # get img and seller info
                        product_img,seller_code,seller_name=Noon_get_img_seller_info(product_url,driver)
                    except (Exception,NoSuchWindowException) as e:
                        print("An error occurred while scraping the img and seller info, Retrying with product ID: ",product_id, " ......")
                        driver.quit()
                        time.sleep(5)
                        scrape_products_info(product_urls[index:],IDs[index:], 500)

                    time.sleep(1.5)

                    # Find the overview element by its class name
                    overview_elements = []
                    num_attempts = 0
                    while not overview_elements and num_attempts < max_attempts:
                        overview_elements = driver.find_elements(by=By.CLASS_NAME, value='sc-3482472f-1')
                        num_attempts += 1
                        if not overview_elements:
                            time.sleep(5)
                            print("Could not find product overview element. Retrying... Attempt:", num_attempts,'\n')

                    if overview_elements:
                        product_details = overview_elements[0].text
                    else:
                        product_details = ""
                        print("Could not find product overview element: ",product_url,'\n')

                    # product_info.append(product_details)

                    # Click the "Specifications" button
                    product_specifications = {}
                    time.sleep(1)

                    try:
                        specifications_button = driver.find_element(by=By.ID, value="Specifications")
                        # Click the "Specifications" button
                        specifications_button.click()

                        # Find all the specifications table elements with the same class name
                        specifications_tables = driver.find_elements(by=By.XPATH, value="//div[contains(@class, 'sc-88825672-2')]/table")

                        # Loop through the tables and extract the data
                        for specifications_table in specifications_tables:
                            # Extract the table rows
                            rows = specifications_table.find_elements(By.TAG_NAME, "tr")
                            # Loop through the rows and extract the data
                            for row in rows:
                                # Get the columns
                                cols = row.find_elements(By.TAG_NAME, "td")
                                # Check that there are two columns (key and value)
                                if len(cols) == 2:
                                    # Get the key and value
                                    key = cols[0].text
                                    value = cols[1].text
                                    # Add the key-value pair to the dictionary
                                    product_specifications[key] = value

                    except NoSuchElementException:
                        if driver.find_elements(by=By.XPATH, value="//div[contains(@class, 'sc-88825672-2')]/table"):                     
                            
                            # Find all the specifications table elements with the same class name
                            specifications_tables = driver.find_elements(by=By.XPATH, value="//div[contains(@class, 'sc-88825672-2')]/table")

                            # Loop through the tables and extract the data
                            for specifications_table in specifications_tables:
                                # Extract the table rows
                                rows = specifications_table.find_elements(By.TAG_NAME, "tr")
                                # Loop through the rows and extract the data
                                for row in rows:
                                    # Get the columns
                                    cols = row.find_elements(By.TAG_NAME, "td")
                                    # Check that there are two columns (key and value)
                                    if len(cols) == 2:
                                        # Get the key and value
                                        key = cols[0].text
                                        value = cols[1].text
                                        # Add the key-value pair to the dictionary
                                        product_specifications[key] = value
                        
                        else:
                            print("Could not find specifications button for pruduct_url:", product_url,'\n')
                            product_specifications = []
                    product_specifications_list = [f"{key}: {value}" for key, value in product_specifications.items()]

                    # product_spec.append(product_specifications)
                    product = {
                        "ProductID":product_id,
                        "ProductBrand":brand,
                        "ProductImage":product_img,
                        "SellerCode":seller_code,
                        "SellerName":seller_name,
                        "ProductDescription":product_details,
                        "ProductSpecifications":product_specifications_list,
                    }
                    products.append(product)

                    with open('Noon_ALL_product_Details22.json', 'a') as f:
                        json.dump(product, f)
                        f.write(',')
                        f.write('\n')
                    print("product scraped successfully")
                    index += 1
                    if index >= len(product_urls):
                        break
                time.sleep(1)
                # time.refresh()
                driver.quit()

        except:
            old_index=index
            print("An error occurred while scraping the website, Retrying with product ID: ",IDs[index], " ......")
            print("current product: ",product_urls[index],'\n')
            if old_index==index:
                CHECK_INDEX+=1
            else:
                CHECK_INDEX=0
            if CHECK_INDEX==2:
                CHECK_INDEX=0
                index+=1
            time.sleep(2)
            driver.quit()
            time.sleep(10)
            scrape_products_info(product_urls[index:],IDs[index:], 500,CHECK_INDEX)

        finally:
            # Close the driver
            driver.quit()

        return products
    
    def scrape_reviews(product_urls, product_ids):
        results = []
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        pNum=0
        try:
            for url,product_id in zip(product_urls, product_ids):
                pNum+=1
                print("###############################################################Product No:",pNum,"####################################################################")
                # Load the page
                driver.get(url)
                time.sleep(2)
                # Find the reviews button and click it
                try:
                    max_check=2
                    while max_check!=0:
                        try:
                            reviews_button = driver.find_element(by=By.ID, value='Reviews')
                            reviews_button.click()
                            break
                        except NoSuchElementException:
                            print(f"No reviews button found on the page for product {url}")
                            max_check-=1
                            time.sleep(2)
                            continue
                except ElementClickInterceptedException:
                    print("NO Reviews Button")
                    continue
                # Find all elements with class "select_lang"
                if driver.find_elements(by=By.CLASS_NAME, value="select_lang"):
                    lang_elements = driver.find_elements(by=By.CLASS_NAME, value="select_lang")
                    all_langues_button = lang_elements[0]
                    all_langues_button.click()

                # Scrape all the reviews from the page
                while True:
                    try:
                        time.sleep(2)
                        reviews = driver.find_elements(by=By.CLASS_NAME, value='noonReviewItem')
                        if not reviews:
                            print("No noonReviewItem")
                            break
                        for review in reviews:
                            # user_name = review.find_element(by=By.CLASS_NAME, value='userName').text
                            rating = len(review.find_elements(by=By.CSS_SELECTOR, value='.ratingCover img[alt="starFilledV2"][color="ratingOrange"], .ratingCover img[alt="starFilledV2"][color="ratingDarkGreen"], .ratingCover img[alt="starFilledV2"][color="ratingRed"], .ratingCover img[alt="starFilledV2"][color="ratingGray"], .ratingCover img[alt="starFilledV2"][color="ratingYellow"], .ratingCover img[alt="starFilledV2"][color="ratingLightGreen"],.ratingCover img[alt="starFilledV2"][color="ratingLightYellow"]'))
                            review_text = review.find_element(by=By.CLASS_NAME, value='reviewDesc').text

                            # Save the results for this product
                            product_data = {"ProductID": product_id, "review": review_text,"rating":rating}
                            results.append(product_data)
                            # Save the results as a JSON file
                            with open('reviews_noon_revieews.json', 'a',encoding='utf-8') as f:
                                json.dump(product_data, f,ensure_ascii=False)
                                f.write(',')
                                f.write('\n')

                        
                        # Check if there is a next page button and click it if it exists
                        try:
                            next_button = driver.find_element(by=By.CLASS_NAME, value="nextPage")
                            if "disabled" in next_button.get_attribute("class"):
                                break
                            next_button.click()
                        except StaleElementReferenceException:
                            print("StaleElementReferenceException: next button is not attached to the page document")
                            time.sleep(2)
                            next_button = driver.find_element(by=By.CLASS_NAME, value="nextPage")
                            if "disabled" in next_button.get_attribute("class"):
                                break
                            next_button.click()
                        except NoSuchElementException:
                            print("NoSuchElementException: next button not found")
                            break

                    except NoSuchElementException:
                        print("No noonReviewItem")
                        break
                print("product Done")
                time.sleep(2)
        except:
            print("Error in website.....")
        return results
    
    def get_remaining_seller_data(dic):

        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)

        for row in dic:
            if row['SellerCode'] == "":
                driver.get(row['ProductLink'])
                print(row['ProductLink'])
                try:
                    sold_by_button = driver.find_element(by=By.XPATH, value="//div[@class='sc-7161241a-8 hSYfAR']")
                    time.sleep(2)
                    sold_by_button.click()
                    time.sleep(3)
                    # Get the seller page URL
                    seller_page_url = driver.current_url
                    # link_tag = driver.find_element(by=By.XPATH, value="//meta[@property='og:url']")
                    # seller_page_url = link_tag.get_attribute("content")
                    print(seller_page_url)
                    # seller_page_url = driver.current_url
                except:
                    seller_page_url=""
                row['SellerCode'] = seller_page_url
                
                with open('seller_codes.json', 'a') as f:
                    json.dump(row, f)  
                    f.write(',')
                    f.write('\n')              
                time.sleep(3)
        with open('Noon_ALL_product_Dataset_Final.json', 'w',encoding='utf-8') as f:
            json.dump(dic, f,ensure_ascii=False)

        driver.quit()

        return dic
    
    def sellerReviews(ids,urls):
        # Initialize the driver and load the page
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        review_data_list=[]
        counter=0
        for id,url in zip(ids,urls):
            counter+=1
            print("######################################################## Seller Code No.: ",counter,"################################################")
            time.sleep(2)
            driver.get(url)
            try:
                if driver.find_element(By.CLASS_NAME, "sc-7368f995-45"):
                    pass
            except:
                # Get all review containers
                containers=driver.find_elements(By.CLASS_NAME, "sc-7368f995-52")
                print("Total Reviews Scarped: ",len(containers))

                # Iterate through each container and get review details
                for container in containers:
                    text = container.find_element(By.CLASS_NAME, "sc-b928625c-5").text
                    review_rating=len(container.find_elements(by=By.CSS_SELECTOR, value='button > img[alt="starFilledV2"][color="ratingOrange"], button > img[alt="starFilledV2"][color="ratingDarkGreen"], button > img[alt="starFilledV2"][color="ratingRed"],button > img[alt="starFilledV2"][color="ratingLightGreen"]'))            
                    #rating = container.find_element(By.XPATH, "//button[@class='sc-ff35799-2 fLlOAH']/img[@class='sc-b960f1b9-0 dkGTfp'][1]")
                    #rating = rating.get_attribute('color')
                    # title = container.find_element(By.CLASS_NAME, "sc-4e19eb22-4").text
                    
                    # Store the extracted data in a dictionary and append it to the list
                    review_data = {'SellerID': id, 'review': text,  'rating': review_rating}
                    review_data_list.append(review_data)

                    with open('sellerReviews2.json', 'a',encoding='utf-8') as f:
                        json.dump(review_data, f,ensure_ascii=False)  
                        f.write(',')
                        f.write('\n')   
                continue
            try:
                # Scroll to the element before clicking it
                view_elements = driver.find_element(By.CLASS_NAME, "sc-7368f995-45")
                driver.execute_script("arguments[0].scrollIntoView();", view_elements)
                time.sleep(2)

                view_elements.click()
                time.sleep(3)
            except:
                    try:
                        if  driver.find_element(By.CLASS_NAME, "sc-7368f995-45"):
                            view_elements = driver.find_element(By.CLASS_NAME, "sc-7368f995-45")
                            driver.execute_script("arguments[0].scrollIntoView();", view_elements)
                            time.sleep(5)
                            view_elements.click()
                    except:
                        pass
            reviews_element = driver.find_element(By.CLASS_NAME, "sc-35c58b02-5")
            reviews_text = reviews_element.text
            reviews_num = int(reviews_text.split()[0])
            print("Total Reviews For This seller: ",reviews_num )

            # Scroll to the end of the page to load all reviews
            # reviews = []
            # num_reviews = 0
            counter2=15
            prev=0
            while True:
                try:
                    time.sleep(3)
                    # Scroll to load more reviews
                    elements = driver.find_elements(By.XPATH, "//div[@class='sc-4e19eb22-0 bINlGD']")
                    driver.execute_script("arguments[0].scrollIntoView();", elements[-1])
                    # Wait for the last element to become visible
                    wait = WebDriverWait(driver, 10)
                    wait.until(EC.visibility_of(elements[-1]))
                    # Get the loaded reviews
                    new_reviews = driver.find_elements(By.XPATH, "//div[@class='sc-4e19eb22-0 bINlGD']")
                    num_new_reviews = len(new_reviews) - reviews_num
                    if prev==num_new_reviews:
                        print("###########################################################")
                        counter2-=1
                        if counter2==0:
                            break
                    else:
                        counter2=15
                    if(len(new_reviews)%1000==0):
                        time.sleep(5)
                        print("processing in: ",len(new_reviews))
                    if num_new_reviews == 0 or len(new_reviews)>=10000:
                        break
                    prev=num_new_reviews
                except:
                    time.sleep(2)
                    continue
                # num_reviews += num_new_reviews
                # reviews += new_reviews[len(reviews):]

            # Get all review containers
            containers=driver.find_elements(By.CLASS_NAME, "sc-4e19eb22-0")
            print("Total Reviews Scarped: ",len(containers))

            # Iterate through each container and get review details
            for container in containers:
                text = container.find_element(By.CLASS_NAME, "sc-4e19eb22-1").text
                review_rating=len(container.find_elements(by=By.CSS_SELECTOR, value='button > img[alt="starFilledV2"][color="ratingOrange"], button > img[alt="starFilledV2"][color="ratingDarkGreen"], button > img[alt="starFilledV2"][color="ratingRed"],button > img[alt="starFilledV2"][color="ratingLightGreen"]'))            
                #rating = container.find_element(By.XPATH, "//button[@class='sc-ff35799-2 fLlOAH']/img[@class='sc-b960f1b9-0 dkGTfp'][1]")
                #rating = rating.get_attribute('color')
                # title = container.find_element(By.CLASS_NAME, "sc-4e19eb22-4").text
                
                # Store the extracted data in a dictionary and append it to the list
                review_data = {'SellerID': id, 'review': text,  'rating': review_rating}
                review_data_list.append(review_data)

                with open('sellerReviews2.json', 'a',encoding='utf-8') as f:
                    json.dump(review_data, f,ensure_ascii=False)  
                    f.write(',')
                    f.write('\n')   
        return review_data_list



#################################################################### scrape_products_pages #####################################################################################

    links=[
        {'url':'https://www.noon.com/egypt-en/electronics-and-mobiles/mobiles-and-accessories/mobiles-20905/?limit=150&page=1',
         "category": "Electronics",
         "subcategory":"Mobile Phones"
         },
         {'url':'https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/tablets/?limit=150',
         "category": "Electronics",
         "subcategory":"Tablets"
         },
         {'url':'https://www.noon.com/egypt-en/electronics-and-mobiles/computers-and-accessories/laptops/?limit=150&page=1',
         "category": "Electronics",
         "subcategory":"Laptops"
         },
         {'url':'https://www.noon.com/egypt-en/electronics-and-mobiles/portable-audio-and-video/headphones-24056/?limit=50&page=1',
         "category": "Electronics",
         "subcategory":"Headphones"
         },
         
         ]

    products = []

    # data=noon_Marketplace_Data(links)

    # with open('noon_pages_data.json', 'w',encoding='utf-8') as f:
    #     json.dump(data, f,ensure_ascii=False)



    # # Load JSON data into a list of dictionaries    
    # with open('noon_pages_data.json',encoding='utf-8') as f:
    #     data = json.load(f)

    # # Find unique rows by creating a new dictionary and checking for duplicate product IDs
    # unique_rows = {}
    # for row in data:
    #     product_id = row['ProductID']
    #     if product_id not in unique_rows:
    #         unique_rows[product_id] = row

    # # Write the unique rows to a new JSON file
    # with open('noon_pages_data_unique.json', 'w',encoding='utf-8') as f:
    #     json.dump(list(unique_rows.values()), f, indent=2,ensure_ascii=False)


#################################################################### scrape_products_info #####################################################################################
    # products = []

    # # data=get_seller_code(links)

    # CHECK_INDEX=0

    # #load unique_sellers dic
    # with open('Noon_seller_code_dictionary.json',encoding='utf-8') as f:
    #     unique_sellers = json.load(f)

    # with open('noon_pages_data_unique.json',encoding='utf-8') as f:
    #     data1 = json.load(f)

    # product_ids = [item['ProductID'] for item in data1]
    # product_links = [item['ProductLink'] for item in data1]

    # start_time = time.time()

    # with open('Noon_ALL_product_Details22.json', 'w',encoding='utf-8') as f:
    #     f.write('[')
    # products = scrape_products_info(product_links,product_ids, chunk_size=500,CHECK_INDEX=0)
    # with open('Noon_ALL_product_Details_Final.json', 'a',encoding='utf-8') as f:
    #     f.write(']')

    # with open('Noon_ALL_product_Details_Final2.json', 'w',encoding='utf-8') as f:
    #     json.dump(products, f,ensure_ascii=False)

    # end_time = time.time()
    # execution_time = end_time - start_time
    # print(execution_time/60)
            
#     ############################################################ clean and merge data ###########################################

    # with open('Noon_ALL_product_Details.json',encoding='utf-8') as f:
    #     data = json.load(f)

    # # Find unique rows by creating a new dictionary and checking for duplicate product IDs
    # unique_rows = {}
    # for row in data:
    #     product_id = row['ProductID']
    #     if product_id not in unique_rows:
    #         unique_rows[product_id] = row

    # # Write the unique rows to a new JSON file
    # with open('Noon_ALL_product_Details_Unique.json', 'w',encoding='utf-8') as f:
    #     json.dump(list(unique_rows.values()), f, indent=2,ensure_ascii=False)


    # with open('noon_pages_data_unique.json',encoding='utf-8') as f:
    #     prod1 = json.load(f)
    # with open('Noon_ALL_product_Details_Unique.json',encoding='utf-8') as f:
    #     prod2 = json.load(f)

    # df1 = pd.DataFrame(prod1)
    # df2 = pd.DataFrame(prod2)
    # merged_df = pd.merge(df1, df2, on='ProductID')


    # for index, row in merged_df.iterrows():
    #     product_desc = row['ProductDescription']
    #     if product_desc.startswith('Highlights\n'):
    #         merged_df.at[index, 'ProductDescription'] = product_desc.replace('Highlights\n', '')
    #     elif product_desc.startswith('Overview\n'):
    #         merged_df.at[index, 'ProductDescription'] = product_desc.replace('Overview\n', '')

    # merged_df = merged_df[merged_df['ProductDescription'].ne("")]

    # merged_df.reset_index(drop=True,inplace=True)
    
    # json_data = merged_df.to_dict(orient='records')
    # # Save the JSON object to a file
    # with open('Noon_ALL_product_Dataset_Final.json', 'w',encoding='utf-8') as f:
    #     json.dump(json_data, f,ensure_ascii=False)

    # with open('Noon_ALL_product_Dataset_Final.json',encoding='utf-8') as f:
    #     prod2 = json.load(f)

    # df2 = pd.DataFrame(prod2)
    # for i in range(len(df2)):
    #     base_url, query_params = df2['ProductImage'][i].split("?format")
    #     df2['ProductImage'][i]=base_url
    #     print(df2['ProductImage'][i])

    # df2.reset_index(drop=True,inplace=True)

    # json_data = df2.to_dict(orient='records')
    # # # Save the JSON object to a file
    # with open('Noon_ALL_product_Dataset_Final.json', 'w',encoding='utf-8') as f:
    #     json.dump(json_data, f,ensure_ascii=False)

        
    # # Read the JSON file into a pandas DataFrame
    # with open('Noon_ALL_product_Dataset_Final.json', 'r', encoding='utf-8') as f:
    #     data = json.load(f)

    # with open('Noon_ALL_product_Dataset_Final.json',encoding='utf-8') as f:
    #     data = json.load(f)
    
    # # iterate over each row
    # for row in data:
    #     # check if the SellerCode is not empty
    #     if row['SellerCode'] and not row['SellerCode'].startswith('https://www.noon.com/'):
    #         row['SellerCode'] = row['SellerCode'].replace('_', '-')
    #         # replace the SellerCode with the new URL format
    #         ProductOfferCode= row['ProductLink'].split("=",2)
    #         ProductOfferCode=(ProductOfferCode[1])
    #         row['SellerCode'] = f"https://www.noon.com/egypt-en/seller/{row['SellerCode']}/?offer_code={ProductOfferCode}&sku={row['ProductID']}"

    # # write the updated data to a new JSON file
    # with open('Noon_ALL_product_Dataset_Final.json', 'w',encoding='utf-8') as f:
    #     json.dump(data, f,ensure_ascii=False)

    # with open('Noon_ALL_product_Dataset_Final.json',encoding='utf-8') as f:
    #     data = json.load(f)

    # data2=get_remaining_seller_data(data)
    # with open('Noon_ALL_product_Dataset_Final.json', 'w',encoding='utf-8') as f:
    #     json.dump(data2, f,ensure_ascii=False)

    # with open('Noon_ALL_product_Dataset_Final.json',encoding='utf-8') as f:
    #     data = json.load(f)

    # # loop through each row in the JSON file
    # for row in data:
    #     # rename SellerCode to SellerUrl
    #     row['SellerUrl'] = row.pop('SellerCode')
        
    #     # extract the SellerID from the SellerUrl
    #     url = row['SellerUrl']
    #     if url=="":
    #         seller_id=""
    #     else:
    #         seller_id = url.split('/')[-2]
    #     row['SellerID'] = seller_id


    # with open('Noon_ALL_product_Dataset_Final.json','w',encoding='utf-8') as f:
    #         json.dump(data, f,ensure_ascii=False)

    # with open('Noon_ALL_product_Dataset_Final.json',encoding='utf-8') as f:
    #     data = json.load(f)

    # for row in data:
    #     row['Marketplace']="Noon"
    
    # with open('Noon_ALL_product_Dataset_Final.json','w',encoding='utf-8') as f:
    #     json.dump(data, f,ensure_ascii=False)

    ############################################################ Scrap ALL Products Reveiws ###########################################

    with open('Noon_ALL_product_Dataset_Final.json',encoding='utf-8') as f:
        data1 = json.load(f)

    product_ids = [item['ProductID'] for item in data1]
    product_links = [item['ProductLink'] for item in data1]
    with open('reviews_noon_revieews.json', 'a',encoding='utf-8') as f:
        f.write('[')
    noon_reveiws=scrape_reviews(product_links, product_ids)
    with open('reviews_noon_revieews.json', 'a',encoding='utf-8') as f:
        f.write(']')
    # Save the results as a JSON file
    with open('Noon_ALL_product_Reviews_Final.json', 'w',encoding='utf-8') as f:
        json.dump(noon_reveiws, f,ensure_ascii=False)
    # ############################################################ Scrap ALL Seller Reveiws ###########################################
    # with open('Noon_ALL_product_Dataset_Final.json', 'r',encoding='utf-8') as f:
    #     data = json.load(f)

    # unique_seller_urls = []
    # unique_seller_ids = []

    # # iterate through each row in the data
    # for row in data:
    #     # extract the seller URL and ID from the row
    #     seller_url = row['SellerUrl']
    #     seller_id = row['SellerID']
        
    #     # check if the seller URL has already been added to the list
    #     if seller_id not in unique_seller_ids:
    #         # if the seller URL is not in the list, add it to the list
    #         unique_seller_urls.append(seller_url)
            
    #         # add the corresponding seller ID to the IDs list
    #         unique_seller_ids.append(seller_id)
            
    # df=pd.DataFrame()
    # df['SellerID']=unique_seller_ids
    # df['SellerUrl']=unique_seller_urls
    # df.reset_index(drop=True,inplace=True)
    # df=df[df.SellerID!=""]
    # json_data = df.to_dict(orient='records')
    # # Save the JSON object to a file
    # with open('unique_seller_ids_urls.json', 'w',encoding='utf-8') as f:
    #     json.dump(json_data, f,ensure_ascii=False)

    # with open('sellerReviews2.json', 'a',encoding='utf-8') as f:
    #     f.write('[')   

    # reviews=sellerReviews(df['SellerID'],df['SellerUrl'])

    # with open('sellerReviews2.json', 'a',encoding='utf-8') as f:
    #     f.write(']')   

    # with open('Noon_ALL_Seller_Reviews_Final.json', 'w',encoding='utf-8') as f:
    #     json.dump(reviews, f,ensure_ascii=False)  

    # ################################################## Data Merge #######################################
    # import json

    # # Step 1: Read the main JSON file
    # with open('Noon_ALL_product_Dataset_Final.json',encoding='utf-8') as file:
    #     main_data = json.load(file)

    # # Step 2: Read the reviews JSON file
    # with open('Noon_ALL_product_Reviews_Final.json',encoding='utf-8') as file:
    #     reviews_data = json.load(file)

    # # Step 3: Group the reviews based on product ID
    # grouped_reviews = {}
    # for review in reviews_data:
    #     product_id = review['ProductID']
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
    #     product_id = product['ProductID']
    #     if product_id in grouped_reviews:
    #         product['ProductReviews'] = grouped_reviews[product_id]
    #     else:
    #         product['ProductReviews'] = []

    # # Step 6: Write the updated data to a new JSON file
    # with open('Noon_Products_Dataset_Final_with_Reveiws.json', 'w',encoding='utf-8') as file:
    #     json.dump(main_data, file, indent=4,ensure_ascii=False)


    # # Step 1: Read the main JSON file
    # with open('Noon_Products_Dataset_Final_with_Reveiws.json',encoding='utf-8') as file:
    #     main_data = json.load(file)

    # # Step 2: Read the reviews JSON file
    # with open('Noon_ALL_Seller_Reviews_Final.json',encoding='utf-8') as file:
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
    # for product in main_data:
    #     product['Marketplace'] = 'Noon'
        
    # # Step 6: Write the updated data to a new JSON file
    # with open('Noon_Dataset_Final.json', 'w',encoding='utf-8') as file:
    #     json.dump(main_data, file, indent=4,ensure_ascii=False)


    return 
Noon_Scrap()


import json
import pandas as pd
