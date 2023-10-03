

# from PIL import Image
# import datetime
# import os
# import fitz
# from flask import Flask, jsonify, request, url_for
# from models import ExtractDataSchema
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# def is_article_block1(block, x_min, y_min, x_max, y_max):
#     block_x_min, block_y_min, block_x_max, block_y_max = block["bbox"]
#     return (
#         block_x_min >= x_min
#         and block_x_max <= x_max
#         and block_y_min >= y_min
#         and block_y_max <= y_max
#         and sum(len(span["text"].split()) for line in block["lines"] for span in line["spans"]) > 10
#     )

# def extract_text_from_area(pdf_path, page_number, x_min, x_max, y_min, y_max):
#     try:
#         doc = fitz.open(pdf_path)
#         page = doc[page_number]
#         blocks = page.get_text("dict", flags=11)["blocks"]
        
#         sorted_blocks = sorted(blocks, key=lambda b: (b["bbox"][0], b["bbox"][1]))

#         extracted_text = []
        

#         for b in sorted_blocks:
#             if is_article_block1(b, x_min, y_min, x_max, y_max):
#                 block_text = ""
#                 for l in b["lines"]:
#                     for s in l["spans"]:
#                         block_text += s["text"]
#                 block_text = block_text.replace("�", "P")

#                 font =  b["lines"][0]["spans"][0]["font"]

#                 extracted_text.append({"font": font, "paragraph": block_text})

        
#         doc.close()
#         return extracted_text
#     except Exception as e:
#         print("Error occurred while extracting text:", str(e))
#         return []

# @app.route('/api/extractdata_withfont', methods=['POST'])
# def extract_articles1():
#     schema = ExtractDataSchema()
#     errors = schema.validate(request.files)

#     if errors:
#         return jsonify({'error': errors}), 400

#     pdf_file = request.files['pdf']  # Access the uploaded PDF file
#     save_path = os.path.join('S:\\FLASK2\\pdf', pdf_file.filename)
#     pdf_file.save(save_path)

#     x_min = int(request.args.get('x_min'))
#     x_max = int(request.args.get('x_max'))
#     y_min = int(request.args.get('y_min'))
#     y_max = int(request.args.get('y_max'))
#     page_number = int(request.args.get('page_number'))

#     extracted_text = extract_text_from_area(save_path, page_number, x_min, x_max, y_min, y_max)

#     # Save cropped image
#     current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"cropped_image_{current_time}.jpg"
#     image_path = os.path.join('S:\\FLASK2\\static', filename)
    
#     doc = fitz.open(save_path)
#     page = doc[page_number]
#     pix = page.get_pixmap(dpi=280)
#     cropped_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#     cropped_image = cropped_image.crop((x_min*4, y_min*4, x_max*4, y_max*4))
#     cropped_image.save(image_path)

#     doc.close()
#     Get_image = url_for('static', filename=filename),
    
#     data = {
#         'image_url': Get_image,
#         'data': extracted_text
#         }
#     return jsonify(data)


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')






    

# from PIL import Image
# import datetime
# import os
# import fitz
# from flask import Flask, jsonify, request, url_for
# from models import ExtractDataSchema
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# def is_article_block1(block, x_min, y_min, x_max, y_max):
#     block_x_min, block_y_min, block_x_max, block_y_max = block["bbox"]
#     return (
#         block_x_min >= x_min
#         and block_x_max <= x_max
#         and block_y_min >= y_min
#         and block_y_max <= y_max
#         and sum(len(span["text"].split()) for line in block["lines"] for span in line["spans"]) > 10
#     )

# def extract_text_from_area(pdf_path, page_number, x_min, x_max, y_min, y_max):

    
#     doc = fitz.open(pdf_path)
#     page = doc[page_number]
#     blocks = page.get_text("dict", flags=11)["blocks"]
        
#     sorted_blocks = sorted(blocks, key=lambda b: (b["bbox"][0], b["bbox"][1]))

#     extracted_text = []
    

#     for b in sorted_blocks:
#         if is_article_block1(b, x_min, y_min, x_max, y_max):
#             block_text = ""
#             for l in b["lines"]:
#                 for s in l["spans"]:
#                     block_text += s["text"]

#             block_text = block_text.replace("�", "P")

#             font =  b["lines"][0]["spans"][0]["font"]
#             fontsize = b["lines"][0]["spans"][0]["size"],
#             extracted_text.append({"font": font,"fontsize": fontsize[0], "paragraph": block_text})

