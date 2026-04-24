**[Leia em Português 🇧🇷](README.pt-BR.md)**

# Legal PDF Processor

A GUI tool to optimize court-case PDFs exported from SAJ (a court management system used by Brazilian State Courts), focused on legal documents that need to be cited in briefs, rulings, and decisions.

Beyond saving tokens when feeding documents to AI agents, it pre-processes files with OCR and removes noise such as electronic signatures, headers, and footers — helping the agent focus on the actual legal content.

## ✨ Features

- **Automatic margin cropping** with customizable measurements in centimeters
- **Smart compression** that preserves the selectable native text layer (~60% average size reduction)
- **Automatic OCR** on scanned pages (IDs, contracts, property records, etc.) using Tesseract
- **Intelligent detection** of pages needing OCR — ignores the SAJ side watermark to avoid duplicated text
- **Simple and intuitive GUI**
- **Batch processing** of multiple files

## 🎯 Motivation

Court-case files from SAJ often contain scanned documents with no text layer, which prevents keyword search and makes it hard to cite documents with the exact page number. This tool automates the entire preparation pipeline for these PDFs.

## 🛠️ Tech stack

- Python 3
- PyMuPDF (fitz) — PDF manipulation
- Pillow — image processing
- pytesseract + Tesseract OCR — text recognition
- Tkinter — graphical interface

## 📦 Installation

### Option 1: Executable (Windows)
Download the ready-to-use `.exe` from the [Releases](../../releases) section of this repository. Only requirement: have [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) installed (check the Portuguese language option during install).

### Option 2: From source

1. Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) (check the Portuguese language option)
2. Install the Python dependencies:
```bash
   pip install -r requirements.txt
```
3. Run:
```bash
   python processador_pdf.py
```

## 🚀 How to use

1. Click **"Selecionar PDFs..."** (Select PDFs) and pick one or more files
2. Click **"Escolher pasta..."** (Choose folder) to set the output directory
3. Adjust the cropping measurements if needed (defaults are tuned for typical SAJ layouts)
4. Choose which operations to apply: cropping, compression, OCR
5. Click **"▶ PROCESSAR"** (Process)

## 📊 Processing order

The program applies operations in the optimal order:

1. **Cropping** margins (focuses on the usable page area)
2. **OCR** on pages detected as scanned (image quality is preserved for best OCR results)
3. **Compression** last (reduces final size without affecting OCR output)

## 📝 License

MIT
