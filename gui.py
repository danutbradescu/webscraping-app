from tkinter import Tk, Button, Label, font, scrolledtext
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import threading
from scraper import scrape_to_csv

# Initialize the main application window
root = Tk()
root.title("Web Scraping Application")

# Custom font
customFont = font.Font(family="Helvetica", size=12)

log_text = scrolledtext.ScrolledText(root, font=customFont, height=10, width=50)
log_text.pack(pady=(10, 20))

progress_bar = ttk.Progressbar(root, orient="horizontal", length=200, mode="indeterminate")
progress_bar.pack(pady=(10, 0))
progress_bar.pack_forget()  # Hide the progress bar initially

status_label = ttk.Label(root, text="", font=("Helvetica", 10))
status_label.pack(pady=(5, 20))

def select_file():
    filepath = askopenfilename(filetypes=[("Parquet Files", "*.parquet"), ("All Files", "*.*")])
    if filepath:
        log_to_widget(f"Selected file: {filepath}")
        select_file_button.pack_forget() 
        progress_bar.pack(pady=(10, 0))  
        progress_bar.start(10) 
        status_label.config(text="Please wait...") 
        start_scraping(filepath)

def start_scraping(filepath):
    def task():
        scrape_to_csv(filepath, log_func=log_to_widget)
        on_scraping_complete()
    threading.Thread(target=task).start()

def on_scraping_complete():
    root.after(0, progress_bar.stop)
    root.after(0, progress_bar.pack_forget)
    root.after(0, lambda: status_label.config(text=""))
    root.after(0, select_file_button.pack)

def log_to_widget(message):
    log_text.insert("end", message + "\n")
    log_text.see("end")

style = ttk.Style()
style.theme_use('vista')

select_file_button = Button(root, text="Select File", command=select_file, font=customFont)
select_file_button.pack(pady=(20, 10))

root.mainloop()
