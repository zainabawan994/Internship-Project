import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, Toplevel
import PyPDF2
from gtts import gTTS
import os
import random

root = tk.Tk()
root.title("PDF Audio + MCQ Generator")
root.geometry("750x550")
root.configure(bg="#F5F7FA")

selected_pdf_path = None

def upload_pdf():
    global selected_pdf_path
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        selected_pdf_path = file_path
        file_label.config(text=f" {os.path.basename(file_path)}")
    else:
        file_label.config(text=" No file selected")

def convert_to_audio():
    if not selected_pdf_path:
        messagebox.showwarning("No File", "Please upload a PDF file first.")
        return
    try:
        with open(selected_pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                content = page.extract_text()
                if content:
                    text += content

        if not text.strip():
            messagebox.showwarning("Empty PDF", "No readable text found in the PDF.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 files", "*.mp3")])
        if save_path:
            if len(text) > 4500:
                messagebox.showinfo("Large Text", "Splitting long text into chunks...")
            chunks = [text[i:i+4500] for i in range(0, len(text), 4500)]
            for i, chunk in enumerate(chunks):
                tts = gTTS(text=chunk, lang='en')
                part_path = save_path.replace(".mp3", f"_part{i+1}.mp3")
                tts.save(part_path)

            messagebox.showinfo("Success", f"Audio saved successfully!\nLocation: {save_path}")
        else:
            messagebox.showinfo("Cancelled", "Audio save cancelled.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{str(e)}")

def generate_mcqs():
    if not selected_pdf_path:
        messagebox.showwarning("No File", "Please upload a PDF file first.")
        return

    try:
        with open(selected_pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                content = page.extract_text()
                if content:
                    text += content

        if not text.strip():
            messagebox.showwarning("Empty PDF", "No readable text found.")
            return

        # Extract sentences and form basic MCQs
        sentences = [s.strip() for s in text.split('.') if len(s.strip().split()) > 6]
        sample_sentences = random.sample(sentences, min(5, len(sentences)))

        mcqs = []
        for i, sent in enumerate(sample_sentences, start=1):
            words = sent.split()
            if len(words) > 6:
                answer = words[-1].rstrip(",.")
                question = sent.replace(answer, "_____")
                options = [answer] + random.sample([w for w in words if w != answer and len(w) > 3], k=3)
                random.shuffle(options)
                mcq = f"Q{i}. {question}?\nA) {options[0]}   B) {options[1]}   C) {options[2]}   D) {options[3]}\nCorrect: {answer}\n"
                mcqs.append(mcq)

        # MCQ popup
        mcq_window = Toplevel(root)
        mcq_window.title("Generated MCQs")
        mcq_window.geometry("700x400")
        mcq_window.configure(bg="#FFFFFF")

        text_area = scrolledtext.ScrolledText(mcq_window, wrap=tk.WORD, font=("Segoe UI", 11), bg="#FAFAFA", fg="#212529", relief="flat")
        text_area.pack(expand=True, fill='both', padx=10, pady=10)

        text_area.insert(tk.END, "\n\n".join(mcqs))
        text_area.configure(state='disabled')

    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate MCQs:\n{str(e)}")


# ==== UI Section ====
title_label = tk.Label(root, text="PDF to Audio & MCQ Generator", font=("Segoe UI", 20, "bold"), bg="#F5F7FA", fg="#212529")
title_label.pack(pady=20)

# Upload Section
upload_frame = tk.Frame(root, bg="#FFFFFF", bd=1, relief="solid", padx=20, pady=20)
upload_frame.pack(pady=10, padx=30, fill='x')

upload_button = tk.Button(upload_frame, text="Upload PDF", command=upload_pdf,
                          bg="#007BFF", fg="white", font=("Segoe UI", 11, "bold"),
                          relief="flat", padx=20, pady=8)
upload_button.pack(anchor='w')

file_label = tk.Label(upload_frame, text="No file selected", bg="#FFFFFF", fg="#6C757D",
                      wraplength=500, font=("Segoe UI", 10))
file_label.pack(anchor='w', pady=5)

# Convert Button
convert_button = tk.Button(root, text="Convert PDF to Audio", command=convert_to_audio,
                           bg="#28A745", fg="white", font=("Segoe UI", 12, "bold"),
                           relief="flat", padx=25, pady=10)
convert_button.pack(pady=15)

# MCQ Button
mcq_button = tk.Button(root, text="Generate MCQs from PDF", command=generate_mcqs,
                       bg="#FFC107", fg="#212529", font=("Segoe UI", 12, "bold"),
                       relief="flat", padx=25, pady=10)
mcq_button.pack()

# Footer
footer_label = tk.Label(root, text="Developed by Zainab", font=("Segoe UI", 9), bg="#F5F7FA", fg="#6C757D")
footer_label.pack(side="bottom", pady=20)

root.mainloop()
