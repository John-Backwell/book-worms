from posixpath import split
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
import time
import random

def get_books_from_list(driver,url,save_file):
    driver.get(url)
    master_list_ids = iterate_through_pages(driver)
    with open (save_file,'w') as file:
        for line in master_list_ids:
            for id in line:
                file.write("%s\n" % id)
        
def get_best_sci_fi_books(driver,save_file):
    get_books_from_list(driver,"https://www.goodreads.com/list/show/3.Best_Science_Fiction_Fantasy_Books",save_file)
        
def iterate_through_pages(driver):
    master_list = []
    last_page = False
    while(not last_page):
        last_page = is_last_page(driver)
        urls = get_max_bookTitle_urls(driver)
        ids_and_names = parse_urls_for_ID_and_name(urls)
        master_list.append(ids_and_names)
        try:
            click_next_page(driver)
        except ElementNotInteractableException:
            print("reached last page")
    return master_list
 
def get_max_bookTitle_urls(driver):
    #returns the urls for each of the 100 maximum books displayed per page
    
    book_titles = driver.find_elements(By.CLASS_NAME,'bookTitle')
    urls = [element.get_attribute("href") for element in book_titles]
    return urls

def parse_urls_for_ID_and_name(urls):
    #parses urls for relevant book ID and name for building text file to pass to scraper
    
    split_urls = [url.rsplit('/',1) for url in urls]
    ids_and_names = [sublist[-1] for sublist in split_urls]
    return ids_and_names

def click_next_page(driver):
    insert_random_wait()
    next_button = driver.find_elements(By.CLASS_NAME,"next_page")
    next_button[0].click()
    
    #closes pop up window if it exists
    try:
        driver.find_element(By.CLASS_NAME,"loginModal")
        close_button = driver.find_elements(By.CLASS_NAME,"gr-iconButton")[-1]
        close_button.click()
    except NoSuchElementException:
        pass
    
def is_last_page(driver):
    
    try:
        next_button = driver.find_element(By.XPATH,"//span[contains(@class,'next_page disabled')]")
        return next_button.is_enabled()
    except NoSuchElementException:
        return False
    
def insert_random_wait():
    random_num = random.random()
    random_sleep = random_num * 10
    time.sleep(random_sleep)

if __name__ == "__main__":
    driver = webdriver.Chrome()
    get_best_sci_fi_books(driver,"best_sci_fi.txt")
    
    
    