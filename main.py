import os
from time import sleep
from dotenv import load_dotenv
from alpha_driver import AlphaDriver
from alpha_bot import AlphaBot
from alpha_gspread import AlphaGspread

load_dotenv()
chrome_driver_filename = os.getenv('CHROME_DRIVER_FILENAME')
profile_path = os.getenv('PROFILE_PATH')
service_account_filename = os.getenv('SERVICE_ACCOUNT_FILENAME')
headless = False
alpha_driver = AlphaDriver(chrome_driver_filename=chrome_driver_filename, profile_path=profile_path, headless=headless)
alpha_bot = AlphaBot(alpha_driver)
alpha_gspread = AlphaGspread(service_account_filename)
#####

def start():
    all_projects = []
    sleep(3)
    month, year = alpha_bot.get_current_month_year()
    date_elements = alpha_bot.get_all_date_elements()
    for date_element in date_elements:
        projects = alpha_bot.get_projects_by_date_element(date_element)
        all_projects.extend(projects)
    alpha_gspread.insert(month, all_projects)


if __name__ == "__main__":
    start()


