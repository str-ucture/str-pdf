import tkinter as tk
from tkinter import messagebox, scrolledtext, filedialog, ttk

import ghostscript
import sys
import os

import requests

# Define authentication
url = f"https://raw.githubusercontent.com/str-ucture/str-key/refs/heads/main/key_25.txt"

response = requests.get(url)
if response.status_code == 200:
    expected_str_key = response.text.strip()
else:
    expected_str_key = None

key_path = r"utils/auth.bin"
if os.path.exists(key_path):
    with open(key_path, "rb") as f:
        stored_str_key = f.read().decode()
else:
    stored_str_key = None

def center_window(win, width, height):
    # Get screen width and height
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()

    # Calculate position x and y coordinates
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Set the geometry of the window
    win.geometry(f'{width}x{height}+{x}+{y}')

def disable_frame(frame):
    for child in frame.winfo_children():
        try:
            child.configure(state='disabled')
        except tk.TclError:
            pass

# Redirect stdout to GUI text box
class TextRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, string):
        self.text_widget.configure(state='normal')    # Enable temporarily
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)                  # Auto-scroll
        self.text_widget.configure(state='disabled')  # Disable again

    def flush(self):
        pass  # Needed for compatibility with stdout

def pdf_to_pdfa(input_pdf_filepath: str, output_pdf_filepath: str) -> None:
    """
    Convert a PDF file(s) to PDF/A file(s).
    """
    args = [
        # r"./Ghostscript/App/bin/gsdll64.dll",                   # Ignored on Windows
        "-dSAFER",                                              # Enforce safe file access
        "-dBATCH",                                              # Batch mode
        "-dNOPAUSE",                                            # No pauses
        pdfa_version,                                           # Specify the -dPDFA option to specify PDF/A-1, -dPDFA=2 for PDF/A-2 or -dPDFA=3 for PDF/A-3.
        "-sDEVICE=pdfwrite",                                    # Output device, alternative = ps2pdf
        "-sColorConversionStrategy=UseDeviceIndependentColor",  # Other options: RGB or CMYK
        "-dPDFACompatibilityPolicy=1",                          # Compliance: 0 (default), 1 (Scrict Compliance)
        "-dCompressFonts=false",                                # Do not compress fonts
        f"-sOutputFile={output_pdf_filepath}",
        input_pdf_filepath
    ]

    print(f"PDF/A Version: {args[4]}")
    print(f"Input PDF: {input_pdf_filepath}")
    print(f"Output PDF/A: {output_pdf_filepath}")
    # Invoke Ghostscript C API
    ghostscript.Ghostscript(*args)
    print(f"File converted successfully.\n")

def convert_single_file():
    input_pdf = filedialog.askopenfilename(
        title="Select PDF to Convert",
        filetypes=[("PDF files", "*.pdf")]
    )
    if not input_pdf:
        print("No input file selected.\n")
        return

    # Suggest output filename
    input_dir = os.path.dirname(input_pdf)
    input_name = os.path.basename(input_pdf)
    pdf_filename, ext = os.path.splitext(input_name)
    suggested_output = os.path.join(input_dir, f"{pdf_filename}.pdf")

    output_pdf = filedialog.asksaveasfilename(
        title="Save PDF/A As",
        initialfile=os.path.basename(suggested_output),
        initialdir=input_dir,
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")]
    )
    if not output_pdf:
        print("No output file selected.\n")
        return

    try:
        print(f"Converting '{input_name}' to PDF/A...")
        pdf_to_pdfa(input_pdf, output_pdf)
        # messagebox.showinfo("Success", "PDF/A conversion completed!")
    except Exception as e:
        print(f"Error during conversion: {e}")
        messagebox.showerror("Error", str(e))

