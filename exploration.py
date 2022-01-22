from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#driver = webdriver.Firefox()

options = webdriver.ChromeOptions()
#options.add_argument("--headless") # Runs Chrome in headless mode.
options.add_argument('--no-sandbox') # Bypass OS security model
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--disable-features=NetworkService")
options.add_argument("--window-size=1920x1080")
options.add_argument("--disable-features=VizDisplayCompositor")
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument("--disable-extensions")
options.add_argument('user-agent={userAgent}')
driver = webdriver.Chrome(options=options, executable_path='/usr/lib/chromium-browser/chromedriver')
link = "https://accounts.craigslist.org/login/tou?rp=%2Fk%2FpPeWzbN77BG_LZ7erXrsjA%2FPKzSZ&rt=P"
driver.get(link)
elem = driver.find_element_by_xpath("/html/body/form[1]/input[4]")
elem.click()
driver.close()
