import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import speech_recognition as sr
import os

def pick_file():
    filename = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if filename:
        file_path.delete(0, tk.END)
        file_path.insert(0, filename)

def transcribe():
    audio_file = file_path.get()
    if not audio_file or not os.path.exists(audio_file):
        messagebox.showerror("Error", "Pick a WAV file first!")
        return
    
    r = sr.Recognizer()
    try:
        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)
        text = r.recognize_google(audio)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, text)
        messagebox.showinfo("Done", "Text ready!")
    except Exception as e:
        messagebox.showerror("Oops", f"Error: {str(e)}")

def save_text():
    text = output_text.get(1.0, tk.END).strip()
    if text:
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filename:
            with open(filename, "w") as f:
                f.write(text)
            messagebox.showinfo("Saved", "Text saved!")

# Make window
root = tk.Tk()
root.title("Speech to Text Tool")
root.geometry("500x400")

tk.Label(root, text="Pick WAV:").pack(pady=10)
file_path = tk.Entry(root, width=50)
file_path.pack()
tk.Button(root, text="Choose File", command=pick_file).pack()

tk.Button(root, text="Transcribe!", bg="lightblue", height=2, command=transcribe).pack(pady=20)

tk.Label(root, text="Text:").pack()
output_text = scrolledtext.ScrolledText(root, height=10, width=60)
output_text.pack(pady=10, padx=10, fill=tk.BOTH)

tk.Button(root, text="Save Text", bg="lightgreen", command=save_text).pack(pady=10)

root.mainloop()
