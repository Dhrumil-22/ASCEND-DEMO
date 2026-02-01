import PyPDF2
import sys
import io

def extract_pdf_text(pdf_path):
    """Extract text from a PDF file."""
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += f"\n--- Page {page_num + 1} ---\n"
                try:
                    page_text = page.extract_text()
                    text += page_text if page_text else "[No text extracted from this page]"
                except Exception as e:
                    text += f"[Error extracting text: {str(e)}]"
            return text
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python extract_pdf_v2.py <pdf_file> <output_file>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    output_path = sys.argv[2]
    
    text = extract_pdf_text(pdf_path)
    
    # Write to file with UTF-8 encoding
    with io.open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    
    print(f"Successfully extracted text from {pdf_path} to {output_path}")
