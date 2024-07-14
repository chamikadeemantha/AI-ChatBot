import tkinter as tk
from tkinter import scrolledtext, filedialog
from PIL import Image
import pytesseract
import PyPDF2
from litellm import completion
import os

# Set ENV variables
os.environ["OPENAI_API_KEY"] = "sk-proj-B9FpF0xAibS6QZMsjnrqT3BlbkFJGoo2CyNF3jjtL8lpB5ij"

# If on Windows, set the tesseract_cmd to the installed location
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_response():
    user_input = input_text.get("1.0", tk.END).strip()
    if user_input:
        messages = [{"content": user_input, "role": "user"}]
        response = completion(model="gpt-3.5-turbo", messages=messages)
        bot_response = response['choices'][0]['message']['content'].strip()
        
        result_text.config(state=tk.NORMAL)
        result_text.insert(tk.END, "User: " + user_input + "\n", "user")
        result_text.insert(tk.END, "Bot: " + bot_response + "\n\n", "bot")
        result_text.config(state=tk.DISABLED)
        input_text.delete("1.0", tk.END)

def upload_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_extension = os.path.splitext(file_path)[1].lower()
        file_content = ""
        
        if file_extension in ['.png', '.jpg', '.jpeg']:
            # Extract text from image using pytesseract
            image = Image.open(file_path)
            file_content = pytesseract.image_to_string(image)
        elif file_extension == '.pdf':
            # Extract text from PDF using PyPDF2
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfFileReader(file)
                for page_num in range(reader.getNumPages()):
                    page = reader.getPage(page_num)
                    file_content += page.extract_text()
        
        if file_content:
            input_text.insert(tk.END, file_content)

# Create the main window
root = tk.Tk()
root.title("Chamika Deemantha ChatBot")

# Create a text widget for user input
input_text = tk.Text(root, height=4, width=100, font=("Helvetica", 12), bg="#f0f0f0", fg="#000000", bd=1, highlightbackground="#000000", highlightthickness=1)
input_text.pack(pady=10)

# Create a frame for buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=7)

# Create a button to upload files
upload_button = tk.Button(button_frame, text="UPLOAD FILE", command=upload_file, font=("Helvetica", 12), bg="#007bcc", fg="#ffffff", bd=1, highlightbackground="#000000", highlightthickness=1)
upload_button.grid(row=0, column=0, padx=5, sticky="w")  # Left corner alignment

# Create a button to send the input to the API
send_button = tk.Button(button_frame, text="GET RESULTS", command=get_response, font=("Helvetica", 12), bg="#ff0000", fg="#ffffff", bd=1, highlightbackground="#000000", highlightthickness=1)
send_button.grid(row=0, column=1, padx=5)  # Middle alignment

# Create a scrolled text widget to display the results
result_text = scrolledtext.ScrolledText(root, state=tk.DISABLED, height=15, width=100, font=("Helvetica", 12), bg="#ffffff", fg="#000000", bd=1, highlightbackground="#000000", highlightthickness=1)
result_text.pack(pady=10)

# Add tags for coloring the text
result_text.tag_configure("user", foreground="#007acc", font=("Helvetica", 12, "bold"))
result_text.tag_configure("bot", foreground="#ff4500", font=("Helvetica", 12, "italic"))

# Run the application
root.mainloop()
