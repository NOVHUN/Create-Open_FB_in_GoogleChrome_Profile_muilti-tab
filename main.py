import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from asyncio import subprocess
import winshell
from selenium import webdriver

def check_chrome_installed():
    # Check if Chrome is installed by looking for the chrome.exe executable
    chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    return os.path.exists(chrome_path)

def on_check_chrome():
    if check_chrome_installed():
        messagebox.showinfo("Chrome Check", "Google Chrome is installed.")
    else:
        # Google Chrome is not installed, show a message box with a download link
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        
        result = messagebox.askyesno("Chrome Check", "Google Chrome is not installed. Do you want to download it?")
        if result:
            # Open a web browser with the download link
            import webbrowser
            webbrowser.open("https://www.google.com/chrome/")
        else:
            messagebox.showinfo("Chrome Check", "You chose not to download Google Chrome.")



def start_chromedriver():
    try:
        # Check if chromedriver.exe is already running
        subprocess.check_output("tasklist /FI \"IMAGENAME eq chromedriver.exe\" 2>NUL | find /I /N \"chromedriver.exe\">NUL", shell=True)
    except subprocess.CalledProcessError:
        # If not running, start chromedriver.exe
        chromedriver_path = os.path.join(os.path.dirname(sys.argv[0]), "chromedriver.exe")
        subprocess.Popen(chromedriver_path)
        
def create_chrome_profiles(num_profiles, shortcut_folder):
    for profile_number in range(1, num_profiles + 1):
        create_chrome_profile(profile_number, shortcut_folder)

def create_chrome_profile(profile_number, shortcut_folder):
    home_dir = os.path.expanduser("~")
    profile_name = "Profile"
    chrome_profile_path = os.path.join(home_dir, "AppData", "Local", "Google", "Chrome", "User Data", f"{profile_name} {profile_number}")
    if not os.path.exists(chrome_profile_path):
        os.makedirs(chrome_profile_path)
        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir={chrome_profile_path}")
        driver = webdriver.Chrome(options=options)
        driver.quit()

        shortcut_path = os.path.join(shortcut_folder, f"{profile_name}_{profile_number}.lnk")
        target = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        create_shortcut(shortcut_path, target, profile_name, profile_number)

        print(f"Profile and shortcut for '{profile_name} {profile_number}' created.")
    else:
        print(f"Profile {profile_name} {profile_number} already exists. Skipping...")

def create_shortcut(shortcut_path, target, profile_name, profile_number):
    shortcut = winshell.shortcut(target)
    shortcut.arguments = f'--profile-directory="{profile_name} {profile_number}" https://www.facebook.com'
    shortcut.write(shortcut_path)


def browse_folder():
    folder_path = filedialog.askdirectory()
    entry_folder_path.delete(0, tk.END)
    entry_folder_path.insert(0, folder_path)

def start_process():
    profile_number_entry = entry_profile_number.get()
    if profile_number_entry.strip():  # Check if entry is not empty or only whitespace
        num_profiles = int(profile_number_entry)
        shortcut_folder = entry_folder_path.get()
        create_chrome_profiles(num_profiles, shortcut_folder)
        refresh_table()
    else:
        print("Please enter the number of profiles.")

def open_all_profiles():
    for item in treeview.get_children():
        profile_name = treeview.item(item, "values")[0]
        profile_number = profile_name.split()[-1]
        shortcut_path = os.path.join(entry_folder_path.get(), f"Profile_{profile_number}.lnk")
        if os.path.exists(shortcut_path):
            os.startfile(shortcut_path)
        else:
            print(f"Shortcut file '{shortcut_path}' not found.")


def show_profile():
    num_profiles = 1  # Assuming you want to create only one new profile at a time
    shortcut_folder = entry_folder_path.get()
    create_chrome_profiles(num_profiles, shortcut_folder)
    refresh_table()

def open_selected_profiles():
    selected_items = treeview.selection()
    for item in selected_items:
        profile_name = treeview.item(item, "values")[0]
        profile_number = profile_name.split()[-1]
        shortcut_path = os.path.join(entry_folder_path.get(), f"Profile_{profile_number}.lnk")
        if os.path.exists(shortcut_path):
            os.startfile(shortcut_path)
        else:
            print(f"Shortcut file '{shortcut_path}' not found.")

