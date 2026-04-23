import fitz
import io
import os
import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox, scrolledtext
from PIL import Image
import pytesseract

# ====== CONFIGURAÇÃO DO TESSERACT ======
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# =========================================


class ProcessadorPDF:
    def __init__(self, root):
        self.root = root
        self.root.title("Processador de PDF — Recorte, Compressão e OCR")
        self.root.geometry("720x620")

        self.arquivos = []
        self.pasta_saida = tk.StringVar()

        self.corte_esquerda = tk.DoubleVar(value=0.00)
        self.corte_direita  = tk.DoubleVar(value=1.72)
        self.corte_topo     = tk.DoubleVar(value=0.69)
        self.corte_baixo    = tk.DoubleVar(value=0.76)

        self.max_dim      = tk.IntVar(value=1400)
        self.jpeg_quality = tk.IntVar(value=65)

        self.aplicar_recorte = tk.BooleanVar(value=True)
        self.aplicar_compressao = tk.BooleanVar(value=True)
        self.aplicar_ocr = tk.BooleanVar(value=True)

        self._montar_interface()

    def _montar_interface(self):
        pad = {"padx": 10, "pady": 5}

        frame_arq = tk.LabelFrame(self.root, text="Arquivos", font=("Arial", 10, "bold"))
        frame_arq.pack(fill="x", **pad)
        tk.Button(frame_arq, text="Selecionar PDFs...", command=self.selecionar_arquivos,
                  width=20).pack(side="left", padx=5, pady=5)
        self.lbl_arquivos = tk.Label(frame_arq, text="Nenhum arquivo selecionado", anchor="w")
        self.lbl_arquivos.pack(side="left", padx=5)

        frame_dest = tk.LabelFrame(self.root, text="Pasta de destino", font=("Arial", 10, "bold"))
        frame_dest.pack(fill="x", **pad)
        tk.Button(frame_dest, text="Escolher pasta...", command=self.selecionar_pasta,
                  width=20).pack(side="left", padx=5, pady=5)
        tk.Entry(frame_dest, textvariable=self.pasta_saida, width=60).pack(side="left", padx=5)

        frame_op = tk.LabelFrame(self.root, text="Opções de processamento", font=("Arial", 10, "bold"))
        frame_op.pack(fill="x", **pad)
        tk.Checkbutton(frame_op, text="Recortar margens", variable=self.aplicar_recorte).grid(row=0, column=0, sticky="w", padx=5)
        tk.Checkbutton(frame_op, text="Comprimir imagens", variable=self.aplicar_compressao).grid(row=0, column=1, sticky="w", padx=5)
        tk.Checkbutton(frame_op, text="OCR em páginas sem texto útil", variable=self.aplicar_ocr).grid(row=0, column=2, sticky="w", padx=5)

        frame_rec = tk.LabelFrame(self.root, text="Recorte (cm)", font=("Arial", 10, "bold"))
        frame_rec.pack(fill="x", **pad)
        tk.Label(frame_rec, text="Esquerda:").grid(row=0, column=0, sticky="e", padx=5)
        tk.Entry(frame_rec, textvariable=self.corte_esquerda, width=8).grid(row=0, column=1, padx=5)
        tk.Label(frame_rec, text="Direita:").grid(row=0, column=2, sticky="e", padx=5)
        tk.Entry(frame_rec, textvariable=self.corte_direita, width=8).grid(row=0, column=3, padx=5)
        tk.Label(frame_rec, text="Topo:").grid(row=0, column=4, sticky="e", padx=5)
        tk.Entry(frame_rec, textvariable=self.corte_topo, width=8).grid(row=0, column=5, padx=5)
        tk.Label(frame_rec, text="Baixo:").grid(row=0, column=6, sticky="e", padx=5)
        tk.Entry(frame_rec, textvariable=self.corte_baixo, width=8).grid(row=0, column=7, padx=5)

        frame_comp = tk.LabelFrame(self.root, text="Compressão", font=("Arial", 10, "bold"))
        frame_comp.pack(fill="x", **pad)
        tk.Label(frame_comp, text="Dimensão máx (px):").grid(row=0, column=0, sticky="e", padx=5)
        tk.Entry(frame_comp, textvariable=self.max_dim, width=8).grid(row=0, column=1, padx=5)
        tk.Label(frame_comp, text="Qualidade JPEG (1-100):").grid(row=0, column=2, sticky="e", padx=5)
        tk.Entry(frame_comp, textvariable=self.jpeg_quality, width=8).grid(row=0, column=3, padx=5)

        self.btn_processar = tk.Button(self.root, text="▶ PROCESSAR", command=self.processar_thread,
                                        bg="#2d7a3e", fg="white", font=("Arial", 11, "bold"),
                                        height=2)
        self.btn_processar.pack(fill="x", **pad)

        self.progresso = ttk.Progressbar(self.root, mode="determinate")
        self.progresso.pack(fill="x", padx=10)

        frame_log = tk.LabelFrame(self.root, text="Log", font=("Arial", 10, "bold"))
        frame_log.pack(fill="both", expand=True, **pad)
        self.log = scrolledtext.ScrolledText(frame_log, height=10, font=("Consolas", 9))
        self.log.pack(fill="both", expand=True, padx=5, pady=5)

    def selecionar_arquivos(self):
        arq = filedialog.askopenfilenames(title="Selecione os PDFs", filetypes=[("PDF", "*.pdf")])
        if arq:
            self.arquivos = list(arq)
            self.lbl_arquivos.config(text=f"{len(self.arquivos)} arquivo(s) selecionado(s)")

    def selecionar_pasta(self):
        pasta = filedialog.askdirectory(title="Escolha a pasta de destino")
        if pasta:
            self.pasta_saida.set(pasta)

    def escrever_log(self, msg):
        self.log.insert(tk.END, msg + "\n")
        self.log.see(tk.END)
        self.root.update_idletasks()

    def processar_thread(self):
        if not self.arquivos:
            messagebox.showwarning("Atenção", "Selecione pelo menos um arquivo PDF.")
            return
        if not self.pasta_saida.get():
            messagebox.showwarning("Atenção", "Escolha a pasta de destino.")
            return
        self.btn_processar.config(state="disabled")
        thread = threading.Thread(target=self.processar, daemon=True)
        thread.start()

    def pagina_precisa_ocr(self, page, minimo_chars=40):
        """
        Detecta se a página é essencialmente uma imagem escaneada.
        Ignora o texto das laterais do SAJ (tarja de protocolo) e cabeçalho/rodapé.
        Conta apenas texto no "miolo" da página.
        """
        rect = page.rect
        # Define área central (descarta 15% de cada lado e 8% do topo/baixo)
        miolo = fitz.Rect(
            rect.x0 + rect.width  * 0.15,
            rect.y0 + rect.height * 0.08,
            rect.x1 - rect.width  * 0.15,
            rect.y1 - rect.height * 0.08
        )
        texto_miolo = page.get_text(clip=miolo).strip()
        return len(texto_miolo) < minimo_chars

    def fazer_ocr_pagina(self, page):
        """Renderiza a página em alta resolução, faz OCR e insere camada de texto invisível."""
        pix = page.get_pixmap(dpi=300)
        img = Image.open(io.BytesIO(pix.tobytes("png")))

        pdf_ocr_bytes = pytesseract.image_to_pdf_or_hocr(img, lang="por", extension="pdf")
        ocr_doc = fitz.open(stream=pdf_ocr_bytes, filetype="pdf")
        ocr_page = ocr_doc[0]

        escala = 72 / 300
        blocks = ocr_page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                for span in line["spans"]:
                    texto = span["text"]
                    if not texto.strip():
                        continue
                    bbox = span["bbox"]
                    x0 = bbox[0] * escala
                    y0 = bbox[1] * escala
                    x1 = bbox[2] * escala
                    y1 = bbox[3] * escala
                    try:
                        page.insert_text(
                            (x0, y1),
                            texto,
                            fontsize=max((y1 - y0) * 0.9, 1),
                            render_mode=3,  # invisível
                            color=(0, 0, 0)
                        )
                    except Exception:
                        pass
        ocr_doc.close()

    def processar(self):
        try:
            pt = 28.35
            os.makedirs(self.pasta_saida.get(), exist_ok=True)
            self.progresso["maximum"] = len(self.arquivos)
            self.progresso["value"] = 0

            MAX_DIM = self.max_dim.get()
            Q = self.jpeg_quality.get()

            for idx, caminho in enumerate(self.arquivos, 1):
                nome = os.path.basename(caminho)
                self.escrever_log(f"\n[{idx}/{len(self.arquivos)}] Processando: {nome}")

                doc = fitz.open(caminho)

                # === 1) RECORTE ===
                if self.aplicar_recorte.get():
                    for page in doc:
                        mb = page.mediabox
                        novo_rect = fitz.Rect(
                            mb.x0 + self.corte_esquerda.get() * pt,
                            mb.y0 + self.corte_baixo.get()    * pt,
                            mb.x1 - self.corte_direita.get()  * pt,
                            mb.y1 - self.corte_topo.get()     * pt
                        )
                        page.set_cropbox(novo_rect)
                    self.escrever_log("  ✓ Recorte aplicado")

                # === 2) OCR (antes da compressão, para máxima qualidade) ===
                if self.aplicar_ocr.get():
                    paginas_ocr = 0
                    paginas_puladas = []
                    for i, page in enumerate(doc):
                        if self.pagina_precisa_ocr(page):
                            try:
                                self.fazer_ocr_pagina(page)
                                paginas_ocr += 1
                                self.escrever_log(f"    → OCR na pág {i+1}")
                            except Exception as e:
                                self.escrever_log(f"    ⚠ Erro OCR pág {i+1}: {e}")
                        else:
                            paginas_puladas.append(i+1)
                    if paginas_ocr:
                        self.escrever_log(f"  ✓ OCR em {paginas_ocr} página(s)")
                    else:
                        self.escrever_log("  ✓ Nenhuma página precisou de OCR")

                # === 3) COMPRESSÃO (por último) ===
                if self.aplicar_compressao.get():
                    for page in doc:
                        for img_info in page.get_images(full=True):
                            xref = img_info[0]
                            try:
                                base = doc.extract_image(xref)
                                pil = Image.open(io.BytesIO(base["image"]))
                                w, h = pil.size
                                if max(w, h) <= MAX_DIM:
                                    continue
                                ratio = MAX_DIM / max(w, h)
                                pil = pil.resize((int(w*ratio), int(h*ratio)), Image.LANCZOS)
                                if pil.mode != "RGB":
                                    pil = pil.convert("RGB")
                                buf = io.BytesIO()
                                pil.save(buf, format="JPEG", quality=Q, optimize=True)
                                page.replace_image(xref, stream=buf.getvalue())
                            except Exception:
                                pass
                    self.escrever_log("  ✓ Compressão aplicada")

                # === Salvar ===
                saida = os.path.join(self.pasta_saida.get(), nome)
                doc.save(saida, garbage=4, deflate=True, clean=True)
                doc.close()

                orig = os.path.getsize(caminho) / 1024
                novo = os.path.getsize(saida) / 1024
                red = (1 - novo/orig) * 100
                self.escrever_log(f"  📦 {orig:.0f} KB → {novo:.0f} KB ({red:+.1f}%)")

                self.progresso["value"] = idx

            self.escrever_log("\n✅ CONCLUÍDO!")
            messagebox.showinfo("Concluído", "Processamento finalizado com sucesso!")
        except Exception as e:
            self.escrever_log(f"\n❌ ERRO: {e}")
            messagebox.showerror("Erro", str(e))
        finally:
            self.btn_processar.config(state="normal")


if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessadorPDF(root)
    root.mainloop()