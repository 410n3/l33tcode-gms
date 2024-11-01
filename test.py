import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import os

@dataclass
class Business:
    """Holds business data."""
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
    """Holds list of Business objects and saves to Excel/CSV."""
    business_list: list[Business] = field(default_factory=list)
    save_at = 'output'
    combined_data_filepath = os.path.join(save_at, "combined_data.xlsx")

    def dataframe(self):
        """Transform business_list to pandas dataframe."""
        return pd.json_normalize((asdict(business) for business in self.business_list), sep="_")

    def save_to_excel(self):
        """Save dataframe to Excel."""
        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        if os.path.exists(self.combined_data_filepath):
            existing_data = pd.read_excel(self.combined_data_filepath)
            combined_data = pd.concat([existing_data, self.dataframe()], ignore_index=True)
            combined_data.to_excel(self.combined_data_filepath, index=False)
        else:
            self.dataframe().to_excel(self.combined_data_filepath, index=False)

    def save_to_csv(self, filename):
        """Save dataframe to CSV."""
        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_csv(f"output/{filename}.csv", index=False)

class L33TCODEGMSApp:
    def __init__(self, root):
        self.root = root
        self.root.title("L33TCODE GMS - Google Map Scraper")
        self.root.geometry("600x400")
        self.create_widgets()
        
    def create_widgets(self):
        title_label = tk.Label(self.root, text="L33TCODE GMS", font=("Arial", 16))
        title_label.pack(pady=10)
        
        instruction_label = tk.Label(self.root, text="Reads search terms from 'input.txt'")
        instruction_label.pack()
        
        save_frame = tk.Frame(self.root)
        save_frame.pack(pady=20)
        
        save_label = tk.Label(save_frame, text="Save as:")
        save_label.grid(row=0, column=0, padx=5)
        
        self.save_option = ttk.Combobox(save_frame, values=["Excel", "CSV"])
        self.save_option.grid(row=0, column=1)

        run_button = tk.Button(self.root, text="Run Scraper", command=self.run_scraper)
        run_button.pack(pady=10)

        # Text area to display results
        self.result_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, width=70, height=10)
        self.result_text.pack(pady=10)

    def run_scraper(self):
        save_format = self.save_option.get()
        input_file_name = 'input.txt'
        input_file_path = os.path.join(os.getcwd(), input_file_name)

        if not os.path.exists(input_file_path):
            messagebox.showerror("File Not Found", f"{input_file_name} is missing.")
            return

        with open(input_file_path, 'r') as file:
            search_list = [line.strip() for line in file.readlines()]

        if not search_list:
            messagebox.showwarning("Empty File", "No search terms found in input.txt.")
            return
        
        messagebox.showinfo("Scraping Started", "Scraping initiated...")
        business_list = BusinessList()
        result_display = []

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://www.google.com/maps")
            
            for search_term in search_list:
                page.fill('//input[@id="searchboxinput"]', search_term)
                page.press('//input[@id="searchboxinput"]', "Enter")
                page.wait_for_timeout(5000)  # Wait for results to load

                # Add your scraping logic here. For demonstration, we simulate results.
                # Here you will add the actual scraping logic to collect the business details
                # For example:
                # business = Business(name="Example", address="123 Example St", ...)
                # business_list.business_list.append(business)
                
                # Simulated data for demonstration (replace this with actual scraping)
                business = Business(name=search_term, address="123 Example St", website="www.example.com", 
                                    category="Restaurant", phone_number="123-456-7890", 
                                    reviews_count=100, reviews_average=4.5)
                business_list.business_list.append(business)
                
                # Displaying the results in the text area
                result_display.append(f"Business Name: {business.name}\n"
                                      f"Address: {business.address}\n"
                                      f"Website: {business.website}\n"
                                      f"Category: {business.category}\n"
                                      f"Phone: {business.phone_number}\n"
                                      f"Reviews Count: {business.reviews_count}\n"
                                      f"Reviews Average: {business.reviews_average}\n"
                                      f"{'='*40}\n")

            browser.close()

        # Save the results in the chosen format
        if save_format == "Excel":
            business_list.save_to_excel()
        elif save_format == "CSV":
            business_list.save_to_csv("google_maps_data")

        # Display results in the text area
        self.result_text.delete(1.0, tk.END)  # Clear previous results
        self.result_text.insert(tk.END, ''.join(result_display))
        messagebox.showinfo("Scraping Complete", f"Data saved as {save_format}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = L33TCODEGMSApp(root)
    root.mainloop()
