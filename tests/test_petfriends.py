import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as chrome_options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

@pytest.fixture
def get_chrome_options():
    options = chrome_options()
    options.add_argument('chrome')
    options.add_argument('--start-maximized')
    options.add_argument('--window-size=1650,900')
    return options

@pytest.fixture
def get_webdriver(get_chrome_options):
    options = get_chrome_options
    pytest.driver = webdriver.Chrome(options=options)
    return pytest.driver

@pytest.fixture(autouse=True)
def testing(get_webdriver):
    pytest.driver = get_webdriver
    pytest.driver.implicitly_wait(10)
    url = "https://petfriends.skillfactory.ru/login"
    pytest.driver.get(url)
    yield
    pytest.driver.quit()

 # 1 тест # У питомцев на главной странице усть имя,фото, описание
def test_show_my_pets():

    pytest.driver.find_element(By.XPATH, "//input[@id='email']").send_keys('repom50797@nazyno.com')
    pytest.driver.find_element(By.XPATH, "//input[@id='pass']").send_keys('12345')
    pytest.driver.find_element(By.XPATH, "//button[contains(text(),'Войти')]").click()
    assert pytest.driver.find_element(By.XPATH, "//h1[contains(text(),'PetFriends')]").text == "PetFriends"
    time.sleep(5)

    images = pytest.driver.find_elements(By.CSS_SELECTOR, ".card .card-img-top")
    names = pytest.driver.find_elements(By.CSS_SELECTOR, '.card .card-title')
    descriptions = pytest.driver.find_elements(By.CSS_SELECTOR, '.card .card-text')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert descriptions[i].text != ''
        assert ', ' in descriptions[i]
        parts = descriptions[i].text.split(",")
        assert len(parts[0]) > 0
        assert len(parts[1]) > 0

# 2 тест # Количество питомцев
def test_amout_my_pets():
    pytest.driver.find_element(By.XPATH, "//input[@id='email']").send_keys('repom50797@nazyno.com')
    pytest.driver.find_element(By.XPATH, "//input[@id='pass']").send_keys('12345')
    pytest.driver.find_element(By.XPATH, "//button[contains(text(),'Войти')]").click()
    pytest.driver.find_element(By.XPATH, "//a[contains(text(),'Мои питомцы')]").click()
    time.sleep(5)
    wait = WebDriverWait(pytest.driver, 15)
    quantity = wait.until(ec.visibility_of_element_located((By.TAG_NAME, 'tr')))
    left_info = pytest.driver.find_element(By.XPATH, ('//body/div[1]/div[1]/div[1]'))
    num = left_info.get_attribute('innerText')
    assert str(len(quantity) - 1) in num

# 3 тест # Получили список имен питомцев
def test_list_pets():
    pytest.driver.find_element(By.XPATH, "//input[@id='email']").send_keys('repom50797@nazyno.com')
    pytest.driver.find_element(By.XPATH, "//input[@id='pass']").send_keys('12345')
    pytest.driver.find_element(By.XPATH, "//button[contains(text(),'Войти')]").click()
    pytest.driver.find_element(By.XPATH, "//a[contains(text(),'Мои питомцы')]").click()

    time.sleep(5)

    names = pytest.driver.find_element(By.XPATH, "//tbody/tr/td[1]")
    for x in names:
        unique_names = x.text
        print("Мы получили имена и сохранили в переменную", unique_names)
        list_names = []
        list_names.append(unique_names)
    print("Тут должен быть список из 3 значений", list_names)

# 4 тест #имеют разные имена
def test_all_my_pets_have_lif_names():
    pytest.driver.find_element(By.XPATH, "//input[@id='email']").send_keys('repom50797@nazyno.com')
    pytest.driver.find_element(By.XPATH, "//input[@id='pass']").send_keys('12345')
    pytest.driver.find_element(By.XPATH, "//button[contains(text(),'Войти')]").click()
    pytest.driver.find_element(By.XPATH, "//a[contains(text(),'Мои питомцы')]").click()
    time.sleep(5)
    names = pytest.driver.find_elements(By.XPATH, "//*[@id='all_my_pets']/table/tbody/tr/td[1]")
    print(names)


# 5 тест #У питомцев на страницу мои питомцы есть имя, катринка, возраст, порода
def test_my_pets_eat_name():
    pytest.driver.find_element(By.XPATH, "//input[@id='email']").send_keys('repom50797@nazyno.com')
    pytest.driver.find_element(By.XPATH, "//input[@id='pass']").send_keys('12345')
    pytest.driver.find_element(By.XPATH, "//button[contains(text(),'Войти')]").click()                
    pytest.driver.find_element(By.XPATH, "//a[contains(text(),'Мои питомцы')]").click()
    time.sleep(5)
    names = pytest.driver.find_elements(By.XPATH, "//*[@id='all_my_pets']/table/tbody/tr[1]/td[1]")

    for i in range(len(names)):
        assert names[i].text != ''


# 6 тест # У питомцев на странице мои питомцы есть фото
def test_my_pets_eat_images():
    pytest.driver.find_element(By.XPATH, "//input[@id='email']").send_keys('repom50797@nazyno.com')
    pytest.driver.find_element(By.XPATH, "//input[@id='pass']").send_keys('12345')
    pytest.driver.find_element(By.XPATH, "//button[contains(text(),'Войти')]").click()
    pytest.driver.find_element(By.XPATH, "//a[contains(text(),'Мои питомцы')]").click()
    time.sleep(5)
    images = pytest.driver.find_elements(By.XPATH, "//*[@id='all_my_pets']/table/tbody/tr[1]/th/img")

    for i in range(len(images)):
        assert images[i].get_attribute('src') != ''

# 7 тест # У питомцев на странице мои питомцы есть возраст
def test_my_pets_eat_ages():
    pytest.driver.find_element(By.XPATH, "//input[@id='email']").send_keys('repom50797@nazyno.com')
    pytest.driver.find_element(By.XPATH, "//input[@id='pass']").send_keys('12345')
    pytest.driver.find_element(By.XPATH, "//button[contains(text(),'Войти')]").click()
    pytest.driver.find_element(By.XPATH, "//a[contains(text(),'Мои питомцы')]").click()
    time.sleep(5)
    ages = pytest.driver.find_elements(By.XPATH, "//*[@id='all_my_pets']/table/tbody/tr[1]/td[3]")
    for i in range(len(ages)):
        assert ages[i].int != ''

# 8 тест # У питомцев на странице мои питомцы есть порода
def test_my_pets_eat_breed():
    pytest.driver.find_element(By.XPATH, "//input[@id='email']").send_keys('repom50797@nazyno.com')
    pytest.driver.find_element(By.XPATH, "//input[@id='pass']").send_keys('12345')
    pytest.driver.find_element(By.XPATH, "//button[contains(text(),'Войти')]").click()
    pytest.driver.find_element(By.XPATH, "//a[contains(text(),'Мои питомцы')]").click()
    time.sleep(5)
    breed = pytest.driver.find_elements(By.XPATH, "//*[@id='all_my_pets']/table/tbody/tr[1]/td[2]")
    for i in range(len(breed)):
        assert breed[i].text != ''
































    # wait = WebDriverWait(pytest.driver, 15)
    # quantity = wait.until(ec.visibility_of_element_located((By.TAG_NAME, 'tr')))
    # left_info = pytest.driver.find_element(By.XPATH, ('//body/div[1]/div[1]/div[1]'))
    # num = left_info.get_attribute('innerText')
    # assert str(len(quantity) - 1) in num







 #