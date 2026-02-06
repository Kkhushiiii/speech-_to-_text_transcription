import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import speech_recognition as sr
import os

def pick_file():
    filename = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if filename:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, filename)
        status_label.config(text="File selected")

def transcribe():
    audio_file = file_entry.get()
    if not audio_file or not os.path.exists(audio_file):
        status_label.config(text="Please select a valid WAV file")
        return

    r = sr.Recognizer()
    try:
        status_label.config(text="Transcribing...")
        root.update_idletasks()

        with sr.AudioFile(audio_file) as source:
            audio = r.record(source)

        text = r.recognize_google(audio)

        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, text)

        status_label.config(text="Transcription completed")

    except Exception as e:
        status_label.config(text="Error during transcription")

def save_text():
    text = output_text.get(1.0, tk.END).strip()
    if text:
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(text)
            status_label.config(text="Text saved successfully")

# ---------------- UI ---------------- #

root = tk.Tk()
root.title("Speech to Text Tool")
root.geometry("600x450")
root.resizable(False, False)

main_frame = tk.Frame(root, padx=20, pady=20)
main_frame.pack(fill=tk.BOTH, expand=True)

tk.Label(main_frame, text="Select WAV Audio File", font=("Arial", 11, "bold"))\
    .grid(row=0, column=0, sticky="w")

file_entry = tk.Entry(main_frame, width=55)
file_entry.grid(row=1, column=0, pady=5, sticky="w")

tk.Button(main_frame, text="Browse", width=12, command=pick_file)\
    .grid(row=1, column=1, padx=10)

tk.Button(
    main_frame,
    text="Transcribe Audio",
    bg="#cce5ff",
    width=25,
    height=2,
    command=transcribe
).grid(row=2, column=0, columnspan=2, pady=15)

tk.Label(main_frame, text="Transcribed Text", font=("Arial", 11, "bold"))\
    .grid(row=3, column=0, sticky="w")

output_text = scrolledtext.ScrolledText(main_frame, width=70, height=10)
output_text.grid(row=4, column=0, columnspan=2, pady=8)

tk.Button(
    main_frame,
    text="Save Text",
    bg="#d4edda",
    width=20,
    command=save_text
).grid(row=5, column=0, columnspan=2, pady=10)

# Status bar
status_label = tk.Label(
    root,
    text="Ready",
    bd=1,
    relief=tk.SUNKEN,
    anchor="w",
    padx=10
)
status_label.pack(side=tk.BOTTOM, fill=tk.X)

root.mainloop()
