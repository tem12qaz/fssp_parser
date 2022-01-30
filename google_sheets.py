import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials

CREDENTIALS_FILE = 'creds.json'  # Имя файла с закрытым ключом, вы должны подставить свое

# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])

TABLE_ID = '1No37zLjP4TuxsgcA0_JIj-_7lpIRAdjb-bBOQ-nG1to'


def add_to_table(data):
    httpAuth = credentials.authorize(httplib2.Http())  # Авторизуемся в системе
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)  # Выбираем работу с таблицами и 4 версию API

    rangeAll = '{0}!A2:Z1000'.format('Парсер')
    body = {}
    resultClear = service.spreadsheets().values().clear(spreadsheetId=TABLE_ID, range=rangeAll,
                                                        body=body).execute()

    service.spreadsheets().values().batchUpdate(spreadsheetId=TABLE_ID, body={
        "valueInputOption": "USER_ENTERED",  # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": [
            {"range": "Парсер!A2:Z1000",
             "majorDimension": "ROWS",  # Сначала заполнять строки, затем столбцы
             "values": data}
        ]
    }).execute()
