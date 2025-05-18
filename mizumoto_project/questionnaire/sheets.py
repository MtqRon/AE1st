import gspread
from google.oauth2 import service_account  # pip install -U google-auth

dataTypes = [
    "time",
    "sex",
    "age",
    "region",
    "purpose",
    "evaluation",
    "comment",
    "is_mail",
    "mail",
]

getlines = 3000

def connect_gspread(sheetNumber=1):
    print("スプレッドシートに接続中...")
    # ここでjsonfile名と2-2で用意したkeyを入力
    jsonf = r"mizumoto-project-04a7d8805a5f.json"
    key = "1atjb5GSACPgYQEe6pZzFkhhDm875I9geraHscFPXyjQ"
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = service_account.Credentials.from_service_account_file(jsonf)
    scopedCredentials = credentials.with_scopes(scope)
    gc = gspread.authorize(scopedCredentials)
    SPREADSHEET_KEY = key
    if sheetNumber == 1:
        worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
    else:
        worksheet = gc.open_by_key(
            SPREADSHEET_KEY).get_worksheet(sheetNumber - 1)

    return worksheet

def getData(line, dataType):
    if line > len(data):
        return "error"

    if dataType in dataTypes:
        index = dataTypes.index(dataType)
        return data[line - 1][index]
    else:
        return "error"


def getLineFromData(dataType, value):
    value = str(value)
    if dataType in dataTypes:
        for i in range(2, getlines):
            if getData(i, dataType) == value:
                return i
        return "error"
    else:
        return "error"


def setData(line, dataType, value):
    if dataType in dataTypes:
        index = dataTypes.index(dataType)
        dataSheet.update_cell(line, index + 1, value)
        return "ok"
    else:
        return "error"


def getNotRegistedLine():
    global data
    data = dataSheet.get_all_values()

    for i in range(1, getlines):
        if getData(i, "mail") == "":
            return i


def getNewLine():
    global data
    data = dataSheet.get_all_values()
    for i in range(1, getlines):
        if getData(i, "id") == "":
            return i


dataSheet = connect_gspread(1)
data = dataSheet.get_all_values()