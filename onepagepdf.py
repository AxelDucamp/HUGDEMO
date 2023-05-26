from PyPDF2 import PdfFileReader, PdfFileWriter

def extract_page_from_pdf(pdf_path, page_num, output_pdf_path):
    reader = PdfFileReader(pdf_path)
    writer = PdfFileWriter()

    # The PyPDF2 library uses a 0-based index for getting pages
    page = reader.getPage(page_num - 1) # Subtract 1 from page_num since pages are zero-indexed
    writer.addPage(page)

    with open(output_pdf_path, 'wb') as output_pdf:
        writer.write(output_pdf)

# Replace these with your PDF path, desired page number, and output PDF path
pdf_path = "hug-en-bref.pdf"
page_num = 4
output_pdf_path = "output.pdf"

extract_page_from_pdf(pdf_path, page_num, output_pdf_path)
