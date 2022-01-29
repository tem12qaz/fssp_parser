import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'creds.json'  # Имя файла с закрытым ключом, вы должны подставить свое

# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])

TABLE_ID = '1AJAH1xoMbFQpdhInkIXbqHcQt3KyUPHICtT-b0xXWtM'


def add_to_table(data):
    httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)  # Выбираем работу с таблицами и 4 версию API

    service.spreadsheets().values().batchUpdate(spreadsheetId=TABLE_ID, body={
        "valueInputOption": "USER_ENTERED",  # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": [
            {"range": "list_2!A2:",
             "majorDimension": "ROWS",  # Сначала заполнять строки, затем столбцы
             "values": data}
        ]
    }).execute()
