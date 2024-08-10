import customtkinter as ctk  # Enhanced tkinter for better UI components.
from tkinter import messagebox  # Import messagebox for displaying alerts.
from selenium import webdriver  # Controls the browser.
from selenium.webdriver.chrome.service import Service  # Manages the service that ChromeDriver needs.
from selenium.webdriver.chrome.options import Options  # Allows options to be set for the Chrome driver.
from webdriver_manager.chrome import ChromeDriverManager  # Manages the ChromeDriver binary installation.
from selenium.webdriver.common.by import By  # Allows selecting elements by their attributes.
import re  # Import regular expressions for URL validation.


def sanitize_filename(filename):
    # Replaces any non-alphanumeric characters with underscores for file naming.
    return "".join([c if c.isalnum() or c in " -_" else "_" for c in filename])


def is_valid_url(url):
    # Regular expression pattern to validate a URL.
    pattern = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(pattern, url) is not None  # Return True if the URL matches the pattern.


def CenterWindowToDisplay(Screen: ctk.CTk, width: int, height: int, scale_factor: float = 1.0):
    """Centers the window to the main display/monitor"""
    screen_width = Screen.winfo_screenwidth()  # Get the screen width
    screen_height = Screen.winfo_screenheight()  # Get the screen height
    x = int(((screen_width / 2) - (width / 2.3)) * scale_factor)  # Calculate x coordinate for centering
    y = int(((screen_height / 2) - (height / 1.7)) * scale_factor)  # Calculate y coordinate for centering
    return f"{width}x{height}+{x}+{y}"  # Return the geometry string for centering the window


class LinkParserApp:
    def __init__(self, root):
        self.root = root  # Reference to the root window
        self.root.title("Website Link Parser")  # Set the title of the window
        self.root.geometry(CenterWindowToDisplay(root, width=400, height=200))  # Center the window on the screen
        self.root.iconbitmap("parsing.ico")  # Set the icon of the window
        ctk.set_appearance_mode("dark")  # Set theme to dark mode
        ctk.set_default_color_theme("blue")  # Set the default color theme to blue

        self.setup_gui()  # Call the method to set up the GUI components

    def setup_gui(self):
        # URL entry label
        self.url_label = ctk.CTkLabel(self.root, text="Enter URL:")  # Create a label for the URL entry
        self.url_label.pack(pady=10)  # Add padding around the label
        # URL entry field
        self.url_entry = ctk.CTkEntry(self.root, width=380,
                                      placeholder_text="https://example.com")  # Create entry field for URL input
        self.url_entry.pack(pady=10)  # Add padding around the entry field

        # Scrape button
        self.scrape_button = ctk.CTkButton(self.root, text="Parse Links",
                                           command=self.scrape_links)  # Create a button to trigger link parsing
        self.scrape_button.pack(pady=10)  # Add padding around the button

        # Exit button
        self.exit_button = ctk.CTkButton(self.root, text="Exit",
                                         command=self.root.quit)  # Create a button to exit the application
        self.exit_button.pack()  # Pack the exit button

    def scrape_links(self):
        url = self.url_entry.get()  # Get URL from the entry widget
        if not url:  # Check if URL is empty
            messagebox.showerror("Error", "URL is required!")  # Show error message if URL is empty
            return
        if not is_valid_url(url):  # Validate the URL format
            messagebox.showerror("Error", "Invalid URL format!")  # Show error if URL is not valid
            return
        self.parse_links(url)  # Call the function to parse links if the URL is valid

    def parse_links(self, url):
        options = Options()  # Initialize Chrome options
        options.add_experimental_option("detach", True)  # Keep the browser window open after script ends
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                                  options=options)  # Set up ChromeDriver with the specified options
        driver.get(url)  # Open the specified URL in the browser
        links = driver.find_elements(By.TAG_NAME, 'a')  # Find all anchor elements (links) on the page
        filename = f"links_{sanitize_filename(driver.title)}.txt"  # Create a filename based on the page title
        with open(filename, 'w') as file:  # Open a text file to write the links
            for link in links:
                name = link.text  # Get the text of the link
                if name:  # Check if the link has text
                    href = link.get_attribute('href')  # Get the URL the link points to
                    file.write(f'"{name}": "{href}"\n')  # Write the link text and URL to the file
        messagebox.showinfo("Success",
                            f"File '{filename}' has been created with the links data.")  # Inform the user that the file has been created


# Run the GUI application
if __name__ == "__main__":
    root = ctk.CTk()  # Create the main application window
    app = LinkParserApp(root)  # Create an instance of the LinkParserApp
    root.mainloop()  # Start the main event loop of the application
