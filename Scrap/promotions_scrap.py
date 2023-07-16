# -*- coding: utf-8 -*-


import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
import csv
from itertools import zip_longest
import time
import json
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'Accept-Language': 'en-US, en;q=0.5'
}

websites=[

    {"website_name":'Noon','url':"https://gccoupons.com/noon-coupons/#coupons"},
    {"website_name":'Amazon','url':"https://gccoupons.com/amazoneg-coupons/#coupons"},
    {"website_name":'jumia','url':"https://gccoupons.com/amazoneg-coupons/#coupons"}

]

url=websites[0]['url']

promotions_title=[]
promotions_coupon=[]
marketplace=[]
def promotion_Scrap(url,market):
    #Request to get all promotions
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    blocks=soup.find_all("div",{'class':'col-sm-12'})
    
    for i in blocks:
        prom=i.find("a",{'class':'coupon-action-button coupon-code'})
        if (prom!= None):
            promotions_title.append(prom.text.replace('\n', '').replace('\r', '').replace('\t', ''))
            promotions_coupon.append(prom.attrs['data-coupon'])
            marketplace.append(market)
    
    promotions=[marketplace,promotions_title,promotions_coupon]
    return promotions

for i in range(len(websites)):
    data=promotion_Scrap(websites[i]['url'],websites[i]['website_name'])
    
columns=['Marketplace','PromotionsTitle','PromotionsCoupon']
data=zip_longest(*data)
df= pd.DataFrame(data,columns=columns)
df=df[['Marketplace','PromotionsTitle','PromotionsCoupon']]
json_data = df.to_dict(orient='records')
# Save the JSON object to a file
with open('promotions_data.json', 'w',encoding='utf-8') as f:
    json.dump(json_data, f,ensure_ascii=False)

df.to_excel('promotions_scrap.xlsx')
