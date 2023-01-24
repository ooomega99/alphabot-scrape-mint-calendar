import gspread
from time import sleep
from gspread.utils import ValueInputOption
from models.nft_project import  SocialMedia, AttributeCategory


class AlphaGspread:
    def __init__(self, service_account_filename):
        self.service_account = gspread.service_account(filename=service_account_filename)
        self.sheet = self.service_account.open("AlphaBot Mint Calendar 2023 - Public")

    def insert(self, month, projects):
        worksheet_list = self.sheet.worksheets()
        selected_worksheet = None
        for worksheet in worksheet_list:
            print(f'worksheet: {worksheet.title}')
            if worksheet.title == month:
                selected_worksheet = worksheet
        if selected_worksheet is None:
            selected_worksheet = self.sheet.add_worksheet(title=month, rows=100, cols=20)
        selected_worksheet.clear()
        # Insert title
        selected_worksheet.format('A1:Z1', {'textFormat': {'bold': True}})
        titles = [ 'Datetime','Picture','Background', 'Name' ]
        for en in AttributeCategory:
            titles.append(en.value)
        for en in SocialMedia:
            titles.append(en.value)
        selected_worksheet.append_row(titles)
        # Insert data
        for project in projects:
            selected_worksheet.append_row(project.to_list(), value_input_option=ValueInputOption.user_entered)
            sleep(1.5)

        # Auto width
        body = {
            "requests": [
                {
                    "updateDimensionProperties": {
                        "range": {
                            "sheetId": str(selected_worksheet.id),
                            "dimension": "COLUMNS",
                            "startIndex": 0,
                            "endIndex": 1
                        },
                        "properties": {
                            "pixelSize": 100
                        },
                        "fields": "pixelSize"
                    }
                }
            ]
        }
        self.sheet.batch_update(body)


