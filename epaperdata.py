
import os
import datetime
from flask import Flask, request, jsonify, url_for
import fitz
from PIL import Image
from models import ExtractDataSchema
app = Flask(__name__)

MAX_IMAGES = 50
image_filenames = []
pdf_filepaths = []

@app.route('/api/extractepaper_data', methods=['POST'])
def extract_epaperdata():
    schema = ExtractDataSchema()
    errors = schema.validate(request.files)

    if errors:
        return jsonify({'error': errors}), 400

    pdf_file = request.files['pdf']

    save_path = os.path.join('S:\\FLASK2\\pdf2', pdf_file.filename)
    pdf_file.save(save_path)

    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"cropped_image_{current_time}.jpg"
    image_path = os.path.join('S:\\FLASK2\\static', filename)

    x_min = int(request.args.get('x_min'))
    x_max = int(request.args.get('x_max'))
    y_min = int(request.args.get('y_min'))
    y_max = int(request.args.get('y_max'))
    page_number = int(request.args.get('page_number'))

    if x_min > x_max:
        x_min, x_max = x_max, x_min
    if y_min > y_max:
        y_min, y_max = y_max, y_min

    doc = fitz.open(save_path)
    page = doc[page_number]
    pix = page.get_pixmap(dpi=280)
    cropped_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    cropped_image = cropped_image.crop((x_min*4, y_min*4, x_max*4, y_max*4))
    cropped_image.save(image_path)
    zoom_factor = 1 
    cropped_image = cropped_image.resize((cropped_image.width * zoom_factor, cropped_image.height * zoom_factor))
    cropped_image.save(image_path)
    image_url = url_for('static',  filename=filename)
    image_filenames.append(filename)

    
    if len(image_filenames) >MAX_IMAGES:
        oldest_image = image_filenames.pop(0)
        os.remove(os.path.join('S:\\FLASK2\\static', oldest_image))
    
    if len(pdf_filepaths)==50:
        oldest_pdf = pdf_filepaths.pop(0)
        os.remove(oldest_pdf)

    pdf_file.save(save_path)
    pdf_filepaths.append(save_path)

    data = {
        'image_url': image_url
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
