import fitz

def create_test_pdf():
    doc = fitz.open()
    page = doc.new_page()
    
    # Insert text with default font (Helvetica usually)
    page.insert_text((50, 50), "Hello World", fontname="helv", fontsize=12)
    
    # Insert text with Times Roman
    page.insert_text((50, 100), "Another Font", fontname="tiro", fontsize=14)
    
    doc.save("test_font.pdf")
    print("Created test_font.pdf")

if __name__ == "__main__":
    create_test_pdf()
