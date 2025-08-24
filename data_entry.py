from datetime import datetime
from logger_config import logger

date_format = "%d-%m-%Y"
CATEGORIES = {
    "I": "Income", 
    "E": "Expense"
}

# -------------------------------------- Custom Exception ---------------------------------------
class DataEntryError(Exception):
    """Custom Exception class for data entry related errors."""
    pass

class InvalidDateError(DataEntryError):
    """Raised when an invalid date format."""
    def __init__(self, message="Date must be in dd-mm-yyyy format."):
        super().__init__(message)

class InvalidAmountError(DataEntryError):
    """Raise when an invalid amount."""
    def __init__(self, message="Amount must be a non-negative and non-zero value."):
        super().__init__(message)

class InvalidCategoryError(DataEntryError):
    """Raised when an invalid category choose."""
    def __init__(self, message="Invalid category. Please enter 'I' for Income and 'E' for Expense."):
        super().__init__(message)

class DescriptionError(DataEntryError):
    """Raise when an description is empty."""
    def __init__(self, message="Description cannot be empty."):
        super().__init__(message)

# --------------------------------------- Data Entry Class -----------------------------------------
class DataEntry:
    def __init__(self, date=None, amount=None, category=None, description=None):
        try:
            self.date = date
            self.amount = amount
            self.category = category
            self.description = description
            logger.info("Data entry class initialized successfully.")
        except Exception as e:
            logger.error("An unexpected error occurrred while initializing data: %s", e, exc_info=True)
            raise DataEntryError("Failed to initialize data.")    

    def get_date(self, prompt="Enter date (dd-mm-yyyy): ", allow_default=False):
        """Get a valid date from user, allow default (today) if enabled."""
        while True:
            try:
                date_input = input(prompt).strip()
                if allow_default and date_input == "":
                    return datetime.today().strftime("%d-%m-%Y")
                return datetime.strptime(date_input, "%d-%m-%Y").strftime("%d-%m-%Y")
            except ValueError as ve:
                logger.error("Invalid date format entered: %s", ve, exc_info=True)
                print("Invalid date format. Please use dd-mm-yyyy")
                raise InvalidDateError() from ve
        
    def get_amount(self):
        try:
            amount = float(input("Enter the amount: "))
            if amount <= 0:
                raise InvalidAmountError()
            return amount
        except ValueError as ve:
            logger.error("An unexpected error while entering amount: %s", ve, exc_info=True)
            raise InvalidAmountError() from ve

    def get_category(self):
        try:
            category = input("Enter the category ('I' for Income and 'E' for Expense): ").upper()
            if category in CATEGORIES:
                return CATEGORIES[category]
            else:
                logger.error("Invalid category entered: %s", category, exc_info=True)
                raise InvalidCategoryError()
        except ValueError as ve:
            logger.error("An unexpected error while getting category: %s", ve, exc_info=True)
            raise InvalidCategoryError() from ve

    def get_description(self):
        description = input("Enter description: ").strip()
        if not description:
            raise DescriptionError()

        logger.info(f"Description entered: {description}")
        return description

# --------------------------------------- Wrapper Function For Enternal Use ---------------------------------------
entry = DataEntry()

def get_date(prompt="Enter date (dd-mm-yyyy): ", allow_default=False):
    """Wrapper function to run get_data."""
    return entry.get_date(prompt=prompt, allow_default=allow_default)

def get_amount():
    """Wrapper function to run get_amount."""
    return entry.get_amount()

def get_category():
    """Wrapper function to run get_category."""
    return entry.get_category()

def get_description():
    """Wrapper function to run get_description."""
    return entry.get_description()