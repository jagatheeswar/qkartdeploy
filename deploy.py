import os
import fitz  # PyMuPDF
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import re

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def extract_book_details(file_path):
    # Open the PDF file
    document = fitz.open(file_path)
    
    # Extract metadata
    metadata = document.metadata
    book_name = metadata.get('title', 'Unknown Title')
    
    # Extract text from the first few pages to find ISBN, author name, and title if needed
    isbn = "Unknown ISBN"
    author_name = "Unknown Author"
    all_text = ""
    
    # If title is not in metadata, search in the first few pages
    if book_name == 'Unknown Title':
        for page_num in range(min(10, len(document))):  # Check first 10 pages
            page = document.load_page(page_num)
            text = page.get_text()
            all_text += text + "\n\n"  # Append text of each page to all_text
            
            # Search for title
            title_match = re.search(r'\bTitle[:\s]*(.+)', text)
            if title_match:
                book_name = title_match.group(1).strip()
            
            # Search for ISBN after 'ISBN:' or 'ISBN-10:' or 'ISBN-13:'
            isbn_match = re.search(r'\bISBN(?:-10)?(?:-13)?[:\s]*([\d\-Xx]+)\b', text)
            if isbn_match:
                isbn = isbn_match.group(1).strip()  # Extract and clean ISBN
            
            # Search for author name after copyright
            copyright_match = re.search(r'Copyright\s+©\s+\d{4}\s+by\s+(.+)', text)
            if copyright_match:
                author_name = copyright_match.group(1).strip()
                print(f"Found author name: {author_name}")
                break  # Assuming the author name is found, exit the loop
    
    total_pages = len(document)
    
    # Close the document
    document.close()
    
    # Print all text in the first 10 pages to the console
    print(all_text)
    
    return {
        "book_name": book_name,
        "author_name": author_name,
        "isbn_number": isbn,
        "total_pages": total_pages
    }

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    
    if file.filename == '':
        return 'No selected file'
    
    if file:
        category = request.form['category']
        subcategory = request.form['subcategory']
        
        category_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(category))
        subcategory_path = os.path.join(category_path, secure_filename(subcategory))
        os.makedirs(subcategory_path, exist_ok=True)
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(subcategory_path, filename)
        file.save(file_path)
        
        # Extract details from the PDF
        details = extract_book_details(file_path)
        
        return render_template('upload_result.html', details=details)

    return 'Failed to upload file'

@app.route('/admin')
def admin_page():
    return render_template('adminindex.html')

if __name__ == "__main__":
    app.run(debug=True)