def refresh_table():
    for item in treeview.get_children():
        treeview.delete(item)
    home_dir = os.path.expanduser("~")
    profile_name = "Profile"
    selected_folder = entry_folder_path.get()  # Get the selected folder
    if os.path.exists(selected_folder):  # Check if the selected folder exists
        for item in os.listdir(os.path.join(home_dir, "AppData", "Local", "Google", "Chrome", "User Data")):
            if item.startswith(profile_name):
                profile_number = item.split()[-1]
                shortcut_path = os.path.join(selected_folder, f"{profile_name}_{profile_number}.lnk")
                if os.path.exists(shortcut_path):  # Check if shortcut exists in selected folder
                    treeview.insert("", "end", values=(f"{profile_name} {profile_number}", "Click to open", shortcut_path))
    else:
        print("Selected folder does not exist.")

# Create and configure the main window
root = tk.Tk()
root.title("Create / Open FB in Google Chrome Profile Manager")
root.state('zoomed')  # Start maximized

# Configure grid weight to make layout responsive
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(3, weight=1)

# Add a new button to check Chrome installation
button_check_chrome = ttk.Button(root, text="Check Chrome Installation", command=on_check_chrome)
button_check_chrome.grid(row=0, column=2, padx=5, pady=5, sticky='ew')

# Your existing interface elements continue below...

style = ttk.Style()
style.configure("TButton", background="#0078D7", foreground="black", font=('Helvetica', 10, 'bold'))
style.configure("Treeview.Heading", background="#0078D7", foreground="black", font=('Helvetica', 10, 'bold'))
style.configure("TLabel", background="#f0f0f0", foreground="black", font=('Helvetica', 10, 'bold'))

# Set the icon for the window
icon_path = "image.png"  # Assuming you converted the ICO file to PNG format
if os.path.exists(icon_path):
    img = tk.PhotoImage(file=icon_path)
    root.tk.call('wm', 'iconphoto', root._w, img)
else:
    print("Icon file not found.")

root.iconbitmap('image.ico')
label_profile_number = ttk.Label(root, text="Number of Profiles:")
label_profile_number.grid(row=0, column=0, padx=10, pady=5, sticky='w')

entry_profile_number = ttk.Entry(root)
entry_profile_number.grid(row=0, column=1, padx=10, pady=5, sticky='ew')

label_folder_path = ttk.Label(root, text="Shortcut Folder:")
label_folder_path.grid(row=1, column=0, padx=10, pady=5, sticky='w')

entry_folder_path = ttk.Entry(root)
entry_folder_path.grid(row=1, column=1, padx=10, pady=5, sticky='ew')

button_browse = ttk.Button(root, text="Browse", command=browse_folder)
button_browse.grid(row=1, column=2, padx=5, pady=5, sticky='ew')

button_start = ttk.Button(root, text="Create More", command=start_process)
button_start.grid(row=2, column=0, padx=5, pady=10, sticky='ew')

button_create_profile = ttk.Button(root, text="Show Profile in Folder", command=show_profile)
button_create_profile.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

button_open_selected = ttk.Button(root, text="Open Selected Profiles", command=open_selected_profiles)
button_open_selected.grid(row=2, column=2, padx=5, pady=5, sticky='ew')

treeview = ttk.Treeview(root, columns=("Profile", "Open Shortcut", "Shortcut Path"), show="headings", selectmode="extended")
treeview.heading("Profile", text="Profile")
treeview.heading("Open Shortcut", text="Open Shortcut")
treeview.heading("Shortcut Path", text="Shortcut Path")
treeview.grid(row=3, column=0, columnspan=3, padx=10, pady=5, sticky='nsew')

# Footer with copyright notice
footer_label = ttk.Label(root, text="\u00A9 2024 Develop by Mr.HUN | All rights reserved.", foreground="black")
footer_label.grid(row=4, column=0, columnspan=3, pady=5)

root.mainloop()
