from PIL import Image
import datetime
import os
import fitz
from flask import Flask, jsonify, request, send_file ,url_for
import base64
from models import ExtractDataSchema
from flask_cors import CORS
# app = Flask(__name__, static_url_path='', static_folder='E:\\FLASK2')

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
    save_path = os.path.join('E:\\FLASK2\\pdf', pdf_file.filename)
    pdf_file.save(save_path)
    
     
    
    x_min = int(request.args.get('x_min'))
    x_max = int(request.args.get('x_max'))
    y_min = int(request.args.get('y_min'))
    y_max = int(request.args.get('y_max'))
    page_number = int(request.args.get('page_number'))
    # save_path = str(request.args.get("pdf","E:\FLASK2\pdf\\1 Jan 2012.pdf"))


    
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

        image_path = os.path.join('E:\\FLASK2\\static', 'cropped_image.jpg')  # Output path for the zoomed image
        

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

        
        pix = page.get_pixmap(dpi=142)
        # pix = page.get_pixmap()
        cropped_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        cropped_image = cropped_image.crop((x_min*2, y_min*2, x_max*2, y_max*2))
        cropped_image.save(image_path)
        zoom_factor = 1 # Adjust the zoom factor according to your requirement
        cropped_image = cropped_image.resize((cropped_image.width * zoom_factor, cropped_image.height * zoom_factor))
        cropped_image.save(image_path)
    doc.close()

    for index, arpara in enumerate(output_content1):
        paragraph = index, arpara.replace("\n", " ")
        output_content2.append(paragraph)

    # image_url   

    # file_response = send_file(image_path, mimetype='image/jpeg')

    image_url = url_for('static', filename=image_path)

    # with open(image_path, 'rb') as image_file:
    #     image_data = image_file.read()
    #     base64_image = base64.b64encode(image_data).decode('utf-8')
        
    # base64_url = f"data:image/jpeg;base64,{base64_image}" 
    
    data = {
        'output_content2': output_content2,
        'image': image_url
        }
    # return file_response
    return jsonify(data)

    

    
    



#==================================================#


@app.route('/api/coordinate', methods=['POST'])

def extract_coordinate():
    schema = ExtractDataSchema()
    errors = schema.validate(request.files)
    if errors:
        return jsonify({'error': errors}), 400
    pdf_file = request.files['pdf']  # Access the uploaded PDF file
    print(pdf_file)

    # Create a folder based on the current date
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    folder_path = os.path.join('E:\\FLASK2\\pdf')
    os.makedirs(folder_path, exist_ok=True)

    # Save the PDF file in the created folder
    save_path = os.path.join(folder_path, pdf_file.filename)
    pdf_file.save(save_path)

    doc = fitz.open(save_path)
    coordinate = []
    for page_number in range(len(doc)):
        Page = doc[page_number]
        data = Page.mediabox.width, Page.mediabox.height
        coordinate.append(data)

    response_data = {
        'coordinates': coordinate,
        'save_path': save_path
    }

    return jsonify(response_data)




@app.route('/api/coordinate', methods=['GET'])
def get_coordinates():
    schema = ExtractDataSchema()
    errors = schema.validate(request.files)
    if errors:
        return jsonify({'error': errors}), 400
    pdf_file = request.files['pdf']  # Access the uploaded PDF file
    print(pdf_file)
    save_path = os.path.join('E:\FLASK2\pdf', pdf_file.filename)
    pdf_file.save(save_path)
    

    # Get the PDF file path from the request query parameters
    pdf_path = request.args.get('pdf_path')

    # Validate the PDF file path
    if not pdf_path:
        return jsonify({'error': 'PDF file path is missing'}), 400

    # Check if the PDF file exists
    if not os.path.exists(pdf_path):
        return jsonify({'error': 'PDF file does not exist'}), 400

    # Open the PDF file
    doc = fitz.open(pdf_path)

    # Extract the coordinates for each page
    coordinates = []
    for page_number in range(len(doc)):
        page = doc[page_number]
        data = page.mediabox.width, page.mediabox.height
        coordinates.append(data)

    # Prepare the response data
    response_data = {
        'coordinates': coordinates,
        'save_path': pdf_path
    }

    # Return the response as JSON
    return jsonify(response_data)


if __name__ == '__main__':
    # app.run(debug=True,host='0.0.0.0')
    app.run(debug=True, host='0.0.0.0', port=8080)
    