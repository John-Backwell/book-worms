from posixpath import split
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException

def get_best_SF_Fantasy_books(driver):
    driver.get("https://www.goodreads.com/list/show/3.Best_Science_Fiction_Fantasy_Books")
    master_list_ids = []
    iterate_through_pages(driver,master_list_ids)
    with open ("best_sci_fi_fantasy.txt",'w') as file:
        file.write(master_list_ids)
        
def iterate_through_pages(driver, master_list):
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
      
def get_max_bookTitle_urls(driver):
    #returns the urls for each of the 100 maximum books displayed per page
    
    book_titles = driver.find_elements(By.CLASS_NAME,'bookTitle')
    urls = [element.get_attribute("href") for element in book_titles]
    return urls

def parse_urls_for_ID_and_name(urls):
    #parses urls for relevant book ID and name for passing to scraper
    
    split_urls = [url.rsplit('/',1) for url in urls]
    ids_and_names = [sublist[-1] for sublist in split_urls]
    return ids_and_names

def click_next_page(driver):
    next_button = driver.find_elements(By.CLASS_NAME,"next_page")
    next_button[0].click()
    
    #closes pop up window if it exists
    if driver.find_element(By.CLASS_NAME,"loginModal").is_displayed():
        close_button = driver.find_elements(By.CLASS_NAME,"gr-iconButton")[-1]
        close_button.click()

def is_last_page(driver):
    try:
        return driver.find_element_by_xpath("//span[contains(@class,'next-page disabled')]").is_displayed()
    except NoSuchElementException:
        return False
    
if __name__ == "__main__":
    driver = webdriver.Chrome()
    get_best_SF_Fantasy_books(driver)
    parse_urls_for_ID_and_name(get_max_bookTitle_urls(driver))
    click_next_page(driver)
    click_next_page(driver)
    
    