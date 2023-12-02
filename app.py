
from PIL import Image
import datetime
import os
import fitz
from flask import Flask, jsonify, request, url_for
from models import ExtractDataSchema
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def is_article_block2(block, x_min, y_min, x_max, y_max):
    block_x_min, block_y_min, block_x_max, block_y_max = block["bbox"]
    if (
        block_x_min >= x_min
        and block_x_max <= x_max
        and block_y_min >= y_min
        and block_y_max <= y_max
        and sum(len(span["text"].split()) for line in block["lines"] for span in line["spans"]) > 10
    ):
        return True
    return False

@app.route('/api/extractdata_withfont2', methods=['POST'])

def extract_articles2():
    schema = ExtractDataSchema()
    errors = schema.validate(request.files)

    if errors:
        return jsonify({'error': errors}), 400

    pdf_file = request.files['pdf']  
    # save_path = os.path.join('/home/myFlaskApp/pdf', pdf_file.filename)
    save_path = os.path.join('S:\\FLASK\\pdf', pdf_file.filename)
    pdf_file.save(save_path)

    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"cropped_image_{current_time}.jpg"
    # image_path = os.path.join('/home/myFlaskApp/static', filename)
    image_path = os.path.join('S:\\FLASK\\static', filename)


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
    blocks = page.get_text("dict", flags=11)["blocks"]

    sorted_blocks = sorted(blocks, key=lambda b: (b["bbox"][1], b["bbox"][0]))

    extracted_text = []

    for b in sorted_blocks:
        newblock = is_article_block2(b, x_min, y_min, x_max, y_max)
        if newblock:
            print("else part")
            block_text = ""
            for l in b["lines"]:
                for s in l["spans"]:
                    block_text += s["text"]+" "

            block_text = block_text.replace("�", "P")

            font = b["lines"][0]["spans"][0]["font"]
            fontsize = b["lines"][0]["spans"][0]["size"]
            extracted_text.append({"font": font, "fontsize": fontsize, "paragraph": block_text})

        else:
            print("else part")
            if (
                x_min <= b["bbox"][0] <= x_max and
                y_min <= b["bbox"][1] <= y_max
            ):
                block_text = ""
                for l in b["lines"]:
                    for s in l["spans"]:
                        block_text += s["text"]+" "
                block_text = block_text.replace("�", "P")
                font = b["lines"][0]["spans"][0]["font"]
                fontsize = b["lines"][0]["spans"][0]["size"],
                extracted_text.append({"font": font,"fontsize": fontsize[0], "paragraph": block_text})
                print(block_text)

    doc.close()

    doc = fitz.open(save_path)
    page = doc[page_number]
    pix = page.get_pixmap(dpi=280)
    cropped_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    cropped_image = cropped_image.crop((x_min*4, y_min*4, x_max*4, y_max*4))
    cropped_image.save(image_path)
    zoom_factor = 1
    cropped_image = cropped_image.resize((cropped_image.width * zoom_factor, cropped_image.height * zoom_factor))
    cropped_image.save(image_path)
    image_url = url_for('static', filename=filename)
    
    data = {
        'image_url': image_url,
        'data': extracted_text
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
