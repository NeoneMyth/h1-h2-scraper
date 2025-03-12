import csv
import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog
from tkinter.ttk import Progressbar, Style 
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse

scraped_content = ""  
scraped_data_list = []  

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def scrape():
    global scraped_content, scraped_data_list
    urls = url_entry.get("1.0", tk.END).strip().split("\n")  
    output_text.delete("1.0", tk.END)  

    scraped_content = ""
    scraped_data_list = [["URL", "Heading"]]

    scrape_button.config(state=tk.DISABLED, text="Scraping...")
    progress_bar["maximum"] = len(urls)
    progress_bar["value"] = 0  

    for i, url in enumerate(urls):
        url = url.strip()
        if not url or not is_valid_url(url):
            scraped_content += f"Invalid URL: {url}\n"
            continue  

        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            headings = soup.find_all(["h1", "h2"])

            scraped_text = f"Scraped from: {url}\n" + "=" * 60 + "\n"
            for tag in headings:
                text = tag.get_text(strip=True)
                scraped_text += f"Heading: {text}\n" + "-" * 50 + "\n"
                scraped_data_list.append([url, text])  

            scraped_content += scraped_text + "\n\n"
            progress_bar["value"] = i + 1  # Update progress bar
            root.update_idletasks()

            time.sleep(2)  
        except requests.exceptions.RequestException as e:
            scraped_content += f"Network error while accessing {url}: {e}\n" + "=" * 60 + "\n\n"

    output_text.insert(tk.END, scraped_content)
    scrape_button.config(state=tk.NORMAL, text="Scrape")  

def save_to_file(file_type="txt"):
    if not scraped_content.strip():
        messagebox.showwarning("No Data", "No scraped data to save. Please scrape first.")
        return

    file_ext = ".txt" if file_type == "txt" else ".csv"
    file_path = filedialog.asksaveasfilename(defaultextension=file_ext,
                                             filetypes=[("Text files", "*.txt"),
                                                        ("CSV files", "*.csv"),
                                                        ("All files", "*.*")])

    if file_path:
        if file_type == "txt":
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(scraped_content)
        else:  
            with open(file_path, "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerows(scraped_data_list)

        messagebox.showinfo("Saved", f"Scraped data saved to:\n{file_path}")

def clear_output():
    output_text.delete("1.0", tk.END)


root = tk.Tk()
root.title("H1 & H2 Scraper Deluxe")  
root.geometry("700x500")  
root.configure(bg="#2e3440")  

frame = tk.Frame(root, bg="#2e3440")
frame.pack(pady=10)

welcome_label = tk.Label(frame, text="🚀 Welcome to H1 & H2 Scraper!", font=("Helvetica", 16, "bold"), fg="#88c0d0", bg="#2e3440")
welcome_label.pack()

tk.Label(frame, text="Enter URLs (one per line):", font=("Helvetica", 12), fg="#d8dee9", bg="#2e3440").pack()

url_entry = tk.Text(frame, width=60, height=5, bg="#3b4252", fg="#eceff4", font=("Consolas", 10))
url_entry.pack(pady=5)

scrape_button = tk.Button(frame, text="Scrape", font=("Helvetica", 12, "bold"), bg="#81a1c1", fg="#2e3440", command=scrape)
scrape_button.pack(pady=5)

progress_bar = Progressbar(frame, orient="horizontal", length=400, mode="determinate", style="Custom.Horizontal.TProgressbar")
progress_bar.pack(pady=5)

output_text = scrolledtext.ScrolledText(root, width=80, height=15, wrap=tk.WORD, bg="#3b4252", fg="#eceff4", font=("Consolas", 10))
output_text.pack(pady=10)

button_frame = tk.Frame(root, bg="#2e3440")
button_frame.pack(pady=5, fill="x")

tk.Button(button_frame, text="Save as TXT", font=("Helvetica", 10), bg="#5e81ac", fg="#eceff4", command=lambda: save_to_file("txt")).pack(side="left", expand=True, fill="x", padx=5)
tk.Button(button_frame, text="Save as CSV", font=("Helvetica", 10), bg="#5e81ac", fg="#eceff4", command=lambda: save_to_file("csv")).pack(side="left", expand=True, fill="x", padx=5)
tk.Button(button_frame, text="Clear Output", font=("Helvetica", 10), bg="#bf616a", fg="#eceff4", command=clear_output).pack(side="left", expand=True, fill="x", padx=5)


style = Style()
style.configure("Custom.Horizontal.TProgressbar", troughcolor="#3b4252", background="#88c0d0", thickness=10)

root.mainloop()