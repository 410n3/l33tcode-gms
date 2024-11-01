from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse
import os
import sys

@dataclass
class Business:
    """holds business data"""
    name: str = None
    address: str = None
    website: str = None
    category: str = None
    phone_number: str = None
    reviews_count: int = None
    reviews_average: float = None
    latitude: float = None
    longitude: float = None


@dataclass
class BusinessList:
    """holds list of Business objects,
    and save to both excel and csv
    """
    business_list: list[Business] = field(default_factory=list)
    save_at = 'output'
    combined_data_filepath = os.path.join(save_at, "combined_data.xlsx")

    def dataframe(self):
        """transform business_list to pandas dataframe

        Returns: pandas dataframe
        """
        return pd.json_normalize(
            (asdict(business) for business in self.business_list), sep="_"
        )

    def save_to_excel(self):
        """saves pandas dataframe to a single excel (xlsx) file"""

        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)

        if os.path.exists(self.combined_data_filepath):
            existing_data = pd.read_excel(self.combined_data_filepath)
            combined_data = pd.concat([existing_data, self.dataframe()], ignore_index=True)
            combined_data.to_excel(self.combined_data_filepath, index=False, header=not os.path.exists(self.combined_data_filepath))
        else:
            self.dataframe().to_excel(self.combined_data_filepath, index=False)

    def save_to_csv(self, filename):
        """saves pandas dataframe to csv file"""

        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_csv(f"output/{filename}.csv", index=False)

    def save_business_to_excel(self, business, search_for):
        """Saves a single Business object to an Excel file"""
        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)

        business_df = pd.json_normalize(asdict(business), sep="_")

        # Check if the file exists
        if os.path.exists(self.combined_data_filepath):
            existing_data = pd.read_excel(self.combined_data_filepath)
            combined_data = pd.concat([existing_data, business_df], ignore_index=True)
            combined_data.to_excel(self.combined_data_filepath, index=False, header=not os.path.exists(self.combined_data_filepath))
        else:
            business_df.to_excel(self.combined_data_filepath, index=False)

# ... (rest of your code)

# Example usage:
# Assuming you have a Business object called 'business' and a BusinessList called 'business_list'
# business_list.save_business_to_excel(business, "example_search")
from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse
import os
import sys

@dataclass
class Business:
    """holds business data"""
    name: str = None
    address: str = None
    website: str = None
    category: str = None
    phone_number: str = None
    reviews_count: int = None
    reviews_average: float = None
    latitude: float = None
    longitude: float = None


@dataclass
class BusinessList:
    """holds list of Business objects,
    and save to both excel and csv
    """
    business_list: list[Business] = field(default_factory=list)
    save_at = 'output'
    combined_data_filepath = os.path.join(save_at, "combined_data.xlsx")

    def dataframe(self):
        """transform business_list to pandas dataframe

        Returns: pandas dataframe
        """
        return pd.json_normalize(
            (asdict(business) for business in self.business_list), sep="_"
        )

    def save_to_excel(self):
        """saves pandas dataframe to a single excel (xlsx) file"""

        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)

        if os.path.exists(self.combined_data_filepath):
            existing_data = pd.read_excel(self.combined_data_filepath)
            combined_data = pd.concat([existing_data, self.dataframe()], ignore_index=True)
            combined_data.to_excel(self.combined_data_filepath, index=False, header=not os.path.exists(self.combined_data_filepath))
        else:
            self.dataframe().to_excel(self.combined_data_filepath, index=False)

    def save_to_csv(self, filename):
        """saves pandas dataframe to csv file"""

        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_csv(f"output/{filename}.csv", index=False)

    def save_business_to_excel(self, business, search_for):
        """Saves a single Business object to an Excel file"""
        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)

        business_df = pd.json_normalize(asdict(business), sep="_")

        # Check if the file exists
        if os.path.exists(self.combined_data_filepath):
            existing_data = pd.read_excel(self.combined_data_filepath)
            combined_data = pd.concat([existing_data, business_df], ignore_index=True)
            combined_data.to_excel(self.combined_data_filepath, index=False, header=not os.path.exists(self.combined_data_filepath))
        else:
            business_df.to_excel(self.combined_data_filepath, index=False)

# Read search from arguments
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--search", type=str)
parser.add_argument("-t", "--total", type=int)
args = parser.parse_args()

if args.search:
    search_list = [args.search]

if args.total:
    total = args.total
else:
    # If no total is passed, we set the value to a random big number
    total = 1_000_000

