#!/usr/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd


class ScrapeSalary:

    def __init__(self, language, seniority):
        self.language = language.lower()
        career_ladder = ["junior", "mid", "senior"]

        if seniority.lower() in career_ladder:
            self.seniority = seniority
        else:
            return

        options = Options()
        options.headless = True
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--incognito")

        driver_path = "/Users/filip/chromedriver/chromedriver"
        self.driver = webdriver.Chrome(options=options, executable_path=driver_path)

        self.load_page()
        self.page_has_loaded()
        self.process_items()

    def page_has_loaded(self):
        print(f"Waiting for page to load.")
        element_present = EC.presence_of_element_located((By.XPATH,
                                                          '//*[@id="root"]/div[3]/div[1]/div/div[2]/div['
                                                          '1]/div/div/div[1]/a/div'))
        WebDriverWait(self.driver, 30).until(element_present)
        print(f"Page loaded.")

    def load_page(self):
        url = f"https://justjoin.it/?q={self.language}@category;{self.seniority}@keyword&tab=with-salary"
        driver = self.driver
        driver.get(url)

    def process_items(self):
        driver = self.driver
        df = pd.DataFrame([], columns=["min_salary", "max_salary", "currency", "language"])

        i = 1
        while True:
            try:
                element_price_xpath = f'//*[@id="root"]/div[3]/div[1]/div/div[2]/div[1]/div/div/div[{i}]/a/div/div[' \
                                      f'3]/div[1]/div[2]/div[1] '
                element = driver.find_element_by_xpath(element_price_xpath).get_attribute("innerHTML")
                elements = element.split(" - ")
                elements.append(elements[1][-3:])
                elements[1] = elements[1][:-4]
                elements[0] = elements[0].replace(" ", "")
                elements[1] = elements[1].replace(" ", "")
                elements.append(self.language)
                i += 1

                df_length = len(df)
                df.loc[df_length] = elements

            except:
                break

        print(df.head())

        save_location = f"{self.language}_data.csv"
        df.to_csv(save_location, index=False)

        print(f"Data imported to: {save_location}.")

    def __exit__(self):
        self.driver.quit()


def main():
    scrape = ScrapeSalary(language="python", seniority="junior")
    return scrape


if __name__ == "__main__":
    main()