def convert_multiple_files():
    # Select input folder
    input_dir = filedialog.askdirectory(title="Select Input Folder Containing PDFs")
    if not input_dir:
        print("No input folder selected.\n")
        return
    
    # Select output folder
    parent_dir = os.path.dirname(input_dir)
    output_dir = filedialog.askdirectory(title="Select Output Folder for PDF/A Files", initialdir=parent_dir)
    if not output_dir:
        print("No output folder selected.\n")
        return

    # Find PDF files directly inside input folder
    pdf_files = []
    for f in os.listdir(input_dir):
        file_path = os.path.join(input_dir, f)
        if os.path.isfile(file_path) and f.lower().endswith('.pdf'):
            pdf_files.append(f)

    if not pdf_files:
        print("No PDF files found in the selected input folder.")
        return
    
    # Process each PDF
    for pdf_file in pdf_files:
        input_pdf = os.path.join(input_dir, pdf_file)
        pdf_filename, ext = os.path.splitext(pdf_file)
        output_name = f"{pdf_filename}.pdf"
        output_pdf = os.path.join(output_dir, output_name)
        try:
            print(f"Converting '{pdf_file}' to PDF/A...")
            pdf_to_pdfa(input_pdf, output_pdf)
        except Exception as e:
            print(f"Error converting '{pdf_file}': {e}")

def show_about():
    messagebox.showinfo("About",
                        "Application Name: str-pdf\n"
                        "Version: 1.0.0\n"
                        "Company: str.ucture GmbH\n"
                        "Website: https://str-ucture.com \n"
                        "Contact: info@str-ucture.com\n"
                        "Developed by: @shailesh-stha")

def show_license():
    messagebox.showinfo("License",
                        "This software is licensed under the GNU AGPLv3.\n"
                        "This product includes Ghostscript, free software licensed under the GPLv3.\n"
                        "Ghostscript copyright © 1988-2023 Artifex Software, Inc.\n"
                        "https://www.gnu.org/licenses/agpl-3.0.html")

# GUI Setup
root = tk.Tk()
root.title("PDF to PDF/A Converter")
center_window(root, 600, 350)

# root.geometry("600x350")
root.resizable(False, False)
root.iconbitmap("utils/str.ico")

menu = tk.Menu(root)
filemenu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="About", command=show_about)
filemenu.add_command(label="License", command=show_license)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit) 
root.config(menu=menu)

# Define a top frame for controls display
top_frame = tk.Frame(root)
top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
top_frame.grid_columnconfigure(0, weight=1)
top_frame.grid_columnconfigure(1, weight=0)

# Define controls
combo_label = tk.Label(top_frame, text="Conversion Format:")
combo_label.grid(row=0, column=1, sticky='w', padx=(5, 0), pady=5)

combobox = ttk.Combobox(top_frame, values=["PDF/A-1b", "PDF/A-2b", "PDF/A-3b"], width=20, state="readonly")
combobox.set("PDF/A-2b")
combobox.grid(row=0, column=2, sticky='e', padx=(10, 0), pady=5)

# Set the PDF/A version based on the selected option
def on_combobox_change(event):
    selected = combobox.get()
    global pdfa_version
    if selected == "PDF/A-1b":
        pdfa_version = "-dPDFA=1"
    elif selected == "PDF/A-2b":
        pdfa_version = "-dPDFA=2"
    elif selected == "PDF/A-3b":
        pdfa_version = "-dPDFA=3"

# Set default value
pdfa_version = "-dPDFA=2"
combobox.bind("<<ComboboxSelected>>", on_combobox_change)

btn_single_pdf = tk.Button(top_frame,
                           text="Select a PDF and Convert",
                           command=convert_single_file,
                           width=30)
btn_multiple_pdf = tk.Button(top_frame,
                             text="Select a Folder and Convert all",
                             command=convert_multiple_files,
                             width=30)

btn_single_pdf.grid(row=0, column=0, sticky='w', padx=(0, 10), pady=5)
btn_multiple_pdf.grid(row=1, column=0, sticky='w', padx=(0, 10), pady=5)

# Define a bottom frame for the log display
log_frame = tk.Frame(root)
log_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)

log_display = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=10)
log_display.configure(font=("Courier New", 8))
log_display.pack(fill=tk.BOTH, expand=True)

# Redirect print
sys.stdout = TextRedirector(log_display)
sys.stderr = TextRedirector(log_display)

if stored_str_key != expected_str_key:
    disable_frame(top_frame)
    disable_frame(log_frame)
    messagebox.showerror("Authentication Failed", "Please Verify the Authentication Key.")
    sys.exit(1)

root.mainloop()