import tkinter as tk
from tkinter import messagebox
from model import get_search_element_info, extract_element_info

def generate_info(search_element):
    data = get_search_element_info(search_element)

    if "error" in data:
        messagebox.showerror("Error", data["error"])
        return

    element_info = extract_element_info(data)

    if "error" in element_info:
        messagebox.showwarning("Warning", element_info["error"])
    else:
        result_text.config(state=tk.NORMAL)
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, f"Search Element: {element_info['name']}\n", "bold")
        result_text.insert(tk.END, f"Description: {element_info['description']}\n")
        result_text.insert(tk.END, f"Website: {element_info['url']}\n")
        result_text.insert(tk.END, f"Biography: {element_info['biography']}\n")
        for info in element_info['contact_info']:
            result_text.insert(tk.END, f"{info}\n")
        result_text.config(state=tk.DISABLED)

def generate_info_callback():
    search_element = entry_search_element.get().strip()
    if not search_element:
        messagebox.showwarning("Warning", "Please enter a search element.")
        return
    generate_info(search_element)

# Create the main Tkinter window
root = tk.Tk()
root.title("Search It")
root.option_add('*Font', 'Helvetica 20 bold')

# Configure colors
background_color = "#f0f0f0"
text_color = "#333333"
button_color = "#4CAF50"
button_text_color = "white"

# Set background color
root.configure(bg=background_color)

# Create and pack the widgets
label_search_element = tk.Label(root, text="SEARCH ELEMENT:", bg=background_color, fg=text_color)
label_search_element.pack(pady=(10, 5))

entry_search_element = tk.Entry(root, bg="white", fg=text_color)
entry_search_element.pack(pady=20)

button_generate_info = tk.Button(root, text="Search", command=generate_info_callback, bg=button_color, fg=button_text_color)
button_generate_info.pack(pady=20)

result_text = tk.Text(root, height=15, width=500, bg="white", fg=text_color)
result_text.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()
