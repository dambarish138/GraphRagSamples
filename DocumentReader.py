import pdfplumber as plumber


def extract_text_with_layout(pdf_path):
    out_text = ""
    with plumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                # Extract text with layout preserved
                text = page.extract_text()
                if text:
                    out_text += out_text + text
    return out_text

def write_to_file(output_file_path, obj):
     with open(output_file_path, 'w') as out:
          out.write(str(obj))
