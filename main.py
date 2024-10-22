import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import logging
import csv
from datetime import datetime


class GmailAccountCreator:
    def __init__(self, chrome_driver_path):
        """Initialize the account creator with webdriver path and setup logging"""
        self.driver_path = chrome_driver_path
        self.setup_logging()

    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            filename=f'account_creation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s",
        )

    def generate_username(self, first_name, last_name, dob):
        """Generate a username based on personal information"""
        birth_year = dob.split("/")[-1]
        username = f"{first_name.lower()}.{last_name.lower()}{birth_year[-2:]}"
        return username

    def create_account(self, first_name, last_name, dob):
        """
        Create a Gmail account for an individual
        Returns tuple: (success: bool, username: str, error_message: str)
        """
        driver = webdriver.Chrome(self.driver_path)
        username = self.generate_username(first_name, last_name, dob)

        try:
            # Navigate to Gmail signup
            driver.get("https://accounts.google.com/signup")

            # Add appropriate delays between actions
            wait = WebDriverWait(driver, 10)

            # Fill in the form (you'll need to update selectors based on current Gmail signup page)
            first_name_field = wait.until(
                EC.presence_of_element_located((By.NAME, "firstName"))
            )
            first_name_field.send_keys(first_name)

            # Log the attempt
            logging.info(f"Attempting to create account for {first_name} {last_name}")

            # Add random delay between actions (2-5 seconds)
            time.sleep(random.uniform(2, 5))

            # NOTE: Additional form filling code would go here
            # This is a simplified version - you'll need to add all required fields

            return True, username, ""

        except TimeoutException as e:
            error_msg = (
                f"Timeout while creating account for {first_name} {last_name}: {str(e)}"
            )
            logging.error(error_msg)
            return False, username, error_msg

        except Exception as e:
            error_msg = f"Error creating account for {first_name} {last_name}: {str(e)}"
            logging.error(error_msg)
            return False, username, error_msg

        finally:
            driver.quit()

    def process_batch(self, input_csv_path, output_csv_path):
        """
        Process a batch of accounts from CSV file
        CSV format: first_name,last_name,dob
        """
        with open(input_csv_path, "r") as input_file, open(
            output_csv_path, "w", newline=""
        ) as output_file:

            reader = csv.DictReader(input_file)
            writer = csv.writer(output_file)
            writer.writerow(
                [
                    "first_name",
                    "last_name",
                    "dob",
                    "username",
                    "status",
                    "error_message",
                ]
            )

            for row in reader:
                # Add delay between accounts (30-60 seconds)
                time.sleep(random.uniform(30, 60))

                success, username, error = self.create_account(
                    row["first_name"], row["last_name"], row["dob"]
                )

                writer.writerow(
                    [
                        row["first_name"],
                        row["last_name"],
                        row["dob"],
                        username,
                        "success" if success else "failed",
                        error,
                    ]
                )


def main():
    creator = GmailAccountCreator("path/to/chromedriver")
    creator.process_batch("input.csv", "output.csv")


if __name__ == "__main__":
    main()
