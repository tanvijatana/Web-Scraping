from selenium import webdriver
from selenium.webdriver.common.by import By
import sys, time
import logging as l
import json
  
try:
    output = []
    categories_pages_dict = {'food-8':16, 'beverages-182':16, 'flowers-plants-203':3, 'everything-else-215':4}
    driver = webdriver.Firefox()
    for key,value in categories_pages_dict.items():
        for page_no in range(1,value):
            driver.get("https://www.traderjoes.com/home/products/category/{}?filters=%7B%22page%22%3A{}%7D".format(key,page_no))
            time.sleep(5)
            product_containers = driver.find_elements(by=By.XPATH, value="//ul[@class='ProductList_productList__list__3-dGs']/li/section")
            for con in product_containers:
                temp = {}
                temp['model'] = "Trader Joe's"
                temp['description'] = "Trader Joe's is a national chain of neighborhood grocery stores. We are committed to providing our customers outstanding value in the form of the best quality products at the best everyday prices."
                temp['image'] = con.find_element(by=By.XPATH, value=".//a//img").get_attribute("src")
                temp['models']={}
                temp['models']['variants'] = []
                try:
                    temp['price'] = con.find_element(by=By.XPATH, value=".//span[@class='ProductPrice_productPrice__price__3-50j']").text.replace('$','')
                except Exception as e:
                    temp["price"] = ''
                try:
                    temp['sale_price'] = con.find_element(by=By.XPATH, value=".//span[@class='ProductPrice_productPrice__price__3-50j']").text.replace('$','')
                except Exception as e:
                    temp["sale_price"] = ''
                temp['title'] = con.find_element(by=By.XPATH, value=".//div/h2/a").text
                temp['url'] = con.find_element(by=By.XPATH, value=".//div/h2/a").get_attribute("href")
                temp['product_id'] = temp['url'].split("-")[-1]  
                output.append(temp)
     
    with open("output/trader_joes.json", "w") as json_file:
        json.dump(output, json_file, indent=4)
      
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    message=str(exc_type)+ str(exc_obj)+' At line no : ' +str(exc_tb.tb_lineno)
    l.error(message)
finally:
    driver.quit()