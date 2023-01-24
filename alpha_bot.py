from selenium.webdriver.common.by import By
from datetime import datetime
from time import sleep
from models.nft_project import NftProject, SocialMediaNft, AttributeNft, SocialMedia, AttributeCategory


class AlphaBot:
    def __init__(self, alpha_driver):
        self.alpha_driver = alpha_driver
        self.alpha_driver.go_to('https://www.alphabot.app/calendar')

    def get_current_month_year(self):
        month_year_xpath = "//div[contains(@class, 'PrivatePickersFadeTransitionGroup-root css-1bx5ylf')]"
        month_year_elements = self.alpha_driver.find_elements_by_xpath(month_year_xpath)
        month = None
        year = None
        for i, month_year_element in enumerate(month_year_elements):
            index_path = i + 1
            path = f"{month_year_xpath}[{index_path}]/div"
            element = self.alpha_driver.find_element_by_xpath(path)
            if i == 0:
                # month = datetime.strptime(element.text, '%B').month
                month = element.text
            else:
                # year = datetime.strptime(element.text, '%Y').year
                year = int(element.text)
        return month, year

    def get_all_date_elements(self):
        # Wait until
        self.alpha_driver.wait_until(by=By.CLASS_NAME, element="MuiButtonBase-root  MuiBox-root css-1te450d")
        date_elements = []
        rows_xpath = "//div[contains(@class, 'css-mvmu1r')]"
        row_elements = self.alpha_driver.find_elements_by_xpath(rows_xpath, wait=3)
        for i, row_element in enumerate(row_elements):
            i += 1
            row_path = f"{rows_xpath}[{i}]/button"
            row_detail_elements = self.alpha_driver.find_elements_by_xpath(row_path, wait=5)
            for j, row_detail_element in enumerate(row_detail_elements):
                att_class = row_detail_element.get_attribute("class")
                if 'outsideCurrentMonth' in att_class:
                    continue
                date_elements.append(row_detail_element)
        return date_elements

    def hide_project_dialog(self):
        xpath = "//div[contains(@class, " \
                "'MuiBackdrop-root MuiBackdrop-invisible css-esi9ax')]"
        dialog_element = self.alpha_driver.find_element_by_xpath(xpath)
        self.alpha_driver.execute_script_with_element(dialog_element, "arguments[0].click();")

    def get_projects_by_date_element(self, date_element):
        date_element.click()
        projects = []
        # Month & year
        month_date_xpath = f"//div[contains(@class, 'MuiBox-root css-1wn58un')]/span[1]"
        month_date_element = self.alpha_driver.find_element_by_xpath(month_date_xpath)
        if month_date_element is None:
            return projects
        month_date = month_date_element.text
        year_xpath = f"//div[contains(@class, 'MuiBox-root css-1wn58un')]/span[2]"
        year_element = self.alpha_driver.find_element_by_xpath(year_xpath)
        year = year_element.text.replace(', ', '')
        print(f'Month date: {month_date}, Year: {year}')
        # Mint project
        mint_project_xpath = f"//div[contains(@class, 'MuiBox-root css-3jiy5t')]/div[1]/div"
        mint_project_elements = self.alpha_driver.find_elements_by_xpath(mint_project_xpath)
        for i, mint_project_element in enumerate(mint_project_elements):
            i += 1
            projects_xpath = f"{mint_project_xpath}[{i}]/div/div"
            project_elements = self.alpha_driver.find_elements_by_xpath(projects_xpath)
            if project_elements is None:
                continue
            for j, project_element in enumerate(project_elements):
                project_element.click()
                project = self.__get_mint_project_in_dialog()
                projects.append(project)
                self.hide_project_dialog()
        # Also mint project
        also_mint_project_xpath = f"//div[contains(@class, 'MuiBox-root css-3jiy5t')]/div[2]/div/div"
        also_mint_project_elements = self.alpha_driver.find_elements_by_xpath(also_mint_project_xpath)
        if also_mint_project_elements is not None:
            for j, project_element in enumerate(also_mint_project_elements):
                project_element.click()
                project = self.__get_mint_project_in_dialog()
                projects.append(project)
                self.hide_project_dialog()
        for project in projects:
            print(f'Project: {project}')
        return projects

    def __get_mint_project_in_dialog(self):
        sleep(1)
        project_dialog_xpath = "//div[contains(@class, 'MuiPopover-paper')]/div"
        project_dialog_element = self.alpha_driver.find_element_by_xpath(project_dialog_xpath)
        assert project_dialog_element
        parts_project_dialog_xpath = f"{project_dialog_xpath}/div"
        part_project_elements = self.alpha_driver.find_elements_by_xpath(parts_project_dialog_xpath)
        project_name = None
        profile_url = None
        background_url = None
        datetime_mint = None
        social_medias = []
        attributes = []
        for i, part_project_element in enumerate(part_project_elements):
            if i == 0:
                # Name
                name_xpath = f"{parts_project_dialog_xpath}[{i+1}]/p"
                name_element = self.alpha_driver.find_element_by_xpath(name_xpath)
                project_name = name_element.text
                # Profile picture
                profile_picture_xpath = f"{parts_project_dialog_xpath}[{i+1}]/div/img"
                profile_picture_element = self.alpha_driver.find_element_by_xpath(profile_picture_xpath)
                if profile_picture_element is not None:
                    profile_url = profile_picture_element.get_attribute("src")
                # Background URL
                background_image_text = part_project_element.value_of_css_property("background-image")
                if 'undefined' not in background_image_text:
                    background_url = background_image_text.split('"')[1]
                print(f'Name: {project_name}, picture url: {profile_url}')
            if i == 1:
                # Datetime
                datetime_xpath = f"{parts_project_dialog_xpath}[{i + 1}]/p"
                datetime_element = self.alpha_driver.find_element_by_xpath(datetime_xpath)
                if ':' in datetime_element.text:
                    date_time_obj = datetime.strptime(datetime_element.text, '%b %d, %I:%M %p')
                    datetime_mint = date_time_obj.replace(year=2023)
                else:
                    date_time_obj = datetime.strptime(datetime_element.text, '%A, %b %d')
                    datetime_mint = date_time_obj.replace(year=2023, hour=23, minute=59, second=59)
                # Social media
                social_media_xpath = f"{parts_project_dialog_xpath}[{i + 1}]/div/a"
                social_media_elements = self.alpha_driver.find_elements_by_xpath(social_media_xpath)
                for social_media_element in social_media_elements:
                    name = social_media_element.get_attribute("aria-label")
                    url = social_media_element.get_attribute("href").replace('?utm_source=alphabot.app', '')
                    social_medias.append(SocialMediaNft(SocialMedia(name), url))
            if i == 2:
                # Attribute
                attributes_xpath = f"{parts_project_dialog_xpath}[{i + 1}]/div"
                attribute_elements = self.alpha_driver.find_elements_by_xpath(attributes_xpath, wait=1)
                if attribute_elements is None:
                    continue
                for j, attribute_element in enumerate(attribute_elements):
                    attribute_xpath = f"{attributes_xpath}[{j + 1}]/span"
                    key_xpath = f"{attribute_xpath}/span"
                    value_xpath = f"{attribute_xpath}/b"
                    key_element = self.alpha_driver.find_element_by_xpath(key_xpath)
                    value_element = self.alpha_driver.find_element_by_xpath(value_xpath)
                    key = key_element.text
                    value = value_element.text
                    if key == 'Supply' and 'K' in value:
                        value = value.replace('K', '')
                        value = str(int(float(value) * 1000))
                    attributes.append(AttributeNft(AttributeCategory(key_element.text), value))
        return NftProject(project_name, background_url, profile_url, datetime_mint, social_medias, attributes)

