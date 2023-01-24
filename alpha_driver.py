from time import sleep
from random import randint
from selenium.webdriver import ChromeOptions
from selenium.webdriver.chrome import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, \
    TimeoutException, ElementClickInterceptedException, StaleElementReferenceException, JavascriptException


class AlphaDriver:
    def __init__(self, chrome_driver_filename: str, profile_path=None, headless=False):
        random_port = randint(9000, 9300)

        chrome_options = ChromeOptions()
        p_refs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", p_refs)
        if headless:
            user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                         'Chrome/91.0.4472.124 Safari/537.36'
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument(f"user-agent={user_agent}")
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--log-level=3")
            chrome_options.add_argument(f'--remote-debugging-port={random_port}')
        chrome_options.add_argument(f"--user-data-dir={profile_path}")
        self.driver = webdriver.WebDriver(executable_path=chrome_driver_filename,
                                          options=chrome_options)
        self.driver.implicitly_wait(0)
        # self.driver.set_window_size(1080, 720)
        self.driver.set_window_size(1920, 1080)

    def wait_until(self, by=None, element=None, delay=3):
        if by is None or element is None:
            return
        WebDriverWait(self.driver, delay).until(
            lambda driver: expected_conditions.presence_of_element_located((by, element)))

    def quit(self):
        print("Quit driver")
        self.driver.quit()

    def refresh(self):
        print("Refresh page")
        self.driver.refresh()

    def execute_script(self, script: str):
        print(f"Execute script: {script}")
        self.driver.execute_script(script)

    def execute_script_with_element(self, element, script: str):
        self.driver.execute_script(script, element)

    def go_to(self, url: str):
        self.driver.get(url)

    def network_error(self):
        try:
            class_body = self.driver.find_element_by_xpath("//body")
            empty_state_div = self.driver.find_element_by_xpath("//div[contains(@class, 'empty-state')]")
            if 'neterror' in class_body.get_attribute("class") or empty_state_div is not None:
                print("XXXXXXXXXXXXXXXXXX HAS NETWORK ERROR XXXXXXXXXXXXXXXXXX")
                return True
        except NoSuchElementException as no_element:
            pass

    def click_script_js(self, script: str):
        try:
            print(f"Click using javascript: {script}")
            self.driver.execute_script(script)
        except JavascriptException:
            pass

    def click_path(self, xpath: str, path: str, max_exception_count=1, safe_wait=None):
        exception_count = 0
        for _ in range(max_exception_count):
            try:
                print(f"Click using path: {xpath}, {path}")
                wait_element = WebDriverWait(self.driver, 3).until(
                    lambda driver: driver.find_element_by_xpath(xpath))
                wait_element.click()
                if safe_wait:
                    WebDriverWait(self.driver, 3).until_not(lambda driver: driver.find_element_by_xpath(xpath))
                sleep(5)
                break
            except ElementClickInterceptedException:
                self.click_script_js(f'''document.querySelector('{path}').click()''')
                sleep(5)
                break
            except (TimeoutException, NoSuchElementException) as error:
                print(f"TimeoutException, NoSuchElementException click_path(): {xpath}, {path}")
                print(error)
                pass
            except StaleElementReferenceException as error:
                exception_count += 1
                if exception_count >= max_exception_count:
                    print(f'StaleElementReferenceException click_path() can not click: {xpath}, {path}')
                    print(error)
                    raise
                sleep(5)

    def find_element_by_xpath(self, xpath: str, wait=0.25):
        try:
            return WebDriverWait(self.driver, wait).until(
                lambda driver: self.driver.find_element(by=By.XPATH, value=xpath))
        except (TimeoutException, NoSuchElementException):
            pass

    def find_elements_by_xpath(self, xpath: str, wait=0.25):
        try:
            return WebDriverWait(self.driver, wait).until(
                lambda driver: self.driver.find_elements(by=By.XPATH, value=xpath))
        except (TimeoutException, NoSuchElementException) as error:
            pass
