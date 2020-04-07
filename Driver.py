from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os

CHROMEDRIVER_PATH = "./chromedriver"
USER_DATA_ROOT = "/chrome_sessions"

def init_driver(user, website_name, debug = False):
    options = Options()
    user_data_path = "./{root}/{user}_{name}".format(root = USER_DATA_ROOT, user = user, name = website_name)

    data_argument = "user-data-dir={}".format(os.path.abspath(user_data_path))

    options.add_argument(data_argument)
    options.add_argument("--window-size=1600,900")

    options.headless = not debug
    driver = webdriver.Chrome(CHROMEDRIVER_PATH, chrome_options=options)
    return driver
