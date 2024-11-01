import tkinter as tk
from tkinter import ttk, messagebox, filedialog
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
            combined_data.to_excel(self.combined_data_filepath, index=False, header=not os.path.exists(self.combined_data_filepath))
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
        self.root.geometry("500x400")
        self.create_widgets()
        
    def create_widgets(self):
        title_label = tk.Label(self.root, text="L33TCODE GMS", font=("Arial", 16))
        title_label.pack(pady=10)
        
        search_frame = tk.Frame(self.root)
        search_frame.pack(pady=5)
        
        search_label = tk.Label(search_frame, text="Search Term:")
        search_label.grid(row=0, column=0, padx=5)
        
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.grid(row=0, column=1)
        
        total_label = tk.Label(search_frame, text="Total Results:")
        total_label.grid(row=1, column=0, padx=5, pady=5)
        
        self.total_entry = tk.Entry(search_frame, width=10)
        self.total_entry.grid(row=1, column=1)
        
        run_button = tk.Button(self.root, text="Run Scraper", command=self.run_scraper)
        run_button.pack(pady=10)
        
        save_frame = tk.Frame(self.root)
        save_frame.pack(pady=5)
        
        save_label = tk.Label(save_frame, text="Save as:")
        save_label.grid(row=0, column=0, padx=5)
        
        self.save_option = ttk.Combobox(save_frame, values=["Excel", "CSV"])
        self.save_option.grid(row=0, column=1)
        
    def run_scraper(self):
        search_term = self.search_entry.get()
        total_results = int(self.total_entry.get()) if self.total_entry.get().isdigit() else 100  # Default to 100 if empty
        save_format = self.save_option.get()
        
        if not search_term:
            messagebox.showwarning("Input Error", "Please enter a search term.")
            return

        messagebox.showinfo("Scraping Started", f"Scraping for '{search_term}'...")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto("https://www.google.com/maps")
            page.fill('//input[@id="searchboxinput"]', search_term)
            page.press('//input[@id="searchboxinput"]', "Enter")
            
            business_list = BusinessList()
            # Add logic for scraping (e.g., using locators)
            # Append scraped data to business_list.business_list

            if save_format == "Excel":
                business_list.save_to_excel()
            elif save_format == "CSV":
                business_list.save_to_csv(f"{search_term}_data")
            
            messagebox.showinfo("Scraping Complete", f"Data saved as {save_format}.")
            browser.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = L33TCODEGMSApp(root)
    root.mainloop()
