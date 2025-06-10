import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import base64
import requests
import os
import json

API_KEY = "AIzaSyDTzn0avrKlIf8ch3B6ICc83wmaHJ66xu4"  # Replace this securely in production

def get_image_mime_type(filepath):
    if filepath.lower().endswith('.png'):
        return 'image/png'
    return 'image/jpeg'

def encode_image_to_base64(filepath):
    try:
        with open(filepath, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        messagebox.showerror("File Error", str(e))
        return None

def analyze_image(api_key, image_base64, mime_type):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={api_key}"

    prompt = """
    Analyze the image and identify each type of fruit. For each fruit type, provide:
    1. The variety of the fruit (e.g., 'Apple', 'Banana', 'Orange').
    2. A count of how many are visible.
    3. An assessment of its ripeness ('unripe', 'ripe', or 'overripe').

    Please provide the response as a JSON object with a single key "fruits".
    """

    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": image_base64
                        }
                    }
                ]
            }
        ],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        content = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        return json.loads(content)
    except Exception as e:
        messagebox.showerror("API Error", f"Failed to analyze image.\n\n{e}")
        return None

class FruitAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fruit Analyzer with Gemini")

        self.image_label = tk.Label(root, text="No image selected")
        self.image_label.pack(pady=10)

        self.select_button = tk.Button(root, text="Select Image", command=self.select_image)
        self.select_button.pack()

        self.analyze_button = tk.Button(root, text="Analyze Image", command=self.analyze_image, state=tk.DISABLED)
        self.analyze_button.pack(pady=10)

        self.result_text = scrolledtext.ScrolledText(root, width=60, height=20)
        self.result_text.pack(padx=10, pady=10)

        self.filepath = None

    def select_image(self):
        filepath = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if filepath:
            self.filepath = filepath
            img = Image.open(filepath).resize((200, 200))
            img_tk = ImageTk.PhotoImage(img)
            self.image_label.configure(image=img_tk, text="", compound=tk.TOP)
            self.image_label.image = img_tk
            self.analyze_button.config(state=tk.NORMAL)
            self.result_text.delete("1.0", tk.END)

    def analyze_image(self):
        if not self.filepath:
            return
        mime_type = get_image_mime_type(self.filepath)
        image_data = encode_image_to_base64(self.filepath)
        if not image_data:
            return
        results = analyze_image(API_KEY, image_data, mime_type)
        if results:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, json.dumps(results, indent=2))

if __name__ == "__main__":
    root = tk.Tk()
    app = FruitAnalyzerApp(root)
    root.mainloop()