if not args.search:
    search_list = []
    # Read search from input.txt file
    input_file_name = 'input.txt'
    # Get the absolute path of the file in the current working directory
    input_file_path = os.path.join(os.getcwd(), input_file_name)
    # Check if the file exists
    if os.path.exists(input_file_path):
        # Open the file in read mode
        with open(input_file_path, 'r') as file:
            # Read all lines into a list
            search_list = file.readlines()

    if len(search_list) == 0:
        print('Error occurred: You must either pass the -s search argument, or add searches to input.txt')
        sys.exit()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://www.google.com/maps", timeout=60000)
    # Wait is added for the development phase. You can remove it in production
    page.wait_for_timeout(5000)

    for search_for_index, search_for in enumerate(search_list):
        print(f"-----\n{search_for_index} - {search_for}".strip())

        page.locator('//input[@id="searchboxinput"]').fill(search_for)
        page.wait_for_timeout(3000)

        page.keyboard.press("Enter")
        page.wait_for_timeout(5000)

        # Scrolling
        page.hover('//a[contains(@href, "https://www.google.com/maps/place")]')

        # This variable is used to detect if the bot
        # scraped the same number of listings in the previous iteration
        previously_counted = 0
        while True:
            page.mouse.wheel(0, 10000)
            page.wait_for_timeout(3000)

            if (
                page.locator(
                    '//a[contains(@href, "https://www.google.com/maps/place")]'
                ).count()
                >= total
            ):
                listings = page.locator(
                    '//a[contains(@href, "https://www.google.com/maps/place")]'
                ).all()[:total]
                listings = [listing.locator("xpath=..") for listing in listings]
                print(f"Total Scraped: {len(listings)}")
                break
            else:
                # Logic to break from loop to not run infinitely
                # in case arrived at all available listings
                if (
                    page.locator(
                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                    ).count()
                    == previously_counted
                ):
                    listings = page.locator(
                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                    ).all()
                    print(f"Arrived at all available\nTotal Scraped: {len(listings)}")
                    break
                else:
                    previously_counted = page.locator(
                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                    ).count()
                    print(
                        f"Currently Scraped: ",
                        page.locator(
                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                        ).count(),
                    )

        business_list = BusinessList()

        # Scraping
        for business_index, listing in enumerate(listings):
            try:
                listing.click()
                page.wait_for_timeout(5000)

                name_xpath = '//h1[@class="DUwDvf lfPIob"]'
                address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
                website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
                phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
                reviews_span_xpath = '//span[@role="img"]'
                category_xpath ='//div[contains(@class, "fontBodyMedium")]//button[contains(@class, "DkEaL")]'


                business = Business()

                if page.locator(name_xpath).count() > 0:
                    business.name = page.locator(name_xpath).inner_text()
                else:
                    business.name = ""
                if page.locator(address_xpath).count() > 0:
                    business.address = page.locator(address_xpath).all()[0].inner_text()
                else:
                    business.address = ""
                if page.locator(website_xpath).count() > 0:
                    business.website = page.locator(website_xpath).all()[0].inner_text()
                else:
                    business.website = ""
                if page.locator(phone_number_xpath).count() > 0:
                    business.phone_number = page.locator(phone_number_xpath).all()[0].inner_text()
                else:
                    business.phone_number = ""

                if page.locator(category_xpath).count() > 0:
                    business.category = page.locator(category_xpath).all()[0].inner_text()
                else:
                    business.category = ""

                
                if listing.locator(reviews_span_xpath).count() > 0:
                    business.reviews_average = float(
                        listing.locator(reviews_span_xpath).all()[0]
                        .get_attribute("aria-label")
                        .split()[0]
                        .replace(",", ".")
                        .strip()
                    )
                    business.reviews_count = int(
                        listing.locator(reviews_span_xpath).all()[0]
                        .get_attribute("aria-label")
                        .split()[2]
                        .replace(',','')
                        .strip()
                    )
                else:
                    business.reviews_average = ""
                    business.reviews_count = ""
                

                #business.latitude, business.longitude = extract_coordinates_from_url(page.url)

                business_list.business_list.append(business)

                # Print the business data after processing each listing
                print(f"Business {business_index + 1}: {business}")

                # Save the business data after processing each listing
                business_list.save_business_to_excel(
                    business,
                    search_for
                )
            except Exception as e:
                print(f'Error occurred: {e}')

        # Save the entire list after processing all listings for a search query
        business_list.save_to_csv(f"google_maps_data_{search_for}".replace(' ', '_'))

    browser.close()
