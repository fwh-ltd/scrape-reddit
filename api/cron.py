from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options


def run():
    options = Options()
    options.headless = False
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
  