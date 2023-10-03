from PIL import Image
import datetime
import os
import fitz
from flask import Flask, jsonify, request,url_for
from models import ExtractDataSchema
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

from PIL import Image

def is_article_block(block, x_min, y_min, x_max, y_max):
    # Check if the block's rectangle intersects with the defined boundaries
    return (
        block[0] >= x_min and
        block[2] <= x_max and
        block[1] >= y_min and
        block[3] <= y_max and
        len(block[4].split()) > 10
    )

@app.route('/api/extract', methods=['POST'])
def extract_articles():
    schema = ExtractDataSchema()
    errors = schema.validate(request.files)

    if errors:
        return jsonify({'error': errors}), 400

    
    pdf_file = request.files['pdf']  # Access the uploaded PDF file
    save_path = os.path.join('S:\\FLASK2\\pdf', pdf_file.filename)
    pdf_file.save(save_path)
    
     
    
    x_min = int(request.args.get('x_min'))
    x_max = int(request.args.get('x_max'))
    y_min = int(request.args.get('y_min'))
    y_max = int(request.args.get('y_max'))
    page_number = int(request.args.get('page_number'))



    
    if x_min>x_max:
                x0=x_max
                x_max=x_min
                x_min=x0
    if y_min>y_max:
                y0=y_max
                y_max=y_min
                y_min=y0 


    output_content1 = []
    output_content2 = []
    doc = fitz.open(save_path)

    if page_number >= 0 and page_number < len(doc):
        page = doc[page_number]
        blocks = page.get_text("blocks")

        from datetime import datetime
        current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cropped_image_{current_time}.jpg"
        image_path = os.path.join('S:\\FLASK2\\static', filename)

        # image_path = os.path.join('E:\\FLASK2\\static', 'cropped_image.jpg')  # Output path for the zoomed image
        

        if blocks:
            article_blocks = [block for block in blocks if is_article_block(block,x_min,y_min, x_max, y_max)]

            if article_blocks:
                sorted_blocks = sorted(article_blocks, key=lambda b: (b[0], b[1]))

                for i, article_block in enumerate(sorted_blocks):
                    article_text = article_block[4]

                    if article_text.strip():
                        article_text = article_text.replace("�", "P")
                        paragraph = article_text
                        output_content1.append(paragraph)
                    else:
                        print(f"Page {page_number+1} - No text found in Article {i+1}")
            else:
                print(f"Page {page_number+1} - No articles found")
                # cropped_text = page.get_text("text", clip=(x_min, y_min, x_max, y_max))
                cropped_text = page.get_text("word", clip=(x_min, y_min, x_max, y_max))

                if cropped_text.strip():
                    paragraph = cropped_text.strip().replace("�", "P")
                    # print(paragraph)
                    output_content1.append(paragraph)
        else:
            print(f"Page {page_number+1} - No words found")

        # crope_image   
        pix = page.get_pixmap(dpi=280)
        cropped_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        cropped_image = cropped_image.crop((x_min*4, y_min*4, x_max*4, y_max*4))
        cropped_image.save(image_path)
        zoom_factor = 1 # Adjust the zoom factor according to your requirement
        cropped_image = cropped_image.resize((cropped_image.width * zoom_factor, cropped_image.height * zoom_factor))
        cropped_image.save(image_path)
    doc.close()

    #image_url 
    
    filename2 = filename
    image_url = url_for('static', filename=filename2)


    for index, arpara in enumerate(output_content1):
        paragraph = index, arpara.replace("\n", " ")
        output_content2.append(paragraph)
    data = {
        'Image': image_url,
        'data': []
    }

    for index, arpara in enumerate(output_content1):
        paragraph = {
            'font': 'font_name',  # Replace 'font_name' with the actual font name
            'para': arpara.replace("\n", " ")
        }
        data['data'].append(paragraph)
    return jsonify(data)
    
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    