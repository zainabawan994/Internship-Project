#  PDF to Audio & MCQ Generator (Python GUI App)

This Python desktop application allows users to:
-  Convert any PDF into an audio book (`.mp3`) using Google Text-to-Speech.
-  Automatically generate Multiple Choice Questions (MCQs) from the text content of a PDF.

It features a clean and professional GUI built using **Tkinter**.

---

##  Features

-  Upload any `.pdf` file
-  Convert the PDF text to an audio file using `gTTS`
-  Automatically generate 5 random MCQs from the PDF content
-  User-friendly interface with modern color theme
- Handles large PDFs by splitting text into chunks

---

##  Interface Preview

- Modern, industrial UI
- Clean button layout
- Scrollable MCQ popup window

---

##  Tech Stack

| Component        | Usage                         |
|------------------|-------------------------------|
| Python           | Core logic and GUI            |
| Tkinter          | GUI for file upload & buttons |
| PyPDF2           | PDF text extraction           |
| gTTS             | Text-to-speech conversion     |
| OS / Random      | File handling, MCQ logic      |



---

##  Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/pdf-audio-mcq-generator.git
cd pdf-audio-mcq-generator

