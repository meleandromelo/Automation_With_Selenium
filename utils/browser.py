from selenium import webdriver


def new_chrome(*, headed=False):
    options = webdriver.ChromeOptions()
    if not headed:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1000")
    options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
    })
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(45)
    return driver
