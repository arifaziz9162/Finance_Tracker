import pandas as pd 
import csv
import matplotlib.pyplot as plt
from datetime import datetime
from data_entry import get_date, get_amount, get_category, get_description
from logger_config import logger

# -------------------------------------- Custom Exception -----------------------------------
class FinanceError(Exception):
    """Custom Exception class for finance tracker related errors."""
    pass

class CSVInitializationError(FinanceError):
    """Raised when CSV initialization fails."""
    def __init__(self, message="Failed to initialize csv fails."):
        super().__init__(message)

class CSVWriteError(FinanceError):
    """Raised when writing to CSV fails."""
    def __init__(self, message="Failed to write entry to csv file."):
        super().__init__(message)

class CSVReadError(FinanceError):
    """Raised when reading CSV fails."""
    def __init__(self, message="Failed to read data from CSV file."):
        super().__init__(message)

class ScatterPlotError(FinanceError):
    """Raised when generate scatter plot fails."""
    def __init__(self, message="Failed to generate scatter plot."):
        super().__init__(message)

# --------------------------------------- Finance Tracker Class ---------------------------------------
class FinanceTracker:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            try:
                df = pd.DataFrame(columns=cls.COLUMNS)
                df.to_csv(cls.CSV_FILE, index=False)
                logger.info("CSV file created successfully.")
            except Exception as e:
                logger.error("An unexpected error occurred while initializing CSV file: %s", e, exc_info=True)
                raise CSVInitializationError() from e

    @classmethod
    def add_entry(cls, date, amount, category, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "category": category,
            "description": description
        }
        try:
            with open(cls.CSV_FILE, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=cls.COLUMNS)
                writer.writerow(new_entry)

            print("Entry added successfully.")
            logger.info(f"New entry added: {new_entry}")
        except Exception as e:
            logger.error("An unexpected error occurred while writing entry to CSV file: %s", e, exc_info=True)
            raise CSVWriteError() from e

    @classmethod
    def get_transaction(cls, start_date, end_date):
        try:
            df = pd.read_csv(cls.CSV_FILE)
            df["date"] = pd.to_datetime(df["date"], format=FinanceTracker.FORMAT)
            start_date = datetime.strptime(start_date, FinanceTracker.FORMAT)
            end_date = datetime.strptime(end_date, FinanceTracker.FORMAT)

            mask = (df["date"] >= start_date) & (df["date"] <= end_date)
            filtered_df = df.loc[mask]

            if filtered_df.empty:
                print("No transaction found in the given date range.")
            else:
                print(
                    f"Transaction from {start_date.strftime(FinanceTracker.FORMAT)} to {end_date.strftime(FinanceTracker.FORMAT)}"
                )
                print(
                    filtered_df.to_string(
                        index=False, formatters={"date": lambda x: x.strftime(FinanceTracker.FORMAT)}
                    )
                )

                total_income = filtered_df[filtered_df["category"] == "Income"] ["amount"].sum()
                total_expense = filtered_df[filtered_df["category"] == "Expense"] ["amount"].sum()
                print("\nSummary:")
                print(f"Total Income: ${total_income:.2f}")
                print(f"Total Expense: ${total_expense:.2f}")
                print(f"Net Savings: ${(total_income - total_expense):.2f}")

                logger.info("Displayed transaction and summary between %s to %s", start_date, end_date)

            return filtered_df
        except Exception as e:
            logger.error("An unexpected error occurred while reading transaction from CSV file: %s", e, exc_info=True)
            raise CSVReadError() from e
        

def add():
    try:
        FinanceTracker.initialize_csv()
        date = get_date(
            "Enter the date of the transaction (dd-mm-yyyy) or press enter for today's date: ",
            allow_default=True
        )
        amount = get_amount()
        category = get_category()
        description = get_description()
        FinanceTracker.add_entry(date, amount, category, description)

        print("\n------------ Final Entry --------------")
        print(f"Date: {date}")
        print(f"Amount: {amount}")
        print(f"Category: {category}")
        print(f"Description: {description}")
    except FinanceError as fe:
        logger.error("FinanceError %s", fe, exc_info=True)
        print(f"Error: {fe}")
    except Exception as e:
        logger.error("An unexpected error occurred while entrying add: %s", e, exc_info=True)
        print("Failed to add entry.")

def scatter_transactions(df):
    try:
        if df.empty:
            logger.warning("Scatter plot skiped because dataframe is empty.")
            print("No data available for scatter plot.")
            return
        df.set_index("date", inplace=True)

        income_df = (df[df["category"] == "Income"])
        expense_df = (df[df["category"] == "expense"])
        
        plt.figure(figsize=(10, 5))
        plt.scatter(income_df.index, income_df["amount"], label="Income", color="g")
        plt.scatter(expense_df.index, expense_df["amount"], label="Expense", color="r")
        plt.xlabel("Date")
        plt.ylabel("Amount")
        plt.title("Income and Expenses Over Time")
        plt.legend()
        plt.grid(True)
        plt.show()
        
        logger.info("Scatter plot displayed successfully.",
            len(income_df), len(expense_df))

    except Exception as e:
        logger.error("An unexpexted error occurred while creating scatter plot: %s", e, exc_info=True)
        raise ScatterPlotError() from e

def main():
    while True:
        print("\n1. Add a new transaction")
        print("\n2. View transaction and summary within a date range")
        print("\n3. Exit the program.")
        try:
            choice = int(input("Enter your choice (1-3): "))

            if choice == 1:
                add()
            elif choice == 2:
                start_date = get_date("Enter the start date (dd-mm-yyyy): ")
                end_date = get_date("Enter the end date (dd-mm-yyyy): ")
                df = FinanceTracker.get_transaction(start_date, end_date)
                if input("Do you want to see a scatter plot? (y/n): ").lower() == "y":
                    scatter_transactions(df)
            elif choice == 3:
                print("Exiting....")
                logger.info("Program exited by user.")
                break
            else:
                print("Invalid choice. Please enter (1, 2, or 3).")
                logger.warning("Invalid menu choice entered: %s", choice)
        except ValueError as ve:
            logger.error("Invalid input. Please enter a numeric (1-3).")
            print("User entered non numeric menu choice.")
        except Exception as e:
            logger.error("An unexpected error occurred while running in main: %s", e, exc_info=True)
            print("Failed to run main.")


if __name__ == "__main__":
    main()