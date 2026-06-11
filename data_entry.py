from datetime import datetime

DATE_FORMAT = "%d-%m-%Y"
CATEGORIES = {"I": "Income", "E": "Expense"}


def get_date(prompt, allow_default=False):
    """
    BUG FIX: Typo "Invalid date frmat. Please entr..." corrected.
    """
    date_str = input(prompt).strip()
    if allow_default and not date_str:
        return datetime.today().strftime(DATE_FORMAT)
    try:
        valid_date = datetime.strptime(date_str, DATE_FORMAT)
        return valid_date.strftime(DATE_FORMAT)
    except ValueError:
        print("Invalid date format. Please enter the date in dd-mm-yyyy format.")
        return get_date(prompt, allow_default)


def get_amount():
    """
    BUG FIX: Error message said "Account must be..." instead of "Amount must be...".
    """
    try:
        amount = float(input("Enter the amount: "))
        if amount <= 0:
            raise ValueError("Amount must be a non-zero positive value.")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()


def get_category():
    category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()
    if category in CATEGORIES:
        return CATEGORIES[category]
    print("Invalid category. Please enter 'I' for Income or 'E' for Expense.")
    return get_category()


def get_description():
    return input("Enter a description (optional): ").strip()
