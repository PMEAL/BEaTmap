from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--headless")

with webdriver.Chrome(options=options) as driver:
    driver.get("https://beatmap.streamlit.app/")
