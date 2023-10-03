
import os
import fitz
from flask import Flask, jsonify, request
from models import ExtractDataSchema
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# def is_article_block(block):
#     return len(block[4].split()) > 10

# def is_article_block(block):
#     # Adjust the coordinates as per your requirement

#     x_min = 300#300  #Minimum x-coordinate
#     x_max = 851#1390  #Maximum x-coordinate
#     y_min = 0#200  # Minimum y-coordinate
#     y_max = 1134#1300 # Maximum y-coordinate

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

#     output_content1 = []
#     output_content2 = []
#     doc = fitz.open(save_path)
#     page_number = 1
#     # for page_number in range(len(doc)):
#     Page = doc[page_number]
#     blocks = Page.get_text("blocks")
#     # print("hello aman",Page.get_text("blocks"))


#     if blocks:
#  
#         article_blocks = [block for block in blocks if is_article_block(block)]
#        

#         if article_blocks:
#             for i, article_block in enumerate(article_blocks):
#                     article_text = article_block[4]

#                     if article_text.strip():
#                         article_text = article_text.replace("�", "P")
#                         paragraph = article_text
                        
#                         output_content1.append(paragraph)
#                     else:
#                         print(f"Page {page_number+1} - No text found in Article {i+1}")
#             else:
#                 print(f"Page {page_number+1} - No articles found")
#         else:
#             print(f"Page {page_number+1} - No words found")
    
#     doc.close()
#     for index,arpara in enumerate(output_content1):
#         paragrap=index,arpara.replace("\n"," ")
#         # result = {"extract_data":paragrap}
#         # output_content2.append(result)
#         output_content2.append(paragrap)
#     return jsonify(output_content2)
    


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

    save_path = os.path.join('E:\\FLASK2', pdf_file.filename)
    pdf_file.save(save_path)

    x_min = int(request.args.get('x_min', '300'))
    x_max = int(request.args.get('x_max', '851'))
    y_min = int(request.args.get('y_min', '0'))
    y_max = int(request.args.get('y_max', '1134'))
    page_number = int(request.args.get('page_number', '1'))

    output_content1 = []
    output_content2 = []
    doc = fitz.open(save_path)

    if page_number >= 0 and page_number < len(doc):
        Page = doc[page_number]
        blocks = Page.get_text("blocks")

        if blocks:
            article_blocks = [block for block in blocks if is_article_block(block, x_min, y_min, x_max, y_max)]

            if article_blocks:
                for i, article_block in enumerate(article_blocks):
                    article_text = article_block[4]

                    if article_text.strip():
                        article_text = article_text.replace("�", "P")
                        paragraph = article_text
                        output_content1.append(paragraph)
                    else:
                        print(f"Page {page_number+1} - No text found in Article {i+1}")
            else:
                print(f"Page {page_number+1} - No articles found")
        else:
            print(f"Page {page_number+1} - No words found")

    doc.close()

    for index, arpara in enumerate(output_content1):
        paragraph = index, arpara.replace("\n", " ")
        output_content2.append(paragraph)

    return jsonify(output_content2)





#==================================================#


# @app.route('/api/coordinate', methods=['POST'])

# def extract_coordinate():
#     schema = ExtractDataSchema()
#     errors = schema.validate(request.files)
#     if errors:
#         return jsonify({'error': errors}), 400
#     pdf_file = request.files['pdf']  # Access the uploaded PDF file
#     save_path = os.path.join('E:\\FLASK2', pdf_file.filename)
#     pdf_file.save(save_path)
#     doc = fitz.open(save_path)
#     coordinate=[]
#     # page_number = 1
#     for page_number in range(len(doc)):
#         Page = doc[page_number]
#         data=Page.mediabox.width, Page.mediabox.height
#         coordinate.append(data)
#         print(coordinate)
#     return jsonify(coordinate)



if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
    


