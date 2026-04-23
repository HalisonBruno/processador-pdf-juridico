# \# Processador de PDF Jurídico

# 

# Ferramenta com interface gráfica para otimizar PDFs processuais do sistema SAJ (Tribunal de Justiça), com foco em documentos jurídicos que precisam ser citados em petições, decisões e sentenças.
# Além de economizar tokens junto ao agente de IA, realiza o pré-processamento com OCR e remove de ruídos como assinatura eletrônica, cabeçalhos e rodapés, contribuindo para maior concentração do agente no conteúdo jurídico do documento.

# 

# \## ✨ Funcionalidades

# 

# \- \*\*Recorte automático de margens\*\* com medidas personalizáveis em centímetros

# \- \*\*Compressão inteligente\*\* que preserva o texto nativo selecionável (redução média de \~60%)

# \- \*\*OCR automático\*\* em páginas escaneadas (RG, contratos, matrículas, etc.) usando Tesseract

# \- \*\*Detecção inteligente\*\* de páginas que precisam de OCR — ignora a tarja lateral do SAJ para evitar duplicação de texto

# \- \*\*Interface gráfica\*\* simples e intuitiva

# \- \*\*Processamento em lote\*\* de múltiplos arquivos

# 

# \## 🎯 Motivação

# 

# Autos processuais do SAJ frequentemente contêm documentos escaneados sem camada de texto, o que impede a pesquisa por termos e dificulta a citação precisa de documentos com o número da folha correspondente. Esta ferramenta automatiza todo o fluxo de preparação desses PDFs.

# 

# \## 🛠️ Tecnologias

# 

# \- Python 3

# \- PyMuPDF (fitz) — manipulação de PDFs

# \- Pillow — processamento de imagens

# \- pytesseract + Tesseract OCR — reconhecimento de texto

# \- Tkinter — interface gráfica

# 

# \## 📦 Instalação

# 

# \### Opção 1: Executável (Windows)

# Baixe o `.exe` pronto na seção \[Releases](../../releases) deste repositório. Requer apenas o \[Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) instalado (marcar idioma Portuguese durante a instalação).

# 

# \### Opção 2: Código-fonte

# 

# 1\. Instale o \[Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) (marcar idioma Portuguese)

# 2\. Instale as dependências Python:

# ```bash

# &#x20;  pip install -r requirements.txt

# ```

# 3\. Execute:

# ```bash

# &#x20;  python processador\_pdf.py

# ```

# 

# \## 🚀 Como usar

# 

# 1\. Clique em \*\*"Selecionar PDFs..."\*\* e escolha um ou mais arquivos

# 2\. Clique em \*\*"Escolher pasta..."\*\* para definir onde salvar

# 3\. Ajuste as medidas de recorte se necessário (padrões configurados para recortes típicos do SAJ)

# 4\. Escolha quais operações aplicar: recorte, compressão, OCR

# 5\. Clique em \*\*"▶ PROCESSAR"\*\*

# 

# \## 📊 Ordem de processamento

# 

# O programa aplica as operações na ordem otimizada:

# 

# 1\. \*\*Recorte\*\* de margens (aproveita a área útil da página)

# 2\. \*\*OCR\*\* nas páginas detectadas como escaneadas (máxima qualidade de imagem preservada)

# 3\. \*\*Compressão\*\* por último (reduz tamanho final sem afetar o OCR)

# 

# \## 📝 Licença

# 

# MIT

