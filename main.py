import tkinter as tk
from tkinter import messagebox
import requests

# Function to fetch company information using API key
def get_company_info(company_name, api_key):
    url = "https://kgsearch.googleapis.com/v1/entities:search"
    params = {
        'query': company_name,
        'key': api_key,
        'limit': 1,
        'indent': True,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        messagebox.showerror("Error", f"Error fetching data from API: {response.status_code}, {response.text}")

# Read API key from file
def read_api_key(file_path):
    try:
        with open(file_path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        messagebox.showerror("Error", f"Error: File '{file_path}' not found.")
        return None

# Function to generate company information
def generate_info(company_name, file_path):
    api_key = read_api_key(file_path)
    if api_key:
        data = get_company_info(company_name, api_key)

        if data:
            company_info = data.get('itemListElement', [])
            if company_info:
                element = company_info[0].get('result', {})
                name = element.get('name', 'N/A')
                description = element.get('description', 'N/A')
                url = element.get('detailedDescription', {}).get('url', 'N/A')
                biography = element.get('detailedDescription', {}).get('articleBody', 'N/A')
                
                # Extract contact information
                contact_info = []
                if 'address' in element:
                    address = element['address']
                    contact_info.append(f"Address: {address.get('addressLocality', 'N/A')}, {address.get('addressRegion', 'N/A')} {address.get('postalCode', 'N/A')}")
                
                if 'contactPoint' in element:
                    for contact_point in element['contactPoint']:
                        contact_info.append(f"{contact_point.get('contactType', 'N/A')}: {contact_point.get('email', 'N/A')} (Email), {contact_point.get('telephone', 'N/A')} (Phone)")
                
                # Display company information
                result_text.config(state=tk.NORMAL)
                result_text.delete('1.0', tk.END)
                result_text.insert(tk.END, f"Search Element: {name}\n", "bold")
                result_text.insert(tk.END, f"Description: {description}\n")
                result_text.insert(tk.END, f"Website: {url}\n")
                result_text.insert(tk.END, f"Biography: {biography}\n")
                for info in contact_info:
                    result_text.insert(tk.END, f"{info}\n")
                result_text.config(state=tk.DISABLED)
            else:
                messagebox.showwarning("Warning", "No information found for the company.")
        else:
            messagebox.showerror("Error", "Failed to fetch data from the API.")

# Function to handle button click
def generate_info_callback():
    company_name = entry_company_name.get().strip()
    if not company_name:
        messagebox.showwarning("Warning", "Please enter a company name.")
        return

    file_path = r"C:\Users\yasas\Downloads\api_key.txt"  # Path to the file storing API key
    generate_info(company_name, file_path)

# Create the main Tkinter window
root = tk.Tk()
root.title(" Search  it")
root.option_add('*Font', 'Helvetica 20 bold')

# Configure colors
background_color = "#f0f0f0"
text_color = "#333333"
button_color = "#4CAF50"
button_text_color = "white"

# Set background color
root.configure(bg=background_color)

# Create and pack the widgets
label_company_name = tk.Label(root, text="SEARCH ELEMENT:", bg=background_color, fg=text_color)
label_company_name.pack(pady=(10, 5))

entry_company_name = tk.Entry(root, bg="white", fg=text_color)
entry_company_name.pack(pady=20)

button_generate_info = tk.Button(root, text="Search", command=generate_info_callback, bg=button_color, fg=button_text_color)
button_generate_info.pack(pady=20)

result_text = tk.Text(root, height=15, width=500, bg="white", fg=text_color)
result_text.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
