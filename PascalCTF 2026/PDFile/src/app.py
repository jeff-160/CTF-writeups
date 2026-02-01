from flask import Flask, render_template, request, send_file, jsonify, url_for
from werkzeug.utils import secure_filename
from lxml import etree
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
import os
import uuid

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pasx'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def sanitize(xml_content):
    try:
        content_str = xml_content.decode('utf-8')
    except UnicodeDecodeError:
        return False
    
    if "&#" in content_str:
        return False
    
    blacklist = [
        "flag", "etc", "sh", "bash", 
        "proc", "pascal", "tmp", "env", 
        "bash", "exec", "file", "pascalctf is not fun", # good old censorship
    ]
    if any(a in content_str.lower() for a in blacklist):
        return False
    return True


def parse_pasx(xml_content):
    """Parse .pasx XML content and extract book data."""
    
    if not sanitize(xml_content):
        raise ValueError("XML content contains disallowed keywords.")
    
    try:
        parser = etree.XMLParser(encoding='utf-8', no_network=False, resolve_entities=True, recover=True)
        root = etree.fromstring(xml_content, parser=parser)
        
        book_data = {
            'title': root.findtext('title', default='Untitled'),
            'author': root.findtext('author', default='Unknown Author'),
            'year': root.findtext('year', default=''),
            'isbn': root.findtext('isbn', default=''),
            'chapters': []
        }
        
        chapters = root.find('chapters')
        if chapters is not None:
            for chapter in chapters.findall('chapter'):
                chapter_data = {
                    'number': chapter.get('number', ''),
                    'title': chapter.findtext('title', default=''),
                    'content': chapter.findtext('content', default='')
                }
                book_data['chapters'].append(chapter_data)
        
        return book_data
    except etree.XMLSyntaxError as e:
        raise ValueError(f"Invalid XML: {str(e)}")


def generate_pdf(book_data, output_path):
    """Generate a PDF from parsed book data."""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'BookTitle',
        parent=styles['Heading1'],
        fontSize=28,
        alignment=TA_CENTER,
        spaceAfter=20
    )
    
    author_style = ParagraphStyle(
        'Author',
        parent=styles['Normal'],
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=10,
        textColor='#666666'
    )
    
    meta_style = ParagraphStyle(
        'Meta',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_CENTER,
        spaceAfter=5,
        textColor='#888888'
    )
    
    chapter_title_style = ParagraphStyle(
        'ChapterTitle',
        parent=styles['Heading2'],
        fontSize=18,
        spaceBefore=20,
        spaceAfter=12
    )
    
    content_style = ParagraphStyle(
        'Content',
        parent=styles['Normal'],
        fontSize=12,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=16
    )
    
    story = []
    
    story.append(Spacer(1, 2 * inch))
    story.append(Paragraph(book_data['title'], title_style))
    story.append(Spacer(1, 0.5 * inch))
    story.append(Paragraph(f"by {book_data['author']}", author_style))
    
    if book_data['year']:
        story.append(Paragraph(f"Published: {book_data['year']}", meta_style))
    
    if book_data['isbn']:
        story.append(Paragraph(f"ISBN: {book_data['isbn']}", meta_style))
    
    story.append(PageBreak())
    
    for chapter in book_data['chapters']:
        chapter_num = chapter['number']
        chapter_title = chapter['title']
        
        if chapter_num and chapter_title:
            heading = f"Chapter {chapter_num}: {chapter_title}"
        elif chapter_title:
            heading = chapter_title
        elif chapter_num:
            heading = f"Chapter {chapter_num}"
        else:
            heading = "Chapter"
        
        story.append(Paragraph(heading, chapter_title_style))
        
        if chapter['content']:
            paragraphs = chapter['content'].split('\n\n')
            for para in paragraphs:
                if para.strip():
                    story.append(Paragraph(para.strip(), content_style))
        
        story.append(Spacer(1, 0.3 * inch))
    
    doc.build(story)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Only .pasx files are allowed'}), 400
    
    try:
        xml_content = file.read()
        book_data = parse_pasx(xml_content)
        
        pdf_filename = f"{uuid.uuid4().hex}.pdf"
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)
        
        generate_pdf(book_data, pdf_path)
        
        return jsonify({
            'success': True,
            'pdf_url': url_for('get_pdf', filename=pdf_filename),
            'book_title': book_data['title'],
            'book_author': book_data['author']
        })
    
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500


@app.route('/pdf/<filename>')
def get_pdf(filename):
    pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
    
    if not os.path.exists(pdf_path):
        return jsonify({'error': 'PDF not found'}), 404
    
    return send_file(pdf_path, mimetype='application/pdf')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
