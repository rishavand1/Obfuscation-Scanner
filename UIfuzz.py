import requests
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def test_wordlist_on_website(wordlist, base_url, output_text):
    """
    Function to test words from a wordlist appended to a base URL and display their HTTP status codes.
    
    :param wordlist: A list of words to append to the base URL
    :param base_url: The base URL to which the words will be appended
    :param output_text: A Tkinter ScrolledText widget for displaying output
    """
    output_text.delete(1.0, tk.END)  # Clear the output text area
    for word in wordlist:
        full_url = f"{base_url}/{word}"  # Append the word to the base URL
        try:
            response = requests.get(full_url)  # Send a GET request
            result = f"URL: {full_url} - Status Code: {response.status_code}\n"
            output_text.insert(tk.END, result)
        except requests.RequestException as e:
            result = f"Error with URL: {full_url} - {e}\n"
            output_text.insert(tk.END, result)

def load_wordlist():
    """
    Open a file dialog to load a wordlist file and return its content as a list of words.
    """
    file_path = filedialog.askopenfilename(
        title="Select Wordlist File",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if file_path:
        try:
            with open(file_path, 'r') as file:
                return [line.strip() for line in file.readlines()], file_path
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load wordlist: {e}")
            return None, None
    return None, None

def start_testing():
    """
    Start testing the wordlist on the given base URL.
    """
    wordlist, file_path = load_wordlist()
    if wordlist:
        base_url = url_entry.get()
        if not base_url:
            messagebox.showwarning("Warning", "Please enter a base URL.")
            return
        
        output_text.insert(tk.END, f"Testing with wordlist: {file_path}\nBase URL: {base_url}\n\n")
        test_wordlist_on_website(wordlist, base_url, output_text)

# Create the main Tkinter window
root = tk.Tk()
root.title("URL Status Code Checker")

# URL Input
tk.Label(root, text="Base URL:").grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)
url_entry = tk.Entry(root, width=50)
url_entry.grid(row=0, column=1, padx=10, pady=10)

# Start Button
start_button = tk.Button(root, text="Start Testing", command=start_testing)
start_button.grid(row=0, column=2, padx=10, pady=10)

# Output Text Area
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=80, height=20)
output_text.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

# Run the Tkinter event loop
root.mainloop()
