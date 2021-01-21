from time import sleep

from selenium import webdriver
import pytest
from django.conf import settings
import os


@pytest.fixture
def base_url():
    """ Начальный url для всех страниц """
    return 'http://127.0.0.1:8000/publisher'


@pytest.fixture
def driver():
    """ Драйвер для браузера """
    files = list((os.listdir('.')))
    for file in files:
        if 'driver' in file:
            driver_name = file.split(".")[0]
            break
    else:
        driver_name = ""
    if driver_name == 'chromedriver':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(f"{settings.BASE_DIR}/chromedriver", options=chrome_options)
    elif driver_name == 'geckodriver':
        mozilla_options = webdriver.FirefoxOptions()
        mozilla_options.add_argument('--headless')
        driver = webdriver.Firefox(executable_path=f"{settings.BASE_DIR}/geckodriver", options=mozilla_options)
    else:
        raise FileNotFoundError('Нет драйвера')
    return driver


def test_get_all_publication_page(driver, base_url):
    driver.get(base_url)
    assert 'Publisher' in driver.title


def test_success_create_author(driver, base_url):
    driver.get(f'{base_url}')
    authors = driver.find_element_by_link_text('Авторы')
    authors.click()
    add_author = driver.find_element_by_link_text('Добавить автора')
    add_author.click()
    surname = driver.find_element_by_xpath('//input[@id="surname"]')
    surname.send_keys('TestSurname')
    name = driver.find_element_by_xpath("//input[@id='name']")
    name.send_keys('TestName')
    patronymic = driver.find_element_by_xpath("//input[@id='patronymic']")
    patronymic.send_keys('TestPatronymic')
    military_rank = driver.find_element_by_xpath("//input[@id='military_rank']")
    military_rank.send_keys('TestRank')
    work_position = driver.find_element_by_xpath("//input[@id='work_position']")
    work_position.send_keys('TestWorkPosition')
    create = driver.find_element_by_xpath("//button[@type='submit']")
    create.submit()
    sleep(0.2)
    assert driver.current_url == f'{base_url}/create_publication/'


def test_success_create_type(driver, base_url):
    driver.get(f'{base_url}')
    authors = driver.find_element_by_link_text('Типы')
    authors.click()
    add_type = driver.find_element_by_link_text('Добавить тип')
    add_type.click()
    type_of_publication = driver.find_element_by_xpath('//input[@id="type_of_publication"]')
    type_of_publication.send_keys('TestType')
    create = driver.find_element_by_xpath("//button[@type='submit']")
    create.submit()
    sleep(0.2)
    assert driver.current_url == f'{base_url}/create_publication/'


def test_success_create_publication_with_only_title(driver, base_url):
    driver.get(f'{base_url}')
    add_publication = driver.find_element_by_link_text('Добавить запись')
    add_publication.click()
    title = driver.find_element_by_xpath('//input[@id="title"]')
    title.send_keys('TestTitle')
    create = driver.find_element_by_xpath("//button[@type='submit']")
    create.submit()
    sleep(0.2)
    assert driver.current_url == f'{base_url}/'


def test_success_update_publication_title(driver, base_url):
    driver.get(f'{base_url}')
    publication = driver.find_element_by_link_text('TestTitle')
    publication.click()
    edit = driver.find_elements_by_class_name('btn')[0]
    edit.click()
    title = driver.find_element_by_xpath('//input[@id="title"]')
    title.clear()
    title.send_keys('AnotherTestTitle')
    save = driver.find_element_by_xpath("//button[@type='submit']")
    save.submit()
    sleep(0.2)


def test_success_update_author(driver, base_url):
    driver.get(f'{base_url}/authors/')
    author = driver.find_element_by_partial_link_text('TestSurname T.T.')
    author.click()
    edit = driver.find_elements_by_class_name('btn')[1]
    edit.click()
    name = driver.find_element_by_xpath('//input[@name="surname"]')
    name.clear()
    name.send_keys('AnotherTestSurname')
    save = driver.find_element_by_xpath("//button[@type='submit']")
    save.submit()
    sleep(0.2)
    assert driver.current_url == f'{base_url}/authors/'


def test_success_update_type(driver, base_url):
    driver.get(f'{base_url}/types')
    edit = driver.find_elements_by_tag_name('a')[-2]
    edit.click()
    type_of_publication = driver.find_element_by_xpath('//input[@name="type_of_publication"]')
    type_of_publication.clear()
    type_of_publication.send_keys('AnotherTestType')
    save = driver.find_element_by_xpath("//button[@type='submit']")
    save.submit()
    sleep(0.2)
    assert driver.current_url == f'{base_url}/types/'


def test_success_delete_publication(driver, base_url):
    driver.get(f'{base_url}')
    publication = driver.find_element_by_link_text('AnotherTestTitle')
    publication.click()
    delete = driver.find_elements_by_class_name('btn')[1]
    delete.click()
    confirm = driver.find_element_by_xpath('//button["Да, удалить"]')
    confirm.submit()
    sleep(0.2)
    assert driver.current_url == f'{base_url}/'


def test_success_delete_author(driver, base_url):
    driver.get(f'{base_url}/authors')
    author = driver.find_element_by_partial_link_text('AnotherTestSurname T.T.')
    author.click()
    delete = driver.find_elements_by_class_name('btn')[0]
    delete.click()
    confirm = driver.find_element_by_xpath('//button["Да, удалить"]')
    confirm.submit()
    sleep(0.2)
    assert driver.current_url == f'{base_url}/authors/'


def test_success_delete_type(driver, base_url):
    driver.get(f'{base_url}/types')
    delete = driver.find_elements_by_tag_name('a')[-1]
    delete.click()
    confirm = driver.find_element_by_xpath('//button["Да, удалить"]')
    confirm.submit()
    sleep(0.2)
    assert driver.current_url == f'{base_url}/types/'
