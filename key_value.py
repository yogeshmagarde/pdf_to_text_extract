# from PIL import Image
# import os
# import fitz
# from flask import Flask, jsonify, request
# from models import ExtractDataSchema
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# from PIL import Image

# def is_article_block(block, x_min, y_min, x_max, y_max):
#     # Check if the block's rectangle intersects with the defined boundaries
#     return (
#         block[0] >= x_min and
#         block[2] <= x_max and
#         block[1] >= y_min and
#         block[3] <= y_max and
#         len(block[4].split()) > 10
#     )

# @app.route('/api/extract', methods=['POST'])
# def extract_articles():
#     schema = ExtractDataSchema()
#     errors = schema.validate(request.files)

#     if errors:
#         return jsonify({'error': errors}), 400

#     pdf_file = request.files['pdf']  # Access the uploaded PDF file

#     save_path = os.path.join('E:\\FLASK2', pdf_file.filename)
#     pdf_file.save(save_path)

#     x_min = int(request.args.get('x_min', '300'))
#     x_max = int(request.args.get('x_max', '851'))
#     y_min = int(request.args.get('y_min', '0'))
#     y_max = int(request.args.get('y_max', '1134'))
#     page_number = int(request.args.get('page_number', '1'))

#     if x_min>x_max:
#                 x0=x_max
#                 x_max=x_min
#                 x_min=x0
#     if y_min>y_max:
#                 y0=y_max
#                 y_max=y_min
#                 y_min=y0 


#     output_content1 = []
#     output_content2 = []
#     doc = fitz.open(save_path)

#     if page_number >= 0 and page_number < len(doc):
#         page = doc[page_number]
#         blocks = page.get_text("blocks")
#         image_path = os.path.join('E:\\FLASK2', 'cropped_image.jpg')  # Output path for the zoomed image

#         if blocks:
#             article_blocks = [block for block in blocks if is_article_block(block,x_min,y_min, x_max, y_max)]

#             if article_blocks:
#                 for i, article_block in enumerate(article_blocks):
#                     article_text = article_block[4]

#                     if article_text.strip():
#                         article_text = article_text.replace("�", "P")
#                         paragraph = article_text
#                         output_content1.append(paragraph)
#                     else:
#                         print(f"Page {page_number+1} - No text found in Article {i+1}")
#             else:
#                 print(f"Page {page_number+1} - No articles found")
#                 # cropped_text = page.get_text("text", clip=(x_min, y_min, x_max, y_max))
#                 cropped_text = page.get_text("word", clip=(x_min, y_min, x_max, y_max))

#                 if cropped_text.strip():
#                     paragraph = cropped_text.strip().replace("�", "P")
#                     print(paragraph)
#                     output_content1.append(paragraph)
#         else:
#             print(f"Page {page_number+1} - No words found")

        
#         pix = page.get_pixmap(dpi=71)
#         # pix = page.get_pixmap()
#         cropped_image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
#         cropped_image = cropped_image.crop((x_min, y_min, x_max, y_max))
#         cropped_image.save(image_path)
#         zoom_factor = 2 # Adjust the zoom factor according to your requirement
#         cropped_image = cropped_image.resize((cropped_image.width * zoom_factor, cropped_image.height * zoom_factor))
#         cropped_image.save(image_path)

#     doc.close()

#     for index, arpara in enumerate(output_content1):
#         paragraph = index, arpara.replace("\n", " ")
#         output_content2.append(paragraph)

#     return jsonify(output_content2)

# if __name__ == '__main__':
#     app.run(debug=True,host='0.0.0.0')


import fitz

pdf_path = "15Feb.pdf"  # Specify the path to your PDF file here

doc = fitz.open(pdf_path)
page = doc[1]

# Read page text as a list of dictionaries
blocks = page.get_text("dict", flags=11)["blocks"]

# Specify the coordinates of the block you want to select
x_min, y_min, x_max, y_max = 68, 193, 300, 639

selected_blocks = []

# Iterate through the blocks and select those within the specified coordinates
for block in blocks:
    bbox = block["bbox"]
    if x_min <= bbox[0] <= x_max and y_min <= bbox[1] <= y_max and x_min <= bbox[2] <= x_max and y_min <= bbox[3] <= y_max:
        selected_blocks.append(block)

# Sort selected blocks by top-to-bottom and left-to-right coordinates
sorted_blocks = sorted(selected_blocks, key=lambda b: (b["bbox"][3], b["bbox"][0]))

# Initialize an empty dictionary to store the key-value pairs
text_dict = {}
current_key = None  # Track the current key

# Define the direction of iteration
direction = "top_to_bottom_left_to_right"

if direction == "top_to_bottom_left_to_right":
    for b in sorted_blocks:  # Iterate through the selected blocks
        block_text = ""
        font_size = b["lines"][0]["spans"][0]["size"]  # Font size of the first span in the first line

        for l in b["lines"]:  # Iterate through the lines in the block
            for s in l["spans"]:  # Iterate through the spans in the line
                block_text += s["text"]  # Concatenate the text within the block

        if 22 <= font_size <= 50:  # Check if font size is between 22 and 50
            current_key = block_text.strip()  # Set the current key
            text_dict[current_key] = None  # Add key to the dictionary
        elif 10 <= font_size <= 15:  # Check if font size is between 10 and 15
            if current_key is not None:
                value = block_text.strip()
                if text_dict[current_key] is None:
                    text_dict[current_key] = value
                else:
                    text_dict[current_key] += " " + value

elif direction == "top_to_bottom_right_to_left":
    for b in reversed(sorted_blocks):  # Iterate through the selected blocks in reverse order
        block_text = ""
        font_size = b["lines"][0]["spans"][0]["size"]  # Font size of the first span in the first line

        for l in b["lines"]:  # Iterate through the lines in the block
            for s in l["spans"]:  # Iterate through the spans in the line
                block_text += s["text"]  # Concatenate the text within the block

        if 22 <= font_size <= 50:  # Check if font size is between 22 and 50
            current_key = block_text.strip()  # Set the current key
            text_dict[current_key] = None  # Add key to the dictionary
        elif 10 <= font_size <= 15:  # Check if font size is between 10 and 15
            if current_key is not None:
                value = block_text.strip()
                if text_dict[current_key] is None:
                    text_dict[current_key] = value
                else:
                    text_dict[current_key] += " " + value

else:
    print("Invalid direction specified.")

print("Key-Value Pairs:")
for key, value in text_dict.items():
    # print("Key:", key)
    print( key,":-", value)
    # print("Value:", value)
    print()
