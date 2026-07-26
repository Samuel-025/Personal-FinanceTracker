from datetime import datetime

date_format = "%d-%m-%Y"


def get_date(prompt, allow_default=False):
    date_str = input(prompt)
    if allow_default and not date_str:
        return datetime.today().strftime("%d-%m-%Y")

    try:
        valid_date = datetime.strptime(date_str, "%d-%m-%Y")
        return valid_date.strftime("%d-%m-%Y")
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-yyyy format.")
        return get_date(prompt, allow_default)


def get_amount():
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            print("Amount must be a positive number greater than 0.")
            return get_amount()
        return amount
    except ValueError:
        print("Invalid input. Please enter a valid numerical amount.")
        return get_amount()


def get_description():
    return input("Enter a description (optional): ")
