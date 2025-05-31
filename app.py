from flask import Flask, render_template, request, redirect, url_for, flash
import os
import uuid

from config import Config, LANGUAGES
from ocr.extract_text import extract_text_from_image, extract_text_from_pdf
from translate.translator import preserve_numbers_translate
from utils.file_loader import is_pdf, is_image

app = Flask(__name__)
app.config.from_object(Config)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html', languages=LANGUAGES)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(url_for('index'))

    file = request.files['file']
    target_language = request.form.get('language')

    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))
    if not target_language or target_language not in LANGUAGES:
        flash('Please select a valid target language')
        return redirect(url_for('index'))
    if file and allowed_file(file.filename):
        filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        try:
            # Extract text from uploaded file
            if is_image(file_path):
                extracted_text = extract_text_from_image(file_path)
            elif is_pdf(file_path):
                extracted_text = extract_text_from_pdf(file_path)
            else:
                flash('Unsupported file format')
                os.remove(file_path)
                return redirect(url_for('index'))

            print(f"\n=== EXTRACTED TEXT ===\n{extracted_text}\n")

            if not extracted_text.strip():
                flash('No text found in the document')
                os.remove(file_path)
                return redirect(url_for('index'))

            # Translate the extracted text
            translated_text = preserve_numbers_translate(extracted_text, target_language)

            print(f"\n=== TRANSLATED TEXT ===\n{translated_text}\n")

            # Clean up file
            os.remove(file_path)

            return render_template('result.html',
                                   original_text=extracted_text,
                                   translated_text=translated_text,
                                   target_language=LANGUAGES[target_language])
        except Exception as e:
            flash(f'Error processing file: {str(e)}')
            if os.path.exists(file_path):
                os.remove(file_path)
            return redirect(url_for('index'))
    else:
        flash('Invalid file type. Please upload an image or PDF file.')
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