#         else:
#             if (
#                 x_min <= b["bbox"][0] <= x_max and
#                 y_min <= b["bbox"][1] <= y_max
#             ):
#                 block_text = ""
#                 for l in b["lines"]:
#                     for s in l["spans"]:
#                         block_text += s["text"]
#                 block_text = block_text.replace("�", "P")
#                 font = b["lines"][0]["spans"][0]["font"]
#                 fontsize = b["lines"][0]["spans"][0]["size"],
#                 extracted_text.append({"font": font,"fontsize": fontsize[0], "paragraph": block_text})
    
#     doc.close()
#     return extracted_text

# @app.route('/api/extractdata_withfont', methods=['POST'])
# def extract_articles1():
#     schema = ExtractDataSchema()
#     errors = schema.validate(request.files)

#     if errors:
#         return jsonify({'error': errors}), 400

#     pdf_file = request.files['pdf']  # Access the uploaded PDF file
#     # save_path = os.path.join('S:\\FLASK2\\pdf', pdf_file.filename)#S:\FLASK2\15Feb.pdf
#     save_path = os.path.join('S:\\FLASK2\\pdf', pdf_file.filename)
#     pdf_file.save(save_path)

#     x_min = int(request.args.get('x_min'))
#     x_max = int(request.args.get('x_max'))
#     y_min = int(request.args.get('y_min'))
#     y_max = int(request.args.get('y_max'))
#     page_number = int(request.args.get('page_number'))

#     if x_min > x_max:
#         x0 = x_max
#         x_max = x_min
#         x_min = x0
#     if y_min > y_max:
#         y0 = y_max
#         y_max = y_min
#         y_min = y0

#     extracted_text = extract_text_from_area(save_path, page_number, x_min, x_max, y_min, y_max)

#     # Save cropped image
#     current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
#     filename = f"cropped_image_{current_time}.jpg"
#     image_path = os.path.join('S:\\FLASK2\\static', filename)
    
#     doc = fitz.open(save_path)
#     page = doc[page_number]
#     pix = page.get_pixmap(dpi=280)
#     cropped_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#     cropped_image = cropped_image.crop((x_min*4, y_min*4, x_max*4, y_max*4))
#     cropped_image.save(image_path)

#     doc.close()
#     Get_image = url_for('static', filename=filename),
#     print(Get_image)
    
#     data = {
#         'image_url': Get_image[0],
#         'data': extracted_text
#         }
#     return jsonify(data)


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')



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

    pdf_file = request.files['pdf']  # Access the uploaded PDF file
    save_path = os.path.join('S:\\FLASK2\\pdf', pdf_file.filename)
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
    blocks = page.get_text("dict", flags=11)["blocks"]

    sorted_blocks = sorted(blocks, key=lambda b: (b["bbox"][0], b["bbox"][1]))

    extracted_text = []
    c=0

    for b in sorted_blocks:
        if is_article_block2(b, x_min, y_min, x_max, y_max):
            
            print("nato nato")
            block_text = ""
            for l in b["lines"]:
                for s in l["spans"]:
                    block_text += s["text"]
            block_text = block_text.replace("�", "P")

            font =  b["lines"][0]["spans"][0]["font"]
            fontsize = b["lines"][0]["spans"][0]["size"],
            extracted_text.append({"font": font,"fontsize": fontsize[0], "paragraph": block_text})

        # if not extracted_text:
        #     block_text = page.get_text("word", clip=(x_min, y_min, x_max, y_max)).strip()
        #     if block_text.strip():
        #         block_text = block_text.replace("�", "P")
        #         extracted_text.append({"font": "", "fontsize": 0, "paragraph": block_text})

        else:
            print("else part")
            #if not is_article_block2:
            # c+=1
            # if c==0:
            if (x_min <= b["bbox"][0] <= x_max and y_min <= b["bbox"][1] <= y_max):
                block_text = ""
                for l in b["lines"]:
                    for s in l["spans"]:
                        block_text += s["text"]
                block_text = block_text.replace("�", "P")
                font = b["lines"][0]["spans"][0]["font"]
                fontsize = b["lines"][0]["spans"][0]["size"],
                extracted_text.append({"font": font,"fontsize": fontsize[0], "paragraph": block_text})

    doc.close()

    doc = fitz.open(save_path)
    page = doc[page_number]
    pix = page.get_pixmap(dpi=280)
    cropped_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    cropped_image = cropped_image.crop((x_min*4, y_min*4, x_max*4, y_max*4))
    cropped_image.save(image_path)
    zoom_factor = 1 # Adjust the zoom factor according to your requirement
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