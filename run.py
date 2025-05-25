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


# def update_sales_worksheet(data):
#     """update sales worksheet, add new row with the list data provided """
#     print('Updating sales worksheet...\n')
#     sales_worksheet = SHEET.worksheet("sales")
#     sales_worksheet.append_row(data)
#     print("Sales updated successfully.\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type. The surplus is defined as the sales figure subtracted from stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet('stock').get_all_values()
    stock_row = stock[-1]
    stock_row_int = [int(value) for value in stock_row]
    surplus_row = []
    for num1, num2 in zip(stock_row_int, sales_row):
        surplus_row.append(num1-num2)
    return surplus_row


def update_worksheet(data, worksheet_type):
    """
    Update the result of surplus data in the spreadsheet
    """
    print("Updating surplus worksheet... \n")
    worksheet = SHEET.worksheet(worksheet_type)
    worksheet.append_row(data)
    print(f"{worksheet_type}update successfully")


def main():
    """Run all program functions"""
    data = get_sales_data()
    update_worksheet(data, 'sales')
    surplus_result = calculate_surplus_data(data)
    update_worksheet(surplus_result, 'surplus')


print("Welcome to love Love Sandwiches Data Automation")
main()
