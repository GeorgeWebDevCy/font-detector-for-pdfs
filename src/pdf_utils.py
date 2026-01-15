import fitz  # PyMuPDF

def analyze_pdf(file_path):
    """
    Analyzes a PDF file and extracts font information.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        list: A list of dictionaries, where each dictionary represents a unique font
              found in the PDF. Keys: 'name', 'type', 'encoding', 'is_embedded'.
              Returns None if an error occurs.
    """
    try:
        doc = fitz.open(file_path)
        fonts = {}

        for page in doc:
            for font in page.get_fonts():
                # font is a tuple: (xref, ext, type, basefont, name, encoding)
                # We use the unique identifier (xref) or basefont name to avoid duplicates
                # However, get_fonts() returns a list of fonts on the page.
                # Let's deduplicate based on 'name' and 'basefont' combination or just 'name'.
                
                # Unpack common fields
                # (xref, ext, type, basefont, name, encoding, ...) - length varies by version, but first few are stable.
                # Modern PyMuPDF get_fonts(full=True) gives more info.
                # Let's use the default list first.
                
                # Structure:
                # [xref, ext, type, basefont, name, encoding]
                if len(font) >= 4:
                    font_name = font[3] # basefont
                    font_type = font[2]
                    font_encoding = font[5] if len(font) > 5 else "n/a"
                    
                    # Create a unique key
                    key = (font_name, font_type, font_encoding)
                    
                    if key not in fonts:
                        fonts[key] = {
                            "name": font_name,
                            "type": font_type,
                            "encoding": font_encoding,
                            # ext often indicates embedded format (e.g., 'n/a', 'ttf', 'cff')
                            # If ext is 'n/a' or empty, it might not be embedded or standard.
                            "is_embedded": font[1] != 'n/a' and font[1] != '' 
                        }

        doc.close()
        return list(fonts.values())

    except Exception as e:
        print(f"Error analyzing PDF: {e}")
        return None

if __name__ == "__main__":
    # Test block
    import sys
    if len(sys.argv) > 1:
        results = analyze_pdf(sys.argv[1])
        if results:
            for f in results:
                print(f)
        else:
            print("No fonts found or error.")
    else:
        print("Usage: python pdf_utils.py <path_to_pdf>")
