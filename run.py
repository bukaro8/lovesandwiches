import gspread
from google.oauth2.service_account import Credentials
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPE_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPE_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")

# sales = SHEET.worksheet('sales')

# data = sales.get_all_values()
# print(data)


def get_sales_data():
    """Get sales figures input form the user """
    print("Please enter sales data form the last market\nData should be six numbers, separated by commas\nExample 10,20,30,40,50,60\n")
    while True:
        data_str = input('Enter your data here: ')
        sales_data = data_str.split(",")
        validated_data = validate_data(sales_data)
        if validated_data is not None:
            return validated_data


def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if string cannot be converted into int,
    or if there aren't exactly 6 values
    """
    try:
        if len(values) != 6:
            raise ValueError(
                f"Data must be six numbers, separated by commas. you entered {len(values)}")
        int_values = [int(value) for value in values]
        return int_values
    except ValueError as e:
        print(e)
        return None


data = get_sales_data()
print(data)
