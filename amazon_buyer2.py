import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import yaml

with open("user_info.yaml", "r") as stream:
    try:
        yaml_file = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

print(yaml_file)
email = yaml_file["username"]
password = yaml_file["password"]


def add_a_new_item(driver, item_name):
    # Enter the item name in the search bar
    search_bar = driver.find_element(By.ID, "twotabsearchtextbox")
    search_bar.clear()
    search_bar.send_keys(item_name)

    # Click on the "Search" button
    search_button = driver.find_element(By.ID, "nav-search-submit-button")
    search_button.click()

    # Wait for the search results to load
    time.sleep(1)
    first_item = driver.find_element(By.XPATH,
                                     "//a[contains(@class,'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal')]")

    link = first_item.get_attribute("href")
    driver.execute_script("window.open('about:blank','secondtab');")
    driver.switch_to.window("secondtab")
    driver.get(link)
    time.sleep(1)
    add_to_cart_button = driver.find_element(By.ID, "add-to-cart-button")
    add_to_cart_button.click()
    time.sleep(2)
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    time.sleep(2)
    return driver


def logging_in(driver, mail_id, password):
    driver.get(
        "https://www.amazon.in/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.in%2F%3F%26ext_vrnc%3Dhi%26tag%3Dgooghydrabk1-21%26ref%3Dnav_signin%26adgrpid%3D61665929249%26hvpone%3D%26hvptwo%3D%26hvadid%3D610714031506%26hvpos%3D%26hvnetw%3Dg%26hvrand%3D16299710400319108230%26hvqmt%3De%26hvdev%3Dc%26hvdvcmdl%3D%26hvlocint%3D%26hvlocphy%3D9050496%26hvtargid%3Dkwd-298441375321%26hydadcr%3D5621_2359492&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=inflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&")
    # Find the email input field and enter the email ID
    email_input = driver.find_element(By.CSS_SELECTOR, "input[type='email'][id='ap_email']")
    email_input.send_keys(str(mail_id))  # Replace with the desired email ID

    click_continue = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][id ='continue']")
    click_continue.click()
    time.sleep(2)

    password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password'][id='ap_password']")
    password_input.send_keys(str(password))
    click_sign_in = driver.find_element(By.CSS_SELECTOR, "input[type='submit'][id='signInSubmit']")
    click_sign_in.click()
    time.sleep(2)
    return driver


# Enter your email address and password here


# The item name that you want to search for
item_name = "iphone 13"


# Open the Amazon login page

# driver = webdriver.Chrome()  # Make sure you have Chrome driver installed and in PATH
# driver = logging_in(driver)
# item_names = ["car","toys","camera"]
# for item_name in item_names:
#     driver = add_a_new_item(item_name)


def get_items(text):
    """
    This function takes a string of text and returns a list of items.

    Args:
    text: A string of text.

    Returns:
    A list of items.
    """
    driver = webdriver.Chrome()  # Make sure you have Chrome driver installed and in PATH
    driver = logging_in(driver, mail_id=email, password=password)
    # browser.find_element_by_id("nav-cart").click()

    items = []
    for word in text.split(","):
        driver = add_a_new_item(driver, word)
        items.append(word)
    time.sleep(2)
    show_cart = driver.find_element(By.ID, "nav-cart").click()

    open_cart = driver.find_element(By.XPATH, "//a[contains(@id,'nav-button-cart')]")
    link = open_cart.get_attribute("href")
    driver.execute_script("window.open('about:blank','secondtab');")
    driver.switch_to.window("secondtab")
    driver.get(open_cart)


items = input("Enter the items you want to buy\n")
get_items(items)
# "iphone 14 pro max black, iphone 14 adapter , iphone 14 back case solid(black)"
