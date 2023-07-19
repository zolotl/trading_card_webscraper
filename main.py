from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import numpy as np
import pandas as pd
from datetime import date
import os


def scrape_product_data(wd, product_name, csv_path, single_csv=True):
    # wait for searchbar to load then search for product
    # WebDriverWait(wd, 20).until(
    # EC.visibility_of_element_located(
    #     (By.XPATH, "//input[@class='search-bar__input']")
    #     )
    # )
    searchbar = wd.find_element(By.XPATH, "//input[@class='search-bar__input']")
    searchbar.clear()
    searchbar.send_keys(product_name)
    wd.find_element(By.CLASS_NAME, "search-bar__submit").click()

    # Wait for product page to appear then scrape the price
    WebDriverWait(wd, 20).until(
    EC.visibility_of_element_located(
        (By.XPATH, "//a[@class='product-item__title text--strong link']")
        )
    )
    price_text = wd.find_element(By.XPATH, "//div[@class='product-item__price-list price-list']/span").text
    price = float(price_text[price_text.find('$') + 1 :].replace(',', ''))


    # read existing csv, append new info and save csv
    curr_date = date.today().strftime("%Y-%m-%d")

    # Save into a single csv file
    if single_csv:
        try:
            df = pd.read_csv(csv_path)
        except:
            df = pd.DataFrame(columns=['date'])
        
        if curr_date in df['date'].values:
            df.loc[df['date'] == curr_date, product_name] = price
        else:
            df.loc[len(df)] = curr_date
            df.loc[df['date'] == curr_date, product_name] = price

    # Save into multiple csv files
    else:
        try:
            df = pd.read_csv(csv_path)
        except:
            df = pd.DataFrame(columns=['date', 'price'])

        if curr_date in df['date'].values:            
            df.loc[df["date"] == curr_date] = [curr_date, price]
        else:
            df.loc[len(df)] =  [curr_date, price]

    df.to_csv(csv_path, index=False)

    print("data saved to ", csv_path, "!")



# website url
website_url = "https://japantradingcardstore.com/en-sg"

# instantiate driver
wd = webdriver.Chrome()
wd.get(website_url)

WebDriverWait(wd, 20).until(
EC.visibility_of_element_located(
    (By.XPATH, "//button[@class='popup-newsletter__close link']")
    )
)
wd.find_element(By.XPATH, "//button[@class='popup-newsletter__close link']").click()

# settings - change these
product_names = ["vstar universe booster box",
                 "pokemon 151 booster box",
                 "vmax climax booster box",
                 "op-01 booster box",
                 "op-02 booster box",
                 "op03 booster box",
                 "op04 booster box"
                 ]
results_dir = 'results'

for product_name in product_names:
    # csv_path = os.path.join(results_dir, product_name + '.csv')
    csv_path = "results\\combined.csv"
    scrape_product_data(wd, product_name, csv_path, single_csv=True)

