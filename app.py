import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import shutil
import os

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def search_keywords(text, keywords):
    found_keywords = {keyword: text.lower().count(keyword.lower()) for keyword in keywords}
    return found_keywords

def copy_to_temp(file_path):
    temp_dir = os.path.join(os.path.expanduser("~"), "temp_selected_files")
    os.makedirs(temp_dir, exist_ok=True)
    shutil.copy(file_path, temp_dir)
    messagebox.showinfo("Info", f"File copied to {temp_dir}")

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        text = extract_text_from_pdf(file_path)
        keywords = entry_keywords.get().split(',')
        keywords = [keyword.strip() for keyword in keywords if keyword.strip()]  # Remove empty keywords
        if not keywords:
            messagebox.showwarning("Warning", "Please enter at least one keyword.")
            return
        keyword_counts = search_keywords(text, keywords)
        result_text = "\n".join([f"Keyword '{keyword}' found {count} times" for keyword, count in keyword_counts.items()])
        
        def on_checkbox_select():
            if var.get():
                copy_to_temp(file_path)
        
        result_window = tk.Toplevel(app)
        result_window.title("Results")
        tk.Label(result_window, text=result_text).pack(pady=10)
        var = tk.BooleanVar()
        checkbox = tk.Checkbutton(result_window, text="Add this file to selected list?", variable=var, command=on_checkbox_select)
        checkbox.pack(pady=10)
        tk.Button(result_window, text="Close", command=result_window.destroy).pack(pady=10)

app = tk.Tk()
app.title("Recruitment Keyword Screener")

frame = tk.Frame(app)
frame.pack(padx=50, pady=50)

label_keywords = tk.Label(frame, text="Please Enter keywords (comma-separated):")
label_keywords.pack()

entry_keywords = tk.Entry(frame, width=50)
entry_keywords.pack()

button_browse = tk.Button(frame, text="Browse PDF", command=open_file)
button_browse.pack(pady=10)

app.mainloop()